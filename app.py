from flask import Flask, render_template, jsonify, request
import time
import logging
import os
from typing import Any, Dict
from datetime import datetime

app = Flask(__name__)

RATES = {'stopped_fare': 0.02, 'moving_fare': 0.05}  # € Por segundo

def setup_logging():
    """Configura el sistema de logging - Comandos van a archivo y consola"""
    # Configuración centralizada
    config: Dict[str, Any] = {
        'logger_name': 'taximeter',
        'log_level': logging.INFO,
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'date_format': '%Y-%m-%d %H:%M:%S'
    }
    
    logger = logging.getLogger(config['logger_name'])
    logger.setLevel(config['log_level'])
    
    # Configurar handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(config['format'], config['date_format']))
    logger.addHandler(console_handler)
    
    return logger


# Configurar loggers
logger = setup_logging()

def calculate_fare(trip: Dict[str, Any]) -> float:
    """Calcula la tarifa total del viaje"""
    return (trip['stopped'] * RATES['stopped_fare'] + 
            trip['moving'] * RATES['moving_fare'])

def add_segment_time(trip: Dict[str, Any]) -> None:
    """Añade el tiempo del segmento actual al contador correspondiente"""
    segment_time = time.time() - trip['start']
    
    if trip['state'] == 'stopped':
        trip['stopped'] += segment_time
    else:
        trip['moving'] += segment_time

# Estado global del viaje
trip: Dict[str, Any] = {
    'active': False,
    'stopped': 0.0,
    'moving': 0.0,
    'state': 'stopped',
    'start': 0.0
}

@app.route('/')
def index():
    """Página principal"""
    logger.info("         🚕🏁 TAXIMETER APP STARTED (WEB MODE) 🚕🏁")
    logger.info("="*40)
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Obtener estado actual del viaje"""
    try:
        current_stopped = trip['stopped']
        current_moving = trip['moving']
        
        if trip['active']:
            current_time = time.time() - trip['start']
            if trip['state'] == 'stopped':
                current_stopped += current_time
            else:
                current_moving += current_time
        
        # Calcular fare en tiempo real
        fare = calculate_fare({
            'stopped': current_stopped,
            'moving': current_moving
        })
        
        return jsonify({
            'success': True,
            'active': trip['active'],
            'state': trip['state'],
            'stopped': round(current_stopped, 1),
            'moving': round(current_moving, 1),
            'total_fare': round(fare, 2)
        })
    except Exception as e:
        logger.error(f"Error in get_status: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/command', methods=['POST'])
def execute_command():
    """Ejecutar comandos"""
    try:
        data = request.get_json()
        command = data.get('command', '').lower()
        response: Dict[str, Any] = {'success': True, 'message': ''}
        
        if command == "start" and not trip['active']:
            trip['active'] = True
            trip['stopped'] = 0.0
            trip['moving'] = 0.0
            trip['state'] = 'stopped'
            trip['start'] = time.time()
            response['message'] = "Trip started."
            logger.info(f"Command: start | New trip started at {datetime.now().strftime('%H:%M:%S')}")
        
        elif command in ("stop", "move") and trip['active']:
            # Añadir tiempo del segmento anterior
            add_segment_time(trip)
            
            # Cambiar al nuevo estado
            new_state = 'stopped' if command == "stop" else 'moving'
            old_state = trip['state']
            trip['state'] = new_state
            trip['start'] = time.time()
            response['message'] = f"Now {new_state}."
            logger.info(f"Command: {command} | State change: {old_state} → {new_state}")
        
        elif command == "finish" and trip['active']:
            # Añadir el último segmento
            add_segment_time(trip)
            
            # Calcular y mostrar la tarifa
            fare = calculate_fare(trip)
            
            # Registrar resumen del viaje
            response['message'] = f"Trip completed! Total: €{fare:.2f}"
            response['summary'] = {
                'stopped': round(trip['stopped'], 1),
                'moving': round(trip['moving'], 1),
                'total': round(fare, 2)
            }
            
            trip['active'] = False
            trip['stopped'] = 0.0
            trip['moving'] = 0.0
            trip['state'] = 'stopped'
            trip['start'] = 0.0
            logger.info(f"Command: finish | TRIP COMPLETED - Stopped: {trip['stopped']:.1f}s, Moving: {trip['moving']:.1f}s, Total fare: €{fare:.2f}")
            logger.info("="*40)

        elif command == "exit":
            # Registrar salida del viaje
            response['exit'] = True
            trip['active'] = False
            trip['stopped'] = 0.0
            trip['moving'] = 0.0
            trip['state'] = 'stopped'
            trip['start'] = 0.0
            response['message'] = "Goodbye!. Ready for new trip."
            logger.info("Command: exit | TAXIMETER APP STOPPED")
            logger.info("="*40)

        else:
            response['success'] = False
            response['message'] = "Invalid command or no active trip."
            logger.warning(f"Command: {command} | {response['message']}")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in execute_command: {e}")
        return jsonify({'success': False, 'message': str(e)})
    
print("📍 Open your browser and go to: http://localhost:5000")
print("📍 Press Ctrl+C to stop the server")

if __name__ == '__main__':
    # Asegurar que existe el directorio templates
    os.makedirs('templates', exist_ok=True)
    
    # Configuración para producción
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    logger.info(f"Starting Taximeter server on {host}:{port}")
    app.run(debug=debug, host=host, port=port)