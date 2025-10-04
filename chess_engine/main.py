import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chess_engine.board.board import Board, WHITE, BLACK
from chess_engine.move_generator.move_generator import MoveGenerator
from chess_engine.evaluation.evaluation import Evaluation
from chess_engine.search.search import Search

def get_color_to_move_from_fen(fen):
    """
    Parses the FEN string to determine whose turn it is.
    'w' for White, 'b' for Black.
    """
    parts = fen.split()
    if len(parts) > 1:
        return WHITE if parts[1] == 'w' else BLACK
    return WHITE # Default to white if not specified

def main():
    """
    Main function to run the chess engine from the command line.
    """
    parser = argparse.ArgumentParser(description="A simple chess engine.")
    parser.add_argument("--fen", type=str, default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", help="FEN string of the board position.")
    parser.add_argument("--depth", type=int, default=3, help="Search depth.")
    args = parser.parse_args()

    fen = args.fen
    depth = args.depth

    color_to_move = get_color_to_move_from_fen(fen)

    board = Board(fen=fen)
    move_generator = MoveGenerator(board)
    evaluator = Evaluation()
    searcher = Search(board, move_generator, evaluator)

    print(f"Position (FEN: {fen}):")
    print(board)
    print(f"Searching for best move for {'White' if color_to_move == WHITE else 'Black'} at depth {depth}...")

    best_move = searcher.search(depth, color_to_move)

    if best_move:
        print(f"Best move found: {best_move}")
    else:
        print("No legal moves found.")

if __name__ == "__main__":
    main()
