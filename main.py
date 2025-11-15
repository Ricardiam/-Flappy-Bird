import pygame
import sys 

# Tamaño ventana
Ancho = 800
Alto = 600
Fps = 60

pygame.init()
pygame.display.set_caption("Geometry Dash")
screen = pygame.display.set_mode((Ancho, Alto))
clock = pygame.time.Clock()


def mostrar_menu():
    print("\n===== Menu =====")
    print("1. Jugar")
    print("2. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            print("Iniciando el juego...\n")
            return 



      
        elif opcion == "2":
            print("Saliendo del juego...")
            sys.exit()
        else:
            print("Opción no válida")


def juego():
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        screen.fill((0, 0, 0))  
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()



if __name__ == "__main__":
    main()   
    juego()  








