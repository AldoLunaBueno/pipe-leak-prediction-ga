import matplotlib.pyplot as plt
from core.topography import TopographyProfile
from core.hydraulics import SteadyStateSolver
from scada.telemetry import SCADANetwork
from visualization.dashboard import HydraulicDashboard

def run_simulation():
    # 1. Resolver Topografía
    topo = TopographyProfile()
    elevation_smooth = topo.apply_smoothing(window_size=120)
    topo_data = {'z_km': topo.z_km, 'elevation': elevation_smooth}
    
    # 2. Inicializar Solucionador e Instrumentación
    solver = SteadyStateSolver(elevation_smooth, topo.z_m)
    network = SCADANetwork(topo.z_km)
    
    # --- ESCENARIO A: ESTADO NOMINAL (SIN FUGA) ---
    head_normal = solver.calculate_head_loss()
    pressure_normal = solver.calculate_gauge_pressure()
    normal_results = {'head': head_normal.copy(), 'pressure': pressure_normal.copy()}
    
    # --- ESCENARIO B: ESTADO CON ANOMALÍA (FUGA SIMULADA) ---
    # Ejemplo: Fuga en el kilómetro 155, perdiendo 0.12 m^3/s de caudal
    Z_LEAK = 155
    Q_LEAK = 0.12
    
    head_leak = solver.calculate_head_loss_with_leak(z_leak_km=Z_LEAK, q_leak=Q_LEAK)
    pressure_leak = solver.calculate_gauge_pressure()
    leak_results = {
        'z_leak_km': Z_LEAK,
        'q_leak': Q_LEAK,
        'head': head_leak.copy(),
        'pressure': pressure_leak.copy()
    }
    
    # 3. Lanzar la interfaz unificada
    dashboard = HydraulicDashboard(topo_data)
    dashboard.render(normal_data=normal_results, leak_data=leak_results, scada_net=network)
    
    # --- CÓDIGO PARA MAXIMIZAR LA VENTANA (A prueba de linters) ---
    manager = plt.get_current_fig_manager()
    
    try:
        # getattr obtiene el atributo si existe, si no, devuelve None (evita el error del linter)
        window = getattr(manager, "window", None)
        frame = getattr(manager, "frame", None) # Algunos backends como wxPython usan 'frame'
        
        if window is not None:
            if hasattr(window, 'showMaximized'):
                window.showMaximized()  # Backend Qt
            elif hasattr(window, 'state'):
                window.state('zoomed')  # Backend Tkinter en Windows
        elif frame is not None and hasattr(frame, 'Maximize'):
            frame.Maximize(True)        # Backend wxPython
            
    except Exception as e:
        print(f"Nota: El backend gráfico actual no soporta maximizado automático. ({e})")
    
    # Desplegar la ventana única
    plt.show()

if __name__ == "__main__":
    run_simulation()