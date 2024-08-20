import random
from turtle import Screen, Turtle
from random import randint, choice
import pygame



screen = Screen()
screen.setup(width=1280, height=1280)
screen.tracer(0)
screen.bgcolor("black")
screen.bgpic("media/aas.gif")

pygame.mixer.init()
pygame.mixer.music.load("media/bg_music.mpeg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
fire_sound = pygame.mixer.Sound("media/fire.mp3")
blast_sound = pygame.mixer.Sound("media/blast.mp3")
game_over_sound = pygame.mixer.Sound("media/game_over.mp3")



class Frame(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.setposition(-610, -610)
        self.pendown()
        self.goto(-610, 450)
        self.goto(610, 450)
        self.goto(610, -610)
        self.goto(-610, -610)
        self.hideturtle()


class Text(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.lives = 3
        self.score = 0
        self.goto(-200, 520)
        self.write("TURTLE INVADERS", font=("Terminal", 30, "normal"))
        self.goto(-600, 520)
        self.write(f"Lives:{self.lives}", font=("Terminal", 25, "normal"))
        self.goto(410, 520)
        self.write(f"Score:{self.score}", font=("Terminal", 25, "normal"))
        self.update()

    def update(self):
        self.clear()
        self.goto(-200, 520)
        self.write("TURTLE INVADERS", font=("Terminal", 30, "normal"))
        self.goto(-600, 520)
        self.write(f"Lives:{self.lives}", font=("Terminal", 25, "normal"))
        self.goto(410, 520)
        self.write(f"Score:{self.score}", font=("Terminal", 25, "normal"))

    def point(self):
        self.score += 10
        self.update()

    def lose_life(self):
        self.lives -= 1
        self.update()

    def game_over(self):
        pygame.mixer.music.stop()
        game_over_sound.play()
        self.goto(-200,0)
        self.write("GAME OVER", font=("Terminal", 100, "normal"))


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.color("green")
        self.shape("turtle")
        self.penup()
        self.goto(0, -580)
        self.setheading(90)
        self.shapesize(2)

    def move_right(self):
        if self.xcor() < 580:
            y_pos = self.ycor()
            new_x = self.xcor() + 20
            self.goto(new_x, y_pos)

    def move_left(self):
        if self.xcor() > -580:
            y_pos = self.ycor()
            new_x = self.xcor() - 20
            self.goto(new_x, y_pos)

    def fire(self):
        fire_sound.play()
        bullet = Turtle()
        bullet.shape("circle")
        bullet.shapesize(0.5)
        bullet.color("red")
        bullet.penup()
        bullet.goto(self.xcor(), self.ycor())
        bullets.append(bullet)

MOVE_SPEED = 1
class Enemy(Turtle):
    def __init__(self, x, y):
        super().__init__()
        colors = ["red", "blue", "pink", "purple", "brown"]
        self.color(choice(colors))
        self.shape("turtle")
        self.shapesize(3)
        self.penup()
        self.setheading(270)
        self.goto(x, y)
        self.move_speed = MOVE_SPEED

    def move(self):
        new_y = self.ycor() - self.move_speed
        self.goto(self.xcor(), new_y)


frame = Frame()
text = Text()
player = Player()

screen.listen()
screen.onkeypress(player.move_right, "Right")
screen.onkeypress(player.move_left, "Left")
screen.onkeypress(player.fire, "space")

LEVEL = 1
enemies = []
bullets = []
GAME_IS_ON = True
count = 0

while GAME_IS_ON:

    if text.score == 150 and LEVEL == 1:
        LEVEL += 1
        MOVE_SPEED +=0.5

    if text.score == 300 and LEVEL == 2:
        LEVEL += 1
        MOVE_SPEED +=0.5

    while len(enemies) < LEVEL * 5:
        enemy = Enemy(randint(-500, 500), 300)
        enemies.append(enemy)

    count += 1
    if count % 15 == 0:
        for i in enemies:
            i.move()


    for bullet in bullets[:]:
        bullet.sety(bullet.ycor() + 2)
        if bullet.ycor() > 400:
            bullet.hideturtle()
            bullets.remove(bullet)


    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.distance(enemy) < 30:
                blast_sound.play()
                bullet.hideturtle()
                enemy.hideturtle()
                bullets.remove(bullet)
                enemies.remove(enemy)
                text.point()

    for enemy in enemies:
        if enemy.ycor() <= -580:
            text.lose_life()
            if text.lives <= 0:
                GAME_IS_ON = False
                text.game_over()
            enemy.hideturtle()
            enemies.remove(enemy)




    screen.update()

screen.mainloop()
