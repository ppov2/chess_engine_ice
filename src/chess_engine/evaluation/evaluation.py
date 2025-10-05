from ..board.board import Board
from ..constants import (
    WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY,
    PIECE_SQUARE_TABLES
)

class Evaluation:
    """
    Calculates the static evaluation of a board position.

    The evaluation is based on two main components:
    1. Material: The sum of the values of the pieces on the board.
    2. Positional: The strategic value of each piece's position, determined by
       Piece-Square Tables (PSTs).
    """
    def __init__(self):
        """
        Initializes the Evaluation class, setting up the material values for each piece.
        """
        self.piece_values = {
            PAWN: 100,
            KNIGHT: 320,
            BISHOP: 330,
            ROOK: 500,
            QUEEN: 900,
            KING: 20000 # A high value to discourage trading the king
        }

    def evaluate(self, board: Board, color_to_move):
        """
        Evaluates the given board position from the perspective of the side to move.

        The score is calculated as a sum of material and positional values for each
        piece. A positive score indicates an advantage for the current player, while
        a negative score indicates a disadvantage.

        Args:
            board (Board): The board object to evaluate.
            color_to_move (int): The color of the player whose turn it is.

        Returns:
            int: The evaluation score, relative to the player to move.
        """
        score = 0
        for r in range(8):
            for c in range(8):
                piece = board.board[r][c]
                if piece != EMPTY:
                    piece_type = piece & 7
                    piece_color = piece & 24

                    # 1. Material Value
                    material_value = self.piece_values.get(piece_type, 0)

                    # 2. Positional Value (from Piece-Square Tables)
                    positional_value = 0
                    pst = PIECE_SQUARE_TABLES.get(piece_type)
                    if pst:
                        # The PSTs are from White's perspective, so we flip the rank for Black
                        if piece_color == WHITE:
                            positional_value = pst[r][c]
                        else:
                            positional_value = pst[7-r][c]

                    piece_score = material_value + positional_value

                    if piece_color == WHITE:
                        score += piece_score
                    else:
                        score -= piece_score

        # Return score from the perspective of the side to move
        return score if color_to_move == WHITE else -score