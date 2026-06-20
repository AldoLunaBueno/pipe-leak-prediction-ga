import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class CylinderMesh3D:
    def __init__(self, z_km, elevation, head, r_visual=12, n_theta=50):
        self.z_km = z_km
        self.elevation = elevation
        self.head = head
        self.r_visual = r_visual 
        self.n_theta = n_theta 

    def generate_mesh(self):
        """
        Traduce el vector 1D a matrices 3D (X, Y, Z) para la superficie cilíndrica.
        """
        N = len(self.z_km)
        theta = np.linspace(0, 2 * np.pi, self.n_theta)
        
        # Vectorización avanzada: Generación del tubo tridimensional
        self.X_mesh = np.tile(self.z_km, (self.n_theta, 1)) 
        self.Y_mesh = self.r_visual * np.cos(theta[:, np.newaxis]) * np.ones(N) 
        self.Z_mesh = self.elevation + self.r_visual * np.sin(theta[:, np.newaxis]) 
        
        # Matriz de carga piezométrica replicada para el mapeo de color
        self.H_mesh = np.tile(self.head, (self.n_theta, 1))

    def plot_3d_simulation(self):
        fig = plt.figure(figsize=(12, 7), facecolor='w') 
        ax = fig.add_subplot(111, projection='3d')
        
        # Normalización de color para emular el caxis de MATLAB
        norm = plt.Normalize(np.min(self.H_mesh), np.max(self.H_mesh))
        face_colors = cm.jet(norm(self.H_mesh))
        
        # Trazado de la tubería sólida con renderizado optimizado
        # cstride=15 salta 15 nodos a lo largo de los 306km.
        # rstride=2 salta 1 nodo en la circunferencia.
        surf = ax.plot_surface(self.X_mesh, self.Y_mesh, self.Z_mesh, 
                               facecolors=face_colors, shade=True, 
                               rstride=2, cstride=15, antialiased=True)
        
        # Configuración de la barra de color
        m = cm.ScalarMappable(cmap=cm.jet, norm=norm)
        m.set_array(self.H_mesh)
        cb = plt.colorbar(m, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1)
        cb.set_label('Piezometric Pressure Head H(z) [meters]', fontsize=11, fontweight='bold')
        
        # Ajuste de aspecto e iluminación
        ax.view_init(elev=25, azim=-55)
        
        # corrección geométrica (evitar el ovalamiento):
        # Extraemos los límites actuales calculados por el motor
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()
        
        # Calculamos la amplitud máxima entre Y y Z
        y_span = y_limits[1] - y_limits[0]
        z_span = z_limits[1] - z_limits[0]
        max_span = max(y_span, z_span)
        
        # Centramos ambos ejes y les asignamos exactamente la misma amplitud
        y_mid = np.mean(y_limits)
        z_mid = np.mean(z_limits)
        
        ax.set_ylim3d([y_mid - max_span/2, y_mid + max_span/2])
        ax.set_zlim3d([z_mid - max_span/2, z_mid + max_span/2])
        
        # Forzamos una caja física donde el largo (X) es 2.5 veces mayor que el alto y ancho (Y, Z)
        ax.set_box_aspect([2.5, 1, 1])
        
        # Descripciones
        ax.set_xlabel('Pipeline Longitudinal Distance (km)', fontweight='bold')
        ax.set_ylabel('Cross-Sectional Width', fontweight='bold')
        ax.set_zlabel('Absolute Topographic Elevation Profile (m)', fontweight='bold')
        ax.set_title('ONP Tramo I: Proportional 3D Solid Cylindrical Flow Simulation', 
                     fontsize=13, fontweight='bold')