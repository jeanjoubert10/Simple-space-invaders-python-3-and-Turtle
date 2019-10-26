# Space invaders Turtle type game J Joubert
# Sounds only for Mac OS using afplay
# Winsound for windows
#   import winsound
#   winsound.PlaySound('laser.WAV, winsound.SND_ASYNC')
# Linux use aplay

# Written on Mac, speed may require adjustment on Windows

import turtle
import random
import os


# Window setup
win = turtle.Screen()
win.bgcolor('black')
win.title('"Space Invaders" with Python 3 and Turtle')
win.setup(width=800, height=800)
win.tracer(0) # No animation until win.update() - try game without this

win.register_shape('ship1.gif')
win.register_shape('alien3.gif')
win.register_shape('alien4.gif')

# Draw border
border = turtle.Turtle()
border.hideturtle()
border.speed(0)
border.color('white')
border.up() # Lift pen up 
border.goto(-300,-300)
border.down()
border.pensize(5)
for side in range(4):
    border.fd(600)
    border.lt(90)

# Create pen for score
pen = turtle.Turtle()
pen.color('red')
pen.up()
pen.hideturtle()
pen.goto(220,-360)
pen.write('Score: 0', align='center', font=('Courier', 24, 'normal'))

# Create pen to write the title on top
pen_title = turtle.Turtle()
pen_title.up()
pen_title.color('yellow')
pen_title.hideturtle()
pen_title.goto(0, 330)
pen_title.write('Simple "Space Invaders" Python 3 Turtle', align='center',
          font=('Courier', 32, 'normal'))

# Create player
player = turtle.Turtle()
player.shape('ship1.gif')
player.up()
player.speed(0) # Max speed
player.goto(0, -250)
player.lt(90) # Face upward (turn left 90 degrees)
score = 0

# Create bullet shot from player ship
bullet = turtle.Turtle()
bullet.color('red')
bullet.speed(0)
bullet.up()
bullet.shape('square')
bullet.shapesize(0.15, 0.6)  # Resize 15% width 60% height
bullet.lt(90)
bullet.goto(1000,1000) # Hide off screen

# Create torpedo dropped from random enemy ship
torpedo = turtle.Turtle()
torpedo.color('yellow')
torpedo.speed(0)
torpedo.up()
torpedo.shape('square')
torpedo.shapesize(0.15, 0.6)
torpedo.lt(90)
torpedo.goto(1000,1000)
laser = 'ready' # Yes I should have used better name

enemy_list = []
enemy_speed = 1   # May need adjustment for windows eg 0.03

#start_position x coord -260 (left) and y 250 (top)
x_list = [-260, -210, -160, -110, -60, -10, 40, 90, 140]
y_list = [250, 200, 150, 100]

# Add enemies to the enemy_list by running through x list and adding at y coord on each step
for i in x_list:
    for j in y_list:
        enemy = turtle.Turtle()
        enemy.color('red')
        enemy.s = 'alien3.gif'
        enemy.shape(enemy.s)
        enemy.up()
        enemy.speed(0)
        enemy.goto(i, j) # i is the xcor() and j the ycor() since we are running through both lists
        enemy.dx = enemy_speed
        enemy_list.append(enemy) # Add each new enemy to the list

# Add shields
shield_list = []
shield_x = [-210, -190, -170, -150, -50, -30, -10, 10, 110, 130, 150, 170]
shield_y = [-200, -220]

for i in shield_x:
    for j in shield_y:
        shield = turtle.Turtle()
        shield.color('yellow')
        shield.shape('square')
        shield.up()
        shield.goto(i, j)
        shield_list.append(shield)

def move_left():  # Only move left if you are right of the left border
    if player.xcor()>=-270:
        player.setx(player.xcor()-40)


def move_right():
    if player.xcor()<= 270:
        player.setx(player.xcor()+40)

def move_enemy():
    for i in enemy_list:
        i.goto(i.xcor() + i.dx, i.ycor())
    
        if i.xcor()>=280 or i.xcor()<=-280: # If enemies reach the side
            for j in enemy_list: # Do this for every enemy in enemy list to keep in sync
                j.dx *= -1  # Flip between positive and negative direction/speed
                j.sety(j.ycor()-30)  # Down 30 pixels

def shoot():
    global shoot # shoot is not a local variable in the function only
    bullet.goto(player.xcor(), player.ycor()+10)    
    shoot = 'fire'


def enemy_laser():
    global laser
    for i in enemy_list:
        x = random.random() # Create probability of firing torpedo only when laser == 'ready' 
        if x < 0.2 and laser == 'ready':
            laser = 'fire'
            torpedo.goto(i.xcor(), i.ycor()-20)
            os.system('afplay missile.WAV&') # Add & to continue game while sound playing

# Turtle object 20x20pixels
def check_collision(): # Did you hit the enemy
    global score
    for i in enemy_list: # Look at every enemy in the list
        if bullet.distance(i)<20: 
            bullet.goto(1000,1000)
            i.goto(1000,1000)
            enemy_list.remove(i)
            score += 1
            pen.clear()
            pen.write(f'Score: {score}', align='center', font=('Courier', 24, 'normal'))


def bullet_shield(): # Did you hit the shield
    for i in shield_list:
        if bullet.distance(i)<=15: # Bullet is smaller 
            bullet.goto(1000,1000) # Hide off screen
            i.goto(1000,1000)
            shield_list.remove(i) # Remove shield block from list
            shoot = 'ready'

def torpedo_shield():
    for i in shield_list:
        if torpedo.distance(i)<=15: # Torpedo is smaller, must be closer
            torpedo.goto(1000,1000)
            laser = 'ready'
            i.goto(1000,1000)
            shield_list.remove(i)


win.listen()
win.onkey(move_left, 'Left')
win.onkey(move_right, 'Right')
win.onkey(shoot, 'space')

game_over = False

def animate_gif():
    for i in enemy_list:
        if i.s == 'alien3.gif':
            i.s = 'alien4.gif'
            i.shape(i.s)
        else:
            i.s = 'alien3.gif'
            i.shape(i.s)
    


counter = 1 # I will use the counter to controll how quickly gif changes

while not game_over:
    
    if counter % 20 == 0: # Based on the game speed I  will change gif every 20th loop
        animate_gif()
    counter += 1
    
    win.update()
    check_collision() # Did you hit the enemy with bullet
    move_enemy() # Move the enemies in a group left and right and down
    enemy_laser() # Shoot at the player
    bullet_shield()
    torpedo_shield()
        
    if shoot == 'fire':     # Every time you hit 'space bar'
        os.system('afplay laser.WAV&')
        if bullet.ycor()<=260:
            bullet.sety(bullet.ycor()+20)
        else:
            bullet.goto(1000,1000) # Hide bullet off screen
            shoot = 'ready'

    if laser == 'fire':     # Random fire from the enemies
        if torpedo.ycor()>= -280:
            torpedo.sety(torpedo.ycor()-5)
        else:
            torpedo.goto(1000,1000)
            laser = 'ready'

    for i in enemy_list:
        if i.distance(player)<=20 or i.ycor() < player.ycor():
            os.system('afplay crash.WAV&')
            game_over = True

    if torpedo.distance(player)<= 20:
        os.system('afplay crash.WAV&')
        game_over = True

    if len(enemy_list) == 0:
        game_over = True
   
    
print('Gamer Over')
pen.clear()
pen.goto(0,0)
pen.write(f'Game Over\nScore: {score}', align='center',
          font=('Courier', 36, 'normal'))
        
    


        
