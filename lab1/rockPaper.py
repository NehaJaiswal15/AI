import tkinter as tk
import random

root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("300x300")

choices = ["Rock", "Paper", "Scissors"]

result_label = tk.Label(root, text="Choose an option!", font=("Arial", 16))
result_label.pack(pady=20)

def play(player_choice):
    comp_choice = random.choice(choices)
    if player_choice == comp_choice:
        result = "Draw!"
    elif (player_choice=="Rock" and comp_choice=="Scissors") or \
         (player_choice=="Paper" and comp_choice=="Rock") or \
         (player_choice=="Scissors" and comp_choice=="Paper"):
        result = "You Win!"
    else:
        result = "You Lose!"

    result_label.config(text=f"You: {player_choice}\nCPU: {comp_choice}\n{result}")

# Buttons
for c in choices:
    tk.Button(root, text=c, width=10, font=("Arial", 14),
              command=lambda x=c: play(x)).pack(pady=5)

root.mainloop()

