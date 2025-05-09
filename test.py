import turtle

t1 = turtle.Turtle()
t2 = turtle.Turtle()

t1.goto(30, 30)
t2.goto(30, 30)

x1,y1=t1.pos()
x2,y2=t2.pos()

print(x1-x2, y2-y1)

turtle.done()

