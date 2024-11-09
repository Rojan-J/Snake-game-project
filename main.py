import pygame
import sys
import random
from pygame.math import Vector2

class Main:
    def __init__(self):
        self.snake=Snake()
        self.fruit=Fruits()  
        
    def update(self):
        self.snake.snake_moving()
        self.check_collision()
        self.check_gameover()
        
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        
    def check_collision(self):
        if self.fruit.pos== self.snake.body[0]:
            self.fruit.randomize()
            
            self.snake.add_block()
        
    def check_gameover(self):
        for block in self.snake[1:]:
            if block==self.snake[0]:
                self.game_over()
                
                
        if not 0<= self.snake.body[0].y < 20 or not 0<= self.snake.body[0].x < 20:
            self.game_over()
    
    def game_over(self):
        pygame.QUIT()
        sys.exit()
        

class Fruits:
    def __init__(self):
        self.x= random.randint(0,39)
        self.y= random.randint(0,39)
        self.pos=Vector2(self.x,self.y)
        
    def draw_fruit(self):
        fruit_rect=pygame.Rect(int(self.pos.x*40) ,int(self.pos.y*40) ,40,40)
        pygame.draw.rect(game_screen,(126,166,114),fruit_rect)
        
    def randomize(self):
        self.x= random.randint(0,39)
        self.y= random.randint(0,39)
        self.pos=Vector2(self.x,self.y)
        
class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block=False
        
    def draw_snake(self):
        for block in self.body:
            x=int(block.x *40)
            y=int(block.y*40)
            block_rect=pygame.Rect(x,y,40,40)
            pygame.draw.rect(game_screen,(183,110,122),block_rect)  
            
    def snake_moving(self):
        if self.new_block==True:
            prev_body=self.body[:]
            prev_body.insert(0,prev_body[0]+self.direction)
            new_body=prev_body
            self.body=new_body[:] 
            self.new_block = False
        else:
            prev_body=self.body[:-1]
            prev_body.insert(0,prev_body[0]+self.direction)
            new_body=prev_body
            self.body=new_body[:] 
            
            
    def add_block(self):
        self.new_block=True

pygame.init()
game_screen=pygame.display.set_mode((800,800))
surface=pygame.Surface((400,400))


# fruit=Fruits()
# snake=Snake()

clock=pygame.time.Clock()

update_screen=pygame.USEREVENT
pygame.time.set_timer(update_screen,150)

main=Main()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == update_screen:
            main.update()
            
        #keyboard setting to move the snake
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.y !=-1:
                    main.snake.direction=Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main.snake.direction.y !=1:
                    main.snake.direction=Vector2(-1,0)
            if event.key == pygame.K_UP:
                if main.snake.direction.y !=1:
                    main.snake.direction=Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y !=-1:
                    main.snake.direction=Vector2(0,1)
                
            
            
    game_screen.fill((20,120,150))   
    main.draw_elements()
    
    
    pygame.display.update()
    
    
    clock.tick(60)