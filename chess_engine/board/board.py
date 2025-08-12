# Piece constants
EMPTY = 0
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 1, 2, 3, 4, 5, 6
WHITE, BLACK = 8, 16

class Board:
    def __init__(self, fen=None):
        if fen:
            self.board = self.load_fen(fen)
        else:
            self.board = self.setup_board()

    def setup_board(self):
        # Standard chess starting position
        board = [
            [BLACK | ROOK, BLACK | KNIGHT, BLACK | BISHOP, BLACK | QUEEN, BLACK | KING, BLACK | BISHOP, BLACK | KNIGHT, BLACK | ROOK],
            [BLACK | PAWN] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [WHITE | PAWN] * 8,
            [WHITE | ROOK, WHITE | KNIGHT, WHITE | BISHOP, WHITE | QUEEN, WHITE | KING, WHITE | BISHOP, WHITE | KNIGHT, WHITE | ROOK],
        ]
        return board

    def load_fen(self, fen):
        # This is a simplified FEN parser. It only handles the piece placement part.
        # A full FEN parser would also handle active color, castling rights, en passant target square, halfmove clock, and fullmove number.
        board = [[EMPTY for _ in range(8)] for _ in range(8)]
        fen_parts = fen.split(' ')
        piece_placement = fen_parts[0]
        ranks = piece_placement.split('/')

        piece_map = {
            'p': BLACK | PAWN, 'n': BLACK | KNIGHT, 'b': BLACK | BISHOP, 'r': BLACK | ROOK, 'q': BLACK | QUEEN, 'k': BLACK | KING,
            'P': WHITE | PAWN, 'N': WHITE | KNIGHT, 'B': WHITE | BISHOP, 'R': WHITE | ROOK, 'Q': WHITE | QUEEN, 'K': WHITE | KING,
        }

        for r, rank in enumerate(ranks):
            c = 0
            for char in rank:
                if char.isdigit():
                    c += int(char)
                else:
                    board[r][c] = piece_map[char]
                    c += 1
        return board


    def to_str(self):
        # For printing the board
        piece_chars = {
            EMPTY: '.',
            WHITE | PAWN: 'P', WHITE | KNIGHT: 'N', WHITE | BISHOP: 'B', WHITE | ROOK: 'R', WHITE | QUEEN: 'Q', WHITE | KING: 'K',
            BLACK | PAWN: 'p', BLACK | KNIGHT: 'n', BLACK | BISHOP: 'b', BLACK | ROOK: 'r', BLACK | QUEEN: 'q', BLACK | KING: 'k',
        }
        board_str = ""
        for row in self.board:
            board_str += " ".join([piece_chars.get(piece, '?') for piece in row]) + "\n"
        return board_str

    def __str__(self):
        return self.to_str()

    def make_move(self, move):
        from_r, from_c = move.from_square
        to_r, to_c = move.to_square

        self.board[to_r][to_c] = move.piece
        self.board[from_r][from_c] = EMPTY

    def unmake_move(self, move):
        from_r, from_c = move.from_square
        to_r, to_c = move.to_square

        self.board[from_r][from_c] = move.piece
        self.board[to_r][to_c] = move.captured_piece

if __name__ == '__main__':
    # Test starting position
    board = Board()
    print("Starting position:")
    print(board)

    # Test FEN position
    fen_string = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
    board_from_fen = Board(fen=fen_string)
    print("\nPosition from FEN:")
    print(board_from_fen)
