# import modules and library
from tkinter import *
import time
import random


class Ball:  # class for ball's actions
    def __init__(self, canvas, paddle, score, color):  # initialisation
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)

        starts = [-2, -1, 1, 2]  # possible start coord
        random.shuffle(starts)

        self.x = random.choice(starts)
        self.y = -2
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):  # platform touch processing
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                self.score.hit()
                return True
        return False

    def draw(self):  # method for ball movement
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 2
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 120, text='You lose', font=('Courier', 30), fill='red')
        if self.hit_paddle(pos):
            self.y = -2
        if pos[0] <= 0:
            self.x = 2
        if pos[2] >= self.canvas_width:
            self.x = -2


class Paddle:  # class for paddle's actions
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(start_1)
        self.starting_point_x = start_1[0]
        self.canvas.move(self.id, self.starting_point_x, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)  # right key press handler
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)  # left key press handler
        self.started = False
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)  # Enter key press handler

    def start_game(self, event):  # method for Enter
        self.started = True

    def turn_right(self, event):  # method for Right Key
        self.x = 2

    def turn_left(self, event):  # method for Left Key
        self.x = -2

    def draw(self):  # paddle movement
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0


class Score:  # counter class
    def __init__(self, canvas, color):  # initialisation
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(480, 17, text=self.score, font=('Courier', 20), fill=color)

    def hit(self):  # platform touch handler
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)


tk = Tk()  # new window for game
tk.title('The Ball Game')  # window's title
tk.resizable(0, 0)  # no resize
tk.wm_attributes('-topmost', 1)

canvas = Canvas(tk, width=500, height=400, highlightthickness=0, bg='grey')  # new canvas for game's objects
canvas.pack()

tk.update()

score = Score(canvas, 'red')
paddle = Paddle(canvas, 'Black')
ball = Ball(canvas, paddle, score, 'purple')
while not ball.hit_bottom:
    if paddle.started:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.0001)
time.sleep(5)
