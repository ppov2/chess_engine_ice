import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chess_engine.board.board import Board, WHITE, BLACK, PAWN, ROOK, EMPTY
from chess_engine.move_generator.move_generator import Move

class TestBoard(unittest.TestCase):

    def test_initial_board_setup(self):
        board = Board()
        self.assertEqual(board.board[0][0], BLACK | ROOK)
        self.assertEqual(board.board[6][0], WHITE | PAWN)
        self.assertEqual(board.board[3][3], EMPTY)

    def test_fen_loading(self):
        fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        board = Board(fen=fen)
        self.assertEqual(board.board[4][4], WHITE | PAWN) # e4
        self.assertEqual(board.board[2][5], EMPTY) # f6 is empty

    def test_make_unmake_move(self):
        board = Board()
        # Move a white pawn e2e4
        move = Move(from_square=(6, 4), to_square=(4, 4), piece=(WHITE | PAWN))

        # Make the move
        board.make_move(move)
        self.assertEqual(board.board[4][4], WHITE | PAWN)
        self.assertEqual(board.board[6][4], EMPTY)

        # Unmake the move
        board.unmake_move(move)
        self.assertEqual(board.board[6][4], WHITE | PAWN)
        self.assertEqual(board.board[4][4], EMPTY)

if __name__ == '__main__':
    unittest.main()
