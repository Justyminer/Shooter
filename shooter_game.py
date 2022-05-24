#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
mixer.init()
window = display.set_mode((700,500))
font.init()
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
mixer.init()
mixer.music.load('space.ogg') 
mixer.music.play()
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Aril', 200)
font4 = font.SysFont('Arial', 200)
font5 = font.SysFont('Arial', 23)
lost = 0
scores = 0
num_fire = 0
rel_time = False

#if lost
#cicle



#keyshot
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_speed,player_x,player_y,width = 60,heigh = 60):
        super().__init__()
        self.image =  transform.scale(image.load(player_image),(width,heigh))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, 640)

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 10, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)
     
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()

  
    


sobd = mixer.Sound('fire.ogg')        
hero = Player('rocket.png',15,10,440)
bullets = sprite.Group()
monsters = sprite.Group()
asters = sprite.Group()
text_reload = font5.render('Wait reload', True, (255,1,1))
for i in range (5):
    monster = Enemy('ufo.png', randint(1,4), randint(10,650), 0)
    monsters.add(monster)
for i in range (5):
    asterm = Enemy('asteroid.png', randint(1,4), randint(10,650), 0)
    asters.add(asterm)

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    hero.fire()
                    sobd.play()
                    num_fire += 1
                else:
                    rel_time = True
                    last_time = timer()
               
                
    
    if finish != True:
        window.blit(background,(0, 0))
        hero.reset()
        hero.update()
        monsters.update()
        bullets.update()
        asters.update()
        monsters.draw(window)
        bullets.draw(window)
        asters.draw(window)
        text_lose = font1.render('Skipped:' + str(lost), 1,(255,255,255))
        text_score = font2.render('Score:' + str(scores), 1,(255,255,255))
        window.blit(text_lose,(10,0))
        window.blit(text_score,(10,25))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    
        for i in sprites_list:  
            scores += 1
            monster = Enemy('ufo.png', 10, randint(10,650), 0)
            monsters.add(monster)
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            text_losem = font4.render('LOSE', True, (255,255,252))
            window.blit(text_losem, (200,200))
        if scores  >= 10:
            finish = True
            text_win = font3.render('WIN', True, (200,123,223))
            window.blit(text_win, (200, 200))
        if sprite.spritecollide(hero, asters, True):
            finish = True
            text_losem = font4.render('LOSE', True, (255,255,252))
            window.blit(text_losem, (200,200))
        if rel_time == True:
            new_time = timer()
            if new_time - last_time >= 3:
                num_fire = 0
                rel_time = False
            window.blit(text_reload,  (50,50))
    display.update()
    time.delay(50)