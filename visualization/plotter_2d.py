import matplotlib.pyplot as plt
import config

class ProfilePlotter2D:
    def __init__(self, z_km, elevation_smooth):
        self.z_km = z_km
        self.elevation = elevation_smooth

    def plot_profile_and_scada(self, scada_readings):
        # Inicialización de la figura con fondo blanco [cite: 51]
        fig, ax = plt.subplots(figsize=(12, 6.5), facecolor='w')
        
        # Trazado del perfil físico de la tubería [cite: 52]
        ax.plot(self.z_km, self.elevation, 'k-', linewidth=2.5, 
                label='Eje del Ducto (Perfil Topográfico de Elevación)')
        
        # Superposición de la instrumentación SCADA [cite: 53]
        for km, data in scada_readings.items():
            pt_x = data['km']
            pt_z = data['elevation']
            pt_p = data['pressure_bar']
            
            # Tallo de anclaje del transmisor [cite: 58]
            ax.plot([pt_x, pt_x], [pt_z, pt_z + 20], 'k-', linewidth=1.8)
            
            # Nodo del Transmisor de Presión (Cuadrado azul) [cite: 59]
            ax.plot(pt_x, pt_z + 20, 's', markersize=10, 
                    markerfacecolor='#0072BD', markeredgecolor='k', linewidth=1.5)
            
            # Ventana de telemetría [cite: 60, 61]
            label_text = f"{data['label']}\n$P_{{gauge}}$: {pt_p:.2f} bar\nElev: {int(round(pt_z))} m"
            ax.text(pt_x + 3, pt_z + 30, label_text, fontsize=8.5,
                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'),
                    verticalalignment='bottom')

        # Controles de presentación [cite: 62]
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.set_xlim([0, 306]) # [cite: 63]
        ax.set_ylim([0, max(self.elevation) + 120]) # [cite: 63]
        
        # Descripciones de ejes [cite: 64, 65, 66]
        ax.set_xlabel('Distancia Longitudinal del Oleoducto (km)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Elevación sobre el Nivel del Mar (m)', fontsize=11, fontweight='bold')
        ax.set_title('Perfil de Instrumentación Industrial: Transmisores de Presión en Oleoducto Norperuano (Tramo I)', 
                     fontsize=12, fontweight='bold')
        ax.legend(loc='upper right', fontsize=10) # [cite: 67]
        
        # Bloque de parámetros del sistema [cite: 68]
        metadata_text = (f"ESPECIFICACIONES DEL SISTEMA\n\n"
                         f"Diámetro Interno: 24 Pulgadas\n"
                         f"Longitud Total: {config.L / 1000} km\n"
                         f"Densidad del Crudo: {config.RHO} kg/m³\n"
                         f"Nodos de Segmentación: {config.N_NODES} ({config.DZ}m)")
        props = dict(boxstyle='square', facecolor='white', alpha=0.95, edgecolor='gray')
        ax.text(0.05, 0.95, metadata_text, transform=ax.transAxes, fontsize=8.5,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        plt.show()