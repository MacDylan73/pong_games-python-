# import turtle and random modules
import turtle as trtl
import random

# initializing variables and list for random starting direction
direction = [.05, -.05]
running = True
rscore = 0
lscore = 0

# creating the window
wn = trtl.Screen()
wn.title("Play Pong by Dylan Folscroft")
wn.bgcolor("Black")
wn.setup(width=1000, height=600)
wn.tracer(0)

# creating a title, instructions, and scoreboard
painter = trtl.Turtle()
painter.speed(0)
painter.hideturtle()
painter.color('White')
painter.penup()
painter.goto(-250, 275)
painter.pendown()
painter.write("Pong v1 by Dylan Folscroft - Control Paddles Using W, S, Up Arrow, And Down Arrow",
              font=('Roboto Mono', 10, 'normal'))
painter.penup()
painter.goto(-40, -275)
painter.pendown()
painter.write(str(lscore) + " - " + str(rscore), font=('Roboto Mono', 15, 'normal'))


# create left paddle
lpaddle = trtl.Turtle()
lpaddle.fillcolor('white')
lpaddle.speed(0)
lpaddle.penup()
lpaddle.shape('square')
lpaddle.shapesize(stretch_len=4)
lpaddle.tilt(90)
lpaddle.goto(-450, 0)

# create right paddle
rpaddle = trtl.Turtle()
rpaddle.fillcolor('white')
rpaddle.speed(0)
rpaddle.penup()
rpaddle.shape('square')
rpaddle.shapesize(stretch_len=4)
rpaddle.tilt(90)
rpaddle.goto(450, 0)

# create ball
ball = trtl.Turtle()
ball.fillcolor('white')
ball.speed(1)
ball.penup()
ball.shape('square')
ball.goto(0, 0)


# create functions to move paddles
def lup():
    y3 = lpaddle.ycor()
    if y3 < 260:
        y3 += 20
    lpaddle.goto(-450, y3)


def ldown():
    y3 = lpaddle.ycor()
    if y3 > -260:
        y3 -= 20
    lpaddle.goto(-450, y3)


def rup():
    y2 = rpaddle.ycor()
    if y2 < 260:
        y2 += 20
    rpaddle.goto(450, y2)


def rdown():
    y2 = rpaddle.ycor()
    if y2 > -260:
        y2 -= 20
    rpaddle.goto(450, y2)


# allow user input to move paddles
wn.listen()
wn.onkeypress(lup, 'w')
wn.onkeypress(ldown, 's')
wn.onkeypress(rup, 'Up')
wn.onkeypress(rdown, 'Down')

# choosing a random starting direction
vertical = random.choice(direction)
horizontal = random.choice(direction)

# game function: update window and allow gameplay
while running is True:
    wn.update()
    # creating ball movement, update score, changing difficulty, create bounce off of paddle and edges
    ball.setx(ball.xcor() + horizontal)
    ball.sety(ball.ycor() + vertical)

    if ball.ycor() <= -290:
        vertical *= -1
    elif ball.ycor() >= 290:
        vertical *= -1
    if ball.xcor() <= -500:
        ball.goto(0, 0)
        horizontal = .05
        rscore += 1
        painter.undo()
        painter.penup()
        painter.goto(-40, -275)
        painter.pendown()
        painter.write(str(lscore) + " - " + str(rscore), font=('Roboto Mono', 15, 'normal'))
    elif ball.xcor() >= 500:
        ball.goto(0, 0)
        horizontal = -.05
        lscore += 1
        painter.undo()
        painter.penup()
        painter.goto(-40, -275)
        painter.pendown()
        painter.write(str(lscore) + " - " + str(rscore), font=('Roboto Mono', 15, 'normal'))
    ball.setx(ball.xcor() + horizontal)
    ball.sety(ball.ycor() + vertical)

    # allow ball bounce off paddle
    if ball.xcor() >= 440:
        if (rpaddle.ycor() - 40) <= ball.ycor() <= (rpaddle.ycor() + 40):
            horizontal += .01
            horizontal *= -1
            horizontal = round(horizontal, 2)
    if ball.xcor() <= -440:
        if (lpaddle.ycor() - 40) <= ball.ycor() <= (lpaddle.ycor() + 40):
            horizontal -= .01
            horizontal *= -1
            horizontal = round(horizontal, 2)


# keep window open
wn.mainloop()
