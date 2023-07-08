# Music by Punch Deck | https://soundcloud.com/punch-deck
# Music promoted by https://www.chosic.com/free-music/all/
# Creative Commons CC BY 3.0
# https://creativecommons.org/licenses/by/3.0/
 
import tkinter
import pygame
pygame.init()
pygame.mixer.music.load("max.mp3")
pygame.mixer.music.play(-1)
HEIGHT = 500
WIDTH = 800
window =  tkinter.Tk()
window.title('Bubble Blaster')
c = tkinter.Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()
ship_id = c.create_polygon(5,5,5,25,30,15,fill='red')
ship_id2 = c.create_oval(0,0,30,30,outline='red')
SHIP_RADIUS = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id,MID_X,MID_Y)
c.move(ship_id2,MID_X,MID_Y)
SHIP_SPEED = 10
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id,0,-SHIP_SPEED)
        c.move(ship_id2,0,-SHIP_SPEED)
    elif event.keysym == 'Down':
        c.move(ship_id,0,SHIP_SPEED)
        c.move(ship_id2,0,SHIP_SPEED)
    elif event.keysym == 'Left':
        c.move(ship_id,-SHIP_SPEED,0)
        c.move(ship_id2,-SHIP_SPEED,0)
    elif event.keysym == 'Right':
        c.move(ship_id,SHIP_SPEED,0)
        c.move(ship_id2,SHIP_SPEED,0)
c.bind_all('<Key>',move_ship)
import random
bubble_id = list()
bubble_radius = list()
bubble_speed = list()
MIN_BUBBLE_RADIUS = 10
MAX_BUBBLE_RADIUS = 30
MAX_BUBBLE_SPEED = 10
GAP = 100
def create_bubble():
    x = WIDTH + GAP
    y = random.randint(0, HEIGHT)
    r = random.randint(MIN_BUBBLE_RADIUS, MAX_BUBBLE_RADIUS)
    id1 = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bubble_id.append(id1)
    bubble_radius.append(r)
    bubble_speed.append(random.randint(1,MAX_BUBBLE_SPEED))
def move_bubbles():
    for i in range(len(bubble_id)):
        c.move(bubble_id[i], -bubble_speed[i], 0)
def get_coords(id):
    pos = c.coords(id)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y
def del_bubble(id):
    del bubble_radius[id]
    del bubble_speed[id]
    c.delete(bubble_id[id])
    del bubble_id[id]
def clean_up_bubbles():
    for id in range(len(bubble_id)-1,-1,-1):
        x,y = get_coords(bubble_id[id])
        if x < -GAP:
            del_bubble(id)
import math
def distance(id1,id2):
    # this cal all be done more clearly with a tuple, but won't
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return math.sqrt((x2-x1)**2+(y2-y1)**2)
def collision():
    points = 0
    for id in range(len(bubble_id)-1,-1,-1):
        d = distance(ship_id2, bubble_id[id])
        b  = SHIP_RADIUS + bubble_radius[id]
        if d < b:
            points += bubble_radius[id] + bubble_speed[id]
            del_bubble(id)
    return points
c.create_text(50,30,text='TIME',fill='white')
c.create_text(150,30,text='SCORE',fill='white')
time_text = c.create_text(50,50,fill='white')
score_text = c.create_text(150,50,fill='white')
def show_score(score):
    c.itemconfig(score_text,text=str(score))
def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))
import time
BUBBLE_CHANCE = 10
TIME_LIMIT = 180
BONUS_SCORE = 1000
score = 0
bonus = 0
end = time.time() + TIME_LIMIT
while time.time() < end:
    if random.randint(1, BUBBLE_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubbles()
    score += collision()
    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        end += TIME_LIMIT
    show_score(score)
    show_time(int(end - time.time()))
    window.update()
    time.sleep(0.01)

c.create_text(MID_X, MID_Y, text='GAME OVER', fill='white',
        font=('Helvetica', 30))
c.create_text(MID_X, MID_Y + 30, text='Score: ' + str(score),
        fill='white')
c.create_text(MID_X, MID_Y + 45, text='Bonus Time: ' +
        str(bonus*TIME_LIMIT), fill='white')

window.mainloop()