import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

import config

class HydraulicDashboard:
    def __init__(self, topo_data):
        self.z_km = topo_data['z_km']
        self.elevation = topo_data['elevation']
        self.n_theta = 50
        self.r_visual = 12

    def _generate_cylinder_mesh(self, head_profile):
        """Helper interno para generar la geometría 3D de la tubería"""
        N = len(self.z_km)
        theta = np.linspace(0, 2 * np.pi, self.n_theta)
        X = np.tile(self.z_km, (self.n_theta, 1))
        Y = self.r_visual * np.cos(theta[:, np.newaxis]) * np.ones(N)
        Z = self.elevation + self.r_visual * np.sin(theta[:, np.newaxis])
        H = np.tile(head_profile, (self.n_theta, 1))
        return X, Y, Z, H

    def _correct_3d_aspect(self, ax):
        """Helper interno para evitar que el cilindro se deforme u ovale"""
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()
        max_span = max(y_limits[1] - y_limits[0], z_limits[1] - z_limits[0])
        y_mid, z_mid = np.mean(y_limits), np.mean(z_limits)
        ax.set_ylim3d([y_mid - max_span/2, y_mid + max_span/2])
        ax.set_zlim3d([z_mid - max_span/2, z_mid + max_span/2])
        ax.set_box_aspect([2.5, 1.4, 1.4])

    def render(self, normal_data, leak_data, scada_net):
        # Crear la figura principal del Dashboard
        fig = plt.figure(figsize=(16, 10), facecolor='w')
        fig.suptitle('SISTEMA EN TIEMPO REAL - MONITOREO DE PRESIONES Y GRADIENTE HIDRÁULICO', 
                     fontsize=14, fontweight='bold', y=0.96)

        # ---------------------------------------------------------------------
        # GRÁFICO 1: 2D Perfil Operacional Normal (Fila 1, Columna 1)
        # ---------------------------------------------------------------------
        ax1 = fig.add_subplot(221)
        ax1.plot(self.z_km, self.elevation, 'k-', linewidth=2, label='Eje del Ducto')
        ax1.set_title('Perfil Operacional: Estado Nominal (Sin Fuga)', fontsize=11, fontweight='bold')
        ax1.grid(True, linestyle='--', linewidth=0.5)
        ax1.set_xlim(0, 340)
        ax1.set_ylim(100, max(self.elevation) + 120)
        ax1.set_ylabel('Elevación (m)', fontweight='bold')
        
        # Inyectar telemetría normal
        scada_normal = scada_net.acquire_sensor_data(self.elevation, normal_data['pressure'])
        for km, data in scada_normal.items():
            ax1.plot(data['km'], data['elevation'] + 20, 's', markerfacecolor='#0072BD', markeredgecolor='k')
            ax1.text(data['km'] + 2, data['elevation'] + 25, f"PT-{km}:\n{data['pressure_bar']:.2f} bar", fontsize=8,
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

        # ---------------------------------------------------------------------
        # GRÁFICO 2: 2D Perfil Operacional Con Fuga (Fila 1, Columna 2)
        # ---------------------------------------------------------------------
        ax2 = fig.add_subplot(222)
        ax2.plot(self.z_km, self.elevation, 'k-', linewidth=2)
        ax2.set_title(f"Alerta de Anomalía: Fuga detectada en km {leak_data['z_leak_km']}", fontsize=11, fontweight='bold', color='red')
        ax2.grid(True, linestyle='--', linewidth=0.5)
        ax2.set_xlim(0, 340)
        ax2.set_ylim(100, max(self.elevation) + 120)
        
        # Resaltar punto de fuga con una línea vertical roja
        ax2.axvline(x=leak_data['z_leak_km'], color='r', linestyle=':', linewidth=2, label='Punto de Fuga')
        
        # Inyectar telemetría con fuga
        scada_leak = scada_net.acquire_sensor_data(self.elevation, leak_data['pressure'])
        for km, data in scada_leak.items():
            ax2.plot(data['km'], data['elevation'] + 20, 's', markerfacecolor='r' if km >= leak_data['z_leak_km'] else '#0072BD', markeredgecolor='k')
            ax2.text(data['km'] + 2, data['elevation'] + 25, f"PT-{km}:\n{data['pressure_bar']:.2f} bar", fontsize=8,
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'), fontweight='bold' if km >= leak_data['z_leak_km'] else 'normal')

        # ---------------------------------------------------------------------
        # GRÁFICO 3: 3D Simulación Cilíndrica Normal (Fila 2, Columna 1)
        # ---------------------------------------------------------------------
        ax3 = fig.add_subplot(223, projection='3d')
        X1, Y1, Z1, H1 = self._generate_cylinder_mesh(normal_data['head'])
        norm = Normalize(np.min(H1), np.max(H1))
        
        ax3.plot_surface(X1, Y1, Z1, facecolors=cm.jet(norm(H1)), shade=True, rstride=2, cstride=15, antialiased=True)
        ax3.view_init(elev=20, azim=-60)
        self._correct_3d_aspect(ax3)
        ax3.set_title('Modelo 3D: Distribución de Carga Nominal', fontsize=10, fontweight='bold')
        ax3.set_xlabel('Distancia (km)', fontsize=8)
        ax3.set_zlabel('Elevación (m)', fontsize=8)

        # ---------------------------------------------------------------------
        # GRÁFICO 4: 3D Simulación Cilíndrica Con Fuga (Fila 2, Columna 2)
        # ---------------------------------------------------------------------
        ax4 = fig.add_subplot(224, projection='3d')
        X2, Y2, Z2, H2 = self._generate_cylinder_mesh(leak_data['head'])
        
        ax4.plot_surface(X2, Y2, Z2, facecolors=cm.jet(norm(H2)), shade=True, rstride=2, cstride=15, antialiased=True)
        ax4.view_init(elev=20, azim=-60)
        self._correct_3d_aspect(ax4)
        ax4.set_title('Modelo 3D: Gradiente de Presión Afectado', fontsize=10, fontweight='bold', color='red')
        ax4.set_xlabel('Distancia (km)', fontsize=8)
        ax4.set_zlabel('Elevación (m)', fontsize=8)

        # Configuración de barra de color única compartida abajo
        m = cm.ScalarMappable(cmap=cm.jet, norm=norm)
        m.set_array(H1)
        
        # Subimos la posición Y de la barra del 0.04 
        # al 0.08 (8% del alto de la figura)
        cb_ax = fig.add_axes((0.4, 0.07, 0.25, 0.02))
        cb = fig.colorbar(m, cax=cb_ax, orientation='horizontal')
        cb.set_label('Carga Piezométrica H(z) [metros]', fontsize=8, fontweight='bold')

        # Levantamos el margen inferior ('bottom') de 0.10 a 0.16 para hacerles espacio
        plt.subplots_adjust(bottom=0.16, top=0.85, hspace=0.25, wspace=0.08)

        plt.subplots_adjust(bottom=0.10, top=0.85, hspace=0.25, wspace=0.08)