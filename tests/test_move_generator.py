import unittest

from src.chess_engine.board.board import Board
from src.chess_engine.move_generator.move_generator import MoveGenerator
from src.chess_engine.constants import WHITE, BLACK

class TestMoveGenerator(unittest.TestCase):

    def test_is_king_in_check(self):
        """Tests the check detection logic."""
        # Position where the black king on e8 is in check from a white pawn on d7
        fen = "4k3/3P4/8/8/8/8/8/4K3 b - - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        self.assertTrue(move_generator.is_king_in_check(BLACK))
        self.assertFalse(move_generator.is_king_in_check(WHITE))

    def test_pinned_piece_cannot_move(self):
        """Tests that a pinned piece cannot move and expose the king to check."""
        # Black knight on e7 is pinned to the king on e8 by a white rook on e1
        fen = "4k3/4n3/8/8/8/8/8/4R3 b - - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(BLACK)
        # The black knight on e7 should not be able to move.
        e7_moves = [m for m in moves if m.from_square == (1, 4)] # e7 is row 1, col 4
        self.assertEqual(len(e7_moves), 0)

    def test_pawn_promotion(self):
        """Tests that pawn promotions are generated correctly."""
        # White pawn on e7, ready to promote, king is moved away
        fen = "8/4P3/8/8/8/8/k7/4K3 w - - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(WHITE)
        promotion_moves = [m for m in moves if m.promotion_piece is not None]
        self.assertEqual(len(promotion_moves), 4)
        move_strs = sorted([str(m) for m in promotion_moves])
        self.assertIn("e7e8q", move_strs)
        self.assertIn("e7e8r", move_strs)
        self.assertIn("e7e8b", move_strs)
        self.assertIn("e7e8n", move_strs)

    def test_en_passant(self):
        """Tests en passant move generation."""
        # Position set up for an en passant capture on d6
        fen = "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(WHITE)
        en_passant_move = [m for m in moves if m.is_en_passant]
        self.assertEqual(len(en_passant_move), 1)
        self.assertEqual(str(en_passant_move[0]), "e5d6")

    def test_castling(self):
        """Tests castling move generation under various conditions."""
        # 1. Legal castling for white
        fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(WHITE)
        castling_moves = {str(m) for m in moves if m.is_castling}
        self.assertIn("e1g1", castling_moves)
        self.assertIn("e1c1", castling_moves)

        # 2. No castling if king is in check (White King on e1 checked by Black bishop on b4)
        fen = "r3k2r/pp1p1ppp/8/8/1b6/8/PPP2PPP/R3K2R w KQkq - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(WHITE)
        castling_moves = {str(m) for m in moves if m.is_castling}
        self.assertEqual(len(castling_moves), 0)

        # 3. No castling through an attacked square (d8 is attacked by white rook on d1)
        fen = "r3k2r/8/8/8/8/8/8/3RK2R b kq - 0 1"
        board = Board(fen=fen)
        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(BLACK)
        castling_moves = {str(m) for m in moves if m.is_castling}
        self.assertNotIn("e8c8", castling_moves) # Queenside should be illegal
        self.assertIn("e8g8", castling_moves)    # Kingside should be legal

    def _perft(self, depth, board, color):
        """A simple performance test to count all legal moves to a certain depth."""
        if depth == 0:
            return 1

        move_generator = MoveGenerator(board)
        moves = move_generator.get_legal_moves(color)

        if depth == 1:
            return len(moves)

        count = 0
        for move in moves:
            board.make_move(move)
            count += self._perft(depth - 1, board, BLACK if color == WHITE else WHITE)
            board.unmake_move(move)
        return count

    def test_perft_starting_position(self):
        """
        Validates the move generator against known node counts from the starting position.
        """
        board = Board() # Standard starting position
        self.assertEqual(self._perft(1, board, WHITE), 20)
        self.assertEqual(self._perft(2, board, WHITE), 400)

    def test_perft_kiwipete(self):
        """
        Validates move generator against the "Kiwipete" FEN, a standard test position.
        """
        fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        board = Board(fen=fen)
        self.assertEqual(self._perft(1, board, WHITE), 48)