# import and initialise pygame
import pygame
import random
import math
from pygame import mixer

pygame.init()

# run screen:
screen = pygame.display.set_mode((800, 600))


# Game Window Visuals:    Title & Icon (32x32 px)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship64.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background1.png')

#background sound

mixer.music.load('Loyalty_Freak.wav')
mixer.music.play(-1)  #-1 plays on loop


# player
PlayerImg = pygame.image.load('spaceship2.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0     #speed

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('alien3.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# bullet - ready = cant see on screen . fire = currently on screen
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
#bulletX_change = 2
bulletY_change = 6
bullet_state = "ready"

#SCORE
score_value = 0
font = pygame.font.Font('Mistic.ttf', 36)
textX = 20
textY = 20

#GAME OVER TEXT:
over_font = pygame.font.Font('Mistic.ttf', 68)

def score(x, y):
    score = font.render("SCORE :  " + str(score_value), True, (139,0,139))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (139, 0, 139))
    screen.blit(over_text, (220, 210))


#functions to draw out the objects
#score = 0
def player(x, y):
    screen.blit(PlayerImg, (x, y))  # blit means to draw: draw image onto screen: (image, (x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):    #bullet state was ready but when call this function, (by presing space written later, it turns to fire)
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))    #so bullet appears in centre & top of nose of spaceship

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return  True
    else:
        return False

# GAME LOOP:
# run screen & loop all events. If close button is being pressed, id false so loop will stop running.
# All events will run in this loop
running = True
while running:
    screen.fill((255, 182, 153))  # this is first bc this is bkground layer, dont want images hiding under this.
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard input:
        if event.type == pygame.KEYDOWN:  # KEYDOWN is pressing key down
            #print("A key has been pressed")
            if event.key == pygame.K_LEFT:
                PlayerX_change = -3
                #print("Left arrow has been pressed ")
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 3
                #print("Right arrow has been pressed ")
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('shootsound.wav')
                    bullet_Sound.play()
                    bulletX = PlayerX
                    fire_bullet(bulletX, bulletY)           #when press space, itll trigger the fire_bullet at these x,y coords.

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0
                #print("Key has been released")

    #PLAYER MOVEMENT
    PlayerX += PlayerX_change
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    #ENEMY MOVEMENT
    for i in range(num_enemies):

        #GAME OVER:
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 2
        elif enemyX[i] >= 736:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -2

        # Collision (ensure in for loop not elif loop)
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_Sound = mixer.Sound('weee.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)



    # BULLET MOVEMENT

    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":                           #if the state = fire by pressing space as written above, itll move tne bullet as described.
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    score(textX, textY)
    player(PlayerX, PlayerY)
    pygame.display.update()  # alyways want this updated when an event happens
