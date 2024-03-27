from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.03)
lost = 0
score = 0
font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 80)
win = font2.render('win', True, (0, 255, 0))
lose = font2.render('lose', True, (0, 255, 0))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

ship = Player('rocket.png', 5, win_height-100, 7)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80,620), -30, randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80,620), -30, randint(1,5))
    asteroids.add(asteroid)
finish = False
game = True
fire_sound = mixer.Sound('fire.ogg')
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
    if not finish:
        window.blit(background, (0, 0))
        text = font1.render(f'Счет: {score}', True, (255, 255,255))
        window.blit(text, (10,20))
        text_lose = font1.render(f'Пропущено: {lost}', True, (255, 255,255))
        window.blit(text_lose,(10,50))
        monsters.draw(window)
        monsters.update() 
        bullets.draw(window)
        bullets.update()
        ship.reset()
        ship.update()
        asteroids.draw(window)
        asteroids.update()
        collides = sprite.groupcollide(bullets, monsters, True, True)
        for i in collides:
            score +=1
            monster = Enemy('ufo.png', randint(80,620), -30, 80, 100, randint(1,5))
            monsters.add(monster)
        if  sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose, (200,200))
        if  sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose, (200,200))
        if score > 9:
            finish = True
            window.blit(win, (200,200))
    display.update()
    time.delay(20)