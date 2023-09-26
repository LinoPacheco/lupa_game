import pygame
import sys
import random

imagem_obstaculo_verde = pygame.image.load('obstaculo_verde.png')  ##
imagem_obstaculo_vermelho = pygame.image.load('obstaculo_vermelho.png')  ##
imagem_player = pygame.image.load('lupa.png')  ##
imagem_player2 = pygame.image.load('craque.png')  ##
imagem_tiro = pygame.image.load('imagem_tiro.png')
imagem_fundo = pygame.image.load('fundo.png')

imagem_obstaculo_verde = pygame.transform.scale(imagem_obstaculo_verde, (80, 80))  ##
imagem_obstaculo_vermelho = pygame.transform.scale(imagem_obstaculo_vermelho, (80, 80))  ##
imagem_player = pygame.transform.scale(imagem_player, (250, 250))  ##
imagem_tiro = pygame.transform.scale(imagem_tiro, (54, 69))  ##
imagem_fundo = pygame.transform.scale(imagem_fundo, (1920, 1080))  ##
imagem_player2 = pygame.transform.scale(imagem_player2, (250, 250))
# Redimensione outras imagens, se necessário

personagens_selecionaveis = [imagem_player, imagem_player2]
# Adicione mais imagens à lista conforme necessário

# Inicialização do Pygame
pygame.init()

# Definições da janela
largura_janela = 1920
altura_janela = 1080
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Jogo 2D com Obstáculos Destrutíveis")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)


# Função para criar a tela inicial
def tela_inicial():
    global botao_play, imagem_jogador, personagem1_rect, personagem2_rect
    jogador_escolhido = None  # Variável para armazenar a escolha do jogador

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifique se o jogador clicou em um dos personagens
                if personagem1_rect.collidepoint(event.pos):
                    jogador_escolhido = personagens_selecionaveis[0]
                elif personagem2_rect.collidepoint(event.pos):
                    jogador_escolhido = personagens_selecionaveis[1]
                # Adicione mais verificações para outros personagens conforme necessário

                # Se o jogador fez uma escolha, saia do loop
                if jogador_escolhido is not None:
                    imagem_jogador = jogador_escolhido
                    return

        # Desenhe a tela de escolha dos personagens
        janela.blit(imagem_fundo, (0, 0))
        personagem1_rect = pygame.Rect(100, 200, 250, 250)
        personagem2_rect = pygame.Rect(400, 200, 250, 250)
        # Desenhe as imagens dos personagens na tela
        janela.blit(imagem_player, personagem1_rect)
        janela.blit(imagem_player2, personagem2_rect)
        # Desenhe outras opções de personagens conforme necessário

        pygame.display.update()


tela_inicial()

pygame.mixer.init()  # Inicialize o mixer de áudio do Pygame
som_tiro = pygame.mixer.Sound('som_tiro.ogg')
explosao = pygame.mixer.Sound('explosao.ogg')

# Personagem
personagem_x = 50
personagem_y = 840
personagem_velocidade = 3

# Tiros
tiros = []

# Obstáculos verdes
obstaculos_verdes = []

# Obstáculos vermelhos
obstaculos_vermelhos = []


def criar_obstaculo_verde():
    x = random.randint(0, largura_janela - 50)
    y = -50
    return [x, y, velocidade_obstaculos]


def criar_obstaculo_vermelho():
    x = random.randint(0, largura_janela - 50)
    y = -50
    return [x, y, velocidade_obstaculos]


def reiniciar_jogo():
    global vidas, pontuacao_total, pontuacao_vidas, pontuacao_velocidade
    vidas = 3
    pontuacao_total = 0
    pontuacao_vidas = 0
    pontuacao_velocidade = 0
    obstaculos_verdes.clear()
    obstaculos_vermelhos.clear()
    tiros.clear()
    tela_inicial()


# Velocidade de queda dos obstáculos (mais baixa)
nivel = 1

# Vidas iniciais
vidas = 3
taxa_aumento_velocidade = 0.0001  # Ajuste conforme necessário
velocidade_obstaculos = 0.5  # Velocidade inicial

# Pontuação total (inicializada apenas uma vez)
pontuacao_total = 0
pontuacao_vidas = 0
pontuacao_velocidade = 0
# Pontuação necessária para ganhar 1 vida extra
pontuacao_para_vida_extra = 25

# Variável para controlar colisões com obstáculos vermelhos
colidiu_com_obstaculo_vermelho = False

# Limite de obstáculos na tela
limite_obstaculos_verdes = 4
limite_obstaculos_vermelhos = 10

tempo_entre_tiros = 40  # Ajuste o valor conforme necessário (em milissegundos)
tempo_decorrido_desde_ultimo_tiro = 0

tamanho_colisao_tiro = (20, 20)  # Ajuste o tamanho conforme necessário

# Loop do jogo

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tempo_decorrido_desde_ultimo_tiro += 1

    # Aumenta a velocidade gradualmente a cada iteração
    velocidade_obstaculos += taxa_aumento_velocidade

    # Verifica se é hora de reiniciar o jogo
    if vidas <= 0 or pontuacao_total <= -1:
        pygame.time.delay(2000)  # Espera 2 segundos
        reiniciar_jogo()
        vidas = 3  # Reinicializa as vidas

    # Movimento do personagem
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        personagem_x -= personagem_velocidade
    if keys[pygame.K_RIGHT]:
        personagem_x += personagem_velocidade

    # Disparo de tiros
    if keys[pygame.K_UP] and tempo_decorrido_desde_ultimo_tiro >= tempo_entre_tiros:
        novo_tiro = [personagem_x + 20, personagem_y + 140]
        tiros.append(novo_tiro)
        som_tiro.play()  # Reproduz o som do tiro
        tempo_decorrido_desde_ultimo_tiro = 0  # Reinicie o contador

    # Movimento dos tiros
    for tiro in tiros:
        tiro[1] -= 3
        if tiro[1] < 0:
            tiros.remove(tiro)

    # Atualiza a posição dos obstáculos verdes e verifica colisões com o personagem
    for obstaculo in obstaculos_verdes.copy():
        obstaculo[1] += obstaculo[2]  # A velocidade é o terceiro elemento da lista
        if obstaculo[1] > altura_janela:
            obstaculos_verdes.remove(obstaculo)
        # Verifica colisão com o personagem
        if pygame.Rect(personagem_x, personagem_y, 220, 220).colliderect(
                pygame.Rect(obstaculo[0], obstaculo[1], 80, 80)):
            vidas -= 1
            obstaculos_verdes.remove(obstaculo)

    # Atualiza a posição dos obstáculos vermelhos e verifica colisões com o personagem
    for obstaculo in obstaculos_vermelhos.copy():
        obstaculo[1] += obstaculo[2]  # A velocidade é o terceiro elemento da lista
        if obstaculo[1] > altura_janela:
            obstaculos_vermelhos.remove(obstaculo)

        # Verifica colisão com o personagem
        if not colidiu_com_obstaculo_vermelho and pygame.Rect(personagem_x, personagem_y, 10, 10).colliderect(
                pygame.Rect(obstaculo[0], obstaculo[1], 10, 10)):
            vidas -= 1
            colidiu_com_obstaculo_vermelho = True  # Evita múltiplas colisões com o mesmo obstáculo
        # Remove a marca de colisão quando o obstáculo se move para fora da tela
        if obstaculo[1] > altura_janela:
            colidiu_com_obstaculo_vermelho = False

    # Verifica colisões entre tiros e obstáculos vermelhos
    for tiro in tiros.copy():
        for obstaculo in obstaculos_vermelhos.copy():
            if pygame.Rect(tiro[0], tiro[1], 10, 10).colliderect(pygame.Rect(obstaculo[0], obstaculo[1], 100, 100)):
                obstaculos_vermelhos.remove(obstaculo)
                explosao.play()  # Reproduz o som do tiro
                pontuacao_total += 5
                pontuacao_vidas += 5
                pontuacao_velocidade += 5

    # Verifica se um obstáculo vermelho está abaixo do jogador
    for obstaculo in obstaculos_vermelhos.copy():
        if obstaculo[1] > personagem_y:
            pontuacao_total -= 8
            pontuacao_vidas -= 8
            obstaculos_vermelhos.remove(obstaculo)

    # Verifica se é hora de criar novos obstáculos verdes
    if len(obstaculos_verdes) < limite_obstaculos_verdes and random.randint(0, 100) < 2:
        obstaculos_verdes.append(criar_obstaculo_verde())

    # Verifica se é hora de criar novos obstáculos vermelhos
    if len(obstaculos_vermelhos) < limite_obstaculos_vermelhos and random.randint(0, 100) < 1:
        obstaculos_vermelhos.append(criar_obstaculo_vermelho())

    # Ganha 1 vida a cada 50 pontos
    while pontuacao_vidas >= pontuacao_para_vida_extra:
        vidas += 1
        pontuacao_vidas -= pontuacao_para_vida_extra

    # ...
    # Dentro do loop principal do jogo:

    # Desenha o fundo
    janela.blit(imagem_fundo, (0, 0))

    # Desenha o personagem
    janela.blit(imagem_jogador, (personagem_x, personagem_y, 50, 50))

    # Desenha os obstáculos verdes
    for obstaculo in obstaculos_verdes:
        janela.blit(imagem_obstaculo_verde, (obstaculo[0], obstaculo[1]))

    # Desenha os obstáculos vermelhos
    for obstaculo in obstaculos_vermelhos:
        janela.blit(imagem_obstaculo_vermelho, (obstaculo[0], obstaculo[1]))

    # Desenha os tiros
    for tiro in tiros:
        janela.blit(imagem_tiro, (tiro[0], tiro[1]))

    # Exibe vidas e pontuação na tela
    fonte = pygame.font.Font(None, 36)
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, (255, 215, 0), (0, 0, 0, 128))
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao_total}", True, (255, 215, 0), (0, 0, 0, 128))

    janela.blit(texto_vidas, (30, 130))
    janela.blit(texto_pontuacao, (30, 100))

    pygame.display.update()
