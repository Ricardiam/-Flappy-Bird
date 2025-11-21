import pygame
import sys 

# --- CONFIGURACIÓN DEL JUEGO ---
Ancho = 800
Alto = 600
black = (0, 0, 0)
Fps = 60

# La imagen de fondo debe existir. Usaremos un color de fondo si la imagen no carga.
try:
    FONDO_NIVEL_1 = pygame.transform.scale(pygame.image.load("image.png"), (Ancho, Alto))
except pygame.error:
    print("Advertencia: No se pudo cargar 'image.png'. Usando fondo negro.")
    FONDO_NIVEL_1 = pygame.Surface((Ancho, Alto))
    FONDO_NIVEL_1.fill(black)


Suelo_Y = Alto - 50
player_size = 40
player_x = 100
player_y = Suelo_Y - player_size
player_color = (255, 255, 0) # Amarillo
color_piso = (104, 106, 217) # Azul/Morado

# --- VARIABLES DE MOVIMIENTO ---
velocidad_y = 0
gravedad = 0.8
fuerza_salto = -15
en_suelo = True

# --- INICIALIZACIÓN DE PYGAME ---
pygame.init()
pygame.display.set_caption("Geometry Dash - Versión Corregida")
screen = pygame.display.set_mode((Ancho, Alto))
clock = pygame.time.Clock()

class ObjetoJuego:
    def __init__(self, x, y, ancho, alto, color):
        self.x, self.y, self.ancho, self.alto, self.color = x, y, ancho, alto, color
        self.rectangulo = pygame.Rect(x, y, ancho, alto)

class NivelBase:
    def __init__(self, fondo, pinchos):
        self.fondo = fondo
        self.pinchos = pinchos
        self.velocidad_nivel = 6  # Velocidad de movimiento del nivel

    def actualizar(self):
        for p in self.pinchos:
            # Mover el pincho hacia la izquierda
            p.x -= self.velocidad_nivel

        # Eliminar pinchos que salen de la pantalla
        for p in self.pinchos[:]:
            if p.x <= -p.width:
                self.pinchos.remove(p)

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        for rect in self.pinchos:
            self.dibujar_pincho(rect, pantalla)

    def dibujar_pincho(self, rect, pantalla):
        # El pincho es un triángulo con base en la parte inferior del rect
        # La altura del pincho debe ser la altura del rectángulo (rect.height)
        
        # Puntos del triángulo: (pico superior, esquina inferior izquierda, esquina inferior derecha)
        p1 = (rect.x + rect.width / 2, rect.y) # Pico superior
        p2 = (rect.x, rect.y + rect.height) # Esquina inferior izquierda
        p3 = (rect.x + rect.width, rect.y + rect.height) # Esquina inferior derecha
        
        pygame.draw.polygon(pantalla, (255, 0, 0), [p1, p2, p3])

class Nivel1(NivelBase):
    def __init__(self):
        pinchos = []
        
        # Altura del pincho (30px para que se asiente limpiamente sobre el suelo de 50px de altura)
        ALTURA_PINCHO = 30
        
        x = 500
        for i in range(10):
            # IMPORTANTE: Se corrigió la altura a 30 para que el triángulo base esté en Suelo_Y (550)
            # Y la parte superior esté en Suelo_Y - 30 (520)
            pinchos.append(pygame.Rect(x, Suelo_Y - ALTURA_PINCHO, 80, ALTURA_PINCHO))
            x += 350  
            
        super().__init__(FONDO_NIVEL_1, pinchos)


# --- FUNCIÓN DE COLISIÓN GEOMÉTRICA (La Solución) ---

# Implementación de la función 'sign' para el método de punto-en-triángulo (sign method)
def sign(p1, p2, p3):
    # Calcula el producto cruzado 2D. 
    # El signo indica si el punto p3 está a la izquierda o derecha de la línea p1-p2.
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def is_point_in_triangle(pt, v1, v2, v3):
    # Un punto 'pt' está dentro del triángulo (v1, v2, v3) si tiene el mismo 'sign' 
    # (o cero) con respecto a los tres lados del triángulo.
    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    # Retorna True si los signos no son mixtos (es decir, todos son positivos o todos son negativos/cero)
    return not (has_neg and has_pos)

def verificar_colision_pincho(player_rect, pincho_rect):
    # 1. Verificar colisión de rectángulo simple (hitbox grueso)
    if not player_rect.colliderect(pincho_rect):
        return False

    # 2. Si hay colisión de rectángulo, verificar si el jugador golpea el triángulo real
    
    # Obtener las coordenadas del triángulo del pincho (Vértices A, B, C)
    A = (pincho_rect.x + pincho_rect.width / 2, pincho_rect.y) # Pico superior
    B = (pincho_rect.x, pincho_rect.y + pincho_rect.height)     # Abajo Izquierda
    C = (pincho_rect.x + pincho_rect.width, pincho_rect.y + pincho_rect.height) # Abajo Derecha

    # Puntos críticos del jugador a verificar (esquinas inferiores y centro inferior)
    puntos_jugador = [
        (player_rect.left, player_rect.bottom),  # Esquina inferior izquierda
        (player_rect.right, player_rect.bottom), # Esquina inferior derecha
        (player_rect.centerx, player_rect.bottom) # Centro inferior
    ]
    
    # Verificar si alguno de los puntos críticos está DENTRO del triángulo
    for pt in puntos_jugador:
        if is_point_in_triangle(pt, A, B, C):
            return True # ¡Colisión confirmada!
            
    return False # Hubo superposición de rectángulos, pero no de geometría real

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


nivel_actual = Nivel1()


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
    if player_y >= Suelo_Y - player_size:
        player_y = Suelo_Y - player_size
        velocidad_y = 0
        en_suelo = True

    # Actualizar el nivel (mover pinchos)
    nivel_actual.actualizar()

    # Crear el rectángulo del jugador para la detección de colisiones
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # --- VERIFICACIÓN DE COLISIÓN (USANDO LA FUNCIÓN CORREGIDA) ---
    for p in nivel_actual.pinchos:
        # Usa la nueva función de colisión geométrica
        if verificar_colision_pincho(player_rect, p):  
            game_over()

    # --- VERIFICACIÓN DE VICTORIA ---
    if len(nivel_actual.pinchos) == 0:
        victoria()

    # --- DIBUJO ---
    nivel_actual.dibujar(screen)
    
    # Dibujar el suelo
    pygame.draw.rect(screen, color_piso, (0, Suelo_Y, Ancho, 50))
    
    # Dibujar el jugador
    pygame.draw.rect(screen, player_color, player_rect)

    pygame.display.flip()
    clock.tick(Fps)

pygame.quit()
sys.exit()