import numpy as np

class SCADANetwork:
    def __init__(self, z_km_array):
        self.z_km = z_km_array
        
        # Definición de las posiciones kilométricas de la telemetría [cite: 54]
        # y sus respectivas etiquetas industriales [cite: 55]
        self.stations = {
            0: 'Estación 1 (San José)',
            65: 'PT-65 Checkpoint',
            135: 'PT-135 Block Valve',
            215: 'PT-215 Checkpoint',
            306: 'Estación 2 (Corrientes)'
        }
        self.readings = {}

    def acquire_sensor_data(self, elevation_profile, pressure_profile):
        """
        Extrae las lecturas de elevación y presión exactas en los nodos de telemetría.
        Devuelve un diccionario estructurado, listo para la visualización o el Algoritmo Genético.
        """
        self.readings = {}
        
        for km_target, label in self.stations.items():
            # Localizar el índice del nodo discreto más cercano (equivalente a min(abs(...)) en MATLAB)
            idx = np.argmin(np.abs(self.z_km - km_target))
            
            self.readings[km_target] = {
                'label': label,
                'index': idx,
                'km': self.z_km[idx],
                'elevation': elevation_profile[idx],
                'pressure_bar': pressure_profile[idx]
            }
            
        return self.readings