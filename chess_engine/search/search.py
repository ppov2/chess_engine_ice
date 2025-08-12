import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from chess_engine.board.board import Board, WHITE, BLACK
from chess_engine.move_generator.move_generator import MoveGenerator
from chess_engine.evaluation.evaluation import Evaluation

class Search:
    def __init__(self, board: Board, move_generator: MoveGenerator, evaluator: Evaluation):
        self.board = board
        self.move_generator = move_generator
        self.evaluator = evaluator

    def search(self, depth, color_to_move):
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        moves = self.move_generator.get_legal_moves(color_to_move)

        for move in moves:
            self.board.make_move(move)
            score = -self.negamax(depth - 1, -beta, -alpha, WHITE if color_to_move == BLACK else BLACK)
            self.board.unmake_move(move)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move

    def negamax(self, depth, alpha, beta, color_to_move):
        if depth == 0:
            return self.evaluator.evaluate(self.board, color_to_move)

        moves = self.move_generator.get_legal_moves(color_to_move)
        if not moves:
            # Placeholder for checkmate/stalemate. A proper check detection is needed.
            # For now, we assume no check.
            return 0

        best_score = -float('inf')

        for move in moves:
            self.board.make_move(move)
            score = -self.negamax(depth - 1, -beta, -alpha, WHITE if color_to_move == BLACK else BLACK)
            self.board.unmake_move(move)

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if alpha >= beta:
                break

        return best_score


if __name__ == '__main__':
    board = Board()
    # For the search, we need to pass a board instance that will be modified.
    # So we need a new MoveGenerator and Evaluator for each search, or they need to be stateless.
    # In our case, they are mostly stateless, but the MoveGenerator depends on the board state.
    # The search class takes instances of these, so it should be fine.

    move_generator = MoveGenerator(board)
    evaluator = Evaluation()
    searcher = Search(board, move_generator, evaluator)

    # Find the best move for White from the starting position at depth 3
    print("Searching for the best move for White (depth 3)...")
    # A depth of 3 is quite low, but should be enough to see if it works.
    # It will take some time to run.
    best_move = searcher.search(3, WHITE)
    print(f"Best move found: {best_move}")

    # Let's try from a different position
    fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
    board_fen = Board(fen=fen)
    move_generator_fen = MoveGenerator(board_fen)
    searcher_fen = Search(board_fen, move_generator_fen, evaluator)
    print("\nSearching for the best move for Black (depth 3)...")
    best_move_fen = searcher_fen.search(3, BLACK)
    print(f"Best move found from FEN: {best_move_fen}")
