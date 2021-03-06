import turtle
import os
import math
import random

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")

#Refister the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")
turtle.register_shape("bullet2.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Set the score to 0
score = 0
#Draw Score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.penup()
player.color("blue")
player.shape("player.gif")
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 20
# Choose the number of enemies
number_of_enemies = 5
#Create an empty list of enemies
enemies = []
#Add enemies to the list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())
# Draw the enemies
for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x=random.randint(-200,200)
    y=random.randint(100,250)
    enemy.setposition(x, y)
enemyspeed = 10

# Create the player's bullet
bullet = turtle.Turtle()
bullet.penup()
bullet.color("yellow")
bullet.shape("bullet2.gif")
#bullet.shape("triangle")

bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 25

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"
finish_status = False

# Move the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = - 280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def finish():
    global finish_status
    finish_status = True
    # Draw END
    the_end = turtle.Turtle()
    the_end.speed(0)
    the_end.color("white")
    the_end.penup()
    the_end.setposition(-250, 0)
    scorestring = "GAME OVER" 
    the_end.write(scorestring, False, align="left", font=("Tahoma", 70, "normal"))
    the_end.hideturtle()

    the_reset = turtle.Turtle()
    the_reset.speed(0)
    the_reset.color("white")
    the_reset.penup()
    the_reset.setposition(-100, -30)
    resetstring = "To restart game press 'r' "
    the_reset.write(resetstring, False, align="left", font=("Tahoma", 15, "normal"))
    the_reset.hideturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 25:
        return True
    else:
        return False

def restart_game():

    if finish_status == True:
        wn.resetscreen ()
        for enemy in enemies:
            enemy.reset()
            enemy.penup()
            enemy.speed(0)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
        #time.sleep(1)
        player.reset()
        player.penup()
        player.color("blue")
        player.shape("player.gif")
        player.speed(0)
        player.setposition(0, -250)
        player.setheading(90)
        bullet.reset()
        bullet.penup()
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

# Create keyboard bindings
turtle.listen()


turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")
turtle.onkey(restart_game, "r")

# Main game loop
while True:

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        #If enemy reaches the bottom line, player loses
        if enemy.ycor() < -260:
            player.hideturtle()
            enemy.hideturtle()
            bullet.hideturtle()
            finish()
            # restart_game(finish_status)
            break

        # Move the enemy until it touches the wall then down
        if enemy.xcor() > 280:
            # Moves all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Changes direction
            enemyspeed *= -1

        if enemy.xcor() < -280:
        #Moves all enemies down
           for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
        # changes direction
           enemyspeed *= -1

        # Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            #Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            # Update the score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))


        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            bullet.hideturtle()
            finish_status = True
            finish()
            # restart_game(finish_status)

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"


wn.mainloop()
