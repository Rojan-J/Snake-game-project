import pygame
import sys
import random
from pygame.math import Vector2
import math

class Main:
    
    def __init__(self):
        self.snake=Snake()
        self.fruit=Fruits()  
        
    def update(self):
        self.snake.snake_moving()
        self.check_collision()
        self.draw_elements()
        #self.check_gameover()

        
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        
    def check_collision(self):

        snake_head_rect = pygame.Rect(int(self.snake.body[0].x * 40), int(self.snake.body[0].y * 40), 40, 40)

    
        if snake_head_rect.colliderect(self.fruit.rect):
            self.fruit.randomize() 
            self.snake.add_block()
        #if self.fruit.pos== self.snake.body[0]:
         #   self.fruit.randomize()
            
          #  self.snake.add_block()
        
    #def check_gameover(self):
     #   for block in self.snake.body[1:]:
      #      if block==self.snake.body[0]:
       #         self.game_over()
                
                
        #if not 0<= self.snake.body[0].y < 20 or not 0<= self.snake.body[0].x < 20:
         #   self.game_over()
    
    #def game_over(self):
        #self.game_state = False
        

class Fruits:
    def __init__(self):
        self.x= random.randint(0,18)
        self.y= random.randint(0,18)
        self.pos=Vector2(self.x,self.y)
        
    def draw_fruit(self):
        apple = pygame.image.load("Project/Snake-game-project/apple1.png").convert_alpha()
        scaled_apple = pygame.transform.scale(apple, (40, 40))
        self.rect = scaled_apple.get_rect(topleft = (int(self.pos.x*40), int(self.pos.y*40)))
        game_screen.blit(scaled_apple, self.rect)
        
    def randomize(self):
        self.x= random.randint(0,19)
        self.y= random.randint(0,19)
        self.pos=Vector2(self.x,self.y)
        
class Snake:
    def __init__(self):
        open_eyes = pygame.image.load("Project/Snake-game-project/eyes3.png").convert_alpha()
        open_eyes_scaled = pygame.transform.scale(open_eyes, (40, 40))

        close_eyes = pygame.image.load("Project/Snake-game-project/eye_closed.png").convert_alpha()
        close_eyes_scaled = pygame.transform.scale(close_eyes, (40, 40))         
        
        tongue = pygame.image.load("Project/Snake-game-project/tongue.png").convert_alpha()
        tongue_scaled = pygame.transform.scale(tongue, (40, 40))



    
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block=False
        self.eyes = [open_eyes_scaled, close_eyes_scaled]
        self.tongue = tongue_scaled
        self.tongue_index = 0
        self.eyes_index = 0
        
    def draw_snake(self):
        for index, block in enumerate(self.body):
            x=int(block.x *40)
            y=int(block.y*40)
            block_rect=pygame.Rect(x,y,40,40)

            
            if index == 0:  # Head of the snake               
                # Determine which corners to round based on direction
                if self.direction == Vector2(1, 0):  # Moving right
                    pygame.draw.rect(game_screen, "#5a6f19", block_rect, border_top_right_radius=10, border_bottom_right_radius= 10)  # Top-right corner
                    eyes_scaled = pygame.transform.rotate(self.eyes[int(self.eyes_index)], 0)
                    eyes_rect = eyes_scaled.get_rect(center=(x + 20, y))
                    if int(self.tongue_index) == 0:
                        rotated_tongue = pygame.transform.rotate(self.tongue, 180)
                        pygame.draw.circle(game_screen, "Black", (x + 35, y+25), 5, 5)
                        tongue_rect = rotated_tongue.get_rect(midleft = (x + 35, y+ 20))
                        game_screen.blit(rotated_tongue, tongue_rect)

                    else:
                        pygame.draw.line(game_screen, "Black", (x+20, y+ 25), (x+ 40, y +25), 3)


                    
                elif self.direction == Vector2(-1, 0):  # Moving left
                    pygame.draw.rect(game_screen, "#5a6f19", block_rect, border_top_left_radius=10, border_bottom_left_radius= 10)  # Top-left corner
                    eyes_scaled = pygame.transform.rotate(self.eyes[int(self.eyes_index)], 0)
                    eyes_rect = eyes_scaled.get_rect(center=(x + 20, y))
                    if int(self.tongue_index) == 0:
                        pygame.draw.circle(game_screen, "Black", (x +5, y+25), 5, 5)
                        rotated_tongue= pygame.transform.rotate(self.tongue, 0)
                        tongue_rect = rotated_tongue.get_rect(midright = (x + 6, y+ 30))
                        game_screen.blit(rotated_tongue, tongue_rect)

                    else:
                        pygame.draw.line(game_screen, "Black", (x+20, y+ 25), (x, y +25), 3)


                elif self.direction == Vector2(0, -1):  # Moving up
                    pygame.draw.rect(game_screen, "#5a6f19", block_rect, border_top_left_radius=10, border_top_right_radius= 10)  # Top-left corner
                    eyes_scaled = pygame.transform.rotate(self.eyes[int(self.eyes_index)], -90)
                    eyes_rect = eyes_scaled.get_rect(center=(x + 35, y +20))
                    
                    if int(self.tongue_index) == 0:
                        pygame.draw.circle(game_screen, "Black", (x +15, y+5), 5, 5)
                        rotated_tongue= pygame.transform.rotate(self.tongue, -90)
                        tongue_rect = rotated_tongue.get_rect(midbottom = (x + 8, y+ 10))
                        game_screen.blit(rotated_tongue, tongue_rect)

                    else:
                        pygame.draw.line(game_screen, "Black", (x+10, y+ 20), (x + 10, y), 3)


                elif self.direction == Vector2(0, 1):  # Moving down
                    pygame.draw.rect(game_screen, "#5a6f19", block_rect, border_bottom_left_radius=10, border_bottom_right_radius= 10)  # Bottom-left corner
                    eyes_scaled = pygame.transform.rotate(self.eyes[int(self.eyes_index)], -90)
                    eyes_rect = eyes_scaled.get_rect(center=(x + 35, y +20))

                    if int(self.tongue_index) == 0:
                        pygame.draw.circle(game_screen, "Black", (x +15, y+35), 5, 5)
                        rotated_tongue= pygame.transform.rotate(self.tongue, 90)
                        tongue_rect = rotated_tongue.get_rect(midtop = (x + 20, y+ 32))
                        game_screen.blit(rotated_tongue, tongue_rect)

                    else:
                        pygame.draw.line(game_screen, "Black", (x+10, y+ 20), (x + 10, y+40), 3)
                    


                game_screen.blit(eyes_scaled, eyes_rect)
                if int(self.eyes_index) == 0: self.eyes_index += 0.02
                else: self.eyes_index += 0.05
                if self.eyes_index > 2: self.eyes_index = 0

                self.tongue_index += 0.02
                if self.tongue_index > 2: self.tongue_index = 0


            else:  # Other blocks without rounded corners
                pygame.draw.rect(game_screen, "#5a6f19", block_rect) 
            
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

game_state = True

def check_game_over(main):
    global game_state
    for block in main.snake.body[1:]:
        if block == main.snake.body[0]:
            game_state = False
    if not 0<= main.snake.body[0].y < 20 or not 0<= main.snake.body[0].x < 20:
        game_state = False

pygame.init()
game_screen=pygame.display.set_mode((800,800))
surface=pygame.Surface((400,400))
background = pygame.image.load("Project/Snake-game-project/background.png").convert_alpha()
background = pygame.transform.scale(background, (800, 800))



# fruit=Fruits()
# snake=Snake()

clock=pygame.time.Clock()

update_screen=pygame.USEREVENT
pygame.time.set_timer(update_screen,150)

main=Main()

while True:
    if game_state == True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == update_screen:
                main.update()
                
            #keyboard setting to move the snake
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if main.snake.direction.x !=-1:
                        main.snake.direction=Vector2(1,0)
                if event.key == pygame.K_LEFT:
                    if main.snake.direction.x !=1:
                        main.snake.direction=Vector2(-1,0)
                if event.key == pygame.K_UP:
                    if main.snake.direction.y !=1:
                        main.snake.direction=Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main.snake.direction.y !=-1:
                        main.snake.direction=Vector2(0,1)
                    
                
        game_screen.blit(background, (0, 0))        
        #game_screen.fill((20,120,150))   
        main.draw_elements()
        check_game_over(main)

    else:
        game_screen.fill((20,120,150)) 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = True
                    main = Main()
    
    
    pygame.display.update()
    
    
    clock.tick(60)