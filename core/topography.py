import numpy as np
import pandas as pd
import config

class TopographyProfile:
    def __init__(self):
        # Vector de distancia horizontal discretizada en metros
        self.z_m = np.arange(0, config.L + config.DZ, config.DZ)
        # Distancia normalizada a kilómetros
        self.z_km = self.z_m / 1000.0  
        self.elevation = np.zeros_like(self.z_km)
        self.elevation_smooth = np.zeros_like(self.z_km)

    def build_elevation(self):
        """
        Construye el perfil de elevación topográfica base evaluando 
        las condiciones de tramo mediante vectorización.
        """
        z = self.z_km
        
        # Implementación vectorizada de las ecuaciones topográficas
        self.elevation = np.piecewise(z, 
            [
                z <= 90, 
                (z > 90) & (z <= 210), 
                z > 210
            ], 
            [
                lambda z: 130 + 0.25 * z,
                lambda z: 152.5 + 1.45 * (z - 90) + 35 * np.sin((z - 90) / 12) * np.cos(z / 25),
                lambda z: 326.5 - 0.95 * (z - 210) + 18 * np.sin((z - 210) / 8)
            ]
        )
        return self.elevation

    def apply_smoothing(self, window_size: int = 120):
        """
        Aplica un filtro de media móvil para suavizar el perfil, 
        replicando el movmean(E, 120) de MATLAB. 
        """
        if not np.any(self.elevation):
            self.build_elevation()
            
        # Convertimos a Serie de Pandas para usar un rolling window centrado
        # min_periods=1 evita que devuelva NaN en los bordes (comportamiento de MATLAB)
        series_e = pd.Series(self.elevation)
        smoothed = series_e.rolling(window=window_size, center=True, min_periods=1).mean()
        self.elevation_smooth = smoothed.to_numpy()
        
        return self.elevation_smooth

# Bloque de prueba local para validar el módulo
if __name__ == "__main__":
    topo = TopographyProfile()
    e_base = topo.build_elevation()
    e_smooth = topo.apply_smoothing()
    
    print(f"Nodos procesados: {len(e_smooth)}")
    print(f"Elevación Inicial (z=0km): {e_smooth[0]:.2f} m")
    print(f"Elevación Final (z=306km): {e_smooth[-1]:.2f} m")