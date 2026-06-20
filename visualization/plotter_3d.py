import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class CylinderMesh3D:
    def __init__(self, z_km, elevation, head, r_visual=12, n_theta=50):
        self.z_km = z_km
        self.elevation = elevation
        self.head = head
        self.r_visual = r_visual # [cite: 18]
        self.n_theta = n_theta # [cite: 17]

    def generate_mesh(self):
        """
        Traduce el vector 1D a matrices 3D (X, Y, Z) para la superficie cilíndrica.
        """
        N = len(self.z_km)
        theta = np.linspace(0, 2 * np.pi, self.n_theta)
        
        # Vectorización avanzada: Generación del tubo tridimensional [cite: 19]
        self.X_mesh = np.tile(self.z_km, (self.n_theta, 1)) # [cite: 22]
        self.Y_mesh = self.r_visual * np.cos(theta[:, np.newaxis]) * np.ones(N) # [cite: 23]
        self.Z_mesh = self.elevation + self.r_visual * np.sin(theta[:, np.newaxis]) # [cite: 24]
        
        # Matriz de carga piezométrica replicada para el mapeo de color [cite: 26]
        self.H_mesh = np.tile(self.head, (self.n_theta, 1))

    def plot_3d_simulation(self):
        fig = plt.figure(figsize=(12, 7), facecolor='w') # [cite: 25]
        ax = fig.add_subplot(111, projection='3d')
        
        # Normalización de color para emular el caxis de MATLAB [cite: 28]
        norm = plt.Normalize(np.min(self.H_mesh), np.max(self.H_mesh))
        face_colors = cm.jet(norm(self.H_mesh))
        
        # Trazado de la tubería sólida [cite: 26]
        surf = ax.plot_surface(self.X_mesh, self.Y_mesh, self.Z_mesh, 
                               facecolors=face_colors, shade=True, 
                               rstride=1, cstride=1, antialiased=True)
        
        # Configuración de la barra de color [cite: 27]
        m = cm.ScalarMappable(cmap=cm.jet, norm=norm)
        m.set_array(self.H_mesh)
        cb = plt.colorbar(m, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1)
        cb.set_label('Piezometric Pressure Head H(z) [meters]', fontsize=11, fontweight='bold')
        
        # Ajuste de aspecto e iluminación [cite: 28, 30]
        ax.view_init(elev=25, azim=-55)
        ax.set_box_aspect([1, 1, 1]) 
        
        # Descripciones [cite: 30, 31]
        ax.set_xlabel('Pipeline Longitudinal Distance (km)', fontweight='bold')
        ax.set_ylabel('Cross-Sectional Width', fontweight='bold')
        ax.set_zlabel('Absolute Topographic Elevation Profile (m)', fontweight='bold')
        ax.set_title('ONP Tramo I: Proportional 3D Solid Cylindrical Flow Simulation', 
                     fontsize=13, fontweight='bold')
        
        plt.show()