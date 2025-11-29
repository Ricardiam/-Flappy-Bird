import sys
import time
import pygame

# Inicialización de pygame
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Geometry Dash Básico")
reloj = pygame.time.Clock()

# Colores
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (100, 100, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
MORADO = (200, 100, 200)

# Constantes del juego
SUELO_Y = ALTO - 50  # Posición Y del suelo

# ====================================================================
# MATRICES DE NIVELES
# ====================================================================

NIVEL_1 = [
    ["pincho", 500],
    ["pincho", 800],
    ["pincho", 1100],
    ["pincho", 1400],
    ["pincho", 1700],
    ["pincho", 2000],
]

NIVEL_2 = [
    ["pincho", 400],
    ["pincho", 550],

    ["bloque", 750, 120, 25],
    ["pincho", 950],
    ["pincho", 1100],

    ["pincho", 1300],
    ["pincho", 1450],
    ["pincho", 1600],

    ["bloque", 1800, 80, 40],
    ["bloque", 1920, 80, 60],
    ["bloque", 2040, 80, 80],

    ["pincho", 2200],
    ["pincho", 2350],

    ["bloque", 2550, 200, 30],
    ["pincho", 2650],

    ["bloque", 2850, 60, 100],
    ["bloque", 2920, 60, 80],
    ["bloque", 2990, 60, 60],
    ["bloque", 3060, 60, 40],
    ["bloque", 3130, 60, 20],

    ["pincho", 3250],
    ["pincho", 3400],
    ["pincho", 3550],
    ["pincho", 3700],

    ["bloque", 3900, 150, 35],
    ["pincho", 4100],

    ["bloque", 4300, 100, 50],
    ["pincho", 4500]
]

NIVEL_3 = [
    ["pincho", 300],
    ["pincho", 450],
    ["pincho", 600],
    ["pincho", 800],
    ["pincho", 950],
    ["pincho", 1100],
    ["pincho", 1300],
    ["pincho", 1500],

    ["bloque", 350, 50, 30],
    ["bloque", 650, 50, 30],
    ["bloque", 900, 50, 30],
    ["bloque", 1200, 50, 30],
    ["bloque", 1400, 50, 30]
]

# ====================================================================
# CLASES DEL JUEGO
# ====================================================================

class Jugador:
    def __init__(self):
        self.tamaño = 40
        self.x = 100
        self.y = SUELO_Y - self.tamaño
        self.velocidad_y = 0
        self.gravedad = 0.9
        self.fuerza_salto = -12
        self.en_suelo = True
    
    def saltar(self):
        if self.en_suelo:
            self.velocidad_y = self.fuerza_salto
            self.en_suelo = False
    
    def actualizar(self, obstaculos=None):
        self.velocidad_y += self.gravedad
        self.y += self.velocidad_y
        
        self.en_suelo = False
        
        if self.y >= SUELO_Y - self.tamaño:
            self.y = SUELO_Y - self.tamaño
            self.velocidad_y = 0
            self.en_suelo = True
        
        if obstaculos:
            for obstaculo in obstaculos:
                if isinstance(obstaculo, Bloque):
                    rect_jugador = self.obtener_rectangulo()
                    rect_obstaculo = obstaculo.obtener_rectangulo()
                    
                    if (self.velocidad_y >= 0 and 
                        rect_jugador.bottom >= rect_obstaculo.top and
                        rect_jugador.bottom - self.velocidad_y <= rect_obstaculo.top and
                        rect_jugador.right > rect_obstaculo.left and
                        rect_jugador.left < rect_obstaculo.right):
                        
                        self.y = rect_obstaculo.top - self.tamaño
                        self.velocidad_y = 0
                        self.en_suelo = True
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, AMARILLO, (self.x, self.y, self.tamaño, self.tamaño))
    
    def obtener_rectangulo(self):
        return pygame.Rect(self.x, self.y, self.tamaño, self.tamaño)

class Obstaculo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.velocidad = 6
    
    def actualizar(self):
        self.x -= self.velocidad
    
    def dibujar(self, pantalla):
        pass
    
    def obtener_rectangulo(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def esta_fuera(self):
        return self.x < -50

class Pincho(Obstaculo):
    def __init__(self, x, ancho=30, alto=40):
        y = SUELO_Y - alto
        super().__init__(x, y, ancho, alto)
        self.color = MORADO
    
    def dibujar(self, pantalla):
        p1 = (self.x, self.y + self.alto)
        p2 = (self.x + self.ancho, self.y + self.alto)
        p3 = (self.x + self.ancho / 2, self.y)
        pygame.draw.polygon(pantalla, self.color, [p1, p2, p3])

class Bloque(Obstaculo):
    def __init__(self, x, ancho=50, alto=30):
        y = SUELO_Y - alto
        super().__init__(x, y, ancho, alto)
        self.color = ROJO
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

class Nivel:
    def __init__(self, numero, color_fondo, velocidad=6):
        self.numero = numero
        self.color_fondo = color_fondo
        self.velocidad = velocidad
        self.obstaculos = []
        self.cargar_desde_matriz()
    
    def cargar_desde_matriz(self):
        niveles_data = {
            1: NIVEL_1,
            2: NIVEL_2,
            3: NIVEL_3
        }

        datos = niveles_data[self.numero]

        for item in datos:
            tipo = item[0]

            if tipo == "pincho":
                x = item[1]
                self.obstaculos.append(Pincho(x))

            elif tipo == "bloque":
                x = item[1]
                ancho = item[2]
                alto = item[3]
                self.obstaculos.append(Bloque(x, ancho, alto))
    
    def actualizar(self):
        for obstaculo in self.obstaculos[:]:
            obstaculo.velocidad = self.velocidad
            obstaculo.actualizar()
            if obstaculo.esta_fuera():
                self.obstaculos.remove(obstaculo)
    
    def dibujar(self, pantalla):
        pantalla.fill(self.color_fondo)
        pygame.draw.rect(pantalla, AZUL, (0, SUELO_Y, ANCHO, 50))
        
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(pantalla)
    
    def verificar_colision(self, jugador):
        rect_jugador = jugador.obtener_rectangulo()
        for obstaculo in self.obstaculos:
            if rect_jugador.colliderect(obstaculo.obtener_rectangulo()):
                if isinstance(obstaculo, Bloque):
                    if (jugador.velocidad_y >= 0 and 
                        rect_jugador.bottom >= obstaculo.y and
                        rect_jugador.bottom - jugador.velocidad_y <= obstaculo.y):
                        continue
                return True
        return False
    
    def esta_completado(self):
        return len(self.obstaculos) == 0

class Juego:
    def __init__(self):
        self.estado = "menu"
        self.nivel_actual = 1
        self.jugador = Jugador()
        self.niveles = {
            1: Nivel(1, (50, 50, 150), 6),
            2: Nivel(2, (150, 50, 50), 7),
            3: Nivel(3, (50, 150, 50), 8)
        }
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
    
    def cambiar_nivel(self, numero_nivel):
        self.nivel_actual = numero_nivel
        self.jugador = Jugador()
    
    def obtener_nivel_actual(self):
        return self.niveles[self.nivel_actual]
    
    def reiniciar_nivel(self):
        nivel = self.nivel_actual
        color = self.niveles[nivel].color_fondo
        vel = self.niveles[nivel].velocidad

        self.niveles[nivel] = Nivel(nivel, color, vel)
        self.jugador = Jugador()

class Menu:
    def __init__(self):
        self.botones = []
    
    def dibujar_menu_principal(self, pantalla):
        pantalla.fill(NEGRO)
        
        fuente = pygame.font.SysFont(None, 80)
        texto = fuente.render("GEOMETRY DASH", True, AMARILLO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 100))
        
        boton_jugar = pygame.Rect(300, 250, 200, 60)
        pygame.draw.rect(pantalla, AZUL, boton_jugar)
        fuente = pygame.font.SysFont(None, 50)
        texto = fuente.render("JUGAR", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 260))
        
        self.botones = [("jugar", boton_jugar)]
    
    def dibujar_menu_niveles(self, pantalla):
        pantalla.fill((20, 20, 60))
        
        fuente = pygame.font.SysFont(None, 60)
        texto = fuente.render("SELECCIONA NIVEL", True, AMARILLO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 50))
        
        self.botones = []
        colores = [VERDE, AMARILLO, ROJO]
        
        for i in range(3):
            boton = pygame.Rect(250, 150 + i * 100, 300, 60)
            pygame.draw.rect(pantalla, colores[i], boton)
            fuente = pygame.font.SysFont(None, 50)
            texto = fuente.render(f"NIVEL {i+1}", True, NEGRO)
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 160 + i * 100))
            self.botones.append((f"nivel_{i+1}", boton))
    
    def verificar_clic(self, posicion):
        for nombre, boton in self.botones:
            if boton.collidepoint(posicion):
                return nombre
        return None

def mostrar_mensaje(pantalla, texto, color, y, tamaño=60):
    fuente = pygame.font.SysFont(None, tamaño)
    texto_render = fuente.render(texto, True, color)
    x = ANCHO//2 - texto_render.get_width()//2
    pantalla.blit(texto_render, (x, y))
    return texto_render

def esperar_tiempo(segundos):
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < segundos:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        reloj.tick(60)

# ====================================================================
# BUCLE PRINCIPAL DEL JUEGO
# ====================================================================

juego = Juego()
menu = Menu()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if juego.estado == "menu":
                boton = menu.verificar_clic(evento.pos)
                if boton == "jugar":
                    juego.cambiar_estado("seleccion_nivel")
            
            elif juego.estado == "seleccion_nivel":
                boton = menu.verificar_clic(evento.pos)
                if boton and boton.startswith("nivel_"):
                    nivel = int(boton.split("_")[1])
                    juego.cambiar_nivel(nivel)
                    juego.cambiar_estado("jugando")
            
            elif juego.estado == "jugando" and evento.button == 1:
                juego.jugador.saltar()
        
        if evento.type == pygame.KEYDOWN:
            if juego.estado == "jugando" and evento.key == pygame.K_SPACE:
                juego.jugador.saltar()
    
    if juego.estado == "menu":
        menu.dibujar_menu_principal(pantalla)
    
    elif juego.estado == "seleccion_nivel":
        menu.dibujar_menu_niveles(pantalla)
    
    elif juego.estado == "jugando":
        nivel_actual = juego.obtener_nivel_actual()
        
        juego.jugador.actualizar(nivel_actual.obstaculos)
        nivel_actual.actualizar()
        
        if nivel_actual.verificar_colision(juego.jugador):
            pantalla.fill(NEGRO)
            mostrar_mensaje(pantalla, "GAME OVER", ROJO, 250)
            mostrar_mensaje(pantalla, "Reiniciando...", (255, 255, 255), 320, 30)
            pygame.display.flip()
            esperar_tiempo(1.5)
            juego.reiniciar_nivel()
        
        elif nivel_actual.esta_completado():
            pantalla.fill(NEGRO)
            mostrar_mensaje(pantalla, f"NIVEL {juego.nivel_actual} COMPLETADO!", VERDE, 250)
            mostrar_mensaje(pantalla, "¡GANASTE!", AMARILLO, 320, 40)
            pygame.display.flip()
            esperar_tiempo(1.5)
            juego.cambiar_estado("seleccion_nivel")
        
        else:
            nivel_actual.dibujar(pantalla)
            juego.jugador.dibujar(pantalla)
            mostrar_mensaje(pantalla, f"Nivel {juego.nivel_actual}", (255, 255, 255), 20, 30)
    
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
