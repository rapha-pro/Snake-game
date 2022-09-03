from tkinter import *
import random

GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 260
SPACE_SIZE = 30
BODY_PARTS = 2
SNAKE_COLOR = "#0F0"
FOOD_COLOR = "#F00"
BACKGROUND_COLOR = "#000"
TEXT_COLOR = "#FFA500"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        print("passed here")
        # turn = 0
        for x_cor, y_cor in self.coordinates:
            square = canvas.create_rectangle(x_cor, y_cor, x_cor + SPACE_SIZE, y_cor + SPACE_SIZE, fill=SNAKE_COLOR)

            self.squares.append(square)
            # turn += 1


class Food:
    def __init__(self):

        self.x = random.randint(1, int((GAME_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
        self.y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE

        while [self.x, self.y] in snake.coordinates:
            self.x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
            self.y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE


        self.coordinates = [self.x, self.y]

        canvas.create_oval(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def next_turn(snakeObj, foodObj):
    x_cor, y_cor = snakeObj.coordinates[0]

    if direction == "up":
        y_cor -= SPACE_SIZE

    elif direction == "down":
        y_cor += SPACE_SIZE

    elif direction == "left":
        x_cor -= SPACE_SIZE

    elif direction == "right":
        x_cor += SPACE_SIZE

    snakeObj.coordinates.insert(0, [x_cor, y_cor])

    square = canvas.create_rectangle(x_cor, y_cor, x_cor + SPACE_SIZE, y_cor + SPACE_SIZE, fill=SNAKE_COLOR,
                                     tags="snake")

    snakeObj.squares.insert(0, square)

    if x_cor == foodObj.coordinates[0] and y_cor == foodObj.coordinates[1]:

        global score, high_score

        print(score)

        score += 1

        if score > int(high_score):
            with open('Highscore.txt', 'w') as var:
                var.write(str(score))

        label.config(text="Score: {}".format(score))

        canvas.delete("food")

        foodObj = Food()

    else:
        # before appending new square, delete last one
        del snakeObj.coordinates[-1]
        canvas.delete(snakeObj.squares[-1])
        del snakeObj.squares[-1]


    if check_collisions(snakeObj):
        game_over()
    else:
        window.after(SPEED, next_turn, snakeObj, foodObj)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snakeobj):
    x_cor, y_cor = snakeobj.coordinates[0]

    if x_cor < 0 or x_cor >= GAME_WIDTH:
        print("GAME OVER")
        return True

    if y_cor < 0 or y_cor >= GAME_HEIGHT:
        print("GAME OVER")
        return True

    for body_part in snakeobj.coordinates[1:]:
        if x_cor == body_part[0] and y_cor == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete('all')
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tags="gameover")

window = Tk()
window.title("Snake game by Raphael")
window.resizable(False, False)
window.config(bg='black')

score = 0

with open('Highscore.txt', 'r') as outfile:
    data = outfile.read()
    high_score = data

direction = 'right'

space = Label(window, fg=TEXT_COLOR, text="", bg=BACKGROUND_COLOR)
space.pack(pady=8)

label = Label(window, fg=TEXT_COLOR, text="Score: {}".format(score), font=('calibri', 20), bg=BACKGROUND_COLOR)
label.place(x=10, y=0)

label2 = Label(window, fg=TEXT_COLOR, text="Highest Score: {}".format(high_score), font=('calibri', 20), bg=BACKGROUND_COLOR)
label2.place(x=400, y=0)

canvas = Canvas(window, highlightthickness=1, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


window.update()

# Center window each time it's launched
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y-40}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

print("hey")
next_turn(snake, food)

window.mainloop()
