"""
This is the main entry point for running the chess engine from the command line.

It allows the user to specify a board position via a FEN string and a search
depth, and it will then use the engine's search algorithm to find and print
the best move for the current player.
"""
import argparse

from .board.board import Board, WHITE
from .move_generator.move_generator import MoveGenerator
from .evaluation.evaluation import Evaluation
from .search.search import Search

def main():
    """
    Sets up the engine, parses command-line arguments, and runs the search.
    """
    parser = argparse.ArgumentParser(
        description="A simple chess engine.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--fen",
        type=str,
        default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        help="FEN string of the board position."
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Search depth for the engine."
    )
    args = parser.parse_args()

    # Initialize the board and engine components
    board = Board(fen=args.fen)
    move_generator = MoveGenerator(board)
    evaluator = Evaluation()
    searcher = Search(board, move_generator, evaluator)

    # Get the color to move from the board state
    color_to_move = board.color_to_move

    # Print the initial position and search parameters
    print(f"Position (FEN: {args.fen}):")
    print(board)
    print(f"Searching for the best move for {'White' if color_to_move == WHITE else 'Black'} at depth {args.depth}...")

    # Run the search
    best_move = searcher.search(args.depth, color_to_move)

    # Print the result
    if best_move:
        print(f"Best move found: {best_move}")
    else:
        print("No legal moves found (Checkmate or Stalemate).")

if __name__ == "__main__":
    main()