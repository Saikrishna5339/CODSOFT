# Tic-Tac-Toe AI using Minimax Algorithm with Alpha-Beta Pruning
# This script implements a Tic-Tac-Toe game where the player plays against an AI.
import math

# Tic-Tac-Toe Board Representation
def print_board(b):
    print("\n  0   1   2")
    for i, row in enumerate(b):
        print(i, " | ".join(row))
        if i < 2:
            print("  ---------")

# Check for a winner
def check_winner(b):
    lines = [
        b[0], b[1], b[2],
        [b[0][0], b[1][0], b[2][0]],
        [b[0][1], b[1][1], b[2][1]],
        [b[0][2], b[1][2], b[2][2]],
        [b[0][0], b[1][1], b[2][2]],
        [b[0][2], b[1][1], b[2][0]],
    ]
    for line in lines:
        if line[0] != ' ' and line.count(line[0]) == 3:
            return line[0]
    return None

# Check if the game is a draw
def is_draw(b):
    return all(cell != ' ' for row in b for cell in row) and not check_winner(b)

# Check available moves
def available_moves(b):
    return [(r, c) for r in range(3) for c in range(3) if b[r][c] == ' ']

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_max, alpha, beta):
    winner = check_winner(board)
    if winner: return (10 - depth) if winner == 'O' else (depth - 10)
    if is_draw(board): return 0

    best = -math.inf if is_max else math.inf
    player = 'O' if is_max else 'X'

    for r, c in available_moves(board):
        board[r][c] = player
        score = minimax(board, depth + 1, not is_max, alpha, beta)
        board[r][c] = ' '

        if is_max:
            best = max(best, score)
            alpha = max(alpha, best)
        else:
            best = min(best, score)
            beta = min(beta, best)

        if beta <= alpha:
            break

    return best


# Find the best move for the AI
def best_move(board):
    best_score = -math.inf
    move = None
    for r, c in available_moves(board):
        board[r][c] = 'O'
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[r][c] = ' '
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

# Main game loop
def play_game():
    board = [[' '] * 3 for _ in range(3)]
    print("Tic-Tac-Toe: You (X) vs AI (O)")
    turn = 'X'

    while True:
        print_board(board)
        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        if turn == 'X':
            try:
                r, c = map(int, input("Your move (row col): ").split())
                if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == ' ':
                    board[r][c] = 'X'
                    turn = 'O'
                else:
                    print("Invalid or occupied cell. Try again.")
            except:
                print("Enter two numbers (row and col) from 0 to 2.")
        else:
            print("AI is thinking...")
            r, c = best_move(board)
            board[r][c] = 'O'
            turn = 'X'

if __name__ == "__main__":
    play_game()

