import pygame
import sys 

# --- CONFIGURACIÓN DEL JUEGO ---
Ancho = 800
Alto = 600
black = (0, 0, 0)
Fps = 60

# --- COLORES GLOBALES ---
COLOR_SUELO_NIVEL1 = (104, 106, 217) # Azul/Morado original
COLOR_SUELO_NIVEL2 = (0, 150, 0)     # Verde para Nivel 2
COLOR_JUGADOR_NIVEL1 = (255, 255, 0) # Amarillo
COLOR_JUGADOR_NIVEL2 = (0, 200, 255) # Azul

# La imagen de fondo debe existir. Usaremos un color de fondo si la imagen no carga.
try:
    FONDO_NIVEL_1 = pygame.transform.scale(pygame.image.load("image.png"), (Ancho, Alto))
except pygame.error:
    print("Advertencia: No se pudo cargar 'image.png'. Usando fondo negro.")
    FONDO_NIVEL_1 = pygame.Surface((Ancho, Alto))
    FONDO_NIVEL_1.fill(black)

# --- CARGAR FONDO NIVEL 2 ---
try:
    # Intenta cargar la imagen 'IMG2.PNG'
    FONDO_NIVEL_2 = pygame.transform.scale(pygame.image.load("IMG2.PNG"), (Ancho, Alto))
    print("Fondo de Nivel 2 (IMG2.PNG) cargado exitosamente.")
except pygame.error:
    # Si la carga falla (por ejemplo, el archivo no existe o está mal escrito), usa un color de prueba
    print("Advertencia: No se pudo cargar 'IMG2.PNG'. Usando fondo azul/morado de prueba.")
    FONDO_NIVEL_2 = pygame.Surface((Ancho, Alto))
    FONDO_NIVEL_2.fill((100, 100, 150)) # Color diferente para que se note el cambio
    
# --- NUEVA CONFIGURACIÓN GLOBAL ---
nivel_actual_index = 0 # 0 para Nivel 1, 1 para Nivel 2, etc.
niveles = [] # Lista de clases de nivel para gestionar la transición

Suelo_Y = Alto - 50
player_size = 40
player_x = 100
player_y = Suelo_Y - player_size

# Variables del jugador que se actualizarán
player_color = COLOR_JUGADOR_NIVEL1
color_piso = COLOR_SUELO_NIVEL1

# --- VARIABLES DE MOVIMIENTO ---
velocidad_y = 0
gravedad = 0.8
fuerza_salto = -15
en_suelo = True

# --- INICIALIZACIÓN DE PYGAME ---
pygame.init()
pygame.display.set_caption("Geometry Dash - Versión Columna y Colores")
screen = pygame.display.set_mode((Ancho, Alto))
clock = pygame.time.Clock()

class ObjetoJuego:
    def __init__(self, x, y, ancho, alto, color):
        self.x, self.y, self.ancho, self.alto, self.color = x, y, ancho, alto, color
        self.rectangulo = pygame.Rect(x, y, ancho, alto)

class NivelBase:
    # MODIFICADO: Ahora el nivel tiene una lista de bloques
    def __init__(self, fondo, pinchos, bloques, velocidad_nivel=6, color_piso_nivel=COLOR_SUELO_NIVEL1):
        self.fondo = fondo
        self.pinchos = pinchos
        self.bloques = bloques # NUEVO: Lista de rectángulos sólidos (columnas)
        self.velocidad_nivel = velocidad_nivel
        self.color_piso_nivel = color_piso_nivel

    def actualizar(self):
        # Mover pinchos
        for p in self.pinchos:
            p.x -= self.velocidad_nivel
        # Mover bloques
        for b in self.bloques:
            b.x -= self.velocidad_nivel

        # Eliminar pinchos que salen de la pantalla
        for p in self.pinchos[:]:
            if p.x <= -p.width:
                self.pinchos.remove(p)
        
        # Eliminar bloques que salen de la pantalla
        for b in self.bloques[:]:
            if b.x <= -b.width:
                self.bloques.remove(b)

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        
        # Dibujar bloques
        for rect in self.bloques:
            pygame.draw.rect(pantalla, (255, 255, 255), rect) # Dibujar el bloque en blanco
            
        # Dibujar pinchos
        for rect in self.pinchos:
            self.dibujar_pincho(rect, pantalla)


    def dibujar_pincho(self, rect, pantalla):
        # El pincho es un triángulo con base en la parte inferior del rect
        
        # Puntos del triángulo: (pico superior, esquina inferior izquierda, esquina inferior derecha)
        p1 = (rect.x + rect.width / 2, rect.y) # Pico superior
        p2 = (rect.x, rect.y + rect.height) # Esquina inferior izquierda
        p3 = (rect.x + rect.width, rect.y + rect.height) # Esquina inferior derecha
        
        pygame.draw.polygon(pantalla, (255, 0, 0), [p1, p2, p3])

# --- CLASE DEL NIVEL 1 ---
class Nivel1(NivelBase):
    def __init__(self):
        pinchos = []
        bloques = []
        ALTURA_PINCHO = 30
        
        x = 500
        for i in range(10):
            pinchos.append(pygame.Rect(x, Suelo_Y - ALTURA_PINCHO, 80, ALTURA_PINCHO))
            x += 350  
            
        # Nivel 1 no tiene bloques, solo pinchos
        super().__init__(FONDO_NIVEL_1, pinchos, bloques, velocidad_nivel=6, color_piso_nivel=COLOR_SUELO_NIVEL1) 

# --- CLASE DEL NIVEL 2 (NUEVO CON BLOQUES Y PINCHOS) ---
class Nivel2(NivelBase):
    def __init__(self):
        pinchos = []
        bloques = []
        ALTURA_PINCHO = 30
        
        x = 600
        
        # Diseño del Nivel 2: Bloques (columnas) y Pinchos intercalados
        for i in range(10):
            # 1. Columna/Bloque
            if i % 2 == 0:
                ALTURA_BLOQUE = 80
                bloques.append(pygame.Rect(x, Suelo_Y - ALTURA_BLOQUE, 100, ALTURA_BLOQUE))
                x += 250
            # 2. Pinchos dobles
            else:
                pinchos.append(pygame.Rect(x, Suelo_Y - ALTURA_PINCHO, 80, ALTURA_PINCHO))
                pinchos.append(pygame.Rect(x + 50, Suelo_Y - ALTURA_PINCHO, 80, ALTURA_PINCHO))
                x += 350 
            
        # Velocidad del Nivel 2: 8 (más rápido)
        # Usa FONDO_NIVEL_2 y el nuevo color de piso verde
        super().__init__(FONDO_NIVEL_2, pinchos, bloques, velocidad_nivel=8, color_piso_nivel=COLOR_SUELO_NIVEL2) 

# --- FUNCIÓN DE COLISIÓN GEOMÉTRICA ---
def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def is_point_in_triangle(pt, v1, v2, v3):
    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def verificar_colision_pincho(player_rect, pincho_rect):
    if not player_rect.colliderect(pincho_rect):
        return False

    A = (pincho_rect.x + pincho_rect.width / 2, pincho_rect.y) # Pico superior
    B = (pincho_rect.x, pincho_rect.y + pincho_rect.height)     # Abajo Izquierda
    C = (pincho_rect.x + pincho_rect.width, pincho_rect.y + pincho_rect.height) # Abajo Derecha

    puntos_jugador = [
        (player_rect.left, player_rect.bottom),  # Esquina inferior izquierda
        (player_rect.right, player_rect.bottom), # Esquina inferior derecha
        (player_rect.centerx, player_rect.bottom) # Centro inferior
    ]
    
    # Solo necesitamos chequear la punta del pincho. Si las esquinas de la base tocan, 
    # significa que el jugador está en la zona de "muerte".
    for pt in puntos_jugador:
        if is_point_in_triangle(pt, A, B, C):
            return True 
            
    return False 

# --- ESTADOS DEL JUEGO ---

def game_over():
    font = pygame.font.SysFont("Arial", 60, bold=True)
    texto = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(texto, (Ancho // 2 - texto.get_width() // 2, Alto // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


def victoria():
    font = pygame.font.SysFont("Arial", 60, bold=True)
    texto = font.render("¡GANASTE!", True, (0, 255, 0))
    screen.blit(texto, (Ancho // 2 - texto.get_width() // 2, Alto // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# --- CONFIGURACIÓN DE NIVELES INICIALES ---
# 1. Definir la lista de niveles
niveles = [
    Nivel1(),
    Nivel2()
]

# 2. Inicializar el juego con el primer nivel
nivel_actual_index = 0
nivel_actual = niveles[nivel_actual_index]

# --- NUEVA FUNCIÓN PARA CAMBIAR DE NIVEL ---
def cambiar_nivel():
    global nivel_actual_index, nivel_actual, player_y, velocidad_y, en_suelo
    global player_color, color_piso # MODIFICADO: Ahora cambiamos los colores globales
    
    # Avanzar al siguiente índice
    nivel_actual_index += 1
    
    if nivel_actual_index < len(niveles):
        # Si hay más niveles, cargar el siguiente
        nivel_actual = niveles[nivel_actual_index]
        
        # Reiniciar la posición del jugador
        player_y = Suelo_Y - player_size
        velocidad_y = 0
        en_suelo = True

        # Establecer nuevos colores basados en el nivel
        if nivel_actual_index == 1:
            player_color = COLOR_JUGADOR_NIVEL2
            color_piso = COLOR_SUELO_NIVEL2
        else:
            player_color = COLOR_JUGADOR_NIVEL1
            color_piso = COLOR_SUELO_NIVEL1


        # Mostrar mensaje de transición
        font = pygame.font.SysFont("Arial", 40, bold=True)
        texto = font.render(f"¡NIVEL {nivel_actual_index + 1} INICIADO!", True, (0, 255, 255))
        screen.blit(texto, (Ancho // 2 - texto.get_width() // 2, Alto // 2 - texto.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)
        
    else:
        # Si no hay más niveles, el juego termina
        victoria()


ejecutando = True
while ejecutando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            # Salto solo si está en el suelo
            if evento.key == pygame.K_SPACE and en_suelo:
                velocidad_y = fuerza_salto
                en_suelo = False

    # --- LÓGICA DE MOVIMIENTO DEL JUGADOR ---
    velocidad_y += gravedad
    player_y += velocidad_y

    # Límite del suelo
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    en_suelo_por_bloque = False

    # --- COLISIÓN CON BLOQUES (NUEVA LÓGICA) ---
    # Verifica si el jugador está colisionando con la parte superior de un bloque
    for b in nivel_actual.bloques:
        # 1. Chequeo de colisión de bloque
        if player_rect.colliderect(b):
            # Colisión por arriba (aterrizando sobre el bloque)
            if velocidad_y > 0 and player_rect.bottom <= b.top + velocidad_y: 
                player_y = b.top - player_size # Posicionar justo encima
                velocidad_y = 0
                en_suelo_por_bloque = True
            # Colisión por lado o por abajo (jugador choca y muere)
            else:
                game_over()
    
    # Actualizar estado en el suelo basado en el suelo principal O un bloque
    if player_y >= Suelo_Y - player_size and not en_suelo_por_bloque:
        player_y = Suelo_Y - player_size
        velocidad_y = 0
        en_suelo = True
    elif en_suelo_por_bloque:
        en_suelo = True
    else:
        en_suelo = False


    # Actualizar el nivel (mover pinchos y bloques)
    nivel_actual.actualizar()

    # Crear el rectángulo del jugador para la detección de colisiones (Actualizado arriba)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # --- VERIFICACIÓN DE COLISIÓN CON PINCHOS ---
    for p in nivel_actual.pinchos:
        if verificar_colision_pincho(player_rect, p):  
            game_over()

    # --- VERIFICACIÓN DE VICTORIA/TRANSICIÓN DE NIVEL ---
    # Si el nivel actual se queda sin pinchos Y sin bloques, pasamos al siguiente
    if len(nivel_actual.pinchos) == 0 and len(nivel_actual.bloques) == 0:
        cambiar_nivel() # Llama a la nueva función de transición

    # --- DIBUJO ---
    nivel_actual.dibujar(screen)
    
    # Dibujar el suelo
    pygame.draw.rect(screen, color_piso, (0, Suelo_Y, Ancho, 50))
    
    # Dibujar el jugador
    pygame.draw.rect(screen, player_color, player_rect)

    # Mostrar nivel actual
    font_level = pygame.font.SysFont("Arial", 20, bold=True)
    texto_nivel = font_level.render(f"Nivel: {nivel_actual_index + 1}", True, (255, 255, 255))
    screen.blit(texto_nivel, (10, 10))

    pygame.display.flip()
    clock.tick(Fps)

pygame.quit()
sys.exit()