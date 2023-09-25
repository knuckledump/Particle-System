import pygame as p
from pygame.locals import *
import sys
import math
import random

WIDTH = 1200
HEIGHT = 800
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 60

class particle:
    def __init__(self,g,x,y):
        
        self.game = g
        self.game.effects.append(self)
        
        self.width = WIDTH
        self.height = HEIGHT
        self.image = p.Surface((self.width,self.height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        
        self.particle_list = []
        self.color = (255,255,255)
        
        self.red_value = 20
        self.green_value = 20
        self.blue_value = 20
        self.decal = 1
        
        self.light_color = (self.red_value,self.green_value,self.blue_value)
        
        self.font = p.font.Font('Retro Gaming.ttf', 32)
    
    def update(self):
        
        self.change_color()
        self.show_color_value()
        x,y = p.mouse.get_pos()
        
        particle = [[x,y] , [random.randint(-30,30)/3,random.randint(-50,0)/3] , random.randint(10,30)]
        self.particle_list.append(particle)
        for par in self.particle_list:
            par[0][0] += par[1][0]
            par[0][1] += par[1][1]
            par[2] -= 0.4
            if par[2] <=0:
                self.particle_list.remove(par)
        
            p.draw.circle(self.game.screen, self.color, [int(par[0][0]), int(par[0][1])], int(par[2]))
            radius = particle[2] * 1.5
            self.game.screen.blit(self.circle_surf(radius, self.light_color), (int(par[0][0] - radius), int(par[0][1] - radius)), special_flags=BLEND_RGB_ADD)
        
    
    def change_color(self):
        
        self.light_color =(self.red_value, self.green_value, self.blue_value) 
        keys = p.key.get_pressed()
        if keys[p.K_r]:
            self.red_value += self.decal
        if keys[p.K_g]:
            self.green_value += self.decal
        if keys[p.K_b]:
            self.blue_value += self.decal
        
        if self.red_value >255:
            self.red_value = 0
        if self.green_value >255:
            self.green_value = 0
        if self.blue_value >255:
            self.blue_value = 0
            
    def show_color_value(self):
        
        text = self.font.render('RGB: '+str(self.red_value)+'/'+str(self.green_value)+'/'+str(self.blue_value), True, WHITE)
        self.game.screen.blit(text,(20,20))
        
    def circle_surf(self,radius, color):
        
        surf = p.Surface((radius * 2, radius * 2))
        p.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf


class game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((WIDTH,HEIGHT),0,32)
        self.clock = p.time.Clock()
        self.running = True
        self.playing = False
        
    
    def new(self):
        self.playing = True
        self.all_sprites = p.sprite.LayeredUpdates()
        self.effects = []
        particle(self,0,0)
        
    
    def events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
        
    def update(self):
        self.all_sprites.update()
         
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        for e in self.effects:
            e.update()
        self.clock.tick(FPS) 
        p.display.update()
        
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
        self.running = False
    

g = game()
g.new()

while g.running:
    g.main()

p.quit()
sys.exit()
