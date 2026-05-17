import time
import logging
import os
from typing import Any, Dict
from datetime import datetime

RATES = {'stopped_fare': 0.02, 'moving_fare': 0.05}  # € Por segundo

def setup_logging():
    """Configura el sistema de logging"""
    # Crear directorio de logs si no existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(f"{log_dir}/taxi-register.log", encoding='utf-8'),
            logging.StreamHandler()  # Opcional: mostrar también en consola
        ]
    )
    return logging.getLogger(__name__)

def add_segment_time(trip: Dict[str, Any]) -> None:
    """Añade el tiempo del segmento actual al contador correspondiente"""
    segment_time = time.time() - trip['start']
    
    if trip['state'] == 'stopped':
        trip['stopped'] += segment_time
    else:
        trip['moving'] += segment_time

def log_command(logger: logging.Logger, command: str, trip: Dict[str, Any], additional_info: str = "") -> None:
    """Registra un comando en el log"""
    if trip['active']:
        log_msg = f"Command: {command} | State: {trip['state']} | Stopped: {trip['stopped']:.1f}s | Moving: {trip['moving']:.1f}s"
        if additional_info:
            log_msg += f" | {additional_info}"
        logger.info(log_msg)
    else:
        logger.info(f"Command: {command} (no active trip)")

def taximeter():
    """Función principal del taxímetro"""
    # Configurar logging
    logger = setup_logging()
    logger.info("")
    logger.info("="*60)
    logger.info("         🏁 === 🚕 TAXIMETER APP STARTED 🚕 === 🏁")
    
    print("\n=== 🚕 Available Commands: 🚕 ===\nstart, stop, move, finish, exit\n")
    
    trip: Dict[str, Any] = {
        'active': False,
        'stopped': 0.0,
        'moving': 0.0,
        'state': 'stopped',  # Puede ser 'stopped' o 'moving'
        'start': 0.0
    }
    
    while True:
        command = input(">🚕 ").strip().lower()
        
        if command == "start" and not trip['active']:
            trip['active'] = True
            trip['stopped'] = 0.0
            trip['moving'] = 0.0
            trip['state'] = 'stopped'
            trip['start'] = time.time()
            print("Trip started.")
            logger.info(f"Command: start | New trip started at {datetime.now().strftime('%H:%M:%S')}")
        
        elif command in ("stop", "move") and trip['active']:
            # Añadir tiempo del segmento anterior
            add_segment_time(trip)
            
            # Cambiar al nuevo estado
            new_state = 'stopped' if command == "stop" else 'moving'
            old_state = trip['state']
            trip['state'] = new_state
            trip['start'] = time.time()
            print(f"Now {new_state}.")
            logger.info(f"Command: {command} | State change: {old_state} → {new_state}")
        
        elif command == "finish" and trip['active']:
            # Añadir el último segmento
            add_segment_time(trip)
            
            # Calcular y mostrar la tarifa
            fare = (trip['stopped'] * RATES['stopped_fare'] + 
                   trip['moving'] * RATES['moving_fare'])
            
            print(f"\nTrip summary:\n"
                  f"  Stopped: {trip['stopped']:.1f}s\n"
                  f"  Moving: {trip['moving']:.1f}s\n"
                  f"  Total: €{fare:.2f}\n")
            
            # Registrar resumen del viaje
            logger.info(f"Command: finish | TRIP COMPLETED - Stopped: {trip['stopped']:.1f}s, Moving: {trip['moving']:.1f}s, Total fare: €{fare:.2f}")
            trip['active'] = False
        
        elif command == "exit":
            print("Goodbye!")
            logger.info("Command: exit | TAXIMETER APP STOPPED")
            break
        
        else:
            error_msg = "Invalid command or no active trip."
            print(error_msg)
            logger.warning(f"Command: {command} | {error_msg}")

if __name__ == "__main__":
    taximeter()