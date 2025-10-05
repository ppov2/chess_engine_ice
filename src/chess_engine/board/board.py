from ..constants import (
    EMPTY, PIECE_MAP, PIECE_CHARS, STARTING_FEN, WHITE, BLACK, PAWN, KING
)

class Board:
    """
    Represents the chess board and the game state.

    Attributes:
        board (list[list[int]]): An 8x8 grid representing the board, with pieces encoded as integers.
        color_to_move (int): The color of the player whose turn it is (WHITE or BLACK).
        castling_rights (str): A string indicating available castling rights (e.g., "KQkq").
        en_passant_square (tuple|None): The coordinates of the en passant target square, if any.
        halfmove_clock (int): The number of halfmoves since the last capture or pawn advance.
        fullmove_number (int): The total number of full moves in the game.
        history (list[dict]): A history of board states for unmaking moves.
    """
    def __init__(self, fen=STARTING_FEN):
        """
        Initializes the board, optionally from a FEN string.

        Args:
            fen (str): A FEN string representing the starting position. Defaults to the standard chess starting position.
        """
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        self.color_to_move = WHITE
        self.castling_rights = "KQkq"
        self.en_passant_square = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.history = []  # For unmake_move
        self.load_fen(fen)

    def load_fen(self, fen):
        """
        Loads a board state from a FEN string and resets the move history.

        Args:
            fen (str): The FEN string to load.

        Raises:
            ValueError: If the FEN string is invalid.
        """
        self.history = []
        try:
            parts = fen.split(' ')
            if len(parts) != 6: raise ValueError("FEN string must have 6 parts")
            piece_placement, active_color, castling, en_passant, halfmove, fullmove = parts

            # 1. Piece Placement
            ranks = piece_placement.split('/')
            if len(ranks) != 8: raise ValueError("FEN piece placement must have 8 ranks")
            for r, rank in enumerate(ranks):
                c = 0
                for char in rank:
                    if c >= 8: break
                    if char.isdigit(): c += int(char)
                    else:
                        self.board[r][c] = PIECE_MAP.get(char)
                        if self.board[r][c] is None: raise ValueError(f"Invalid piece '{char}'")
                        c += 1

            # 2. Active Color
            if active_color == 'w': self.color_to_move = WHITE
            elif active_color == 'b': self.color_to_move = BLACK
            else: raise ValueError(f"Invalid active color '{active_color}'")

            # 3. Castling Rights
            if castling != '-' and (not set(castling).issubset(set('KQkq')) or len(set(castling)) != len(castling)):
                raise ValueError(f"Invalid castling rights '{castling}'")
            self.castling_rights = castling

            # 4. En Passant
            if en_passant != '-':
                if not ('a' <= en_passant[0] <= 'h' and '1' <= en_passant[1] <= '8'):
                    raise ValueError(f"Invalid en passant square '{en_passant}'")
                self.en_passant_square = (8 - int(en_passant[1]), ord(en_passant[0]) - ord('a'))
            else: self.en_passant_square = None

            self.halfmove_clock = int(halfmove)
            self.fullmove_number = int(fullmove)
        except (IndexError, ValueError, KeyError) as e:
            raise ValueError(f"Invalid FEN string: '{fen}'. Error: {e}")

    def to_str(self):
        """
        Returns a human-readable string representation of the board.
        """
        return "\n".join([" ".join([PIECE_CHARS.get(p, '?') for p in row]) for row in self.board])

    def __str__(self):
        return self.to_str()

    def make_move(self, move):
        """
        Applies a move to the board, updating the game state.

        This method handles all move types, including standard moves, captures,
        en passant, castling, and pawn promotions. It also updates all
        relevant game state variables like turn, castling rights, and clocks.

        Args:
            move (Move): The move object to apply.
        """
        self.history.append({
            "castling_rights": self.castling_rights,
            "en_passant_square": self.en_passant_square,
            "halfmove_clock": self.halfmove_clock,
        })

        from_r, from_c = move.from_square
        to_r, to_c = move.to_square
        piece = move.piece
        piece_type = piece & 7

        # Update halfmove clock
        if piece_type == PAWN or move.captured_piece != EMPTY:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Update en passant square
        if piece_type == PAWN and abs(from_r - to_r) == 2:
            self.en_passant_square = (from_r + (1 if self.color_to_move == BLACK else -1), from_c)
        else:
            self.en_passant_square = None

        # Move piece
        self.board[from_r][from_c] = EMPTY
        self.board[to_r][to_c] = piece

        # Handle special move logic
        if move.is_en_passant:
            captured_pawn_r = from_r
            captured_pawn_c = to_c
            self.board[captured_pawn_r][captured_pawn_c] = EMPTY
        elif move.is_castling:
            rook_from_c, rook_to_c = (7, 5) if to_c == 6 else (0, 3)
            rook_piece = self.board[from_r][rook_from_c]
            self.board[from_r][rook_from_c] = EMPTY
            self.board[from_r][rook_to_c] = rook_piece
        elif move.promotion_piece:
            self.board[to_r][to_c] = move.promotion_piece

        # Update castling rights
        if piece_type == KING:
            if self.color_to_move == WHITE: self.castling_rights = self.castling_rights.replace('K', '').replace('Q', '')
            else: self.castling_rights = self.castling_rights.replace('k', '').replace('q', '')

        if (from_r, from_c) == (7, 0) or (to_r, to_c) == (7, 0): self.castling_rights = self.castling_rights.replace('Q', '')
        if (from_r, from_c) == (7, 7) or (to_r, to_c) == (7, 7): self.castling_rights = self.castling_rights.replace('K', '')
        if (from_r, from_c) == (0, 0) or (to_r, to_c) == (0, 0): self.castling_rights = self.castling_rights.replace('q', '')
        if (from_r, from_c) == (0, 7) or (to_r, to_c) == (0, 7): self.castling_rights = self.castling_rights.replace('k', '')

        # Update turn
        if self.color_to_move == BLACK: self.fullmove_number += 1
        self.color_to_move = BLACK if self.color_to_move == WHITE else WHITE

    def unmake_move(self, move):
        """
        Reverts a move, restoring the board to its previous state.

        This method correctly undoes all move types, including special moves,
        by restoring the previous game state from the history stack.

        Args:
            move (Move): The move object to revert.
        """
        last_state = self.history.pop()
        self.castling_rights = last_state["castling_rights"]
        self.en_passant_square = last_state["en_passant_square"]
        self.halfmove_clock = last_state["halfmove_clock"]

        from_r, from_c = move.from_square
        to_r, to_c = move.to_square
        piece = move.piece

        # Reverse turn
        self.color_to_move = piece & (WHITE | BLACK)
        if self.color_to_move == BLACK: self.fullmove_number -= 1

        # Move piece back
        self.board[from_r][from_c] = piece
        self.board[to_r][to_c] = move.captured_piece

        # Reverse special moves
        if move.is_en_passant:
            self.board[to_r][to_c] = EMPTY
            captured_pawn_r = from_r
            captured_pawn_c = to_c
            self.board[captured_pawn_r][captured_pawn_c] = move.captured_piece
        elif move.is_castling:
            rook_from_c, rook_to_c = (5, 7) if to_c == 6 else (3, 0)
            rook_piece = self.board[from_r][rook_from_c]
            self.board[from_r][rook_from_c] = EMPTY
            self.board[from_r][rook_to_c] = rook_piece