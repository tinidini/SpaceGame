import pygame
import sys
sys.setrecursionlimit(100000)

from pygame.time import Clock
pygame.font.init()
pygame.mixer.init()

##### constants & prep #####

WIDTH, HEIGHT=900, 500
WIN=pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("First Game :D")

BORDER=pygame.Rect(WIDTH//2-5, 0, 3, HEIGHT) #limit the space in which the spaceships can move

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
LRED=(200,0,0)
YELLOW=(255,255,0)
GREEN=(0,255,0)
LGREEN=(0,200,0)

FPS=60
VEL=5 #moving speed
LASER_VEL=7
MAX_LASERS=10
SP_W, SP_H=55,40 # width, height

HEALTH_FONT=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans', 100)
INTRO_FONT=pygame.font.SysFont('comicsans', 70)
BUTTON_FONT=pygame.font.SysFont('comicsans', 40)

YELLOW_HIT=pygame.USEREVENT+1 #create events so we can check for them later in the main function
RED_HIT=pygame.USEREVENT+2

LASER_HIT_SOUND=pygame.mixer.Sound('/Users/adinaciubancan/Documents/PythonProj/Assets/Grenade+1.mp3')
LASER_FIRE_SOUND=pygame.mixer.Sound('/Users/adinaciubancan/Documents/PythonProj/Assets/Gun+Silencer.mp3')

##### import spaceship images #####

YELLOW_SPACESHIP_IMAGE=pygame.image.load(r'/Users/adinaciubancan/Documents/PythonProj/Assets/spaceship_yellow.png')
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SP_W, SP_H)), 90)

RED_SPACESHIP_IMAGE=pygame.image.load(r'/Users/adinaciubancan/Documents/PythonProj/Assets/spaceship_red.png')
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SP_W, SP_H)), 270)

SPACE=pygame.transform.scale(pygame.image.load(r'/Users/adinaciubancan/Documents/PythonProj/Assets/space-bg.jpg'), (WIDTH, HEIGHT))
clock=pygame.time.Clock()
######### START GAME #######

def quitgame():
    pygame.quit()
    quit()

def button(msg, x,y,w,h,icolor, acolor,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()

    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(WIN, acolor, (x,y,w,h)) 
        if click[0]==1 and action != None:
            action()

            
    else: pygame.draw.rect(WIN, icolor,(x,y,w,h))

    button_text=BUTTON_FONT.render(msg,1,BLACK)
    WIN.blit(button_text,(button_text.get_rect(center=(x+(w/2), y+(h/2)))))
    


def game_intro():


    intro=True

    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(BLACK)
        intro_text=INTRO_FONT.render("Welcome, tap to start",1,WHITE)
        WIN.blit(intro_text,(intro_text.get_rect(center=(WIDTH//2, HEIGHT//2-100))))
        

        button("START", 150,350,100,50,GREEN, LGREEN,main_f)
        button("QUIT", 650,350,100,50,RED,LRED,quitgame)

        pygame.display.update()
        clock.tick(15)

################################################################
def draw_window(red, yellow,red_lasers,yellow_lasers,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,RED, BORDER )

####show health on the screen
    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("Health: "+str(yellow_health),1,WHITE)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y)) #project image onto screen
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    



    for laser in red_lasers:
        pygame.draw.rect(WIN, RED, laser)

    for laser in yellow_lasers:
        pygame.draw.rect(WIN, YELLOW, laser)
    pygame.display.update() #show changes




######control the spaceships######
def yellow_movement(keys_pressed, yellow):
                ##yellow##
        if keys_pressed[pygame.K_a] and yellow.x-VEL > 0: #left
            yellow.x-= VEL

        if keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width < BORDER.x: #right
            yellow.x+= VEL

        if keys_pressed[pygame.K_w] and yellow.y-VEL > 0: #up
            yellow.y-= VEL

        if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height < HEIGHT-15: #down
            yellow.y+= VEL

def red_movement(keys_pressed, red):
                ##yellow##
        if keys_pressed[pygame.K_LEFT]and red.x-VEL > BORDER.x+ BORDER.width: #left
            red.x-= VEL

        if keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width < WIDTH: #right
            red.x+= VEL

        if keys_pressed[pygame.K_UP] and red.y-VEL > 0: #up
            red.y-= VEL

        if keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height < HEIGHT-15: #down
            red.y+= VEL
###################################

##########laser behaviour##########

def handle_lasers(yellow_lasers,red_lasers,yellow,red):
    for laser in yellow_lasers:
        laser.x+=LASER_VEL
        if red.colliderect(laser):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_lasers.remove(laser)
        elif laser.x>WIDTH:
            yellow_lasers.remove(laser)

    for laser in red_lasers:
        laser.x-=LASER_VEL
        if yellow.colliderect(laser):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_lasers.remove(laser)
        elif laser.x<0: #remove lasers from board if they miss
            red_lasers.remove(laser)

###################################


##### health management/winner #####
def  draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2-draw_text.get_width()
                    //2, HEIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
####################################


def main_f():

    yellow=pygame.Rect(100,300,SP_W,SP_H)
    red=pygame.Rect(700,300,SP_W,SP_H)

    red_lasers=[]
    yellow_lasers=[]

    red_health=10
    yellow_health=10

    clock=pygame.time.Clock()
    run=True

    while run:
        clock.tick(FPS) #control fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit when we press the exit button, prevents the need of a force quit
                 run=False
                 pygame.quit()
            ###### lasers #######
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q and len(yellow_lasers)<MAX_LASERS:
                     laser=pygame.Rect(
                         yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                     yellow_lasers.append(laser)
                     LASER_FIRE_SOUND.play()

                             
                if event.key==pygame.K_RSHIFT and len(red_lasers)<MAX_LASERS:
                     laser=pygame.Rect(
                         red.x, red.y + red.height//2 - 2, 10, 5)
                     red_lasers.append(laser)
                     LASER_FIRE_SOUND.play()

            #print(red_lasers, yellow_lasers)
        ##health
            if event.type==RED_HIT:
                red_health-=1
                LASER_HIT_SOUND.play()

            if event.type==YELLOW_HIT:
                yellow_health-=1
                LASER_HIT_SOUND.play()


###### manage health #####
        winner_text=""
        if red_health<=0:
            winner_text="YELLOW WON THE WAR!"

        if yellow_health<=0:
            winner_text="RED WON THE WAR!"
    
        if winner_text!="":
            draw_winner(winner_text)
            break
         



        keys_pressed=pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow) 
        red_movement(keys_pressed, red) 

        handle_lasers(yellow_lasers,red_lasers,yellow,red)

        draw_window(red, yellow, red_lasers, yellow_lasers, red_health, yellow_health)

    main_f() #restart the game

game_intro()
if __name__ == "__main__": #prevents running the game by accident if this file was imported
    main_f()