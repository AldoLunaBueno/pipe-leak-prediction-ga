import math

# 1. Parámetros de Discretización
L = 306000          # Longitud total Tramo I en metros [cite: 35, 36]
DZ = 100            # Tamaño del paso espacial en metros [cite: 36]
N_NODES = int(L / DZ) + 1  # 3,061 nodos estructurales [cite: 37, 38]

# 2. Especificaciones Físicas de la Tubería
D_IN_INCHES = 24
D_IN = D_IN_INCHES * 0.0254       # Diámetro interno en metros (0.6096 m) [cite: 38, 39]
AREA = math.pi * (D_IN / 2)**2    # Área transversal en m^2 [cite: 39]

# 3. Propiedades del Fluido y Gravedad
G = 9.81            # Aceleración de la gravedad en m/s^2 [cite: 39, 40]
RHO = 875           # Densidad del crudo en kg/m^3 [cite: 40, 41]

# 4. Condiciones de Frontera y Operación
F_FACTOR = 0.019    # Factor de fricción de Darcy-Weisbach [cite: 41]
H_INLET = 440       # Carga piezométrica inicial en Estación 1 (m) [cite: 41, 42]
Q_FLOW = 0.52       # Caudal en estado estacionario (m^3/s) [cite: 42]