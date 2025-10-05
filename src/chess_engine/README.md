# Python Chess Engine

A lightweight, educational chess engine written in Python, designed with a focus on clear, modular, and well-documented code. This project serves as a practical example of the core components of a chess engine, including board representation, legal move generation, evaluation functions, and search algorithms.

## Features

This engine has been refactored and improved to include a robust set of features:

-   **Modular Architecture**: The project is structured as a proper Python package with a clear separation of concerns into `board`, `move_generator`, `evaluation`, and `search` modules.
-   **Full FEN Parsing**: The engine can load any valid Forsyth-Edwards Notation (FEN) string, allowing for easy setup of custom positions.
-   **Legal Move Generation**: The move generator produces fully legal moves, correctly handling all special chess rules:
    -   **En Passant**
    -   **Pawn Promotion**
    -   **Castling**
-   **Check and Checkmate Detection**: The engine accurately identifies checks, checkmates, and stalemates.
-   **Sophisticated Evaluation**: The evaluation function goes beyond simple material counting and incorporates **Piece-Square Tables (PSTs)** to understand the strategic value of piece placement.
-   **Alpha-Beta Search with Quiescence**: The search algorithm uses a Negamax framework with alpha-beta pruning and includes a **quiescence search** to mitigate the horizon effect and improve tactical accuracy.
-   **Comprehensive Test Suite**: The project is supported by a robust suite of unit tests to ensure correctness and prevent regressions.

## Getting Started

### Prerequisites

-   Python 3.6+

### Installation

No external libraries are required. Simply clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

### How to Run the Engine

You can run the engine from the command line to find the best move for a given position. The main script is located at `src.chess_engine.main`.

To run the engine from the root of the project, use the following command:

```bash
python3 -m src.chess_engine.main [OPTIONS]
```

**Options:**

-   `--fen <FEN_STRING>`: Specify the board position using a FEN string. Defaults to the standard starting position.
-   `--depth <INTEGER>`: Set the search depth for the engine. Defaults to `3`.

**Examples:**

1.  **Find the best move from the starting position at depth 3:**
    ```bash
    python3 -m src.chess_engine.main
    ```

2.  **Find the best move for Black from the Sicilian Defense opening at depth 4:**
    ```bash
    python3 -m src.chess_engine.main --fen "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2" --depth 4
    ```

### How to Run Tests

The project includes a comprehensive suite of unit tests. To run them, navigate to the root directory of the project and run the following command:

```bash
python3 -m unittest discover .
```

This will automatically discover and run all tests in the `tests` directory.