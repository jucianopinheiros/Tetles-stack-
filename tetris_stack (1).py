"""
Tetris Stack - Tema 3
Faculdade Estácio - Estrutura de Dados - Turma 9001
Aluno: Francisco Juciano Pinheiro

Simulação didática do comportamento de pilha (stack) em Tetris:
- Representa o tabuleiro como uma lista de linhas (cada linha é lista de 0/1)
- Gera peças simples (I, O, L, ┐ shapes) e as "solta" verticalmente
- Remove linhas completas (clear) e conta pontos

Como executar:
    python3 tetris_stack.py
"""
import random
import time
import copy

BOARD_WIDTH = 10
BOARD_HEIGHT = 16

PIECES = {
    "I": [[1],[1],[1],[1]],            # vertical bar (4x1)
    "O": [[1,1],
          [1,1]],                      # square 2x2
    "L": [[1,0],
          [1,0],
          [1,1]],                      # L shape
    "Z": [[1,1,0],
          [0,1,1]]                     # Z shape
}

def criar_tabuleiro():
    return [[0]*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

def imprimir_tabuleiro(board):
    for row in board:
        print("".join(["■" if c else "." for c in row]))
    print("-"*BOARD_WIDTH)

def pode_posicionar(board, piece, top_row, left_col):
    piece_h = len(piece)
    piece_w = len(piece[0])
    # verifica limites
    if left_col < 0 or left_col + piece_w > BOARD_WIDTH:
        return False
    if top_row + piece_h > BOARD_HEIGHT:
        return False
    # verifica colisões
    for r in range(piece_h):
        for c in range(piece_w):
            if piece[r][c]:
                if board[top_row + r][left_col + c]:
                    return False
    return True

def fixar_peca(board, piece, top_row, left_col):
    for r in range(len(piece)):
        for c in range(len(piece[0])):
            if piece[r][c]:
                board[top_row + r][left_col + c] = 1

def limpar_linhas(board):
    cleared = 0
    new_board = [row for row in board if not all(cell==1 for cell in row)]
    cleared = BOARD_HEIGHT - len(new_board)
    # insere linhas vazias no topo
    while len(new_board) < BOARD_HEIGHT:
        new_board.insert(0, [0]*BOARD_WIDTH)
    return new_board, cleared

def gerar_peca_aleatoria():
    nome = random.choice(list(PIECES.keys()))
    # aleatoriza rotação 0/90/180/270 (apenas rotaciona a matriz)
    piece = PIECES[nome]
    rotations = random.randint(0,3)
    for _ in range(rotations):
        piece = rotacionar(piece)
    return piece

def rotacionar(piece):
    # rotaciona 90 graus (matriz)
    h = len(piece)
    w = len(piece[0])
    new_p = [[0]*h for _ in range(w)]
    for r in range(h):
        for c in range(w):
            new_p[c][h-1-r] = piece[r][c]
    return new_p

def soltar_peca(board, piece):
    piece_h = len(piece)
    piece_w = len(piece[0])
    # posição inicial: topo, centro horizontal aproximado
    left = (BOARD_WIDTH - piece_w)//2
    top = 0
    # se não cabe já, game over
    if not pode_posicionar(board, piece, top, left):
        return False, 0
    # desce até colidir
    while True:
        if pode_posicionar(board, piece, top+1, left):
            top += 1
        else:
            # fixa no topo atual
            fixar_peca(board, piece, top, left)
            board, cleared = limpar_linhas(board)
            return True, cleared

def simular_partida(steps=50, delay=0.2):
    board = criar_tabuleiro()
    score = 0
    for step in range(1, steps+1):
        piece = gerar_peca_aleatoria()
        ok, cleared = soltar_peca(board, piece)
        if not ok:
            print("GAME OVER - Não foi possível posicionar a peça.")
            break
        score += cleared * 100
        print(f"\nStep {step} | Peça gerada | Linhas limpas: {cleared} | Score: {score}")
        imprimir_tabuleiro(board)
        time.sleep(delay)
    print(f"\nFim da simulação. Score final: {score}")

def main():
    print("🎮 Tetris Stack - Simulação de pilha (versão simples)")
    try:
        passos = int(input("Quantos passos/peças deseja simular? (ex: 30) ") or "30")
    except ValueError:
        passos = 30
    simular_partida(steps=passos, delay=0.15)

if __name__ == "__main__":
    main()
