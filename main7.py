import pygame
import sys 


FONDO_NIVEL_1 = pygame.transform.scale(pygame.image.load("img1.png"), (800, 600))
FONDO_NIVEL_2 = pygame.transform.scale(pygame.image.load("img2.png"), (800, 600))
FONDO_NIVEL_3 = pygame.transform.scale(pygame.image.load("img3.jpeg"), (800, 600))  # ← NUEVO FONDO NIVEL 3


Ancho = 800
Alto = 600
black = (0, 0, 0)
Fps = 60


Suelo_Y = Alto - 50 
player_size = 40
player_x = 100
player_y = Suelo_Y - player_size

# ============================================
# COLORES DEL PERSONAJE PERSONALIZADO
# ============================================
color_borde_externo = (128, 0, 128)   # Morado oscuro (borde exterior)
color_verde = (0, 255, 0)              # Verde brillante (capa media)
color_borde_morado = (75, 0, 130)      # Morado (borde interno)
color_celeste = (0, 191, 255)          # Celeste (cuadrado central)

color_piso = (104, 106, 217)


velocidad_y = 0
velocidad_x = 5
gravedad = 0.8
fuerza_salto = -15
en_suelo = True
en_plataforma = False  # ← NUEVO: Detectar si está en plataforma


pygame.init()
pygame.display.set_caption("Geometry Dash")
screen = pygame.display.set_mode((Ancho, Alto))
clock = pygame.time.Clock()


# ============================================
# FUNCIÓN PARA DIBUJAR EL PERSONAJE
# ============================================
def dibujar_personaje(pantalla, rect):
    """
    Dibuja el personaje en capas:
    Morado oscuro → Verde → Morado → Celeste
    """
    # CAPA 1: Borde exterior MORADO OSCURO
    pygame.draw.rect(pantalla, color_borde_externo, rect)
    
    # CAPA 2: Cuadrado VERDE
    rect_verde = rect.inflate(-6, -6)  
    pygame.draw.rect(pantalla, color_verde, rect_verde)
    
    # CAPA 3: Borde MORADO interno
    rect_borde_interno = rect_verde.inflate(-8, -8)
    pygame.draw.rect(pantalla, color_borde_morado, rect_borde_interno)
    
    # CAPA 4: Cuadrado CELESTE central
    rect_celeste = rect_borde_interno.inflate(-8, -8)
    pygame.draw.rect(pantalla, color_celeste, rect_celeste)


class ObjetoJuego:
    def __init__(self, x, y, ancho, alto, color):
        self.x, self.y, self.ancho, self.alto, self.color = x, y, ancho, alto, color
        self.rectangulo = pygame.Rect(x, y, ancho, alto)

class NivelBase:
    def __init__(self, fondo, pinchos, plataformas=None):  # ← Agregado plataformas
        self.fondo = fondo
        self.pinchos = pinchos
        self.plataformas = plataformas if plataformas else []  # ← Lista de plataformas
        self.velocidad_nivel = 6  

    def actualizar(self):
        # Mover pinchos
        for p in self.pinchos:
            p.x -= self.velocidad_nivel

        for p in self.pinchos[:]:
            if p.x <= -50:
                self.pinchos.remove(p)
        
        # ← NUEVO: Mover plataformas
        for plat in self.plataformas:
            plat.x -= self.velocidad_nivel
        
        for plat in self.plataformas[:]:
            if plat.x <= -100:
                self.plataformas.remove(plat)

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        
        # Dibujar plataformas flotantes
        for plat in self.plataformas:
            pygame.draw.rect(pantalla, (255, 100, 0), plat)  # Naranja brillante
            pygame.draw.rect(pantalla, (200, 50, 0), plat, 3)  # Borde oscuro
        
        # Dibujar pinchos
        for rect in self.pinchos:
            self.dibujar_pincho(rect, pantalla)

    def dibujar_pincho(self, rect, pantalla):
        p1 = (rect.x, rect.y + rect.height)
        p2 = (rect.x + rect.width, rect.y + rect.height)
        p3 = (rect.x + rect.width / 2, rect.y)
        pygame.draw.polygon(pantalla, (226, 92, 250), [p1, p2, p3])


# ==================== NIVEL 1 ====================
class Nivel1(NivelBase):
    def __init__(self):
        pinchos = []
        
        x = 500
        for i in range(10):
            pinchos.append(pygame.Rect(x, Suelo_Y - 30, 30, 40))
            x += 350  

        super().__init__(FONDO_NIVEL_1, pinchos)


# ==================== NIVEL 2 ====================
class Nivel2(NivelBase):
    def __init__(self):
        pinchos = []
        
        x = 400
        for i in range(15):
            if i % 3 == 0:
                pinchos.append(pygame.Rect(x, Suelo_Y - 35, 35, 45))
            else:
                pinchos.append(pygame.Rect(x, Suelo_Y - 30, 30, 40))
            
            if i % 2 == 0:
                x += 250
            else:
                x += 320

        super().__init__(FONDO_NIVEL_2, pinchos)


# ==================== NIVEL 3 - MEJORADO ====================
class Nivel3(NivelBase):
    def __init__(self):
        pinchos = []
        plataformas = []  # ← NUEVO: Lista de plataformas flotantes
        
        # Nivel 3: Patrón complejo con pinchos Y plataformas en el aire
        x = 350
        for i in range(25):  # ← Aumentado de 20 a 25 obstáculos
            
            # Cada 4 obstáculos, crear plataforma flotante
            if i % 4 == 0 and i > 0:
                # Plataforma en el aire (a diferentes alturas)
                altura_plataforma = Suelo_Y - 120 - (i % 3) * 30  # Alturas variables
                plataformas.append(pygame.Rect(x, altura_plataforma, 80, 15))
                x += 100
            
            # Crear grupos de pinchos juntos
            if i % 6 == 0 or i % 6 == 1:
                # Grupo de pinchos muy juntos (difícil)
                pinchos.append(pygame.Rect(x, Suelo_Y - 32, 28, 38))
                x += 160  # Muy juntos
            elif i % 6 == 2:
                # Pincho GIGANTE
                pinchos.append(pygame.Rect(x, Suelo_Y - 45, 40, 55))
                x += 280
            elif i % 6 == 3:
                # Doble pincho
                pinchos.append(pygame.Rect(x, Suelo_Y - 30, 30, 40))
                pinchos.append(pygame.Rect(x + 35, Suelo_Y - 30, 30, 40))
                x += 250
            else:
                # Pincho normal
                pinchos.append(pygame.Rect(x, Suelo_Y - 30, 30, 40))
                x += 240

        super().__init__(FONDO_NIVEL_3, pinchos, plataformas)  # ← Pasar plataformas
        self.velocidad_nivel = 8  # ← Aumentado de 7 a 8 (MÁS RÁPIDO)


def reiniciar_nivel():
    global player_y, velocidad_y, en_suelo, en_plataforma  # ← Agregado en_plataforma
    player_y = Suelo_Y - player_size
    velocidad_y = 0
    en_suelo = True
    en_plataforma = False


def game_over():
    font = pygame.font.SysFont(None, 60)
    texto = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(texto, (250, 250))
    pygame.display.flip()
    pygame.time.wait(1500)

    reiniciar_nivel()


def victoria():
    global estado_juego, nivel_completado
    font = pygame.font.SysFont(None, 60)
    texto = font.render("¡GANASTE!", True, (0, 255, 0))
    screen.blit(texto, (250, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    
    estado_juego = "niveles"
    nivel_completado += 1

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
    boton_nivel1 = pygame.Rect(250, 150, 300, 60)
    pygame.draw.rect(screen, (150, 0, 200), boton_nivel1)
    txt = pygame.font.SysFont(None, 50).render("Nivel 1", True, (255, 255, 255))
    screen.blit(txt, (330, 160))

    # Botón Nivel 2
    boton_nivel2 = pygame.Rect(250, 240, 300, 60)
    pygame.draw.rect(screen, (200, 0, 150), boton_nivel2)
    txt2 = pygame.font.SysFont(None, 50).render("Nivel 2", True, (255, 255, 255))
    screen.blit(txt2, (330, 250))

    # Botón Nivel 3 - NUEVO
    boton_nivel3 = pygame.Rect(250, 330, 300, 60)
    pygame.draw.rect(screen, (255, 0, 100), boton_nivel3)
    txt3 = pygame.font.SysFont(None, 50).render("Nivel 3", True, (255, 255, 255))
    screen.blit(txt3, (330, 340))

    return boton_nivel1, boton_nivel2, boton_nivel3


nivel_actual = Nivel1()
estado_juego = "menu"
nivel_completado = 0



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
                
                # ← NUEVO: Detectar clic en Nivel 3
                elif boton_nivel3.collidepoint(evento.pos):
                    nivel_actual = Nivel3()
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
        boton_nivel1, boton_nivel2, boton_nivel3 = dibujar_menu_niveles()

    elif estado_juego == "jugando":

        velocidad_y += gravedad
        player_y += velocidad_y

        # Resetear estado de plataforma
        en_plataforma = False

        # Detectar colisión con suelo
        if player_y >= Suelo_Y - player_size:
            player_y = Suelo_Y - player_size
            velocidad_y = 0
            en_suelo = True
        else:
            en_suelo = False

        nivel_actual.actualizar()

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # ← NUEVO: Colisión con plataformas flotantes
        for plat in nivel_actual.plataformas:
            # Si el jugador está cayendo Y toca la plataforma desde arriba
            if player_rect.colliderect(plat) and velocidad_y > 0:
                # Colocar jugador encima de la plataforma
                if player_rect.bottom >= plat.top and player_rect.top < plat.top:
                    player_y = plat.top - player_size
                    velocidad_y = 0
                    en_suelo = True
                    en_plataforma = True

        # Colisión con pinchos
        for p in nivel_actual.pinchos:
            if player_rect.colliderect(p):
                game_over()

        if len(nivel_actual.pinchos) == 0:
            victoria()

        nivel_actual.dibujar(screen)
        pygame.draw.rect(screen, color_piso, (0, Suelo_Y, Ancho, 50))
        
        # Dibujar personaje personalizado
        dibujar_personaje(screen, player_rect)

    pygame.display.flip()
    clock.tick(Fps)