# Space invaders Turtle type game J Joubert
# Relied quite a lot on the tutorial by Christian Thompson(Youtube)
# Sounds only for Mac OS using afplay
# Winsound for windows
#   import winsound
#   winsound.PlaySound('laser.WAV, winsound.SND_ASYNC')
# Linux use aplay

# Written on Mac, speed may require adjustment on Windows
# This code can be copied, changed, updated and if improved - please let me know how!!

import turtle
import random
import os
#import time # and time.sleep(0.017) windows


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
        #self.write('Score: 0', align='center', font=('Courier', 24, 'normal'))


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
            self.setx(self.xcor()-40)


    def move_right(self):
        if self.xcor()<= 270:
            self.setx(self.xcor()+40)


class Bullet(turtle.Turtle):
    def __init__(self, player, shield_list):
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
    
        
    def shoot(self):
        if self.state == 'ready':
            self.goto(self.player.xcor(), self.player.ycor()+10)    
            self.state = 'fire'
            os.system('afplay laser.WAV&')


    def bullet_shield(self): # Did you hit the shield
        for i in self.shield_list:
            if self.distance(i)<=15: # Bullet is smaller 
                self.goto(1000,1000) # Hide off screen
                i.goto(1000,1000)
                self.shield_list.remove(i) # Remove shield block from list
                self.state = 'ready'


class Torpedo(turtle.Turtle):
    def __init__(self, enemy_list):
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
        for i in self.enemy_list:
            if i.s == 'alien3.gif':
                i.s = 'alien4.gif'
                i.shape(i.s)
            else:
                i.s = 'alien3.gif'
                i.shape(i.s)
        


class Game():
    def __init__(self):
        self.win = turtle.Screen()
        self.win.bgcolor('black')
        self.win.title('"Space Invaders" with Python 3 and Turtle')
        self.win.setup(width=800, height=800)
        self.win.tracer(0) # No animation until win.update() - try game without this

        self.win.register_shape('ship1.gif')
        self.win.register_shape('alien3.gif')
        self.win.register_shape('alien4.gif')
        self.win.listen()

        self.pen = Pen()

        
    def new_game(self):
        # Creating instances of the classes:
        self.shield_list = []
        self.shield_x = [-210, -190, -170, -150, -50, -30, -10, 10, 110, 130, 150, 170]
        self.shield_y = [-200, -220]

        self.enemy_list = []
        self.enemy_speed = 1   # May need adjustment for windows eg 0.03

        #start_position x coord -260 (left) and y 250 (top)
        self.x_list = [-260, -210, -160, -110, -60, -10, 40, 90, 140]
        self.y_list = [250, 200, 150, 100]

        self.counter = 1 # I will use the counter to controll how quickly gif changes
        self.score = 0

        self.pen.clear()
        
        self.player = Player()
        self.border = Border()
        self.title = Title()
        self.bullet = Bullet(self.player, self.shield_list)
        self.torpedo = Torpedo(self.enemy_list)
        
        self.pen.goto(220,-360)
        self.pen.write('Score: 0', align='center', font=('Courier', 24, 'normal'))
        

        # Add enemies to the enemy_list by running through x list and adding at y coord on each step
        for i in self.x_list:
            for j in self.y_list:
                self.enemy = Enemy(self.enemy_list)
                self.enemy.goto(i, j) # i is the xcor() and j the ycor() since we are running through both lists
                self.enemy_list.append(self.enemy) # Add each new enemy to the list
                

        # Add shields
        for i in self.shield_x:
            for j in self.shield_y:
                self.shield = turtle.Turtle()
                self.shield.color('yellow')
                self.shield.shape('square')
                self.shield.up()
                self.shield.goto(i, j)
                self.shield_list.append(self.shield)

        


        self.run()

    def run(self):
        self.playing = True

        while self.playing:
            self.events()
            self.update()

        

    def events(self):
        self.win.onkey(self.player.move_left, 'Left')
        self.win.onkey(self.player.move_right, 'Right')
        self.win.onkey(self.bullet.shoot, 'space')
        self.win.onkey(self.quit_game, 'q')


    def update(self):
        #time.sleep(0.017) # windows?
        
        if self.counter % 20 == 0: # Based on the game speed I  will change gif every 20th loop
            self.enemy.animate_gif()
            
        self.counter += 1
        self.win.update()
        self.torpedo.torpedo_fire() # Shoot at the player
        self.bullet.bullet_shield()
       
        self.enemy.move_enemy()

        
        for i in self.enemy_list: # Look at every enemy in the list
            if self.bullet.distance(i)<20: 
                self.bullet.goto(1000,1000)
                i.goto(1000,1000)
                self.enemy_list.remove(i)
                self.score += 1
                self.pen.clear()
                self.pen.write(f'Score: {self.score}', align='center', font=('Courier', 24, 'normal'))

        for i in self.shield_list:
            if self.torpedo.distance(i)<=15: # Torpedo is smaller, must be closer
                self.torpedo.goto(1000,1000)
                self.torpedo.state = 'ready'
                i.goto(1000,1000)
                self.shield_list.remove(i)

        
        
        if self.bullet.state == 'fire':     # Every time you hit 'space bar'
            
            if self.bullet.ycor()<=260:
                self.bullet.sety(self.bullet.ycor()+20)
            else:
                self.bullet.goto(1000,1000) # Hide bullet off screen
                self.bullet.state = 'ready'

        if self.torpedo.state == 'fire':     # Random fire from the enemies
            if self.torpedo.ycor()>= -280:
                self.torpedo.sety(self.torpedo.ycor()-5)
            else:
                self.torpedo.goto(1000,1000)
                self.torpedo.state = 'ready'

        for i in self.enemy_list:
            if i.distance(self.player)<=20 or i.ycor() < self.player.ycor():
                os.system('afplay crash.WAV&')
                self.playing = False

        if self.torpedo.distance(self.player)<= 20:
            self.win.update()
            os.system('afplay crash.WAV&')
            self.playing = False

        if len(self.enemy_list) == 0:
            self.playing = False


    def show_start_screen(self):
        self.waiting = True
        self.pen.goto(0, 0)
        self.win.onkey(self.wait_for_keypress, 'space')
        
        while self.waiting:
            self.win.bgcolor('black')
            self.pen.write('Simple Space invaders using Python 3 and Turtle\n\n\tPress the "space" key to continue',
                      align='center', font=('Courier', 24, 'normal'))

    
    def show_game_over_screen(self):
        # Remove all objects
        self.player.goto(1000,1000)
        self.bullet.goto(1000,1000)
        self.torpedo.goto(1000,1000)
        
        for i in self.enemy_list:
            i.goto(1000,1000)

        for i in self.shield_list:
            i.goto(1000,1000)

        self.win.update()
        self.waiting = True
        self.pen.goto(0, 0)
        self.win.onkey(self.wait_for_keypress, 'space')
        
        while self.waiting:
            self.win.bgcolor('black')
            self.pen.write(f'\t   Score: {self.score} \n\nPress the "space" key for new game',
                      align='center', font=('Courier', 24, 'normal'))

    

    def wait_for_keypress(self):
        self.waiting = False

    def quit_game(self):
        self.playing = False




game = Game()
game.show_start_screen()

        

while True:
    game.new_game()
    game.show_game_over_screen()

   
    
print('Gamer Over')
pen.clear()
pen.goto(0,0)
pen.write(f'Game Over\nScore: {score}', align='center',
          font=('Courier', 36, 'normal'))

        
    


        
