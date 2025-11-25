import pygame
import sys 

# Cargar fondos
FONDO_NIVEL_1 = pygame.transform.scale(pygame.image.load("img1.png"), (800, 600))
FONDO_NIVEL_2 = pygame.transform.scale(pygame.image.load("img1.png"), (800, 600))  # Mismo fondo por ahora

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

class Nivel2(NivelBase):
    def __init__(self):
        pinchos = []
        
        # Patrón diferente para el nivel 2
        x = 400
        for i in range(8):
            pinchos.append(pygame.Rect(x, Suelo_Y - 30, 30, 40))
            x += 250  # Más juntos que en el nivel 1
            
        # Agregar algunos pinchos dobles
        pinchos.append(pygame.Rect(600, Suelo_Y - 30, 30, 40))
        pinchos.append(pygame.Rect(630, Suelo_Y - 30, 30, 40))
        
        pinchos.append(pygame.Rect(1000, Suelo_Y - 30, 30, 40))
        pinchos.append(pygame.Rect(1030, Suelo_Y - 30, 30, 40))

        super().__init__(FONDO_NIVEL_2, pinchos)

def reiniciar_nivel():
    global player_y, velocidad_y, en_suelo, nivel_actual
    player_y = Suelo_Y - player_size
    velocidad_y = 0
    en_suelo = True
    # Mantener el mismo nivel actual al reiniciar
    if isinstance(nivel_actual, Nivel1):
        nivel_actual = Nivel1()
    elif isinstance(nivel_actual, Nivel2):
        nivel_actual = Nivel2()

def game_over():
    font = pygame.font.SysFont(None, 60)
    texto = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(texto, (250, 250))
    pygame.display.flip()
    pygame.time.wait(1500)

    reiniciar_nivel()   # ← Reiniciar sin cerrar el juego

def victoria():
    font = pygame.font.SysFont(None, 60)
    texto = font.render("¡GANASTE!", True, (0, 255, 0))
    screen.blit(texto, (250, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    
    # Si estamos en el nivel 1, pasar al nivel 2
    if isinstance(nivel_actual, Nivel1):
        nivel_actual = Nivel2()
        reiniciar_nivel()
    else:
        # Si estamos en el nivel 2, mostrar mensaje de victoria final
        font = pygame.font.SysFont(None, 40)
        texto = font.render("¡FELICIDADES! Completaste todos los niveles", True, (0, 255, 0))
        screen.blit(texto, (150, 350))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

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

    boton_nivel1 = pygame.Rect(250, 200, 300, 60)
    pygame.draw.rect(screen, (150, 0, 200), boton_nivel1)

    txt = pygame.font.SysFont(None, 50).render("Nivel 1", True, (255, 255, 255))
    screen.blit(txt, (330, 210))
    
    boton_nivel2 = pygame.Rect(250, 300, 300, 60)
    pygame.draw.rect(screen, (200, 100, 0), boton_nivel2)

    txt2 = pygame.font.SysFont(None, 50).render("Nivel 2", True, (255, 255, 255))
    screen.blit(txt2, (330, 310))

    return boton_nivel1, boton_nivel2

nivel_actual = Nivel1()
estado_juego = "menu"

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
        boton_nivel1, boton_nivel2 = dibujar_menu_niveles()

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
        
        # Mostrar indicador de nivel actual
        font = pygame.font.SysFont(None, 30)
        if isinstance(nivel_actual, Nivel1):
            nivel_texto = font.render("Nivel 1", True, (255, 255, 255))
        else:
            nivel_texto = font.render("Nivel 2", True, (255, 255, 255))
        screen.blit(nivel_texto, (20, 20))

    pygame.display.flip()
    clock.tick(Fps)
    