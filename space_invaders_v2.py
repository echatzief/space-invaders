import turtle
import random
import os
import math

class SpaceInvaders:
    
    def __init__(self):
        self.score = 100 #2: We should start with 100 as initial score
        self.playerspeed = 15
        self.number_of_enemies = 4 #1 Initial number of enemies to be 4
        self.enemiesList = []
        self.enemiesSpeedList = []
        self.bulletspeed = 20
        self.bulletstate = "ready"
        self.score_pen = None

    def run(self):
        self.setup()
        self.loop()

    def loop(self):
        while True:
            
            #7 If no enemies exist then terminate the game and show winning message
            if len(self.enemiesList) == 0:
                print("YOU WON")
                break
            
            for enemy in self.enemiesList:
                
                idx = self.enemiesList.index(enemy)
 
                x = enemy.xcor()
                x = x + self.enemiesSpeedList[idx]
                enemy.setx(x)

                #Move enemy back and down
                if enemy.xcor() > 280:
                    self.enemiesSpeedList[idx] =  self.enemiesSpeedList[idx] * -1
                    y = enemy.ycor()
                    y = y - 40
                    enemy.sety(y)
                if enemy.xcor() < -280: 
                    self.enemiesSpeedList[idx] =  self.enemiesSpeedList[idx] * -1
                    y = enemy.ycor()
                    y = y - 40
                    enemy.sety(y)

                #Check for collision between bullet and enemy
                if self.is_collision(self.bullet, enemy):
                    self.shoot_enemy(enemy, idx)
    
                #Check for collision between enemy and player
                if self.is_collision(self.player, enemy):
                    os.system("afplay explosion.wav&")
                    self.player.hideturtle()
                    enemy.hideturtle()
                    print("GAME OVER")
                    break
            
            #Move the bullet only when bulletstate is "fire"
            if self.bulletstate == "fire":
                y = self.bullet.ycor()
                y = y + self.bulletspeed
                self.bullet.sety(y)

            #Check to see if bullet has reached the top
            if self.bullet.ycor() > 275:
                self.bullet.hideturtle()
                self.bulletstate = "ready"

    def setup(self):
        self.setup_screen()
        self.register_graphics()
        self.draw_border()
        self.draw_score()
        self.draw_player()
        self.setup_enemies()
        self.draw_bullet()
        self.attach_keyboard_events()

    def setup_screen(self):
        self.win = turtle.Screen()
        self.win.bgcolor("black")
        self.win.title("Space Invaders")
        self.win.bgpic("space_invaders_background.gif")
    
    def setup_enemies(self):
        for i in range(self.number_of_enemies):
            self.enemiesList.append(turtle.Turtle())
            #4 Enemy random speed between 1 and 3
            self.enemiesSpeedList.append(random.randint(1, 3))

        for enemy in self.enemiesList:
            self.draw_enemy(enemy)

    def register_graphics(self):
        turtle.register_shape("invader.gif")
        turtle.register_shape("red_invader.gif")
        turtle.register_shape("player.gif")
        
    def draw_border(self):
        self.border_pen = turtle.Turtle()
        self.border_pen.speed(0)
        self.border_pen.color("white")
        self.border_pen.penup()
        self.border_pen.setposition(-300,-300)
        self.border_pen.pensize(3)
        self.border_pen.pendown()
        for side in range(4):
            self.border_pen.fd(600)
            self.border_pen.lt(90)
            self.border_pen.hideturtle()
    
    def draw_score(self):
        if self.score_pen is not None:
            self.score_pen.clear()
        else:
            self.score_pen = turtle.Turtle()
        self.score_pen.speed(0)
        self.score_pen.color("white")
        self.score_pen.penup()
        self.score_pen.setposition(-290,280)
        self.score_pen.clear()
        self.scorestring = "Score: %s" % self.score
        self.score_pen.write(self.scorestring, False, align="left", font = ("Arial", 14, "bold"))
        self.score_pen.hideturtle()

    def draw_player(self):
        self.player = turtle.Turtle()
        self.player.color("blue")
        self.player.shape("player.gif")
        self.player.speed(0)
        self.player.penup()
        self.player.setposition(0, -250)
        self.player.setheading(90)

    def draw_bullet(self):
        self.bullet = turtle.Turtle()
        self.bullet.color("yellow")
        self.bullet.shape("triangle")
        self.bullet.speed(0)
        self.bullet.penup()
        self.bullet.setheading(90)
        self.bullet.shapesize(0.5, 0.5)
        self.bullet.hideturtle()

    def draw_enemy(self, enemy, color = 'green'):
        enemy.color(color)
        if color == 'green':
            enemy.shape("invader.gif")
        else:
            enemy.shape("red_invader.gif")
        enemy.speed(0)
        enemy.penup()
        x = random.randint(-200, 200)
        y = random.randint(100, 200)
        enemy.setposition(x, y)

    def attach_keyboard_events(self):
        turtle.listen()
        turtle.onkey(self.player_move_left, "Left")
        turtle.onkey(self.player_move_right,"Right")
        turtle.onkey(self.fire_bullet, "space")

    def player_move_left(self):
        x = self.player.xcor()
        x = x - self.playerspeed
        if x < -280:
            x = -280
        self.player.setx(x)

    def player_move_right(self):
        x = self.player.xcor()
        x = x + self.playerspeed
        if x > 280:
            x = 280
        self.player.setx(x)

    def fire_bullet(self):
        if self.bulletstate == "ready":
            os.system("afplay laser.wav&")
            x = self.player.xcor()
            y = self.player.ycor() + 10
            self.bullet.setposition(x,y)
            self.bullet.showturtle()
            self.bulletstate = "fire"
            
            #3 Reduce the score by one when player fires
            self.score = self.score - 1
            self.draw_score()

    def is_collision(self, t1, t2):
        distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(),2))
        if distance < 15:
            return True
        else:
            return False
    
    def shoot_enemy(self, enemy, idx):
        os.system("afplay explosion.wav&")
        enemy_color = enemy.color()[0]

        #Reset the bullet
        self.bullet.hideturtle()
        self.bulletstate = "ready"
        self.bullet.setposition(0, -400)
       
        # Delete current enemy
        enemy.clear()
        enemy.hideturtle()
        del self.enemiesList[idx]
        del self.enemiesSpeedList[idx]

        #5 Show two red enemies if a green is killed
        if enemy_color == 'green':
            for i in range(2):
                new_enemy = turtle.Turtle()
                self.draw_enemy(new_enemy, 'red') 
                self.enemiesList.append(new_enemy)
                #4 Enemy random speed between 1 and 3
                self.enemiesSpeedList.append(random.randint(1, 3)) 

        #Update the score
        #6 If red enemy is killed get double points from green
        if enemy_color == 'red':
            self.score += 20
        else:
            self.score += 10
        self.draw_score()
        
game = SpaceInvaders()
game.run()


