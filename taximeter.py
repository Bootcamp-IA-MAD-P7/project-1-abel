import time
from typing import Any, Dict

RATES = {'stopped_fare': 0.02, 'moving_fare': 0.05}  # € Por segundo

def add_segment_time(trip: Dict[str, Any]) -> None:
    """Añade el tiempo del segmento actual al contador correspondiente"""

    if trip['state'] == 'stopped':
        trip['stopped'] += time.time() - trip['start']
    else:
        trip['moving'] += time.time() - trip['start']

def taximeter():
    print("\n=== Welcome to the TAXIMETER APP ===\nCommands: start, stop, move, finish, exit\n")
    
    trip: Dict[str, Any] = {
        'active': False,
        'stopped': 0.0,
        'moving': 0.0,
        'state': 'stopped',  # Puede ser 'stopped' o 'moving'
        'start': 0.0
    }
    
    while True:
        command = input("> ").strip().lower()
        
        if command == "start" and not trip['active']:
            trip['active'] = True
            trip['stopped'] = 0.0
            trip['moving'] = 0.0
            trip['state'] = 'stopped'
            trip['start'] = time.time()
            print("Trip started.")
        
        elif command in ("stop", "move") and trip['active']:
            # Añadir tiempo del segmento anterior
            add_segment_time(trip)
            
            # Cambiar al nuevo estado
            new_state = 'stopped' if command == "stop" else 'moving'
            trip['state'] = new_state
            trip['start'] = time.time()
            print(f"Now {new_state}.")
        
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
            
            trip['active'] = False
        
        elif command == "exit":
            print("Goodbye!")
            break
        
        else:
            print("Invalid command or no active trip.")

if __name__ == "__main__":
    taximeter()