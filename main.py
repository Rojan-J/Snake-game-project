import pygame
import sys
import random
from pygame.math import Vector2

import math
import heapq

class Block:
    def __init__(self):
        self.parent_i=10
        self.parent_j=5
        self.f=float("inf")
        self.g=float("inf")
        self.h=0
        self.dir = None

class Main:
    def __init__(self, snake_color):
        self.snake=Snake(snake_color)
        self.fruit=Fruits()
        self.bonus = Pepper()
        self.score = 0
        self.eaten = None
        self.count_down = 0
        self.bonus_count_down = 0
        self.button_click_sound=pygame.mixer.Sound("Project/Snake-game-project/ui-click-menu-modern-interface-select-small-01-230473.mp3")
        self.path = None
        self.direction = None
        
        self.boom_image=pygame.image.load("Project/Snake-game-project/[CITYPNG.COM]HD Bomb Boom Comic Cartoon Explosion PNG - 1000x1000.png")
        self.boom_image = pygame.transform.scale(self.boom_image, (100, 100))
        self.boom_display_time=0
        

    def is_safe(self,row,col):
        return (1<=row<21) and (1<=col<21)
    
    def snake_body_collision(self, row, col, snake_body):
        for block in snake_body:
            if Vector2(row, col) == block:
                return False
        return True

    def fruit_eaten(self,row,col,fruit_pos):
        return row== int(fruit_pos[0]) and col == int(fruit_pos[1])

    def h_value_calculation(self,row,col, fruit_pos):
        return abs(row-fruit_pos[0])+abs(col-fruit_pos[1])

    #def draw_path()
    def reconstruct_path(self,block_inf, fruit_pos):
        path=[]
        direction = []
        current_i,current_j= map(int, fruit_pos)
        
        while block_inf[current_i-1][current_j-1].parent_i != current_i or block_inf[current_i-1][current_j-1].parent_j != current_j:
            path.append((current_i,current_j))
            direction.append(block_inf[current_i-1][current_j-1].dir)
            temporary_i=block_inf[current_i-1][current_j-1].parent_i
            temporary_j=block_inf[current_i-1][current_j-1].parent_j
            current_i , current_j =temporary_i ,temporary_j
        
        direction.reverse()
        path.reverse()
        self.direction = direction
        self.path = path



    def ai_search(self, start_point, fruit_pos):
        visited_blocks=[[False for _ in range(20)] for _ in range(20)] 
        block_inf=[[Block() for _ in range(20)] for _ in range(20)]
        fruit_pos = (int(fruit_pos[0]), int(fruit_pos[1]))
        i,j= map(int, start_point)
        block_inf[i -1][j- 1].f=0
        block_inf[i- 1][j-1].g=0
        block_inf[i-1][j-1].h=0
        block_inf[i-1][j-1].parent_i=i
        block_inf[i-1][j-1].parent_j=j
        block_inf[i-1][j-1].dir = (0,0)
        
        open_list=[]
        heapq.heappush(open_list,(0.0,i,j))
        
        fruit_found=False
        all_path = False
        
       
        while open_list:
            best_block=heapq.heappop(open_list)
            i,j=best_block[1],best_block[2]
            visited_blocks[i- 1][j-1]=True
            
            possible_moves= [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for move in possible_moves:
                next_i=i+move[0]
                next_j=j+move[1]
                
                
                if self.is_safe(next_i,next_j) and self.snake_body_collision(next_i, next_j, self.snake.body):
                    if visited_blocks[next_i-1][next_j-1]: continue

                    if self.fruit_eaten(next_i, next_j, fruit_pos):
                        block_inf[next_i-1][next_j-1].parent_i = i
                        block_inf[next_i-1][next_j-1].parent_j = j
                        block_inf[next_i-1][next_j-1].dir = move
                        self.reconstruct_path(block_inf, fruit_pos)
                        fruit_found = True
                        return 

                    
                    else:
                        g_new=block_inf[i-1][j-1].g+1.0
                        h_new=self.h_value_calculation(next_i,next_j,fruit_pos)
                        f_new=g_new+h_new
                        
                        if block_inf[next_i-1][next_j-1].f==float("inf") or block_inf[next_i-1][next_j-1].f>f_new:
                            heapq.heappush(open_list,(f_new,next_i,next_j))
                            block_inf[next_i-1][next_j-1].f=f_new
                            block_inf[next_i-1][next_j-1].g=g_new
                            block_inf[next_i-1][next_j-1].h=h_new
                            block_inf[next_i-1][next_j-1].parent_i=i
                            block_inf[next_i-1][next_j-1].parent_j=j
                            block_inf[next_i-1][next_j-1].dir=move
                    
        if not fruit_found:
            return True
    
    def backup_path(self, start_point):
        i, j = map(int, start_point)
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        max_free_space = -1
        best_move = None

        for move in possible_moves:
            next_i = i + move[0]
            next_j = j + move[1]
            if self.is_safe(next_i, next_j) and self.snake_body_collision(next_i, next_j, self.snake.body):
                free_space = self.calculate_free_space(next_i, next_j)
                if free_space > max_free_space:
                    max_free_space = free_space
                    best_move = move
        return best_move
    
    def calculate_free_space(self, i, j):
        visited = set()
        stack = [(i, j)]
        free_space = 0

        while stack:
            x, y = stack.pop()
            if (x, y) in visited or not self.is_safe(x, y) or not self.snake_body_collision(x, y, self.snake.body):
                continue
            visited.add((x, y))
            free_space += 1

            # Check adjacent cells
            possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for move in possible_moves:
                stack.append((x + move[0], y + move[1]))

        return free_space
        

    def update(self):    
        if ai_state: 
            self.snake_moving_ai()
        else: self.snake.snake_moving()
        self.check_collision()
        self.draw_elements()

    def check_fruit_pos(self):
        for block in self.snake.body:
            if self.fruit.pos == block:
                return False

        return True
    
    def check_pepper_pos(self):
        for block in self.snake.body:
            if self.bonus.pos == block or self.bonus.pos==self.fruit.pos:
                return False

        if self.bonus.pos == self.fruit.pos:
            return False

        return True

    def draw_path(self):
        self.final_path = self.path
        if self.final_path != None:
            for point in self.final_path[:]:
                
                path_rect = pygame.Rect(int((point[0])*40), int((point[1])*40), 40, 40)
                pygame.draw.circle(game_screen, "Red", ((int((point[0]+0.5)*40), int((point[1]+0.5)*40))), 5)

    def draw_elements(self):
        self.count_down += 1
        score_texts={
            "apple":"+5",
            "strawberry":"+5",
            "pineapple":"+10",
            "blueberry":"+10",
            "mango":"+15"
        }
        
        if self.eaten:
            fruit_score = game_font_3.render(score_texts[self.eaten], True, text_color)
            fruit_score_rect = fruit_score.get_rect(center=(int(self.snake.body[0].x * 40), int(self.snake.body[0].y * 40) - 20))
            game_screen.blit(fruit_score, fruit_score_rect)
        
        
        # if self.boom_display_time>0:
        #     boom_rect = self.boom_image.get_rect(center=(int(self.snake.body[0].x * 40), int(self.snake.body[0].y * 40) - 40))  
        if self.boom_display_time > 0:
        # Position the boom image in front of the snake's head depending on its direction
             
            if self.snake.direction == Vector2(1, 0) or Vector2(-1,0):  
                boom_rect = self.boom_image.get_rect(center=(int(self.snake.body[0].x * 40) + 40, int(self.snake.body[0].y * 40)-40)) 
            elif self.snake.direction == Vector2(0, -1) or Vector2(0,1):  
                boom_rect = self.boom_image.get_rect(center=(int(self.snake.body[0].x * 40)-60, int(self.snake.body[0].y * 40)))  

            game_screen.blit(self.boom_image, boom_rect)
            self.boom_display_time-=1
             
        self.draw_path()
        self.fruit.draw_fruit()
        if not ai_state:
            if self.bonus.pepper_index == 1: self.bonus.draw_pepper()
        self.snake.draw_snake()

        bonus_text = game_font_1.render("Warning: Bonus is finishing!", True, text_color)
        bonus_text_rect = bonus_text.get_rect(center=(440, 100))
        if self.bonus_count_down >=3:
            game_screen.blit(bonus_text, bonus_text_rect)

        if self.count_down > 30: 
            self.eaten = None
            self.count_down = 0

        if tutorial:
            game_screen.blit(home, home_rect)
        
    def check_collision(self):
        global ai_state, blinking_speed, snake_color
        prev_blinking_speed = blinking_speed
        prev_snake_color = snake_color
        snake_head_rect = pygame.Rect(int(self.snake.body[0].x * 40), int(self.snake.body[0].y * 40), 40, 40)
    
        if snake_head_rect.colliderect(self.fruit.rect):
            if ai_state and not tutorial: 
                self.bonus_count_down += 1
                if self.bonus_count_down >= 5:
                    self.bonus_count_down = 0
                    self.path = None
                    pygame.time.set_timer(update_screen, difficulty)
                    ai_state = False
                    blinking_speed = prev_blinking_speed
                    self.snake.snake_color = prev_snake_color
            if self.fruit.fruit_index//3 == 0: 
                self.score += 5
                self.snake.add_block()
                self.eaten = "apple"
                self.count_down = 0
                
            elif self.fruit.fruit_index == 1: 
                self.score += 5
                self.snake.add_block()
                self.eaten  ="strawberry"
                self.count_down = 0

            elif self.fruit.fruit_index == 2: 
                self.score += 10
                for _ in range(2): self.snake.add_block()
                self.eaten  ="pineapple"
                self.count_down = 0

            elif self.fruit.fruit_index == 3: 
                self.score += 10
                for _ in range(2): self.snake.add_block()
                self.eaten  ="blueberry"
                self.count_down = 0

            elif self.fruit.fruit_index == 4: 
                self.score += 15
                for _ in range(3): self.snake.add_block()
                self.eaten  ="mango"
                self.count_down = 0

            self.fruit.randomize()
            self.bonus.index_randomize()
            
            while not self.check_fruit_pos():
                self.fruit.randomize()

            while not self.check_pepper_pos():
                self.bonus.randomize()
            
            self.snake.play_eating_sound()
            
            if ai_state:
                self.path = None  # Clear the path
                self.ai_search(tuple(self.snake.body[0]), tuple(self.fruit.pos))

        if not ai_state:
            if snake_head_rect.colliderect(self.bonus.rect): #AI should enter here
                self.score += 15

                self.boom_display_time=120
                
                for _ in range(3): self.snake.add_block()
                self.bonus.randomize()
                self.bonus.index_randomize()
                
                self.snake.bonus_sound.play()
                while not self.check_pepper_pos():
                    self.bonus.randomize()
                ai_state = True
                pygame.time.set_timer(update_screen, 80)
                prev_blinking_speed = blinking_speed
                blinking_speed = 100
                prev_snake_color = snake_color
                self.snake.snake_color = "Red"

 
    def add_bonus(self):
        self.bonus.draw_pepper()
        
    def play_botton_click(self):
        self.button_click_sound.play()
        
    def snake_moving_ai(self):
        self.snake.last_body = self.snake.body[:]
        if not self.ai_search(tuple(self.snake.body[0]), tuple(self.fruit.pos)):
            self.directions = self.direction
            if self.directions and len(self.directions) > 0:
                self.snake.direction = Vector2(self.directions.pop(0))
                self.snake.last_body = self.snake.body[:]
                if self.snake.new_block==True:
                    prev_body=self.snake.body[:]
                    prev_body.insert(0,prev_body[0]+self.snake.direction)
                    new_body=prev_body
                    self.snake.body=new_body[:] 
                    self.snake.new_block = False
                else:
                    prev_body=self.snake.body[:-1]
                    prev_body.insert(0,prev_body[0]+self.snake.direction)
                    new_body=prev_body
                    self.snake.body=new_body[:]
        else:
            best_move = self.backup_path(tuple(self.snake.body[0]))
            if best_move:
                self.snake.direction = Vector2(best_move)
                prev_body=self.snake.body[:-1]
                prev_body.insert(0,prev_body[0]+self.snake.direction)
                new_body=prev_body
                self.snake.body=new_body[:]
                self.ai_search(tuple(self.snake.body[0]), tuple(self.fruit.pos))
            
            else:
                prev_body=self.snake.body[:-1]
                prev_body.insert(0,prev_body[0]+self.snake.direction)
                new_body=prev_body
                self.snake.body=new_body[:]
                self.ai_search(tuple(self.snake.body[0]), tuple(self.fruit.pos))

                

class Fruits:
    def __init__(self):
        self.apple = pygame.image.load("Project/Snake-game-project/apple1.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (40, 40))
        
        self.strawberry = pygame.image.load("Project/Snake-game-project/strawberry.png").convert_alpha()
        self.strawberry= pygame.transform.scale(self.strawberry, (32, 40))
        
        self.pineapple = pygame.image.load("Project/Snake-game-project/pineapple.png").convert_alpha()
        self.pineapple = pygame.transform.scale(self.pineapple, (27, 40))
        
        self.blueberry = pygame.image.load("Project/Snake-game-project/blueberry.png").convert_alpha()
        self.blueberry = pygame.transform.scale(self.blueberry, (40, 40))
        
        self.mango = pygame.image.load("Project/Snake-game-project/mango.png").convert_alpha()
        self.mango = pygame.transform.scale(self.mango, (40, 40))

        self.x= random.randint(1,19)
        self.y= random.randint(1,19)
        self.pos=Vector2(self.x,self.y)
        self.rect = pygame.Rect(-1, -1, 1, 1)
        self.fruit_index = 0

    def draw_fruit(self):       
        fruit = [self.apple, self.strawberry, self.pineapple, self.blueberry, self.mango]
        surf = fruit[self.fruit_index]
        self.rect = surf.get_rect(center = (int((self.pos.x + 0.5)*40), int((self.pos.y+0.5)*40)))
        game_screen.blit(surf, self.rect)
        
    def randomize(self):
        self.fruit_index = random.choices([0,1,2,3,4],weights=[25,25,20,20,10])[0]
        if self.fruit_index in [1, 2, 4]: y_border = 19
        else: y_border = 20

        if self.fruit_index == 4: x_border = 19
        else: x_border = 20

        self.x= random.randint(1,x_border)
        self.y= random.randint(1, y_border)
        self.pos=Vector2(self.x,self.y)

        
class Snake:
    def __init__(self, snake_color):
        open_eyes = pygame.image.load("Project/Snake-game-project/eyes3.png").convert_alpha()
        open_eyes_scaled = pygame.transform.scale(open_eyes, (40, 40))

        close_eyes = pygame.image.load("Project/Snake-game-project/eye_closed.png").convert_alpha()
        close_eyes_scaled = pygame.transform.scale(close_eyes, (40, 40))         
        
        tongue = pygame.image.load("Project/Snake-game-project/tongue.png").convert_alpha()
        tongue_scaled = pygame.transform.scale(tongue, (40, 40))

        end_eye = pygame.image.load("Project/Snake-game-project/end_eye.png")
    
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.last_body = None
        self.new_block=False
        self.eyes = [open_eyes_scaled, close_eyes_scaled]
        self.eyes_index = 0
        self.end_eyes = pygame.transform.scale(end_eye, (40, 40))
        self.tongue = tongue_scaled
        self.tongue_index = 0
        self.snake_color = snake_color
        
        self.eating_sound=pygame.mixer.Sound("Project/Snake-game-project/apple-munch-40169 (mp3cut.net).mp3")
        self.hitting_wall_sound=pygame.mixer.Sound("Project/Snake-game-project/hitting-wall-85571 (mp3cut.net).mp3")
        self.self_hitting_sound=pygame.mixer.Sound("Project/Snake-game-project/self-hitting-230542.mp3")
        self.game_over_sound=pygame.mixer.Sound("Project/Snake-game-project/game-over-89697.mp3")
        self.bonus_sound=pygame.mixer.Sound("Project/Snake-game-project/supernatural-explosion-104295.mp3")
        
    def draw_snake(self):
        for index, block in enumerate(self.body):
            x=int(block.x *40)
            y=int(block.y*40)
            block_rect=pygame.Rect(x,y,40,40)

            
            if index == 0:  # Head of the snake               
                # Determine which corners to round based on direction
                if self.direction == Vector2(1, 0):  # Moving right
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_top_right_radius=10, border_bottom_right_radius= 10)  # Top-right corner
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
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_top_left_radius=10, border_bottom_left_radius= 10)  # Top-left corner
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
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_top_left_radius=10, border_top_right_radius= 10)  # Top-left corner
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
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_bottom_left_radius=10, border_bottom_right_radius= 10)  # Bottom-left corner
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

        
            elif index <len(self.body)-1:  # Other blocks without rounded corners
                pygame.draw.rect(game_screen, self.snake_color, block_rect) 
            
            else:  #tail block
                prev_block=self.body[index-1]
                direction=block-prev_block
                
                if direction==pygame.Vector2(1,0):
                    pygame.draw.circle(game_screen, self.snake_color, (x, y + 20), 20)  # Rounded tail
                
                elif direction==pygame.Vector2(-1,0):
                    pygame.draw.circle(game_screen, self.snake_color, (x + 40, y + 20), 20)
                
                elif direction==pygame.Vector2(0,1):
                    pygame.draw.circle(game_screen, self.snake_color, (x + 20, y), 20)
                
                elif direction==pygame.Vector2(0,-1):
                    pygame.draw.circle(game_screen, self.snake_color, (x + 20, y + 40), 20)
                
    def draw_end_snake(self):
        for index, block in enumerate(self.body):
            x=int(block.x*40)
            y=int(block.y*40)
            block_rect=pygame.Rect(x,y,40,40)
            
            if index == 0:  # Head of the snake               
                # Determine which corners to round based on direction
                if self.direction == Vector2(1, 0):  # Moving right
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_top_right_radius=10, border_bottom_right_radius= 10)  # Top-right corner
                    end_eyes_scaled = pygame.transform.rotate(self.end_eyes, 0)
                    end_eyes_rect = end_eyes_scaled.get_rect(center=(x + 20, y))
                    rotated_tongue = pygame.transform.rotate(self.tongue, 180)
                    pygame.draw.circle(game_screen, "Black", (x + 35, y+25), 5, 5)
                    tongue_rect = rotated_tongue.get_rect(midleft = (x + 35, y+ 20))

                    
                elif self.direction == Vector2(-1, 0):  # Moving left
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_top_left_radius=10, border_bottom_left_radius= 10)  # Top-left corner
                    end_eyes_scaled = pygame.transform.rotate(self.end_eyes, 0)
                    end_eyes_rect = end_eyes_scaled.get_rect(center=(x + 20, y))
                    pygame.draw.circle(game_screen, "Black", (x +5, y+25), 5, 5)
                    rotated_tongue= pygame.transform.rotate(self.tongue, 0)
                    tongue_rect = rotated_tongue.get_rect(midright = (x + 6, y+ 30))


                elif self.direction == Vector2(0, -1):  # Moving up
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_top_left_radius=10, border_top_right_radius= 10)  # Top-left corner
                    end_eyes_scaled = pygame.transform.rotate(self.end_eyes, -90)
                    end_eyes_rect = end_eyes_scaled.get_rect(center=(x + 35, y +20))
                    pygame.draw.circle(game_screen, "Black", (x +15, y+5), 5, 5)
                    rotated_tongue= pygame.transform.rotate(self.tongue, -90)
                    tongue_rect = rotated_tongue.get_rect(midbottom = (x + 8, y+ 10))



                elif self.direction == Vector2(0, 1):  # Moving down
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_bottom_left_radius=10, border_bottom_right_radius= 10)  # Bottom-left corner
                    end_eyes_scaled = pygame.transform.rotate(self.end_eyes, -90)
                    end_eyes_rect = end_eyes_scaled.get_rect(center=(x + 35, y +20))
                    pygame.draw.circle(game_screen, "Black", (x +15, y+35), 5, 5)
                    rotated_tongue= pygame.transform.rotate(self.tongue, 90)
                    tongue_rect = rotated_tongue.get_rect(midtop = (x + 20, y+ 32))

                game_screen.blit(rotated_tongue, tongue_rect)
                game_screen.blit(end_eyes_scaled, end_eyes_rect)

            else:  #tail block
                if index==len(self.body)-1:
                    prev_block=self.body[index-1]
                    direction=block-prev_block
                            
                    if direction==pygame.Vector2(1,0):
                                pygame.draw.circle(game_screen, self.snake_color, (x, y + 20), 20)  # Rounded tail
                            
                    elif direction==pygame.Vector2(-1,0):
                                pygame.draw.circle(game_screen, self.snake_color, (x + 40, y + 20), 20)
                            
                    elif direction==pygame.Vector2(0,1):
                                pygame.draw.circle(game_screen, self.snake_color, (x + 20, y), 20)
                            
                    elif direction==pygame.Vector2(0,-1):
                                pygame.draw.circle(game_screen, self.snake_color, (x + 20, y + 40), 20)
                else:
                    pygame.draw.rect(game_screen,self.snake_color,block_rect)
                    
    def undo(self):
        self.body = self.last_body


    def snake_moving(self):
        self.last_body = self.body[:]
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
        
    def play_eating_sound(self):
        self.eating_sound.play()
        
    def play_hitting_wall(self):
        self.hitting_wall_sound.play()
        
    def play_self_hitting(self):
        self.self_hitting_sound.play()
        
    def play_game_over(self):
        self.game_over_sound.play()


class Pepper:
    def __init__(self):
        self.x= random.randint(1,19)
        self.y= random.randint(1,19)
        self.pos=Vector2(self.x,self.y)
        self.rect = pygame.Rect(-1, -1, 1, 1)
        self.pepper_index = 0

    def draw_pepper(self):
        pepper = pygame.image.load("Project/Snake-game-project/pepper.png").convert_alpha()
        pepper = pygame.transform.scale(pepper, (27, 40))
        self.rect = pepper.get_rect(center = (int((self.pos.x + 0.5)*40), int((self.pos.y+0.5)*40)))
        game_screen.blit(pepper, self.rect)

    def index_randomize(self):
        self.pepper_index = random.randint(0,8)
        
    def randomize(self):
        self.x= random.randint(1,20)
        self.y= random.randint(1,19)
        self.pos=Vector2(self.x,self.y)
        


def settings():
    global snake_color, background, difficulty, game_state, text_color, blinking_speed, light_bg, night_bg

    background_text = game_font_2.render("Background", True, "Black")
    background_text_rect = background_text.get_rect(center=(440, 60))

    light_bg_icon = pygame.transform.scale(light_bg, (120, 120))
    light_bg_icon_rect = light_bg_icon.get_rect(center= (300, 160))

    night_bg_icon = pygame.transform.scale(night_bg, (120, 120))
    night_bg_icon_rect = night_bg_icon.get_rect(center= (580, 160))

    selected_light_bg = pygame.Rect(light_bg_icon_rect.topleft[0]- 3, light_bg_icon_rect.topleft[1] -3, 126, 126)
    selected_night_bg = pygame.Rect(night_bg_icon_rect.topleft[0]- 3, night_bg_icon_rect.topleft[1] -3, 126, 126)
    selected_bg = [selected_light_bg, selected_night_bg]
    selected_bg_index = 0

    snake_color_text = game_font_2.render("Snake Color", True, "Black")
    snake_color_text_rect = snake_color_text.get_rect(center= (440, 300))

    snake_green = pygame.Rect(180, 340, 120, 120)
    snake_yellow = pygame.Rect(380, 340, 120, 120)
    snake_blue = pygame.Rect(580, 340, 120, 120)

    selected_green = pygame.Rect(snake_green.topleft[0] - 3, snake_green.topleft[1] - 3, 126, 126)
    selected_yellow = pygame.Rect(snake_yellow.topleft[0] - 3, snake_yellow.topleft[1] - 3, 126, 126)
    selected_blue = pygame.Rect(snake_blue.topleft[0] - 3, snake_blue.topleft[1] - 3, 126, 126)
    selected_color = [selected_green, selected_yellow, selected_blue]
    selected_color_index = 0

    difficulty_text = game_font_2.render("Speed", True, "Black")
    difficulty_text_rect = difficulty_text.get_rect(center= (440, 540))

    slow = pygame.image.load('Project/Snake-game-project/turtle2.png').convert_alpha()
    slow = pygame.transform.scale(slow, (120, 120))
    slow = pygame.transform.flip(slow,True, False)
    slow_text = game_font_3.render("Slow", True, "Black")


    medium = pygame.image.load("Project/Snake-game-project/snake2.png").convert_alpha()
    medium = pygame.transform.scale(medium, (120, 120))
    medium_text = game_font_3.render("Medium", True, "Black")

    fast = pygame.image.load("Project/Snake-game-project/cheetah.png").convert_alpha()
    fast = pygame.transform.scale(fast, (120, 120))
    fast_text = game_font_3.render("Fast", True, "Black")

    slow_rect = slow.get_rect(topleft = (180, 580))
    slow_text_rect = slow_text.get_rect(midtop = (240, 700))
    
    medium_rect = medium.get_rect(topleft = (380, 580))
    medium_text_rect  =medium_text.get_rect(midtop = (440, 700))
    
    fast_rect = fast.get_rect(topleft = (580, 580))
    fast_text_rect = fast_text.get_rect(midtop = (640, 700))

    selected_speed = [slow_text, medium_text, fast_text]
    selected_speed_rect = [slow_text_rect, medium_text_rect, fast_text_rect]
    selected_speed_index = 1

    start = game_font_2.render("Start", True, "Black")
    start2_rect = pygame.Rect(540, 760, 200, 100)

    home = game_font_2.render("Home Page", True, "Black")
    home_rect = pygame.Rect(140, 760, 200, 100)

    while True:
        game_screen.fill("#bbff86")
        game_screen.blit(background_text, background_text_rect)

        game_screen.blit(light_bg_icon, light_bg_icon_rect)
        game_screen.blit(night_bg_icon, night_bg_icon_rect)

        game_screen.blit(snake_color_text, snake_color_text_rect)
        pygame.draw.rect(game_screen, "#5a6f19", snake_green)
        pygame.draw.rect(game_screen, "#f5ce18", snake_yellow)
        pygame.draw.rect(game_screen, "#23d4df", snake_blue)

        game_screen.blit(difficulty_text, difficulty_text_rect)
        game_screen.blit(slow, slow_rect)
        game_screen.blit(medium, medium_rect)
        game_screen.blit(fast, fast_rect)

        add_buttomn(game_screen, start2_rect, start)
        add_buttomn(game_screen, home_rect, home)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if light_bg_icon_rect.collidepoint(event.pos):
                    selected_bg_index = 0
                    background = pygame.transform.scale(light_bg, (800, 800))
                    text_color = "Black"

                if night_bg_icon_rect.collidepoint(event.pos):
                    selected_bg_index = 1
                    background = pygame.transform.scale(night_bg, (800, 800))
                    text_color = "White"

                if snake_green.collidepoint(event.pos):
                    selected_color_index = 0
                    snake_color = "#5a6f19"     #Green

                if snake_yellow.collidepoint(event.pos):
                    selected_color_index = 1
                    snake_color = "#f5ce18"     #Yellow
                
                if snake_blue.collidepoint(event.pos):
                    selected_color_index = 2
                    snake_color = "#23d4df"     #Blue

                if slow_rect.collidepoint(event.pos):
                    selected_speed_index = 0
                    difficulty = 200
                    blinking_speed = 40
                    pygame.time.set_timer(update_screen, difficulty)

                if medium_rect.collidepoint(event.pos):
                    selected_speed_index = 1
                    difficulty = 150
                    blinking_speed = 60
                    pygame.time.set_timer(update_screen, difficulty)

                if fast_rect.collidepoint(event.pos):
                    selected_speed_index = 2
                    difficulty = 100
                    blinking_speed = 80
                    pygame.time.set_timer(update_screen, difficulty)

                if start2_rect.collidepoint(event.pos):
                    main.play_botton_click()
                    game_over_sound_played=False
                    game_over_start_time=None
                    pygame.mixer.music.stop()
                    return True
                
                if home_rect.collidepoint(event.pos):
                    main.play_botton_click()
                    background = default_background
                    snake_color = "#5a6f19"
                    text_color = "Black"
                    difficulty = 150
                    blinking_speed = 60
                    return False
                
        pygame.draw.rect(game_screen, "Red", selected_bg[selected_bg_index], width= 3)
        pygame.draw.rect(game_screen, "Red", selected_color[selected_color_index], width= 3)
        game_screen.blit(selected_speed[selected_speed_index], selected_speed_rect[selected_speed_index])




        pygame.display.update()
                

game_state = False
start_page = True
tutorial = False
ai_state = False


def check_game_over(main):
    global game_state
    for block in main.snake.body[1:]:
        if block == main.snake.body[0]:
            main.snake.play_self_hitting()
            game_state = False
    if not 1<= main.snake.body[0].y < 21 or not 1<= main.snake.body[0].x < 21:
        main.snake.play_hitting_wall()
        game_state = False


pygame.mixer.pre_init(44100,-16,2,512)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Project/Snake-game-project/Sneaky-Snitch(chosic.com).mp3")

game_screen=pygame.display.set_mode((880,880),pygame.RESIZABLE | pygame.SCALED)   #pygame.scaled is added to prevent full screen problems
pygame.display.set_caption("Snake")
surface=pygame.Surface((400,400))
light_bg = pygame.image.load("Project/Snake-game-project/bg4.png").convert_alpha()
night_bg = pygame.image.load("Project/Snake-game-project/night4.jpeg").convert_alpha()
default_background = pygame.transform.scale(light_bg, (800, 800))

snake_color = "#5a6f19"
background = default_background
difficulty = 150
blinking_speed = 60
text_color = "Black"

# fruit=Fruits()
# snake=Snake()

clock=pygame.time.Clock()

#Fonts
game_font = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 150) #Name of the game
game_font_1 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 50) #Our brand
game_font_2 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 40) #keys
game_font_3 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 20) #scores 
game_font_4 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 100) #game_over_scores 


#Start Page
start_surf = pygame.image.load("Project/Snake-game-project/start_page.jpg").convert_alpha()
start_surf = pygame.transform.scale(start_surf, (880, 880))

start_title = game_font.render("Snake", True, "Black")
start_title_rect = start_title.get_rect(center = (440, 240))

ronil_brand = game_font_1.render("RONIL", True, "Black")
ronil_brand_rect = ronil_brand.get_rect(center=(440, 340))

start_click = game_font_2.render("Start", True, "Black")
start_rect = pygame.Rect(140, 490, 200, 100)

tutorial_click = game_font_2.render("Tutorial", True, "Black")
tutorial_rect = pygame.Rect(140, 640, 200, 100)

home = pygame.image.load("Project/Snake-game-project/home.png")
home = pygame.transform.scale(home, (40, 40))
home_rect = home.get_rect(center=(440, 860))


def add_buttomn(screen, rect, text, rect_color = "White", shadow_color = "#979797"):
    shadow_rect = pygame.Rect(rect.x + 5, rect.y + 5, 200, 100)
    text_rect = text.get_rect(center= (rect.center))
    pygame.draw.rect(screen, shadow_color, shadow_rect)
    pygame.draw.rect(screen, rect_color, rect)
    game_screen.blit(text, text_rect)

update_screen=pygame.USEREVENT
pygame.time.set_timer(update_screen,150)



main=Main(snake_color)
def display_score(main):
    score = main.score
    score_text = game_font_3.render(f"Score: {score}", True, "White")
    score_text_rect = score_text.get_rect(midleft = (60, 20))
    game_screen.blit(score_text, score_text_rect)


game_over_start_time=None
game_over_sound_played=False

tutorial_speed = 90

while True:
    if not game_state:
        if not start_page:
            main.snake.undo()
            main.snake.draw_end_snake()
            #Gameover Page
            
            if game_over_start_time is None:
                game_over_start_time=pygame.time.get_ticks()
                
            elapsed_time=pygame.time.get_ticks()-game_over_start_time
            
            if elapsed_time>=1000:
                if not game_over_sound_played:
                    main.snake.play_game_over()
                    game_over_sound_played=True
                    
                
                game_over_title = game_font.render("Game Over!", True, text_color)
                if ai_state: game_over_rect = game_over_title.get_rect(center= (440, 120))
                else: game_over_rect = game_over_title.get_rect(center= (440, 240))

                restart = game_font_1.render("Press space to restart", True, text_color)
                restart_rect = restart.get_rect(center=(440, 540))

                home_page = game_font_2.render("Home Page", True, "Black")
                home_page_click_rect = pygame.Rect(340, 590, 200, 100)

                no_path_text = game_font_1.render("Sorry: There is no path available", True, text_color)
                no_path_rect = no_path_text.get_rect(center = (440, 260))
                last_score_text = game_font_4.render(f"Score: {main.score}", True, text_color)
                last_score_rect = last_score_text.get_rect(center= (440, 390))
                game_screen.blit(last_score_text, last_score_rect)
                game_screen.blit(game_over_title, game_over_rect)
                game_screen.blit(restart, restart_rect)
                add_buttomn(game_screen, home_page_click_rect, home_page)
                if ai_state: game_screen.blit(no_path_text, no_path_rect)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = True
                        main = Main(snake_color)
                        game_over_sound_played=False
                        game_over_start_time=None
                        start_page = False


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_page_click_rect.collidepoint(event.pos):
                        main.play_botton_click()
                        background = default_background
                        snake_color = "#5a6f19"
                        text_color = "Black"
                        game_over_sound_played = False
                        game_over_start_time = None
                        difficulty = 150
                        blinking_speed = 60
                        game_state = False
                        main.score =0
                        start_page = True
                        ai_state = False
                        tutorial= False
                        pygame.time.set_timer(update_screen, difficulty)
        else:
            
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1) 

            game_screen.blit(start_surf, (0,0))
            game_screen.blit(start_title, start_title_rect)
            game_screen.blit(ronil_brand, ronil_brand_rect)
            add_buttomn(game_screen, start_rect, start_click)
            add_buttomn(game_screen, tutorial_rect, tutorial_click)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        main.play_botton_click()
                        background = default_background
                        snake_color = "#5a6f19"
                        text_color = "Black"
                        difficulty = 150
                        blinking_speed = 60
                        game_state = False
                        main.score =0
                        start_page = True
                        ai_state = False
                        tutorial = False
                        pygame.time.set_timer(update_screen, difficulty)
                        if settings():
                            game_state = True
                            main = Main(snake_color)
                            start_page = False
                        
                        else:
                            game_state = False
                            start_page = True
                            
                    elif tutorial_rect.collidepoint(event.pos):
                        pygame.time.set_timer(update_screen, tutorial_speed)
                        main.play_botton_click()
                        pygame.mixer.music.stop()
                        tutorial = True
                        game_state = True
                        start_page = False
                        ai_state = True
                        main = Main(snake_color)





    else:
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
                if event.key == pygame.K_ESCAPE:
                    background = default_background
                    snake_color = "#5a6f19"
                    text_color = "Black"
                    game_over_sound_played = False
                    game_over_start_time = None
                    difficulty = 150
                    blinking_speed = 60
                    game_state = False
                    main.score =0
                    start_page = True
                    ai_state = False
                    tutorial = False
                    pygame.time.set_timer(update_screen, difficulty)

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_rect.collidepoint(event.pos):
                    main.play_botton_click()
                    background = default_background
                    snake_color = "#5a6f19"
                    text_color = "Black"
                    difficulty = 150
                    blinking_speed = 60
                    game_state = False
                    start_page = True
                    tutorial = False
                    ai_state =False
                    pygame.time.set_timer(update_screen, difficulty)
                    
        game_screen.fill("#005e20")
        back_rect = background.get_rect(topleft = (40, 40))
        game_screen.blit(background, back_rect)    
        display_score(main)    

        #game_screen.fill((20,120,150))
        check_game_over(main)
        if game_state: main.draw_elements()  
    
    pygame.display.update()
    
    
    clock.tick(blinking_speed)