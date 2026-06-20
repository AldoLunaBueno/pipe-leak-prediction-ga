import math

# 1. Parámetros de Discretización
L = 306000          # Longitud total Tramo I en metros
DZ = 100            # Tamaño del paso espacial en metros
N_NODES = int(L / DZ) + 1  # 3,061 nodos estructurales

# 2. Especificaciones Físicas de la Tubería
D_IN_INCHES = 24
D_IN = D_IN_INCHES * 0.0254       # Diámetro interno en metros (0.6096 m)
AREA = math.pi * (D_IN / 2)**2    # Área transversal en m^2

# 3. Propiedades del Fluido y Gravedad
G = 9.81            # Aceleración de la gravedad en m/s^2
RHO = 875           # Densidad del crudo en kg/m^3

# 4. Condiciones de Frontera y Operación
F_FACTOR = 0.019    # Factor de fricción de Darcy-Weisbach
H_INLET = 440       # Carga piezométrica inicial en Estación 1 (m)
Q_FLOW = 0.52       # Caudal en estado estacionario (m^3/s)