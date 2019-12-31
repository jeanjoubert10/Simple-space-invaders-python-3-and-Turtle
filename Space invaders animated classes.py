# Space invaders Turtle type game J Joubert
# Relied quite a lot on the tutorial by Christian Thompson(Youtube)

# Sounds only for Mac OS using afplay
# Winsound for windows
#   import winsound
#   winsound.PlaySound('laser.WAV, winsound.SND_ASYNC')
# Linux use aplay

# Written on Mac, speed may require adjustment on Windows
# This code can be copied, changed, updated and if improved - please let me know how!

import turtle
import random
import os
#import time # and time.sleep(0.017) for windows


# Window setup
win = turtle.Screen()
win.bgcolor('black')
win.title('"Space Invaders" with Python 3 and Turtle')
win.setup(width=800, height=800)
win.tracer(0) # No animation until win.update() - try game without this

win.register_shape('ship1.gif')
win.register_shape('alien3.gif')
win.register_shape('alien4.gif')
win.listen()

class Border(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='square')

        self.hideturtle()
        self.speed(0)
        self.color('white')
        self.up() # Lift pen up 
        self.goto(-300,-300)
        self.down()
        self.pensize(5)
        for side in range(4):
            self.fd(600)
            self.lt(90)

class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='square')
        self.color('red')
        self.up()
        self.hideturtle()
        self.goto(220,-360)
        self.write('Score: 0', align='center', font=('Courier', 24, 'normal'))


class Title(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='square')
        self.up()
        self.color('yellow')
        self.hideturtle()
        self.goto(0, 330)
        self.write('Simple "Space Invaders" Python 3 Turtle', align='center',
          font=('Courier', 32, 'normal'))

class Player(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='ship1.gif')
        self.up()
        self.speed(0) # Max speed
        self.goto(0, -250)
        self.lt(90) # Face upward (turn left 90 degrees)

    def move_left(self):  # Only move left if you are right of the left border
        if self.xcor()>=-270:
            self.setx(player.xcor()-40)


    def move_right(self):
        if self.xcor()<= 270:
            self.setx(player.xcor()+40)


class Bullet(turtle.Turtle):
    def __init__(self, player, shield_list, enemy_list, pen):
        super().__init__(shape='square')

        self.color('red')
        self.speed(0)
        self.up()
        self.shape('square')
        self.shapesize(0.15, 0.6)  # Resize 15% width 60% height
        self.lt(90)
        self.goto(1000,1000) # Hide off screen
        self.state = 'ready'
        self.player = player
        self.shield_list = shield_list
        self.enemy_list = enemy_list
        self.pen = pen

    def shoot(self):
        if self.state == 'ready':
            os.system('afplay laser.WAV&')
            self.goto(player.xcor(), player.ycor()+10)    
            self.state = 'fire'

    def bullet_shield(self): # Did you hit the shield
        for i in self.shield_list:
            if self.distance(i)<=15: # Bullet is smaller 
                self.goto(1000,1000) # Hide off screen
                i.goto(1000,1000)
                shield_list.remove(i) # Remove shield block from list
                self.state = 'ready'

    
    def check_collision(self): # Did you hit the enemy
        global score
        for i in enemy_list: # Look at every enemy in the list
            if self.distance(i)<20: 
                self.goto(1000,1000)
                i.goto(1000,1000)
                enemy_list.remove(i)
                score += 1
                self.pen.clear()
                self.pen.write(f'Score: {score}', align='center', font=('Courier', 24, 'normal'))


class Torpedo(turtle.Turtle):
    def __init__(self, enemy_list, shield_list):
        super().__init__(shape='square')

        self.color('yellow')
        self.speed(0)
        self.up()
        self.shapesize(0.15, 0.6)
        self.lt(90)
        self.goto(1000,1000)
        self.state = 'ready' # Yes I should have used better name
        self.enemy_list = enemy_list

    def torpedo_fire(self): # enemy laser
        for i in self.enemy_list:
            x = random.random() # Create probability of firing torpedo only when laser == 'ready' 
            if x < 0.2 and self.state == 'ready':
                self.state = 'fire'
                self.goto(i.xcor(), i.ycor()-20)
                os.system('afplay missile.WAV&') # Add & to continue game while sound playing



    def torpedo_shield(self):
        for i in shield_list:
            if self.distance(i)<=15: # Torpedo is smaller, must be closer
                self.goto(1000,1000)
                self.state = 'ready'
                i.goto(1000,1000)
                shield_list.remove(i)
            

class Enemy(turtle.Turtle):
    def __init__(self, enemy_list):
        super().__init__(shape='square')
        self.s = 'alien3.gif'
        self.shape(self.s)
        self.up()
        self.speed(0)
        self.dx = 1 #speed
        self.enemy_list = enemy_list

    def move_enemy(self):
        for i in self.enemy_list:
            i.goto(i.xcor() + i.dx, i.ycor())
    
            if i.xcor()>=280 or i.xcor()<=-280: # If enemies reach the side
                for j in self.enemy_list: # Do this for every enemy in enemy list to keep in sync
                    j.dx *= -1  # Flip between positive and negative direction/speed
                    j.sety(j.ycor()-30)  # Down 30 pixels

    def animate_gif(self):
        for i in enemy_list:
            if i.s == 'alien3.gif':
                i.s = 'alien4.gif'
                i.shape(i.s)
            else:
                i.s = 'alien3.gif'
                i.shape(i.s)
        

enemy_list = []
enemy_speed = 1   # May need adjustment for windows eg 0.03

#start_position x coord -260 (left) and y 250 (top)
x_list = [-260, -210, -160, -110, -60, -10, 40, 90, 140]
y_list = [250, 200, 150, 100]

# Add enemies to the enemy_list by running through x list and adding at y coord on each step
for i in x_list:
    for j in y_list:
        enemy = Enemy(enemy_list)
        enemy.goto(i, j) # i is the xcor() and j the ycor() since we are running through both lists
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



# Creating instances of the classes:
player = Player()
pen = Pen()
border = Border()
title = Title()
bullet = Bullet(player, shield_list, enemy_list, pen)
torpedo = Torpedo(enemy_list, shield_list)


counter = 1 # I will use the counter to controll how quickly gif changes
score = 0
game_over = False


win.onkey(player.move_left, 'Left')
win.onkey(player.move_right, 'Right')
win.onkey(bullet.shoot, 'space')


while not game_over:
    #time.sleep(0.017) # windows?
    
    if counter % 20 == 0: # Based on the game speed I  will change gif every 20th loop
        enemy.animate_gif()
    counter += 1
    
    win.update()
    bullet.check_collision() # Did you hit the enemy with bullet
    torpedo.torpedo_fire() # Shoot at the player
    bullet.bullet_shield()
    torpedo.torpedo_shield()
    enemy.move_enemy()
        
    if bullet.state == 'fire':     # Every time you hit 'space bar'
        
        if bullet.ycor()<=260:
            bullet.sety(bullet.ycor()+20)
        else:
            bullet.goto(1000,1000) # Hide bullet off screen
            bullet.state = 'ready'

    if torpedo.state == 'fire':     # Random fire from the enemies
        if torpedo.ycor()>= -280:
            torpedo.sety(torpedo.ycor()-5)
        else:
            torpedo.goto(1000,1000)
            torpedo.state = 'ready'

    for i in enemy_list:
        if i.distance(player)<=20 or i.ycor() < player.ycor():
            os.system('afplay crash.WAV&')
            game_over = True

    if torpedo.distance(player)<= 20:
        win.update()
        os.system('afplay crash.WAV&')
        game_over = True

    if len(enemy_list) == 0:
        game_over = True
   
    
print('Gamer Over')
pen.clear()
pen.goto(0,0)
pen.write(f'Game Over\nScore: {score}', align='center',
          font=('Courier', 36, 'normal'))

        
    


        
