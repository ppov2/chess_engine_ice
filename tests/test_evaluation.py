import unittest

from src.chess_engine.board.board import Board
from src.chess_engine.evaluation.evaluation import Evaluation
from src.chess_engine.constants import WHITE, BLACK

class TestEvaluation(unittest.TestCase):

    def test_initial_position(self):
        """
        Tests that the initial board position evaluates to 0.
        The positional scores are symmetrical, so they cancel each other out.
        """
        board = Board()
        evaluator = Evaluation()
        self.assertEqual(evaluator.evaluate(board, WHITE), 0)
        self.assertEqual(evaluator.evaluate(board, BLACK), 0)

    def test_white_advantage_with_pst(self):
        """
        Tests a position where Black has a material advantage.
        The score should reflect both the material and positional difference.
        """
        # Position where white is missing a knight from g1
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1"
        board = Board(fen=fen)
        evaluator = Evaluation()
        # Material: -320 for the knight.
        # Positional: Knight on g1 has a PST value of -40. By removing it, White's
        # positional score relative to Black's improves by 40.
        # Total: -320 + 40 = -280
        self.assertEqual(evaluator.evaluate(board, WHITE), -280)

    def test_black_advantage_with_pst(self):
        """
        Tests a position where White has a material advantage.
        """
        # Position where black is missing a rook from a8
        fen = "1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
        board = Board(fen=fen)
        evaluator = Evaluation()
        # Material: +500 for the rook.
        # Positional: Rook on a8 has a PST value of 0, so no positional change.
        # Total score from White's perspective is +500.
        # From Black's perspective, this is -500.
        self.assertEqual(evaluator.evaluate(board, BLACK), -500)

    def test_positional_evaluation(self):
        """
        Tests that the evaluation function correctly applies positional scores.
        """
        # Position after 1. e4. Material is equal, but White has a positional advantage.
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        board = Board(fen=fen)
        evaluator = Evaluation()
        # White pawn moves from e2 to e4.
        # Positional value at e2 is -20. Positional value at e4 is +20.
        # The net change is +40 for White.
        # The test asserts from Black's perspective, so the expected score is -40.
        self.assertEqual(evaluator.evaluate(board, BLACK), -40)