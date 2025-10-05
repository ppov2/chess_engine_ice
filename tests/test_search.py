import unittest

from src.chess_engine.board.board import Board
from src.chess_engine.move_generator.move_generator import MoveGenerator
from src.chess_engine.evaluation.evaluation import Evaluation
from src.chess_engine.search.search import Search
from src.chess_engine.constants import WHITE, BLACK

class TestSearch(unittest.TestCase):

    def test_finds_winning_capture(self):
        """
        Tests that the search can find a simple, winning capture.
        """
        # Position where White's rook on a2 can capture Black's rook on a8.
        fen = "r3k3/8/8/8/8/8/R7/4K3 w - - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        evaluator = Evaluation()
        searcher = Search(board, move_generator, evaluator)

        # At any depth, the best move should be to take the hanging rook.
        best_move = searcher.search(depth=2, color_to_move=WHITE)
        self.assertIsNotNone(best_move)
        self.assertEqual(str(best_move), "a2a8")

    def test_finds_checkmate(self):
        """
        Tests that the search can find a forced mate-in-1.
        The test validates this by checking that the move found leads to a position
        where the opponent has no legal moves and is in check.
        """
        # Position: White to move and deliver mate with the queen.
        fen = "1k6/3Q4/1K6/8/8/8/8/8 w - - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        evaluator = Evaluation()
        searcher = Search(board, move_generator, evaluator)

        best_move = searcher.search(depth=2, color_to_move=WHITE)
        self.assertIsNotNone(best_move)

        # Make the move and verify it's checkmate
        board.make_move(best_move)
        post_move_generator = MoveGenerator(board)
        self.assertTrue(post_move_generator.is_king_in_check(BLACK))
        self.assertEqual(len(post_move_generator.get_legal_moves(BLACK)), 0)

    def test_stalemate(self):
        """
        Tests that the search correctly identifies a stalemate and returns no move.
        """
        # Position: Black to move, but is stalemated by the White queen.
        fen = "7k/5Q2/8/8/8/8/8/K7 b - - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        evaluator = Evaluation()
        searcher = Search(board, move_generator, evaluator)

        # In a stalemate, there are no legal moves, so search should return None.
        best_move = searcher.search(depth=2, color_to_move=BLACK)
        self.assertIsNone(best_move)

    def test_quiescence_search_avoids_blunder(self):
        """
        Tests that quiescence search correctly evaluates captures and avoids blunders.
        """
        # Position: White to move.
        # Taking the pawn on e7 with the queen (Qxe7+) looks good to a shallow search,
        # but it's a blunder because the king will recapture (Kxe7), winning the queen.
        # A good search should avoid this and choose a safer move.
        fen = "3rk3/4p3/8/8/8/8/8/3QK3 w - - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        evaluator = Evaluation()
        searcher = Search(board, move_generator, evaluator)

        # A depth-1 search without quiescence might pick Qxe7 (d1e7).
        # With quiescence, it should see the recapture and choose a better move.
        best_move = searcher.search(depth=1, color_to_move=WHITE)
        self.assertIsNotNone(best_move)
        # Assert that the search does NOT choose the blunder.
        self.assertNotEqual(str(best_move), "d1e7")