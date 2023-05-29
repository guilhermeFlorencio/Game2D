import pygame
import numpy as np
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.music.set_volume(0.2) 
background_music = pygame.mixer.music.load('sound/background_music.mp3') 
pygame.mixer.music.play(-1) 

sound_collision = pygame.mixer.Sound('sound/collision_music.wav')

width = 640
height = 480
background_image = pygame.image.load(r'image/background_terra.png')
dialog_box = pygame.image.load(r'image/dialog_box.png')
x_snake = int(width/2) 
y_snake = int(height/2)

speed = 10
x_controle = speed
y_controle = 0


x_apple = randint(40, 600)
y_apple = randint(50, 430)
white = (255, 255, 255)
brown = (120,64,8)
black = (0,0,0)
pontos = 0
fonte = pygame.font.SysFont('arial', 30, bold=True, italic=False)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('The life snake')
relogio = pygame.time.Clock()
snake_list = []
comprimento_inicial = 5
morreu = False


def imagemNegativa(imagem):
    img_array = pygame.surfarray.array3d(imagem)
    img_negativa = -img_array + 255
    img_negativa = np.clip(img_negativa, 0, 255)  # Garante que os valores estejam no intervalo correto
    img_negativa = img_negativa.astype(np.uint8)  # Converte de volta para tipo de dados uint8
    img_negativa_surface = pygame.surfarray.make_surface(img_negativa)
    return img_negativa_surface

background_image_negativa = imagemNegativa(background_image);

def snake_increase(snake_list):
    for XeY in snake_list:
        pygame.draw.rect(screen, brown, (XeY[0], XeY[1], 20, 20))

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_snake, y_snake, snake_list, lista_cabeca, x_apple, y_apple, morreu
    pontos = 0
    comprimento_inicial = 5
    x_snake = int(width/2) 
    y_snake = int(height/2)
    snake_list = []
    lista_cabeca = []
    x_apple = randint(40, 600)
    y_apple = randint(50, 430)
    morreu = False

while True:
    relogio.tick(30)
    screen.fill(white) 
    screen.blit(background_image, (0, 0))
    mensagem = f'Pontos: {pontos}'
    screen.blit(dialog_box, (220, 10))
    texto_formatado = fonte.render(mensagem, False, black)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == speed:
                    pass
                else:
                    x_controle = -speed
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -speed:
                    pass
                else:
                    x_controle = speed
                    y_controle = 0
            if event.key == K_w:
                if y_controle == speed:
                    pass
                else:
                    y_controle = -speed
                    x_controle = 0
            if event.key == K_s:
                if y_controle == -speed:
                    pass
                else:
                    y_controle = speed
                    x_controle = 0

    x_snake = x_snake + x_controle
    y_snake = y_snake + y_controle
        
    cobra = pygame.draw.rect(screen, brown, (x_snake,y_snake,20,20))
    maca = pygame.draw.rect(screen, (255,0,0), (x_apple,y_apple,20,20))
    
    if cobra.colliderect(maca):
        x_apple = randint(40, 600)
        y_apple = randint(50, 430)
        pontos += 1
        sound_collision.play()
        comprimento_inicial = comprimento_inicial + 1

    lista_cabeca = []
    lista_cabeca.append(x_snake)
    lista_cabeca.append(y_snake)
    
    snake_list.append(lista_cabeca)

    if snake_list.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem = 'Pressione a tecla R para jogar novamente'
        mensagem2 = 'A Ganância que move... É a mesma que te mata...'
        texto_formatado = fonte2.render(mensagem2, True, white)
        texto_formatado = fonte2.render(mensagem, True, white)
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            screen.fill((255,255,255))
            screen.blit(background_image_negativa, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()

            ret_texto.center = (width//2, height//2) 
            screen.blit(texto_formatado, ret_texto)
            pygame.display.update()

    
    if x_snake > width:
        x_snake = 0
    if x_snake < 0:
        x_snake = width
    if y_snake < 0:
        y_snake = height
    if y_snake > height:
        y_snake = 0

    if len(snake_list) > comprimento_inicial:
        del snake_list[0]

    snake_increase(snake_list)

    screen.blit(texto_formatado, (450,40))

    
    pygame.display.update()