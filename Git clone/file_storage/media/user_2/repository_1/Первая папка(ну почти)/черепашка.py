import turtle

win = turtle.Screen()
win.title("Turtle")
win.setup(width=1.0,height=1.0)

t = turtle.Turtle()


def t_up():
    t.setheading(90)

def t_down():
    t.setheading(270)

def t_left():
    t.setheading(180)

def t_right():
    t.setheading(360)


def t_pen_up():
    t.up()

def t_pen_down():
    t.down()

def spase():
    t.forward(5)

win.listen()
win.onkeypress(t_up,"Up")
win.onkeypress(t_down,"Down")
win.onkeypress(t_left,"Left")
win.onkeypress(t_right,"Right")
win.onkeypress(t_pen_up,"a")
win.onkeypress(t_pen_down,"s")
win.onkeypress(spase,"space")


win.mainloop()