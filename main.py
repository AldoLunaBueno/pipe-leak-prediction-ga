from core.topography import TopographyProfile
from core.hydraulics import SteadyStateSolver
from scada.telemetry import SCADANetwork
from visualization.plotter_2d import ProfilePlotter2D
from visualization.plotter_3d import CylinderMesh3D

def run_simulation():
    # 1. Modelado Topográfico
    topo = TopographyProfile()
    elevation_base = topo.build_elevation()
    elevation_smooth = topo.apply_smoothing(window_size=120)
    
    # 2. Resolución Hidráulica
    solver = SteadyStateSolver(elevation_smooth, topo.z_m)
    head_profile = solver.calculate_head_loss()
    pressure_profile = solver.calculate_gauge_pressure()
    
    # 3. Telemetría SCADA
    network = SCADANetwork(topo.z_km)
    scada_data = network.acquire_sensor_data(elevation_smooth, pressure_profile)
    
    # 4. Visualización 2D
    plotter_2d = ProfilePlotter2D(topo.z_km, elevation_smooth)
    plotter_2d.plot_profile_and_scada(scada_data)
    
    # 5. Simulación 3D
    mesh_3d = CylinderMesh3D(topo.z_km, elevation_smooth, head_profile)
    mesh_3d.generate_mesh()
    mesh_3d.plot_3d_simulation()

if __name__ == "__main__":
    run_simulation()