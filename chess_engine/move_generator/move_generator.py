import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from chess_engine.board.board import Board, WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY

class Move:
    def __init__(self, from_square, to_square, piece, captured_piece=EMPTY):
        self.from_square = from_square
        self.to_square = to_square
        self.piece = piece
        self.captured_piece = captured_piece

    def __str__(self):
        # A simple string representation, e.g., "e2e4"
        return f"{self.square_to_str(self.from_square)}{self.square_to_str(self.to_square)}"

    def square_to_str(self, square):
        row, col = square
        return f"{chr(ord('a') + col)}{8 - row}"


class MoveGenerator:
    def __init__(self, board: Board):
        self.board = board

    def get_legal_moves(self, color):
        # For now, this will just generate pseudo-legal moves
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board.board[r][c]
                if piece != EMPTY and (piece & color):
                    moves.extend(self.get_piece_moves((r, c), piece))
        return moves

    def get_piece_moves(self, square, piece):
        piece_type = piece & 7
        if piece_type == PAWN:
            return self.get_pawn_moves(square, piece)
        elif piece_type == KNIGHT:
            return self.get_knight_moves(square, piece)
        elif piece_type == BISHOP:
            return self.get_sliding_piece_moves(square, piece, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
        elif piece_type == ROOK:
            return self.get_sliding_piece_moves(square, piece, [(-1, 0), (1, 0), (0, -1), (0, 1)])
        elif piece_type == QUEEN:
            return self.get_sliding_piece_moves(square, piece, [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)])
        elif piece_type == KING:
            return self.get_king_moves(square, piece)
        return []

    def get_pawn_moves(self, square, piece):
        moves = []
        r, c = square
        color = piece & 24

        direction = -1 if color == WHITE else 1
        start_row = 6 if color == WHITE else 1

        # 1. Move forward
        if 0 <= r + direction < 8 and self.board.board[r + direction][c] == EMPTY:
            moves.append(Move(square, (r + direction, c), piece))
            # 2. Double move from starting rank
            if r == start_row and self.board.board[r + 2 * direction][c] == EMPTY:
                moves.append(Move(square, (r + 2 * direction, c), piece))

        # 3. Captures
        for dc in [-1, 1]:
            if 0 <= c + dc < 8 and 0 <= r + direction < 8:
                target_piece = self.board.board[r + direction][c + dc]
                if target_piece != EMPTY and not (target_piece & color):
                    moves.append(Move(square, (r + direction, c + dc), piece, captured_piece=target_piece))

        return moves

    def get_knight_moves(self, square, piece):
        moves = []
        r, c = square
        color = piece & 24

        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target_piece = self.board.board[nr][nc]
                if target_piece == EMPTY:
                    moves.append(Move(square, (nr, nc), piece))
                elif not (target_piece & color):
                    moves.append(Move(square, (nr, nc), piece, captured_piece=target_piece))
        return moves

    def get_king_moves(self, square, piece):
        moves = []
        r, c = square
        color = piece & 24

        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in king_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target_piece = self.board.board[nr][nc]
                if target_piece == EMPTY:
                    moves.append(Move(square, (nr, nc), piece))
                elif not (target_piece & color):
                    moves.append(Move(square, (nr, nc), piece, captured_piece=target_piece))
        return moves

    def get_sliding_piece_moves(self, square, piece, directions):
        moves = []
        r, c = square
        color = piece & 24

        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + i * dr, c + i * dc

                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break # Off board

                target_piece = self.board.board[nr][nc]

                if target_piece == EMPTY:
                    moves.append(Move(square, (nr, nc), piece))
                else:
                    if not (target_piece & color):
                        moves.append(Move(square, (nr, nc), piece, captured_piece=target_piece))
                    break # Blocked by a piece
        return moves


if __name__ == '__main__':
    board = Board()
    move_generator = MoveGenerator(board)

    print("--- White's moves in starting position ---")
    white_moves = move_generator.get_legal_moves(WHITE)
    for move in white_moves:
        print(move)

    print("\n--- Black's moves in starting position ---")
    black_moves = move_generator.get_legal_moves(BLACK)
    for move in black_moves:
        print(move)

    # Test from a different position
    fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
    board_from_fen = Board(fen=fen)
    move_generator_fen = MoveGenerator(board_from_fen)

    print(f"\n--- Black's moves from FEN: {fen} ---")
    black_moves_fen = move_generator_fen.get_legal_moves(BLACK)
    for move in black_moves_fen:
        print(move)
