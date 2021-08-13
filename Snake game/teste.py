'''
import pygame                   # Importando a biblioteca pygame
from pygame.locals import *     # Importando um sub-módulo e todas as suas funções e constantes.
from sys import exit            # Importando a função 'exit' do módulo 'sys' para podermos fechar a janela do nosso game.
from random import randint      # Ela sorteia valores de um determinado intervalo escolhido.
pygame.init()                   # Iniciando todas as funções da biblioteca pygame.
lista_cobra = list()            # Criando uma lista para armazenar todas as posições em que a cobra passou.
comprimento_inicial = 5         # Criando um limitador de tamanho para a lista_cobra
morreu = False                  # Criando uma variável ,para caso a cobra morra,ela se torne True.

# Música
pygame.mixer.music.set_volume(0.2)                                              # Controlando o som da música de fundo
musica_de_fundo = pygame.mixer.music.load('BoxCat Games - CPU Talk.mp3')        # Carregando o arquivo mp3
pygame.mixer.music.play(-1)                                                     # Tocando a música; O '-1' serve para repetir a música,assim que ela acabar.
musica_de_colisão = pygame.mixer.Sound('smw_coin.wav')                          # Carregando o arquivo wav                                          
musica_de_colisão.set_volume(0.5)                                               # Controlando o som da música de colisão

#Criando a tela:
largura = 640
altura = 480
x_cobra = largura / 2                         # Essas variáveis vão controlar
y_cobra = altura / 2                          # a posição do objeto na tela.

#Colisões:
x_maca = randint(40, 600)               # x_maca e y_maca, vai assumir diferentes valores,mudando o lugar em que o retângulo azul vai ser posicionado
y_maca = randint(50, 430)               # logo após as colisões com o retângulo vermelho.

#Controlando a cobra:
velocidade = 10
x_controle = velocidade
y_controle = 0                          # Para evitar que a cobra ande nas diagonais


#Gerando Textos:
#fonte = pygame.font.SysFont('Fonte', tamanho do texto, Negrito(sim/nao), Itálico(sim/nao))
fonte = pygame.font.SysFont('arial', 40, True, True)    # Fonte
pontos = 0

#Criando a tela 2:
tela = pygame.display.set_mode((largura, altura)) # Essa função recebe uma tupla,com as dimensões da tela.
pygame.display.set_caption('Teste')               # Essa função é para escolher o nome do arquivo.

#Criando um relogio ,para mudar a velocidade com que o objeto se movimenta em Hertz.
relogio = pygame.time.Clock()

#Criando função para aumentar o tamanho da cobra.
def aumentaCobra(lista):
    for posição in lista:
        pygame.draw.rect(tela, (0, 255, 0), (posição[0], posição[1], 20, 20))

#Criando função para reiniciar o jogo.
def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeça, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = largura / 2
    y_cobra = largura / 2
    lista_cobra = list()
    lista_cabeça = list()
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morreu = False


while True:                             # Loop principal.
    relogio.tick(30)                    # Para mudar a velocidade com que o objeto se movimenta na tela. Através dos frames.
    tela.fill((255,255,255))            # Para limpar a tela a cada iteração do loop infinito.
    mensagem = f'Pontos : {pontos}'     # Texto
    texto_formatado = fonte.render(mensagem, True, (0,0,0))   # parâmetros: (mensagem, Serrilhamento da mensagem, cor) Essa função junta o texto com a fonte.
    
    for event in pygame.event.get():    # Loop para conferir se tal evento ocorreu.
        if event.type == QUIT:
            pygame.quit()
            exit()

        # Para conferir qual tecla vai ser pressionada
        # Além disso,bloqueando os movimentos em relação a outra tecla
        # Para evitar que mais de 1 tecla seja apertada ao mesmo tempo e evitando algum erro no programa.   
        if event.type == KEYDOWN:       
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = - velocidade
                    y_controle = 0

            if event.key == K_d:
                if x_controle == - velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0

            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = - velocidade
                
            if event.key == K_s:
                if y_controle == - velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = velocidade

    # Fazendo a cobra se movimentar sozinha e sem ir para as diagonais.
    x_cobra += x_controle           
    y_cobra += y_controle

    # Criando objetos:
    ret_cobra = pygame.draw.rect(tela, (0,255,0), (x_cobra, y_cobra, 20, 20))       # Desenhando na tela; (Aonde vai desenhar, (tupla para cor), (Tupla para as dimensões,x, y, largura,altura em pixels))               
    ret_maca = pygame.draw.rect(tela, (255,0,0), (x_maca, y_maca, 20, 20))
    
    # Colisão2:
    if ret_cobra.colliderect(ret_maca):                                             # Método utilizado para saber se o retângulo   
        x_maca = randint(40, 600)                                                   # vermelho colidiu com o azul.
        y_maca = randint(50, 430)
        pontos+= 1                                         
        musica_de_colisão.play()
        comprimento_inicial += 1

    
    # Criando uma lista para armazenar as posições da cabeça da cobra;
    lista_cabeça = list()
    lista_cabeça.append(x_cobra)
    lista_cabeça.append(y_cobra)
    lista_cobra.append(lista_cabeça)

    # Criando uma condição caso a cobra colida com ela mesma,para finalizar o jogo e aparecer um menu.
    if lista_cobra.count(lista_cabeça) > 1:
        fonte2 = pygame.font.SysFont('arial',20,True, True,)
        mensagem2 = 'Game Over! Aperte a Tecla R para reiniciar o jogo!'
        texto_formatado2 = fonte2.render(mensagem2, True, (0,0,0))

        # Pegando o retângulo que fica ao redor do texto.
        ret_texto = texto_formatado2.get_rect()

        morreu = True
        while morreu:
            tela.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            ret_texto.center = (largura //2 , altura //2)           # Colocando no meio da tela
            tela.blit(texto_formatado2, ret_texto)
            pygame.display.update()

    # Para fazer a cobra aparecer do outro lado da tela,quando ela ultrapassar os limites de altura e largura.                     
    if x_cobra > largura:
        x_cobra = 0

    if x_cobra < 0:
        x_cobra = largura

    if y_cobra > altura:
        y_cobra = 0

    if y_cobra < 0:
        y_cobra = altura

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumentaCobra(lista_cobra)
    
    
    #pygame.draw.circle(tela, (0,255,0), (300, 260), 40)          Desenhando na tela; (Aonde vai desenhar, (tupla para cor), (Tupla para o plano cartesiano x e y), raio do círculo)
    #pygame.draw.line(tela, (255,255,0), (390, 0), (390, 600), 5) Desenhando na tela; (Aonde vai desenhar, (tupla para cor), (Tupla para x e y,para iniciar a linha), (Tupla para x e y,para ligar os pontos e fazer uma linha), espessura da linha)    
    



    tela.blit(texto_formatado, (400, 40))                   # Linha para mostrar o texto na tela . (texto, (lugar aonde o texto vai ficar.))
    pygame.display.update()                                 # Linha para atualizar o jogo assim que um evento ocorrer.
                                                            # Caso contrário,o jogo vai travar.

    pygame.font.get_fonts()                                 # Comando para saber as fontes existentes.'''