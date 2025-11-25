import pygame
import sys 


FONDO_NIVEL_1 = pygame.transform.scale(pygame.image.load("img1.png"), (800, 600))
FONDO_NIVEL_2 = pygame.transform.scale(pygame.image.load("img2.png"), (800, 600))  # ← NUEVO FONDO


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


class ObjetoJuego:
    def __init__(self, x, y, ancho, alto, color):
        self.x, self.y, self.ancho, self.alto, self.color = x, y, ancho, alto, color
        self.rectangulo = pygame.Rect(x, y, ancho, alto)

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
            pinchos.append(pygame.Rect(x, Suelo_Y - 30, 30, 40))
            x += 350  

        super().__init__(FONDO_NIVEL_1, pinchos)


# ==================== NUEVO NIVEL 2 ====================
class Nivel2(NivelBase):
    def __init__(self):
        pinchos = []
        
        # Patrón más difícil: pinchos más juntos y en diferentes alturas
        x = 400
        for i in range(15):
            # Alterna entre pinchos en el suelo y pinchos más altos
            if i % 3 == 0:
                # Pincho más alto (requiere salto más preciso)
                pinchos.append(pygame.Rect(x, Suelo_Y - 35, 35, 45))
            else:
                # Pincho normal
                pinchos.append(pygame.Rect(x, Suelo_Y - 30, 30, 40))
            
            # Distancia variable entre pinchos (más desafiante)
            if i % 2 == 0:
                x += 250  # Más cerca
            else:
                x += 320  # Un poco más lejos

        super().__init__(FONDO_NIVEL_2, pinchos)
# ======================================================


def reiniciar_nivel():
    global player_y, velocidad_y, en_suelo
    player_y = Suelo_Y - player_size
    velocidad_y = 0
    en_suelo = True


def game_over():
    font = pygame.font.SysFont(None, 60)
    texto = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(texto, (250, 250))
    pygame.display.flip()
    pygame.time.wait(1500)

    reiniciar_nivel()


def victoria():
    global estado_juego, nivel_completado  # ← MODIFICADO
    font = pygame.font.SysFont(None, 60)
    texto = font.render("¡GANASTE!", True, (0, 255, 0))
    screen.blit(texto, (250, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    
    # En lugar de cerrar, volver al menú de niveles
    estado_juego = "niveles"
    nivel_completado += 1  # ← Marcar nivel como completado

def dibujar_menu():
    screen.fill((30, 30, 30))

    font = pygame.font.SysFont(None, 80)
    titulo = font.render("Geometry Dash", True, (255, 255, 0))
    screen.blit(titulo, (180, 100))

    boton_jugar = pygame.Rect(300, 250, 200, 60)
    pygame.draw.rect(screen, (100, 100, 255), boton_jugar)

    texto = pygame.font.SysFont(None, 50).render("JUGAR", True, (255, 255, 255))
    screen.blit(texto, (345, 260))

    return boton_jugar


def dibujar_menu_niveles():
    screen.fill((20, 20, 60))
    font = pygame.font.SysFont(None, 60)
    texto = font.render("NIVELES", True, (255, 255, 0))
    screen.blit(texto, (300, 50))

    # Botón Nivel 1
    boton_nivel1 = pygame.Rect(250, 180, 300, 60)
    pygame.draw.rect(screen, (150, 0, 200), boton_nivel1)
    txt = pygame.font.SysFont(None, 50).render("Nivel 1", True, (255, 255, 255))
    screen.blit(txt, (330, 190))

    # Botón Nivel 2 (NUEVO)
    boton_nivel2 = pygame.Rect(250, 280, 300, 60)
    pygame.draw.rect(screen, (200, 0, 150), boton_nivel2)
    txt2 = pygame.font.SysFont(None, 50).render("Nivel 2", True, (255, 255, 255))
    screen.blit(txt2, (330, 290))

    return boton_nivel1, boton_nivel2


nivel_actual = Nivel1()
estado_juego = "menu"
nivel_completado = 0  # ← Contador de niveles completados



ejecutando = True
while ejecutando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

   
        if estado_juego == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    estado_juego = "niveles"

  
        elif estado_juego == "niveles":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_nivel1.collidepoint(evento.pos):
                    nivel_actual = Nivel1()
                    reiniciar_nivel()
                    estado_juego = "jugando"
                
                # ← NUEVO: Detectar clic en Nivel 2
                elif boton_nivel2.collidepoint(evento.pos):
                    nivel_actual = Nivel2()
                    reiniciar_nivel()
                    estado_juego = "jugando"

        
        elif estado_juego == "jugando":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo:
                    velocidad_y = fuerza_salto
                    en_suelo = False

   
    if estado_juego == "menu":
        boton_jugar = dibujar_menu()

    elif estado_juego == "niveles":
        boton_nivel1, boton_nivel2 = dibujar_menu_niveles()  # ← MODIFICADO

    elif estado_juego == "jugando":

        velocidad_y += gravedad
        player_y += velocidad_y

        if player_y >= Suelo_Y - player_size:
            player_y = Suelo_Y - player_size
            velocidad_y = 0
            en_suelo = True

        nivel_actual.actualizar()

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        for p in nivel_actual.pinchos:
            if player_rect.colliderect(p):
                game_over()

        if len(nivel_actual.pinchos) == 0:
            victoria()

        nivel_actual.dibujar(screen)
        pygame.draw.rect(screen, color_piso, (0, Suelo_Y, Ancho, 50))
        pygame.draw.rect(screen, player_color, player_rect)

    pygame.display.flip()
    clock.tick(Fps)