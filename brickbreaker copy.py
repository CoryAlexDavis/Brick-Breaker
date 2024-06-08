"""
File: brickbreaker.py
----------------
YOUR DESCRIPTION HERE
"""

import tkinter
import time
import random

# How big is the playing area?
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 800     # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 8              # How many rows of bricks are there?
N_COLS = 10             # How many columns of bricks are there?
SPACING = 5             # How much space is there between each brick?
BRICK_START_Y = 50      # The y coordinate of the top-most brick
BRICK_HEIGHT = 20       # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS+1) * SPACING ) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 80
PADDLE_SIZE = 30

def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    #create a function for the bricks at the top of the canvas
    # this draws 8 rows of bricks
    brick_group(canvas)

    #function to place the ball in the middle of the canvas
    ball = make_ball(canvas)
    paddle = make_paddle(canvas)
    bounce_ball(ball, canvas, paddle)
    #function to make the ball bounce around the screen
    #function to make the curser move to bounce the ball
    canvas.mainloop()

def brick_group(canvas):
    for row in range(N_ROWS):
        # this draws one row of bricks
        for brick in range(N_COLS):
            draw_bricks(canvas, row, brick)

def draw_bricks(canvas, row, brick):
    x = brick * (BRICK_WIDTH + SPACING)
    y = row * (BRICK_HEIGHT + SPACING)
    color = get_color(row, brick)
    brick = canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, fill=color)
    return brick

def get_color(row, brick):
    if (row + brick) % 2 == 0:
        return 'green'
    else:
        return 'red'

def make_paddle(canvas):
    #start_y = PADDLE_Y
    #end_y = start_y - PADDLE_WIDTH
    #start_x = (CANVAS_WIDTH / 2) - PADDLE_SIZE /2
    #end_x = start_x + PADDLE_SIZE
    paddle = canvas.create_rectangle(0, PADDLE_Y, PADDLE_WIDTH, CANVAS_HEIGHT -20, fill='black', outline='orange')
    return paddle

def make_ball(canvas):
    start_y = CANVAS_HEIGHT / 2 - BALL_SIZE / 2
    end_y = start_y + BALL_SIZE
    start_x = CANVAS_WIDTH / 2 - BALL_SIZE / 2
    end_x = start_x + BALL_SIZE
    ball = canvas.create_oval(start_x, start_y, end_x, end_y, fill='red', outline='green')
    return ball

def bounce_ball(ball, canvas, paddle):
    dx = 5
    dy = 5
    while True:
        mouse_x = canvas.winfo_pointerx()
        canvas.moveto(paddle, mouse_x, PADDLE_Y)
        canvas.move(ball, dx, dy)
        if hit_paddle(canvas, ball, paddle):
            dy *= -1
        #if ball y coordinate is  >= canvas height or <= 0 invert dy
        elif hit_left_wall(canvas, ball) or hit_right_wall(canvas, ball):
            dx *= -1
        #if x coordinate is not >0 and  <= canvas width invert dx
        elif hit_top_wall(canvas, ball) or hit_bottom_wall(canvas, ball):
            dy *= -1
        elif hit_brick(canvas, ball):
            dy *= -1

        canvas.update()
        time.sleep(1/50)

def hit_brick(canvas, ball):
    brick_cords = canvas.coords(ball)
    x1 = brick_cords[0]
    y1 = brick_cords[1]
    x2 = brick_cords[2]
    y2 = brick_cords[3]
    results = canvas.find_overlapping(x1, y1, x2, y2)
    if len(results) > 1:
        canvas.delete(results[0])
    return len(results) > 1

def hit_paddle(canvas, object, paddle):
    paddle_cords = canvas.coords(paddle)
    x1 = paddle_cords[0]
    y1 = paddle_cords[1]
    x2 = paddle_cords[2]
    y2 = paddle_cords[3]
    results = canvas.find_overlapping(x1, y1, x2, y2)
    return len(results) > 1

def hit_bottom_wall(canvas, object):
    return get_bottom_y(canvas, object) >= CANVAS_HEIGHT
def hit_right_wall(canvas, object):
    return get_right_x(canvas, object) >= CANVAS_WIDTH
def hit_top_wall(canvas, obeject):
    return get_top_y(canvas, obeject) <= 0
def hit_left_wall(canvas, object):
    return get_left_x(canvas, object) <= 0
def get_bottom_y(canvas, object):
    return canvas.coords(object)[3]

def get_right_x(canvas, object):
    return canvas.coords(object)[2]

def get_top_y(canvas, object):
    '''
    This friendly method returns the y coordinate of the top of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(object)[1]

def get_left_x(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[0]

def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas

if __name__ == '__main__':
    main()
