import pygame
import sys 

FONDO_NIVEL_1 = pygame.transform.scale(pygame.image.load("img1.png"), (800, 600))

Ancho = 800
Alto = 600
black = (0, 0, 0)
Fps = 60

Suelo_Y = Alto - 50 
player_size = 40
player_x = 100
player_y = Suelo_Y - player_size
player_color = (255, 255, 0)
color_piso = (104, 106, 217)

velocidad_y = 0
velocidad_x = 5
gravedad = 0.8
fuerza_salto = -15
en_suelo = True

pygame.init()
pygame.display.set_caption("Geometry Dash")
screen = pygame.display.set_mode((Ancho, Alto))
clock = pygame.time.Clock()

class NivelBase:
    def __init__(self, fondo, pinchos):
        self.fondo = fondo
        self.pinchos = pinchos
        self.velocidad_nivel = 6  

    def actualizar(self):
        for p in self.pinchos:
            p.x -= self.velocidad_nivel

        for p in self.pinchos[:]:
            if p.x <= -50:
                self.pinchos.remove(p)

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        for rect in self.pinchos:
            self.dibujar_pincho(rect, pantalla)

    def dibujar_pincho(self, rect, pantalla):
        p1 = (rect.x, rect.y + rect.height)
        p2 = (rect.x + rect.width, rect.y + rect.height)
        p3 = (rect.x + rect.width / 2, rect.y)
        pygame.draw.polygon(pantalla, (226, 92, 250), [p1, p2, p3])

class Nivel1(NivelBase):
    def __init__(self):
        pinchos = []
        
        x = 500
        for i in range(10):
            pinchos.append(pygame.Rect(x, Suelo_Y - 30, 50, 40))
            x += 350  

        super().__init__(FONDO_NIVEL_1, pinchos)

def esta_dentro_del_triangulo(px, py, p1, p2, p3):
    # Usamos el método de barycentric coordinates para ver si un punto está dentro del triángulo
    denom = (p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1])
    if denom == 0:
        return False

    a = ((p2[1] - p3[1]) * (px - p3[0]) + (p3[0] - p2[0]) * (py - p3[1])) / denom
    b = ((p3[1] - p1[1]) * (px - p3[0]) + (p1[0] - p3[0]) * (py - p3[1])) / denom
    c = 1 - a - b

    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

def colision_con_pincho(player_rect, pincho_rect):
    # Obtenemos los puntos del triángulo
    p1 = (pincho_rect.x, pincho_rect.y + pincho_rect.height)
    p2 = (pincho_rect.x + pincho_rect.width, pincho_rect.y + pincho_rect.height)
    p3 = (pincho_rect.x + pincho_rect.width / 2, pincho_rect.y)

    # Verificamos si alguno de los 4 vértices del jugador está dentro del triángulo
    for px, py in [(player_rect.x, player_rect.y),
                   (player_rect.x + player_rect.width, player_rect.y),
                   (player_rect.x, player_rect.y + player_rect.height),
                   (player_rect.x + player_rect.width, player_rect.y + player_rect.height)]:
        if esta_dentro_del_triangulo(px, py, p1, p2, p3):
            return True
    return False

def game_over():
    font = pygame.font.SysFont(None, 60)
    texto = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(texto, (250, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def victoria():
    font = pygame.font.SysFont(None, 60)
    texto = font.render("¡GANASTE!", True, (0, 255, 0))
    screen.blit(texto, (250, 250))
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
            if evento.key == pygame.K_SPACE and en_suelo:
                velocidad_y = fuerza_salto
                en_suelo = False

    velocidad_y += gravedad
    player_y += velocidad_y

    if player_y >= Suelo_Y - player_size:
        player_y = Suelo_Y - player_size
        velocidad_y = 0
        en_suelo = True

    nivel_actual.actualizar()

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # COLISIÓN CON PINCHOS (ahora con el triángulo)
    for p in nivel_actual.pinchos:
        if colision_con_pincho(player_rect, p):
            game_over()

    # FIN DEL JUEGO
    if len(nivel_actual.pinchos) == 0:
        victoria()

    nivel_actual.dibujar(screen)
    pygame.draw.rect(screen, color_piso, (0, Suelo_Y, Ancho, 50))
    pygame.draw.rect(screen, player_color, player_rect)

    pygame.display.flip()
    clock.tick(Fps)

pygame.quit()
sys.exit()