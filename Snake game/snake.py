import pygame                                               # Importando a biblioteca pygame
from pygame.locals import *                                 # Importando o sub-módulo locals e todas as suas funções
from sys import exit                                        # Importando a função 'exit' da biblioteca 'sys'
from random import randint                                  # Importando a função 'randint' da biblioteca 'random'.

pygame.init()                                               # Iniciando todas as funções da biblioteca 'pygame'.
lista_cobra = list()                                        # Criando lista para armazenar todas as coordenadas da cobra.
comprimento_inicial = 5                                     # Criando um limitador de tamanho para a lista_cobra
death = False                                               # Caso a cobra colida com ela mesma,"death" passa a ser true

#Músicas
pygame.mixer.music.set_volume(0.2 )
musica_de_fundo = pygame.mixer.music.load('BoxCat Games - CPU Talk.mp3')    # Upload da música em formato mp3.
pygame.mixer.music.play(-1)                                                 # Tocando a música. '-1' como parâmetro,para reiniciar a música assim que a mesma acabar.
musica_de_colisao = pygame.mixer.Sound('smw_coin.wav')

# Criando a tela:
largura = 640                                                   # Largura e altura são as dimensões da tela.
altura = 480                                                
x_snake = largura / 2                                           # x e y são as coordenadas da localização do objeto na tela.
y_snake = altura / 2                                            # estão dividindo por 2 ,para tentarmos colocar o objeto ao centro da tela.

tela = pygame.display.set_mode((largura,altura))                # Tela criada
pygame.display.set_caption('Snake Game')                             # Escolhendo o nome do arquivo

relogio = pygame.time.Clock()                                   # Função para mudar a velocidade com que o objeto é movimentado.
#Criando função para aumentar o tamanho da cobra:
def aumenta_cobra(lista):
    for posição in lista:
        pygame.draw.rect(tela, (0, 255, 0), (posição[0],posição[1], 20, 20))

#Criando função para reiniciar o jogo,assim que a cobra morrer.
def reiniciar_jogo():
    global comprimento_inicial, x_apple,y_apple, x_snake,y_snake, lista_cobra, lista_cabeca, death, pontos
    pontos = 0
    comprimento_inicial = 5
    x_apple = randint(40, 600)
    y_apple = randint(50, 430)
    x_snake = largura / 2
    y_snake = altura / 2
    lista_cobra = list()
    lista_cabeca = list()
    death = False


#Gerando textos:
fonte = pygame.font.SysFont('arial', 40, bold =True, italic =True)   # Criando a fonte do texto
pontos = 0                                                           # Contador

#Colisões:
x_apple = randint(40, 600)                                           # Para fazer com que a maçã se reposicione em outro lugar
y_apple = randint(50, 430)                                           # a cada colisão feita pela cobra

#Controlando a cobra,para evitar movimentos na diagonais:
speed = 10 
x_control = speed
y_control = 0                                                       

while True:                                                         # Loop Principal.
    relogio.tick(30)                                                # Modificando em Hertz a velocidade do objeto.
    tela.fill((255,255,255))                                        # Função para preencher a tela com a cor da tela,quando o objeto é movimentado.
    mensage = f'Pontos: {pontos}'                                   # Escrevendo a mensagem.
    texto_formatado = fonte.render(mensage, True, (0, 0, 0))        # Função para juntar a fonte com o texto. (mensagem, Serrilhamento do texto, tupla com a cor do texto)
    
    for event in pygame.event.get():                                # Loop para verificar se algum evento ocorreu.                           
        if event.type == QUIT:
            pygame.quit()
            exit()
        # Teclas a serem pressionadas;
        # Bloqueando os movimentos em relação a outra tecla:    
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_control == speed:
                    pass
                else:
                    x_control = - speed
                    y_control = 0
            
            if event.key == K_d:
                if x_control == - speed:
                    pass
                else:
                    x_control = speed
                    y_control = 0

            if event.key == K_w:
                if y_control == speed:
                    pass
                else:
                    x_control = 0
                    y_control = - speed
            
            if event.key == K_s:
                if y_control == - speed:
                    pass
                else:
                    x_control = 0
                    y_control = speed

    # Cobra se movimentando sozinha:                
    x_snake += x_control
    y_snake += y_control


    #Criando objeto:
    snake = pygame.draw.rect(tela, (0,255,0), (x_snake, y_snake, 20, 20))           
    apple = pygame.draw.rect(tela, (255,0 ,0), (x_apple, y_apple, 20, 20))
        
    #Colisões 2:
    if snake.colliderect(apple):
        x_apple = randint(40, 600)
        y_apple = randint(50, 430)
        pontos += 1
        musica_de_colisao.play()
        comprimento_inicial += 1
    
    # Criando uma lista para guardar as coordenadas da cabeça da cobra:
    lista_cabeca = list()
    lista_cabeca.append(x_snake)
    lista_cabeca.append(y_snake)

    # Lista para guardar todas as coordenadas da cobra:
    lista_cobra.append(lista_cabeca)
    # Quando a cobra colidir com ela mesma,ela vai morrer:
    if lista_cobra.count(lista_cabeca) > 1:
        second_fonte = pygame.font.SysFont('arial', 20, True, True)
        second_mensage = 'Game Over! Aperte a tecla R para reiniciar o jogo!'
        second_formatado = second_fonte.render(second_mensage,True, (0,0,0))
        # Pegando o retângulo que fica ao redor do texto.
        ret_text = second_formatado.get_rect()
        # De volta para o loop principal:
        death = True
        while death:
            tela.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            ret_text.center = (largura//2 , altura//2)
            tela.blit(second_formatado, ret_text)
            pygame.display.update()
    # Para fazer a cobra aparecer do outro lado da tela;
    # Quando ela ultrapassar os limites de altura e largura:
    if x_snake > largura:
        x_snake = 0

    if x_snake < 0:
        x_snake = largura

    if y_snake > altura:
        y_snake = 0

    if y_snake < 0:
        y_snake = altura

    # Para evitar que a cobra cresça de forma desnecessária:
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]
    
    # Aumentando o tamanho da cobra:
    aumenta_cobra(lista_cobra)


    #Para mostrar o texto na tela:
    tela.blit(texto_formatado, (400, 40))  # Parâmetros (função utilizada para juntar o texto e a fonte, (tupla com as coordenadas aonde vai ser localizado o texto))


    # Para atualizar o loop: 
    pygame.display.update()