import tkinter as tk
from tkinter import messagebox
import random

# Initialize the game board
board = [" " for _ in range(9)]
current_player = "X"
game_over = False
computer_player = "O"

# Create a function to check for a win
def check_win(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

# Create a function to check if the board is full
def is_board_full(board):
    return " " not in board

# Minimax function for the computer player with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win(board, computer_player):
        return 1
    elif check_win(board, "X"):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = computer_player
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = " "
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score

# Computer's move using Minimax with Alpha-Beta Pruning
def computer_move():
    best_move = None
    best_score = -float("inf")
    alpha = -float("inf")
    beta = float("inf")
    for i in range(9):
        if board[i] == " ":
            board[i] = computer_player
            score = minimax(board, 0, False, alpha, beta)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
            alpha = max(alpha, score)
    make_move(best_move)

# Create a function to handle player moves
def make_move(index):
    global current_player, game_over, computer_player
    if board[index] == " " and not game_over:
        board[index] = current_player
        buttons[index].config(text=current_player)
        if check_win(board, current_player):
            if current_player == computer_player:
                messagebox.showinfo("Tic-Tac-Toe", "Computer wins!")
            else:
                messagebox.showinfo("Tic-Tac-Toe", f"Player {current_player} wins!")
            game_over = True
        elif is_board_full(board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            game_over = True
        else:
            current_player = "O" if current_player == "X" else "X"
            if current_player == computer_player:
                computer_move()

# Reset the game
def reset_game():
    global board, current_player, game_over
    board = [" " for _ in range(9)]
    game_over = False
    # Update the current player based on the selected game mode
    current_player = "X" if computer_player != "X" else "O"
    for button in buttons:
        button.config(text=" ")
    if computer_player == "O" and current_player == "O":
        computer_move()


# Create the main GUI window
window = tk.Tk()
window.title("Tic-Tac-Toe")

# Create buttons for the game
buttons = []
for i in range(9):
    row = i // 3
    col = i % 3
    button = tk.Button(window, text=" ", font=("normal", 20), width=5, height=2,
                       command=lambda i=i: make_move(i))
    button.grid(row=row, column=col)
    buttons.append(button)

# Create a menu to select the game mode
def select_mode(mode):
    global computer_player
    if mode == "1 Player":
        computer_player = "O"
        reset_game()
    else:
        computer_player = None

mode_menu = tk.Menu(window)
window.config(menu=mode_menu)
mode_menu.add_command(label="1 Player", command=lambda: select_mode("1 Player"))
mode_menu.add_command(label="2 Players", command=lambda: select_mode("2 Players"))

# Create a reset button
reset_button = tk.Button(window, text="Reset", font=("normal", 16), width=10, height=2, command=reset_game)
reset_button.grid(row=3, column=1)

# Run the GUI main loop
window.mainloop()
