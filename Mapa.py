import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Configuración de pantalla
width, height = 1200, 600

# Definición de intersecciones (esquinas)
Intersecciones = {
    "MOB_IB": (50, 500),
    "MOB_T_Ps": (275, 500),

    "T_E": (275, 475),
    "T_An": (275, 450),
    "T_D": (275, 425),
    "T_V": (275, 400),
    "T_Ad": (300, 375),
    "T_S": (325, 350),
    "T_G": (350, 325),
    "T_Pr": (350, 300),

    "MOB_SF": (400, 525),

    "SF_Ps": (400, 500),
    "SF_E": (400, 475),
    "SF_An": (400, 450),
    "SF_D": (400, 425),
    "SF_V": (400, 400),
    "SF_Ad": (400, 375),
    "SF_S": (400, 350),
    "SF_G": (400, 325),
    "SF_Pr": (400, 300),

    "AGC_SF": (400, 50),

    "AGC_PÁO": (950, 50),
    "AGC_IB": (50, 50),
    "MOB_PÁO": (1150, 550),

    # Residencial Tecnológico.
    "MOB_C": (450, 525),
    "AGC_C": (450, 50),
    "MOB_M": (500, 530),
    "AGC_M": (500, 50),
    "MOB_I": (550, 535),
    "AGC_I": (550, 50),
    "MOB_Q": (600, 540),
    "X_Q": (600, 50),
    "MOB_F": (650, 545),
    "X_F": (650, 50),
    "MOB_B": (700, 550),
    "X_B": (700, 50),
    "MOB_E": (750, 555),
    "X_E": (750, 50),

    "SF_I": (400, 460),
    "I_C": (450, 460),
    "I_M": (500, 460),
    "I_I": (550, 460),
    "I_Q": (600, 460),
    "I_F": (650, 460),
    "I_B": (700, 460),
    "I_E": (750, 460),

    "Ad_C": (450, 375),
    "Ad_M": (500, 375),
    "Ad_I": (550, 375),
    "Ad_Q": (600, 375),
    "Ad_F": (650, 375),

    "SF_Ag": (400, 290),
    "Ag_C": (450, 290),
    "Ag_M": (500, 290),
    "Ag_I": (550, 290),

    "MOB_A": (900, 550),
    "AGC_A": (600, 50)
}

# Definición de calles como aristas con atributos
Calle = {
    "Calle1": {"origen": "MOB_IB", "destino": "MOB_T_Ps", "nombre": ""},
    "Calle10": {"origen": "MOB_T_Ps", "destino": "MOB_SF", "nombre": ""},

    "Calle1200": {"origen": "MOB_T_Ps", "destino": "SF_Ps", "nombre": ""},
    "Calle1201": {"origen": "T_E", "destino": "SF_E", "nombre": ""},
    "Calle1202": {"origen": "T_An", "destino": "SF_An", "nombre": ""},
    "Calle1203": {"origen": "T_D", "destino": "SF_D", "nombre": ""},
    "Calle1204": {"origen": "T_V", "destino": "SF_V", "nombre": ""},
    "Calle1205": {"origen": "T_Ad", "destino": "SF_Ad", "nombre": ""},
    "Calle1206": {"origen": "T_S", "destino": "SF_S", "nombre": ""},
    "Calle1207": {"origen": "T_G", "destino": "SF_G", "nombre": ""},
    "Calle1208": {"origen": "T_Pr", "destino": "SF_Pr", "nombre": ""},

    "Calle2": {"origen": "MOB_T_Ps", "destino": "T_E", "nombre": ""},
    "Calle3": {"origen": "T_E", "destino": "T_An", "nombre": ""},
    "Calle4": {"origen": "T_An", "destino": "T_D", "nombre": ""},
    "Calle5": {"origen": "T_D", "destino": "T_V", "nombre": ""},
    "Calle6": {"origen": "T_V", "destino": "T_Ad", "nombre": ""},
    "Calle7": {"origen": "T_Ad", "destino": "T_S", "nombre": ""},
    "Calle8": {"origen": "T_S", "destino": "T_G", "nombre": ""},
    "Calle9": {"origen": "T_G", "destino": "T_Pr", "nombre": ""},

    "Calle119": {"origen": "T_Pr", "destino": "SF_Pr", "nombre": ""},
    "Calle40": {"origen": "SF_Pr", "destino": "AGC_SF", "nombre": ""},
    "Calle41": {"origen": "AGC_SF", "destino": "AGC_IB", "nombre": ""},
    "Calle42": {"origen": "AGC_IB", "destino": "MOB_IB", "nombre": ""},

    "Calle112": {"origen": "MOB_SF", "destino": "SF_Ps", "nombre": ""},
    "Calle12": {"origen": "SF_Ps", "destino": "SF_E", "nombre": ""},
    "Calle13": {"origen": "SF_E", "destino": "SF_An", "nombre": ""},
    "Calle14": {"origen": "SF_An", "destino": "SF_D", "nombre": ""},
    "Calle15": {"origen": "SF_D", "destino": "SF_V", "nombre": ""},
    "Calle16": {"origen": "SF_V", "destino": "SF_Ad", "nombre": ""},
    "Calle17": {"origen": "SF_Ad", "destino": "SF_S", "nombre": ""},
    "Calle18": {"origen": "SF_S", "destino": "SF_G", "nombre": ""},
    "Calle19": {"origen": "SF_G", "destino": "SF_Pr", "nombre": ""}
    # Puedes añadir más calles con sus atributos
}

# Construir conexiones entre calles (grafo enfocado en líneas)
ConexionesCalles = {}
for calle_id, calle_info in Calle.items():
    conexiones = []
    for otra_calle_id, otra_calle_info in Calle.items():
        if calle_id != otra_calle_id:
            # Si comparten una intersección, están conectadas
            if (calle_info["origen"] == otra_calle_info["origen"] or
                calle_info["origen"] == otra_calle_info["destino"] or
                calle_info["destino"] == otra_calle_info["origen"] or
                calle_info["destino"] == otra_calle_info["destino"]):
                conexiones.append(otra_calle_id)
    ConexionesCalles[calle_id] = conexiones

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Fondo blanco
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)  # Configuración 2D
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_streets():
    glColor3f(0, 0, 0)  # Color negro para las líneas de las calles
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for calle in Calle.values():
        x1, y1 = Intersecciones[calle["origen"]]
        x2, y2 = Intersecciones[calle["destino"]]
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
    glEnd()

def draw_intersections():
    glColor3f(1, 0, 0)  # Color rojo para las intersecciones
    glPointSize(10)
    glBegin(GL_POINTS)
    for coord in Intersecciones.values():
        glVertex2f(coord[0], coord[1])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_streets()
    draw_intersections()
    pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        display()
    pygame.quit()

if __name__ == "__main__":
    main()
