import unittest

from src.chess_engine.board.board import Board
from src.chess_engine.move_generator.move_generator import Move
from src.chess_engine.constants import (
    WHITE, BLACK, PAWN, ROOK, EMPTY,
    WHITE_PAWN, BLACK_ROOK, WHITE_KING, BLACK_KING
)

class TestBoard(unittest.TestCase):

    def test_initial_board_setup(self):
        """
        Tests that the board is set up correctly in the standard starting position.
        """
        board = Board()
        self.assertEqual(board.board[0][0], BLACK_ROOK)
        self.assertEqual(board.board[6][0], WHITE_PAWN)
        self.assertEqual(board.board[3][3], EMPTY)
        self.assertEqual(board.color_to_move, WHITE)
        self.assertEqual(board.castling_rights, "KQkq")
        self.assertIsNone(board.en_passant_square)
        self.assertEqual(board.halfmove_clock, 0)
        self.assertEqual(board.fullmove_number, 1)

    def test_fen_loading_valid(self):
        """
        Tests loading a board from a valid, non-starting FEN string.
        """
        fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        board = Board(fen=fen)
        self.assertEqual(board.board[4][4], WHITE_PAWN) # e4
        self.assertEqual(board.board[2][5], EMPTY) # f6 is empty
        self.assertEqual(board.color_to_move, BLACK)
        self.assertEqual(board.castling_rights, "KQkq")
        self.assertIsNone(board.en_passant_square)
        self.assertEqual(board.halfmove_clock, 1)
        self.assertEqual(board.fullmove_number, 2)

    def test_fen_loading_with_en_passant(self):
        """
        Tests loading a FEN string with an en passant square.
        """
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        board = Board(fen=fen)
        self.assertEqual(board.en_passant_square, (5, 4)) # e3 square

    def test_fen_loading_invalid(self):
        """
        Tests that the FEN loader raises ValueError for invalid FEN strings.
        """
        invalid_fens = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0", # Too few parts
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP w KQkq - 0 1", # Missing rank
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1", # Invalid color
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Z - 0 1", # Invalid castling
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e9 0 1", # Invalid en passant
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - x 1", # Invalid halfmove
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 y", # Invalid fullmove
            "rnbqkbnr/pppppppz/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", # Invalid piece
        ]
        for fen in invalid_fens:
            with self.assertRaises(ValueError, msg=f"FEN should be invalid: {fen}"):
                Board(fen=fen)

    def test_make_unmake_move(self):
        """
        Tests the make_move and unmake_move methods.
        """
        board = Board()
        # Move a white pawn e2e4
        move = Move(from_square=(6, 4), to_square=(4, 4), piece=WHITE_PAWN)

        # Make the move
        board.make_move(move)
        self.assertEqual(board.board[4][4], WHITE_PAWN)
        self.assertEqual(board.board[6][4], EMPTY)

        # Unmake the move
        board.unmake_move(move)
        self.assertEqual(board.board[6][4], WHITE_PAWN)
        self.assertEqual(board.board[4][4], EMPTY)