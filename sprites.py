# Sprite classes 
import pygame as pg
from settings import *
from os import path 
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.loadimg()
        self.image = self.standing_frames[0]
        self.image = pg.transform.scale(self.image,(50,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image1.get_rect()
        self.rect.center = (70, HEIGHT-100)
        self.pos = vec(70, HEIGHT-100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def loadimg(self):
        self.image1 = pg.image.load("p1.png")
        self.image1 = pg.transform.scale(self.image1,(50,80))
        self.image1.set_colorkey(BLACK)
        self.image2 = pg.image.load("p2.png")
        self.image2 = pg.transform.scale(self.image2,(50,80))
        self.image2.set_colorkey(BLACK)
        self.standing_frames=[self.image1,self.image2]
        
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3.5:
                self.vel.y = -3.5        

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.bottomright = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self,game,x, y):
        pg.sprite.Sprite.__init__(self)
        self.image3 = pg.image.load("g1.png")
        self.image3.set_colorkey(BLACK)
        self.image3 = pg.transform.scale(self.image3,(100,30))
        self.image4 = pg.image.load("g2.png")
        self.image4 = pg.transform.scale(self.image4,(150,40))
        self.image4.set_colorkey(BLACK)
        images=[self.image3,self.image4]
        self.image = random.choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Carrots(pg.sprite.Sprite):
    def __init__(self,game,plat):
        pg.sprite.Sprite.__init__(self)
        self.plat=plat
        self.game=game
        self.image = pg.image.load('carrot.png')
        self.image = pg.transform.scale(self.image,(30,35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom  = self.plat.rect.top-7

    def update(self):
        self.rect.bottom  = self.plat.rect.top-7
        if not self.game.platforms.has(self.plat):
            self.kill()
        
        
