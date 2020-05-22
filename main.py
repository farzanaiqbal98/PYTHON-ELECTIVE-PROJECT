# PYGAME PROJECT- UP N UP!
# COURSE MSP(PH4031D)- G SLOT
# Group No 20 -Members:ALKA PB ,FARZANA IQBAL ,JISHNU K
# Sprites form opengameart.org from Kenny.nl
# Background images from freepik.com
# Music credits opengameart.org
# Background vector created by pikisuperstar - www.freepik.com
# Background vector created by freepik - www.freepik.com



import pygame as pg
import random
from settings import *
from sprites import *
import os 

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.icon=pg.image.load('jumping.png')
        pg.display.set_icon(self.icon)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = os.path.dirname(__file__)
        try:
            f=open(path.join(self.dir, HS_FILE), 'r') 
            self.highscore = int(f.read())
        except:
            f=open(path.join(self.dir, HS_FILE), 'r')  
            self.highscore = 0
        self.jump_sound = pg.mixer.Sound("Jump.ogg")
       
        self.backg = pg.image.load("9290.jpg")
        self.backg = pg.transform.scale(self.backg,(2400,1500))
        self.Sbackg = pg.image.load("2850058.jpg")
        self.Gbackg = pg.image.load("2799007.jpg")
        

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.carrots = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Creating the basic/initial platforms
        for plat in PLATFORM_LIST:
            p = Platform(self,*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            #Adding carrots randomly on the  initial platform
            i = random.randrange(10,30)
            if i > 15 and i <26 :
                c=Carrots(self,p)
                self.carrots.add(c)
                self.all_sprites.add(c)
                
        self.intro_sound = pg.mixer.Sound("happyland_128.ogg")
        self.run()

    def run(self):
        # Game Loop
        self.intro_sound.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
         # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right +30 and  self.player.pos.x > lowest.rect.left - 30:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # if player hits a carrot
        carr_hits = pg.sprite.spritecollide(self.player, self.carrots, True)
        for car in carr_hits:
            self.score+=50    

        # Die ! All platforms below the window is killed
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 5:
            width = random.randrange(60, 100)
            p = Platform(self,random.randrange(0,WIDTH-90-width),random.randrange(-55, -20))
            if p.rect.left > 0 and p.rect.right< WIDTH:
                self.platforms.add(p)
                self.all_sprites.add(p)
            #Adding carrots randomly on the new platform
            if width > 50  and width <70:
                c=Carrots(self,p)
                self.carrots.add(c)
                self.all_sprites.add(c)
          

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
               

    def draw(self):
        # Game Loop - draw
        self.screen.fill(WHITE)
        self.screen.blit(self.backg,(0,0))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()
        

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(WHITE)
        self.screen.blit(self.Sbackg,(0,0))
          
        self.draw_text(TITLE, 48,txt1, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Help our Bunny to collect all carrots and go up!", 20, (24,116,205), WIDTH / 2, HEIGHT / 2-50)
        self.draw_text("Go up +10 points", 20,txt1, WIDTH / 2, HEIGHT / 2+30)
        self.draw_text("Grab a carrot +50 points", 20,txt1, WIDTH / 2, HEIGHT / 2+60)
        self.draw_text("If bunny falls you lose!!", 20,txt1, WIDTH / 2, HEIGHT / 2+90)
        self.draw_text("Press Arrows to move and Space to jump!", 20, (16,78,139), WIDTH / 2, HEIGHT / 2+120)
        
        self.draw_text("Press a key to play", 22,BLACK, WIDTH / 2, HEIGHT * 3 / 4+20)
        self.draw_text("High Score: " + str(self.highscore), 22,BLACK, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        
        self.screen.fill(WHITE)
        self.screen.blit(self.Gbackg,(0,0))

        self.draw_text("GAME OVER!!!!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Help our Bunny again!", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Press a key to try again!", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4+40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        font.set_bold(True)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



g = Game()
open_sound = pg.mixer.Sound("New Kind Of Humanity.wav")
open_sound.play()


g.show_start_screen()
pg.mixer.stop()
while g.running:
    pg.mixer.stop()
    g.new()
    pg.mixer.pause()
    close_sound = pg.mixer.Sound("mushroom dance.ogg")
    close_sound.play()
    g.show_go_screen()

pg.quit()
