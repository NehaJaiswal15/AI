import tkinter as tk

SIZE = 3
PLAYER_X = "X"   
PLAYER_O = "O"  

board = [[None]*SIZE for _ in range(SIZE)]

def check_winner():
    lines = []
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(SIZE)] for c in range(SIZE)])
    lines.append([board[i][i] for i in range(SIZE)])
    lines.append([board[i][SIZE-1-i] for i in range(SIZE)])

    for line in lines:
        if line[0] and all(cell == line[0] for cell in line):
            return line[0]
    return None

def is_full():
    return all(all(cell for cell in row) for row in board)

def minimax(is_ai):
    winner = check_winner()
    if winner == PLAYER_O:
        return 1
    if winner == PLAYER_X:
        return -1
    if is_full():
        return 0

    if is_ai:
        best = -100
        for r in range(SIZE):
            for c in range(SIZE):
                if not board[r][c]:
                    board[r][c] = PLAYER_O
                    best = max(best, minimax(False))
                    board[r][c] = None
        return best
    else:
        best = 100
        for r in range(SIZE):
            for c in range(SIZE):
                if not board[r][c]:
                    board[r][c] = PLAYER_X
                    best = min(best, minimax(True))
                    board[r][c] = None
        return best

def best_move():
    best_score = -100
    move = None
    for r in range(SIZE):
        for c in range(SIZE):
            if not board[r][c]:
                board[r][c] = PLAYER_O
                score = minimax(False)
                board[r][c] = None
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

def on_click(r, c):
    if board[r][c] or check_winner():
        return

    board[r][c] = PLAYER_X
    buttons[r][c].config(text=PLAYER_X)

    if check_winner() or is_full():
        status.config(text="X wins!" if check_winner() else "Draw")
        return

    ai_r, ai_c = best_move()
    board[ai_r][ai_c] = PLAYER_O
    buttons[ai_r][ai_c].config(text=PLAYER_O)

    winner = check_winner()
    if winner:
        status.config(text=f"{winner} wins!")
    elif is_full():
        status.config(text="Draw")

root = tk.Tk()
root.title("Tic Tac Toe - Minimax")

buttons = []
for r in range(SIZE):
    row = []
    for c in range(SIZE):
        btn = tk.Button(
            root, text="", font=("Arial", 32),
            width=3, height=1,
            command=lambda r=r, c=c: on_click(r, c)
        )
        btn.grid(row=r, column=c)
        row.append(btn)
    buttons.append(row)

status = tk.Label(root, text="You are X", font=("Arial", 14))
status.grid(row=SIZE, column=0, columnspan=SIZE)

root.mainloop()