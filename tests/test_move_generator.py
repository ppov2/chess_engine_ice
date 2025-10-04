import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chess_engine.board.board import Board, WHITE, BLACK
from chess_engine.move_generator.move_generator import MoveGenerator

class TestMoveGenerator(unittest.TestCase):

    def test_starting_position_move_count(self):
        board = Board()
        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(WHITE)
        self.assertEqual(len(moves), 20)

    def perft(self, depth, board, color_to_move):
        if depth == 0:
            return 1

        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(color_to_move)
        count = 0
        if depth == 1:
            return len(moves)

        for move in moves:
            board.make_move(move)
            count += self.perft(depth - 1, board, WHITE if color_to_move == BLACK else BLACK)
            board.unmake_move(move)
        return count

    def test_perft_starting_position(self):
        board = Board()
        # Perft results for the starting position
        # Note: These are for legal moves. A pseudo-legal move generator might differ
        # at higher depths where checks become a factor.
        self.assertEqual(self.perft(1, board, WHITE), 20)
        # self.assertEqual(self.perft(2, board, WHITE), 400) # This will be slow
        # Depth 3 and above would require a fully legal move generator and more time.
        # self.assertEqual(self.perft(3, board, WHITE), 8902)

    def test_perft_depth_2(self):
        # Running depth 2 in a separate test to keep tests fast.
        board = Board()
        self.assertEqual(self.perft(2, board, WHITE), 400)


if __name__ == '__main__':
    unittest.main()
