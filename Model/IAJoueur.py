from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *

import numpy as np
import random
import math
import copy


class Board():
    def __init__(self, plateau: list) -> None:
        self.plateau = copy.deepcopy(plateau)

    def __str__(self):
        return self.__visualise()

    def __len__(self):
        return len(self.plateau)

    def to_matrice(self) -> np.ndarray:
        matrice = []

        for row in self.getPlateau():
            line = []

            for cell in row:
                if cell is None:
                    line.append(-1)
                else:
                    # Rouge
                    if getCouleurPion(cell):
                        line.append(1)
                    else:
                        line.append(0) # jaune

            matrice.append(line)

        return np.array(matrice)

    def __visualise(self) -> None:
        """
        Fonction permettant de transformer un plateau en text

        :param plateau: le plateau à convertir en text
        :raise TypeError: si le paramètre plateau n'est pas un plateau
        :return: le text représentant le tableau
        """

        if not type_plateau(self.plateau):
            raise TypeError("toStringPlateau : Le premier paramètre ne correspond pas à un plateau")

        affichage = ''

        for ligne in self.plateau:
            ligne_affichage = '|'

            for cellule in ligne:
                if cellule is None:
                    ligne_affichage += ' |'
                else:
                    if getCouleurPion(cellule):
                        cube_couleur = '\x1B[41m \x1B[0m'
                    else:
                        cube_couleur = '\x1B[43m \x1B[0m'

                    ligne_affichage += cube_couleur + '|'

            affichage += ligne_affichage + '\n'

        affichage += '-' + '--' * len(self.plateau[0]) + '\n'
        affichage += ' ' + ' '.join(
            str(i) for i in range(len(self.plateau[0]))
        )

        return affichage

    def is_valid_move(self, num_col: int) -> bool:
        """
        Function that return a boolean that indicate if a move is valid or not

        :param num_col: the column number where the pion will be added
        :return: a boolean

        """

        return self.plateau[0][num_col] is None

    def placerPion(self, couleur, num_col) -> None:
        """
        Function that let the computer play a pion

        :param couleur: color of the pion
        :param num_col: the column number where the pion will be added
        :raise ValueError: if the move is not valid
        :return: None
        """

        if not self.is_valid_move(num_col):
            raise ValueError('Column is full')

        pion = construirePion(couleur)
        placerPionPlateau(self.plateau, pion, num_col)

    def getPlateau(self) -> list:
        """
        Function that returns the current board
        :return: list representing the current board
        """

        return self.plateau

    def copy(self):
        """
        Function that copy the current board
        :return: a new instance of the class with the same board
        """

        return Board(copy.deepcopy(self.plateau))

    @staticmethod
    def is_valid_location(board, col):
        return board[const.NB_LINES - 1][col] == None

    def get_valid_locations(self) -> int:
        """
        Function that get all valid columns
        :return: a list of int
        """

        valid_locations = []
        for col in range(const.NB_COLUMNS):
            if Board.is_valid_location(self.plateau, col):
                valid_locations.append(col)
        return valid_locations

COLUMN_COUNT = 7
ROW_COUNT = 6
PLAYER_PIECE = 0
AI_PIECE = 1
EMPTY = -1
WINDOW_LENGTH = 4

class AI:
    def __init__(self, players: list):
        self.players = players

    def getPlayerWin(self, plateau, player: int) -> int:
        pions_gagnant = getPionsGagnantsPlateau(plateau.getPlateau())

        if len(pions_gagnant) > 0:
            return getPionsGagnantsPlateau(plateau.getPlateau())[0][const.COULEUR] == player

        return False

    def is_terminal_node(self, board):
        return AI.winning_move(board.to_matrice(), self.players[0]) or AI.winning_move(board.to_matrice(), self.players[1]) or len(
            board.get_valid_locations()) == 0


    @staticmethod
    def winning_move(board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

    @staticmethod
    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    @staticmethod
    def score_position(board, piece):
        score = 0
        board = board.to_matrice()

        ## Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += AI.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += AI.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += AI.evaluate_window(window, piece)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += AI.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_valid_locations()
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:

            if is_terminal:
                if self.getPlayerWin(board, self.players[0]):
                    return None, 100000000000000

                elif self.getPlayerWin(board, self.players[1]):
                    return None, -10000000000000
                else:
                    return None, 0
            else:
                return None, AI.score_position(board, self.players[0])

        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                b_copy.placerPion(self.players[0], col)

                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                b_copy.placerPion(self.players[1], col)

                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

model = AI([1, 0])

def generation_coups(mode: bool, plateau: list) -> int:
    """
    Fonction qui génère un coups de l'ordinateur

    :param mode: le mode de jeux
    :param plateau: le plateau
    :return: un entier qui représente le coups de l'ordinateur
    """

    if mode:
        coups = random.randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)
    else:
        coups = model.minimax(Board(plateau), 5, -math.inf, math.inf, True)[0]

    return coups


if __name__ == '__main__':
    board = Board(construirePlateau())
    model = AI([1, 0])
    depth = 10 #paramétrer le niveau l'IA ici
    model.minimax(board, depth, -math.inf, math.inf, True)

