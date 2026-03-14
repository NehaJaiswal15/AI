import tkinter as tk
import random

ROWS = 10
COLS = 10
CELL = 60
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

COLORS = [
    "#F6E58D", "#DFF9FB", "#FFBE76", "#F9CAE1",
    "#BAD7E9", "#E8F8F5"
]

BG = "#F5F5F5"
TEXT = "#222222"
SNAKE_COLOR = "#2E8B57"
LADDER_COLOR = "#2F3640"
PLAYER_COLOR = "#2980B9"

root = tk.Tk()
root.title("Snakes and Ladders")
root.configure(bg=BG)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG,
    highlightthickness=0
)
canvas.pack(pady=10)

cells = {}

def draw_board():
    num = 1
    reverse = False

    for r in range(ROWS-1, -1, -1):
        cols = range(COLS-1, -1, -1) if reverse else range(COLS)
        for c in cols:
            x1, y1 = c * CELL, r * CELL
            x2, y2 = x1 + CELL, y1 + CELL

            color = COLORS[(num-1) % len(COLORS)]

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#DDDDDD"
            )

            canvas.create_text(
                x1 + 5, y2 - 5,
                text=str(num),
                anchor="sw",
                font=("Arial", 10),
                fill=TEXT
            )

            cells[num] = ((x1 + x2)//2, (y1 + y2)//2)
            num += 1

        reverse = not reverse

draw_board()

snakes = {
    99: 78,
    95: 56,
    92: 73,
    87: 24,
    64: 60,
    62: 19,
    54: 34,
    49: 11
}

ladders = {
    4: 25,
    13: 46,
    27: 53,
    33: 49,
    42: 63,
    50: 69,
    62: 81,
    74: 92
}

import math

def draw_snake(start, end):
    x1, y1 = cells[start]
    x2, y2 = cells[end]

    segments = 22
    amplitude = 18  
    body_radius = 10

    dx = (x2 - x1) / segments
    dy = (y2 - y1) / segments

    angle = math.atan2(y2 - y1, x2 - x1)

    for i in range(segments):
        t = i / segments

        radius = body_radius * (0.4 + 0.6 * (1 - t))

        offset = math.sin(t * math.pi * 4) * amplitude

        ox = offset * math.cos(angle + math.pi/2)
        oy = offset * math.sin(angle + math.pi/2)

        cx = x1 + dx * i + ox
        cy = y1 + dy * i + oy

        canvas.create_oval(
            cx-radius, cy-radius,
            cx+radius, cy+radius,
            fill="#2E8B57",
            outline=""
        )

    head_radius = body_radius * 1.2
    canvas.create_oval(
        x1-head_radius, y1-head_radius,
        x1+head_radius, y1+head_radius,
        fill="#2E8B57",
        outline=""
    )

    eye_offset = 4
    canvas.create_oval(
        x1-eye_offset-2, y1-eye_offset-2,
        x1-eye_offset+2, y1-eye_offset+2,
        fill="white"
    )
    canvas.create_oval(
        x1+eye_offset-2, y1-eye_offset-2,
        x1+eye_offset+2, y1-eye_offset+2,
        fill="white"
    )


def draw_ladder(start, end):
    x1,y1 = cells[start]
    x2,y2 = cells[end]
    offset = 8

    canvas.create_line(x1-offset,y1, x2-offset,y2, width=4, fill=LADDER_COLOR)
    canvas.create_line(x1+offset,y1, x2+offset,y2, width=4, fill=LADDER_COLOR)

    for i in range(6):
        t = i / 5
        xr = (1-t)*x1 + t*x2
        yr = (1-t)*y1 + t*y2
        canvas.create_line(
            xr-offset, yr, xr+offset, yr,
            width=3, fill=LADDER_COLOR
        )

for s,e in snakes.items():
    draw_snake(s,e)

for s,e in ladders.items():
    draw_ladder(s,e)

player_pos = 1
moves = 0

px, py = cells[player_pos]
player = canvas.create_oval(
    px-10, py-10, px+10, py+10,
    fill=PLAYER_COLOR,
    outline=""
)

def move_player(pos):
    x,y = cells[pos]
    canvas.coords(player, x-10, y-10, x+10, y+10)

panel = tk.Frame(root, bg=BG)
panel.pack(pady=10)

dice_label = tk.Label(panel, text="🎲 0", font=("Arial",14), bg=BG)
dice_label.grid(row=0, column=0, padx=15)

move_label = tk.Label(panel, text="Moves: 0", font=("Arial",14), bg=BG)
move_label.grid(row=0, column=1, padx=15)

status_label = tk.Label(panel, text="", font=("Arial",12), bg=BG)
status_label.grid(row=1, column=0, columnspan=3)

def roll_dice():
    global player_pos, moves
    dice = random.randint(1,6)
    dice_label.config(text=f"🎲 {dice}")

    if player_pos + dice <= 100:
        player_pos += dice

        if player_pos in snakes:
            player_pos = snakes[player_pos]
            status_label.config(text="🐍 Snake bite!")
        elif player_pos in ladders:
            player_pos = ladders[player_pos]
            status_label.config(text="🪜 Ladder climb!")
        else:
            status_label.config(text="")

        move_player(player_pos)

    moves += 1
    move_label.config(text=f"Moves: {moves}")

    if player_pos == 100:
        status_label.config(text="🎉 You Win!")

roll_btn = tk.Button(
    root,
    text="Roll Dice",
    font=("Arial",12),
    command=roll_dice,
    bg="#FFFFFF",
    relief="solid"
)
roll_btn.pack(pady=5)

root.mainloop()
