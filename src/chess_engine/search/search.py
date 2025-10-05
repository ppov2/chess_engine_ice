from ..board.board import Board
from ..move_generator.move_generator import MoveGenerator
from ..evaluation.evaluation import Evaluation
from ..constants import WHITE, BLACK, EMPTY

# A large value to represent checkmate, greater than any possible board evaluation.
MATE_SCORE = 100000

class Search:
    """
    Implements the search algorithm to find the best move.

    This class uses a Negamax framework with alpha-beta pruning to search the
    game tree. It also incorporates a quiescence search to improve tactical stability.
    """
    def __init__(self, board: Board, move_generator: MoveGenerator, evaluator: Evaluation):
        """
        Initializes the Search class.

        Args:
            board (Board): The board object to perform the search on.
            move_generator (MoveGenerator): The move generator for finding legal moves.
            evaluator (Evaluation): The evaluator for scoring board positions.
        """
        self.board = board
        self.move_generator = move_generator
        self.evaluator = evaluator

    def search(self, depth, color_to_move):
        """
        Finds the best move for a given color at a specified search depth.

        This is the main entry point for the search. It iterates through all legal
        moves at the root of the search tree and uses the negamax algorithm to
        evaluate each move.

        Args:
            depth (int): The maximum depth to search.
            color_to_move (int): The color of the player to find a move for.

        Returns:
            Move|None: The best move found, or None if no legal moves are available.
        """
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        moves = self.move_generator.get_legal_moves(color_to_move)

        if not moves:
            return None # Game is over (checkmate or stalemate)

        for move in moves:
            self.board.make_move(move)
            score = -self.negamax(depth - 1, -beta, -alpha, BLACK if color_to_move == WHITE else WHITE)
            self.board.unmake_move(move)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break # Prune

        return best_move

    def negamax(self, depth, alpha, beta, color_to_move):
        """
        Performs a recursive Negamax search with alpha-beta pruning.

        Args:
            depth (int): The remaining depth to search.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.
            color_to_move (int): The color of the player whose turn it is.

        Returns:
            int: The evaluation score for the position.
        """
        if depth == 0:
            return self.quiescence_search(alpha, beta, color_to_move)

        moves = self.move_generator.get_legal_moves(color_to_move)
        if not moves:
            # If no legal moves, it's either checkmate or stalemate.
            if self.move_generator.is_king_in_check(color_to_move):
                return -MATE_SCORE # This side is in checkmate
            else:
                return 0 # This is a stalemate

        best_score = -float('inf')
        for move in moves:
            self.board.make_move(move)
            score = -self.negamax(depth - 1, -beta, -alpha, BLACK if color_to_move == WHITE else WHITE)
            self.board.unmake_move(move)

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if alpha >= beta:
                break # Prune

        return best_score

    def quiescence_search(self, alpha, beta, color_to_move):
        """
        A specialized search that only considers 'forcing' moves (captures)
        to avoid the horizon effect and ensure the engine doesn't end its
        search in the middle of a tactical sequence.

        Args:
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.
            color_to_move (int): The color of the player whose turn it is.

        Returns:
            int: The evaluation of the 'quiet' position.
        """
        stand_pat_score = self.evaluator.evaluate(self.board, color_to_move)

        if stand_pat_score >= beta:
            return beta

        alpha = max(alpha, stand_pat_score)

        # Generate only capture moves
        moves = self.move_generator.get_legal_moves(color_to_move)
        capture_moves = [move for move in moves if move.captured_piece != EMPTY]

        for move in capture_moves:
            self.board.make_move(move)
            score = -self.quiescence_search(-beta, -alpha, BLACK if color_to_move == WHITE else WHITE)
            self.board.unmake_move(move)

            if score >= beta:
                return beta

            alpha = max(alpha, score)

        return alpha