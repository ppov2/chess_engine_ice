import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from chess_engine.board.board import Board, WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY

class Evaluation:
    def __init__(self):
        self.piece_values = {
            PAWN: 100,
            KNIGHT: 320,
            BISHOP: 330,
            ROOK: 500,
            QUEEN: 900,
            KING: 20000
        }

    def evaluate(self, board: Board, color_to_move):
        score = 0
        for r in range(8):
            for c in range(8):
                piece = board.board[r][c]
                if piece != EMPTY:
                    piece_type = piece & 7
                    piece_color = piece & 24
                    value = self.piece_values.get(piece_type, 0)
                    if piece_color == WHITE:
                        score += value
                    else:
                        score -= value

        # Return score from the perspective of the side to move
        if color_to_move == WHITE:
            return score
        else:
            return -score

if __name__ == '__main__':
    # Test with starting position (should be 0)
    board = Board()
    evaluator = Evaluation()
    score = evaluator.evaluate(board, WHITE)
    print(f"Evaluation of starting position: {score}")

    # Test with a position where white is up a pawn
    fen_white_up = "rnbqkbnr/pp1ppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board_white_up = Board(fen=fen_white_up)
    score_white_up = evaluator.evaluate(board_white_up, WHITE)
    print(f"Evaluation (White's perspective, White up a pawn): {score_white_up}")

    # Test with a position where black is up a pawn
    fen_black_up = "rnbqkbnr/pppppppp/8/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    board_black_up = Board(fen=fen_black_up)
    score_black_up = evaluator.evaluate(board_black_up, WHITE)
    print(f"Evaluation (White's perspective, Black up a pawn): {score_black_up}")
