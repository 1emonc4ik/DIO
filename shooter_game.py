from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((1200, 720))
display.set_caption('GALAGA')
background = transform.scale(image.load('planeta.jpg'), (1200, 720))
Game_over = transform.scale(image.load('Game_over.jpg'), (1200, 720))
You_win = transform.scale(image.load('you_win.jpg'), (1200, 720))

mixer.init()
mixer.music.load('star_wars.ogg')
laser = mixer.Sound('fire.ogg')
mixer.music.play()

font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 40)
font3 = font.SysFont('Arial', 40)
font4 = font.SysFont('Arial', 40)
lost = 0
kills = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 15:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 1115:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 605:
            self.rect.y += self.speed
            
    def fire(self):
        bullet = Bullet('laser.png', self.rect.centerx, self.rect.top, 10, 40, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost

        self.rect.y += self.speed
        if self.rect.y > 700:
            lost += 1
            self.rect.x = randint(1, 1120)
            self.rect.y = 0
            self.kill()

class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.x = randint(1, 1120)
            self.rect.y = 0
            self.kill()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
         
death_star = Player('pngwing.png', 560, 610, 80, 100, 9)

monsters = sprite.Group()
for i in range(6):
    monster = Enemy('Boba_fett.png', randint(1, 1120), 0, 80, 130, randint(1, 2))
    monsters.add(monster)    

bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(2):
    asteroid = Enemy1('asteroid.png', randint(1, 1120), 0, 80, 130, randint(1, 2))
    asteroids.add(asteroid)

game = True
clock = time.Clock()
FPS = 60
finish = False
rel_time = False
num_fire = 0
life = 10

while game:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 15 and rel_time == False:
                    num_fire += 1
                    laser.play()
                    death_star.fire()
                if num_fire >= 15 and rel_time == False:
                    end_time = timer()
                    rel_time = True

    if not finish:
        death_star.reset()
        death_star.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window) 
        bullets.update()
        if rel_time == True:
            new_time = timer()
            if new_time - end_time < 3:
                window.blit(font3.render('Перезарядка...', True, (255, 0, 0)), (500, 360))
            else:
                rel_time = False
                num_fire = 0
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            kills += 1 
            monster = Enemy('Boba_fett.png', randint(1, 1120), 0, 80, 130, randint(1, 2))
            monsters.add(monster) 
        if sprite.spritecollide(death_star, monsters, False) or sprite.spritecollide(death_star, asteroids, True):
            sprite.spritecollide(death_star, monsters, True)
            sprite.spritecollide(death_star, monsters, True)
            life -= 1
    
    text_lose = font1.render('Пропущенo:'+ str(lost) + '|5', True, (255, 255, 255))
    text_win = font2.render('Счёт:'+ str(kills), True, (255, 255, 255))
    lifes = font4.render('Жизней:'+ str(life), True, (255, 255, 255))
    window.blit(text_lose, (10, 60))
    window.blit(text_win, (10, 20))
    window.blit(lifes, (10, 100))

    if life == 0 or lost > 5:
        finish = True
        window.blit(Game_over, (0, 0))

    if kills >= 10:
        finish = True
        window.blit(You_win, (0, 0))

    display.update()
    clock.tick(FPS)
