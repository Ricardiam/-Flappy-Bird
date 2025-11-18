import pygame
import sys 
# fondo

FONDO_NIVEL_1 = pygame.transform.scale(pygame.image.load("image.png"), (800, 600))
# Constantes
Ancho = 800
Alto = 600
black = (0, 0, 0)
Fps = 60

# Personaje
Suelo_Y = Alto - 50
player_size = 40      
player_x = 100       
player_y = Suelo_Y - player_size
player_color = (255, 255, 0)  
color_piso = (104, 106, 217)

# Física
velocidad_y = 0
velocidad_x = 5 
gravedad = 0.8
fuerza_salto = -15
en_suelo = True

# Inicialización
pygame.init()
pygame.display.set_caption("Geometry Dash")
screen = pygame.display.set_mode((Ancho, Alto))
clock = pygame.time.Clock()

# Clase (ObjetoJuego) 

class ObjetoJuego:
    def __init__(self, x, y, ancho, alto, color):
        self.x, self.y, self.ancho, self.alto, self.color = x, y, ancho, alto, color
        self.rectangulo = pygame.Rect(x, y, ancho, alto)

# Loop principal
ejecutando = True
while ejecutando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and en_suelo:
                velocidad_y = fuerza_salto
                en_suelo = False
    
    # ← NUEVO: Movimiento horizontal
    player_x += velocidad_x
    
    # ← NUEVO: Reiniciar posición al salir de pantalla
    if player_x > Ancho:
        player_x = -player_size
    
    # Física del salto
    velocidad_y += gravedad
    player_y += velocidad_y
    
    # Colisión con el suelo
    if player_y >= Suelo_Y - player_size:
        player_y = Suelo_Y - player_size
        velocidad_y = 0
        en_suelo = True
    
    # Renderizado
    screen.blit(FONDO_NIVEL_1, (0, 0))
    pygame.draw.rect(screen, color_piso, (0, Suelo_Y, Ancho, 50))
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))
    
    pygame.display.flip()
    clock.tick(Fps)


pygame.quit()
sys.exit()