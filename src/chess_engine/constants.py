# Piece Types
EMPTY = 0
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 1, 2, 3, 4, 5, 6

# Piece Colors
WHITE = 8
BLACK = 16

# Piece-Color Combinations
WHITE_PAWN = WHITE | PAWN
WHITE_KNIGHT = WHITE | KNIGHT
WHITE_BISHOP = WHITE | BISHOP
WHITE_ROOK = WHITE | ROOK
WHITE_QUEEN = WHITE | QUEEN
WHITE_KING = WHITE | KING

BLACK_PAWN = BLACK | PAWN
BLACK_KNIGHT = BLACK | KNIGHT
BLACK_BISHOP = BLACK | BISHOP
BLACK_ROOK = BLACK | ROOK
BLACK_QUEEN = BLACK | QUEEN
BLACK_KING = BLACK | KING

# FEN-to-Piece Mapping
PIECE_MAP = {
    'p': BLACK_PAWN, 'n': BLACK_KNIGHT, 'b': BLACK_BISHOP, 'r': BLACK_ROOK, 'q': BLACK_QUEEN, 'k': BLACK_KING,
    'P': WHITE_PAWN, 'N': WHITE_KNIGHT, 'B': WHITE_BISHOP, 'R': WHITE_ROOK, 'Q': WHITE_QUEEN, 'K': WHITE_KING,
}

# Piece-to-Character Mapping (for board printing)
PIECE_CHARS = {
    EMPTY: '.',
    WHITE_PAWN: 'P', WHITE_KNIGHT: 'N', WHITE_BISHOP: 'B', WHITE_ROOK: 'R', WHITE_QUEEN: 'Q', WHITE_KING: 'K',
    BLACK_PAWN: 'p', BLACK_KNIGHT: 'n', BLACK_BISHOP: 'b', BLACK_ROOK: 'r', BLACK_QUEEN: 'q', BLACK_KING: 'k',
}

# Standard starting FEN
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# --- Piece-Square Tables (PSTs) ---
# The values are from White's perspective. For Black, the board is flipped vertically.

PAWN_PST = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_PST = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_PST = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_PST = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_PST = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

# King PST for Middle Game
KING_PST_MG = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

# King PST for End Game
KING_PST_EG = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

# Maps piece type to its corresponding PST
PIECE_SQUARE_TABLES = {
    PAWN: PAWN_PST,
    KNIGHT: KNIGHT_PST,
    BISHOP: BISHOP_PST,
    ROOK: ROOK_PST,
    QUEEN: QUEEN_PST,
    KING: KING_PST_MG # Default to middlegame PST for now
}