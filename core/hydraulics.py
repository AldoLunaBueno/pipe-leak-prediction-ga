import numpy as np
import config

class SteadyStateSolver:
    def __init__(self, elevation_profile, z_m):
        self.elevation = elevation_profile
        self.z_m = z_m
        self.head = np.zeros_like(self.elevation)
        self.pressure_bar = np.zeros_like(self.elevation)

    def calculate_head_loss(self):
        """
        Resuelve la Carga Piezométrica (H) en estado estacionario de forma vectorizada.
        """
        # Cálculo de la pérdida por fricción constante por metro
        friction_loss_per_m = (config.F_FACTOR * config.Q_FLOW**2) / (2 * config.G * config.D_IN * config.AREA**2)
        
        # H(i) = H_inlet - (E(i) - E(0)) - (pérdida_fricción * z(i))
        self.head = config.H_INLET - (self.elevation - self.elevation[0]) - (friction_loss_per_m * self.z_m)
        
        return self.head

    def calculate_gauge_pressure(self):
        """
        Calcula la presión manométrica local y la convierte directamente a Bar.
        """
        if not np.any(self.head):
            self.calculate_head_loss()
            
        # P = rho * g * (H - E) convertida a Bar (1 bar = 10^5 Pa)
        self.pressure_bar = (config.RHO * config.G * (self.head - self.elevation)) / 1e5
        
        return self.pressure_bar
    
    def calculate_head_loss_with_leak(self, z_leak_km, q_leak):
        """
        Resuelve la Carga Piezométrica (H) introduciendo una fuga.
        z_leak_km: Posición de la fuga en kilómetros.
        q_leak: Magnitud del caudal perdido en m^3/s.
        """
        z_leak_m = z_leak_km * 1000
        
        # 1. Crear un vector de caudales para cada nodo usando np.where
        Q_array = np.where(self.z_m < z_leak_m, config.Q_FLOW, config.Q_FLOW - q_leak)
        
        # 2. Calcular la pérdida de fricción por metro en cada nodo
        friction_loss_per_m = (config.F_FACTOR * Q_array**2) / (2 * config.G * config.D_IN * config.AREA**2)
        
        # 3. Integración numérica: pérdida acumulada a lo largo de la tubería
        # Multiplicamos por DZ y hacemos la suma acumulada
        cumulative_friction = np.cumsum(friction_loss_per_m * config.DZ)
        
        # 4. H(z) = H_inlet - dE - suma(hf)
        self.head = config.H_INLET - (self.elevation - self.elevation[0]) - cumulative_friction
        
        return self.head