from ..board.board import Board
from ..constants import (
    WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY,
    WHITE_KING, BLACK_KING
)

class Move:
    """
    Represents a single move in a chess game.

    Attributes:
        from_square (tuple): The starting (row, col) of the move.
        to_square (tuple): The ending (row, col) of the move.
        piece (int): The piece being moved.
        captured_piece (int): The piece being captured, if any.
        promotion_piece (int|None): The piece to promote a pawn to, if applicable.
        is_en_passant (bool): True if the move is an en passant capture.
        is_castling (bool): True if the move is a castling move.
    """
    def __init__(self, from_square, to_square, piece, captured_piece=EMPTY, promotion_piece=None, is_en_passant=False, is_castling=False):
        self.from_square = from_square
        self.to_square = to_square
        self.piece = piece
        self.captured_piece = captured_piece
        self.promotion_piece = promotion_piece
        self.is_en_passant = is_en_passant
        self.is_castling = is_castling

    def __str__(self):
        """
        Returns a string representation of the move in UCI format (e.g., "e2e4", "e7e8q").
        """
        move_str = f"{self.square_to_str(self.from_square)}{self.square_to_str(self.to_square)}"
        if self.promotion_piece:
            piece_type = self.promotion_piece & 7
            if piece_type == QUEEN: move_str += 'q'
            elif piece_type == ROOK: move_str += 'r'
            elif piece_type == BISHOP: move_str += 'b'
            elif piece_type == KNIGHT: move_str += 'n'
        return move_str

    def square_to_str(self, square):
        """Converts a (row, col) tuple to algebraic notation (e.g., (0, 0) -> "a8")."""
        row, col = square
        return f"{chr(ord('a') + col)}{8 - row}"


class MoveGenerator:
    """
    Generates all legal moves for a given board position.
    """
    def __init__(self, board: Board):
        """
        Initializes the MoveGenerator.

        Args:
            board (Board): The board object to generate moves for.
        """
        self.board = board

    def get_legal_moves(self, color):
        """
        Generates all fully legal moves for a given color.

        This is the main public method for move generation. It produces a list of
        pseudo-legal moves and then filters them to ensure that none of them
        leave the king in check.

        Args:
            color (int): The color of the player to generate moves for (WHITE or BLACK).

        Returns:
            list[Move]: A list of all legal moves.
        """
        legal_moves = []
        pseudo_legal_moves = self._get_pseudo_legal_moves(color)

        for move in pseudo_legal_moves:
            self.board.make_move(move)
            king_square = self._find_king(color)
            if king_square and not self.is_square_attacked(king_square, BLACK if color == WHITE else WHITE):
                legal_moves.append(move)
            self.board.unmake_move(move)

        return legal_moves

    def _get_pseudo_legal_moves(self, color):
        """
        Generates all pseudo-legal moves (does not check for checks).
        """
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board.board[r][c]
                if piece != EMPTY and (piece & color):
                    moves.extend(self.get_piece_moves((r, c), piece))

        moves.extend(self.get_castling_moves(color))
        return moves

    def is_king_in_check(self, color):
        """
        Checks if the king of the specified color is in check.

        Args:
            color (int): The color of the king to check.

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        king_square = self._find_king(color)
        if not king_square: return False
        return self.is_square_attacked(king_square, BLACK if color == WHITE else WHITE)

    def _find_king(self, color):
        """
        Finds the square of the king for a given color.
        """
        king_to_find = WHITE_KING if color == WHITE else BLACK_KING
        for r in range(8):
            for c in range(8):
                if self.board.board[r][c] == king_to_find:
                    return (r, c)
        return None

    def is_square_attacked(self, square, attacker_color):
        """
        Checks if a given square is attacked by an opponent.

        Args:
            square (tuple): The (row, col) of the square to check.
            attacker_color (int): The color of the attacking pieces.

        Returns:
            bool: True if the square is under attack, False otherwise.
        """
        r, c = square

        pawn_dir = 1 if attacker_color == WHITE else -1
        for dc in [-1, 1]:
            if 0 <= r + pawn_dir < 8 and 0 <= c + dc < 8 and self.board.board[r + pawn_dir][c + dc] == (attacker_color | PAWN):
                return True

        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            if 0 <= r + dr < 8 and 0 <= c + dc < 8 and self.board.board[r + dr][c + dc] == (attacker_color | KNIGHT):
                return True

        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            if 0 <= r + dr < 8 and 0 <= c + dc < 8 and self.board.board[r + dr][c + dc] == (attacker_color | KING):
                return True

        sliding_directions = {BISHOP: [(-1, -1), (-1, 1), (1, -1), (1, 1)], ROOK: [(-1, 0), (1, 0), (0, -1), (0, 1)]}
        for piece_type, directions in sliding_directions.items():
            for dr, dc in directions:
                for i in range(1, 8):
                    nr, nc = r + i * dr, c + i * dc
                    if not (0 <= nr < 8 and 0 <= nc < 8): break
                    target_piece = self.board.board[nr][nc]
                    if target_piece != EMPTY:
                        if target_piece == (attacker_color | piece_type) or target_piece == (attacker_color | QUEEN):
                            return True
                        break
        return False

    def get_piece_moves(self, square, piece):
        """
        Dispatches move generation to the correct function based on piece type.
        """
        piece_type = piece & 7
        if piece_type == PAWN: return self.get_pawn_moves(square, piece)
        if piece_type == KNIGHT: return self.get_knight_moves(square, piece)
        if piece_type == BISHOP: return self.get_sliding_piece_moves(square, piece, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
        if piece_type == ROOK: return self.get_sliding_piece_moves(square, piece, [(-1, 0), (1, 0), (0, -1), (0, 1)])
        if piece_type == QUEEN: return self.get_sliding_piece_moves(square, piece, [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)])
        if piece_type == KING: return self.get_king_moves(square, piece)
        return []

    def get_pawn_moves(self, square, piece):
        """
        Generates all pseudo-legal moves for a pawn, including promotions and en passant.
        """
        moves = []
        r, c = square
        color = piece & (WHITE | BLACK)
        direction = -1 if color == WHITE else 1
        promotion_rank = 0 if color == WHITE else 7

        # Standard forward move
        if 0 <= r + direction < 8 and self.board.board[r + direction][c] == EMPTY:
            if r + direction == promotion_rank:
                for p_piece in [QUEEN, ROOK, BISHOP, KNIGHT]:
                    moves.append(Move(square, (r + direction, c), piece, promotion_piece=color | p_piece))
            else:
                moves.append(Move(square, (r + direction, c), piece))

            # Double move from start
            start_row = 6 if color == WHITE else 1
            if r == start_row and self.board.board[r + 2 * direction][c] == EMPTY:
                moves.append(Move(square, (r + 2 * direction, c), piece))

        # Captures
        for dc in [-1, 1]:
            if 0 <= c + dc < 8 and 0 <= r + direction < 8:
                target_piece = self.board.board[r + direction][c + dc]
                if target_piece != EMPTY and not (target_piece & color):
                    if r + direction == promotion_rank:
                        for p_piece in [QUEEN, ROOK, BISHOP, KNIGHT]:
                            moves.append(Move(square, (r + direction, c + dc), piece, captured_piece=target_piece, promotion_piece=color | p_piece))
                    else:
                        moves.append(Move(square, (r + direction, c + dc), piece, captured_piece=target_piece))
                # En passant
                if (r + direction, c + dc) == self.board.en_passant_square:
                    moves.append(Move(square, (r + direction, c + dc), piece, captured_piece=self.board.board[r][c+dc], is_en_passant=True))
        return moves

    def get_knight_moves(self, square, piece):
        """
        Generates all pseudo-legal moves for a knight.
        """
        moves = []
        r, c = square
        color = piece & (WHITE | BLACK)
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board.board[nr][nc]
                if target == EMPTY: moves.append(Move(square, (nr, nc), piece))
                elif not (target & color): moves.append(Move(square, (nr, nc), piece, captured_piece=target))
        return moves

    def get_king_moves(self, square, piece):
        """
        Generates all pseudo-legal moves for a king.
        """
        moves = []
        r, c = square
        color = piece & (WHITE | BLACK)
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board.board[nr][nc]
                if target == EMPTY: moves.append(Move(square, (nr, nc), piece))
                elif not (target & color): moves.append(Move(square, (nr, nc), piece, captured_piece=target))
        return moves

    def get_sliding_piece_moves(self, square, piece, directions):
        """
        Generates all pseudo-legal moves for sliding pieces (bishop, rook, queen).
        """
        moves = []
        r, c = square
        color = piece & (WHITE | BLACK)
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + i * dr, c + i * dc
                if not (0 <= nr < 8 and 0 <= nc < 8): break
                target = self.board.board[nr][nc]
                if target == EMPTY:
                    moves.append(Move(square, (nr, nc), piece))
                else:
                    if not (target & color): moves.append(Move(square, (nr, nc), piece, captured_piece=target))
                    break
        return moves

    def get_castling_moves(self, color):
        """
        Generates pseudo-legal castling moves.
        """
        moves = []
        if self.is_king_in_check(color): return []

        opponent_color = BLACK if color == WHITE else WHITE

        if color == WHITE:
            king_square, k_rook_square, q_rook_square = (7, 4), (7, 7), (7, 0)
            k_castle_char, q_castle_char = 'K', 'Q'
        else:
            king_square, k_rook_square, q_rook_square = (0, 4), (0, 7), (0, 0)
            k_castle_char, q_castle_char = 'k', 'q'

        # Kingside castling
        if k_castle_char in self.board.castling_rights:
            if self.board.board[king_square[0]][king_square[1]+1] == EMPTY and self.board.board[king_square[0]][king_square[1]+2] == EMPTY:
                if not self.is_square_attacked((king_square[0], king_square[1]+1), opponent_color) and \
                   not self.is_square_attacked((king_square[0], king_square[1]+2), opponent_color):
                    moves.append(Move(king_square, (king_square[0], king_square[1]+2), color | KING, is_castling=True))

        # Queenside castling
        if q_castle_char in self.board.castling_rights:
            if self.board.board[king_square[0]][king_square[1]-1] == EMPTY and self.board.board[king_square[0]][king_square[1]-2] == EMPTY and self.board.board[king_square[0]][king_square[1]-3] == EMPTY:
                if not self.is_square_attacked((king_square[0], king_square[1]-1), opponent_color) and \
                   not self.is_square_attacked((king_square[0], king_square[1]-2), opponent_color):
                    moves.append(Move(king_square, (king_square[0], king_square[1]-2), color | KING, is_castling=True))

        return moves