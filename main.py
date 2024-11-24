import pygame
import sys
import random
from pygame.math import Vector2  #using vector2 to represent the 2D positions in game_screen grid

import math
import heapq

class Block:    #representing a block class of properties for path finding
    def __init__(self):
        self.parent_i=10        #row and col indexes for start position
        self.parent_j=5
        self.f=float("inf")     #f= g+h
        self.g=float("inf")     #g: movement cost from start node to a given node
        self.h=0                #h: cost to move from the given node to the final destination
        self.dir = None

class Main:     #containing snakke, fruit and AI logic
    def __init__(self, snake_color):
        self.snake=Snake(snake_color)
        self.fruit=Fruits()
        self.bonus = Bonus()
        self.score = 0
        self.eaten = None
        self.count_down = 0
        self.bonus_count_down = 0
        self.button_click_sound=pygame.mixer.Sound("Project/Snake-game-project/ui-click-menu-modern-interface-select-small-01-230473.mp3")
        self.path = None
        self.direction = None
        
        #load explosion image for bonus part
        self.boom_image=pygame.image.load("Project/Snake-game-project/[CITYPNG.COM]HD Bomb Boom Comic Cartoon Explosion PNG - 1000x1000.png")
        self.boom_image = pygame.transform.scale(self.boom_image, (100, 100))
        self.boom_display_time=0
        self.mango_bonus = False    #flag indicating if mango bonus is active
        self.mango_count_down  =0   #timer for mango bonus duration
        
    #A* algorithm part:
    
    def is_safe(self,row,col):     #check if snake's position is within safe boundaries
        return (1<=row<21) and (1<=col<21)
    
    def snake_body_collision(self, row, col, snake_body):  #check if snake's body collides with itself at a give position
        for block in snake_body:
            if Vector2(row, col) == block:
                return False
        return True

    def fruit_eaten(self,row,col,fruit_pos):     
        return row== int(fruit_pos[0]) and col == int(fruit_pos[1])

    def h_value_calculation(self,row,col, fruit_pos):    #calculate the manhattan distance value as h
        return abs(row-fruit_pos[0])+abs(col-fruit_pos[1])

    
    def reconstruct_path(self,block_inf, fruit_pos):     #reconstructs the path from fruit to the snake's head current position
        path=[]
        direction = []
        current_i,current_j= map(int, fruit_pos)         #start from the fruit position(we are going backward)
        
        #continue tracking back until the current cell no longer has a parent
        while block_inf[current_i-1][current_j-1].parent_i != current_i or block_inf[current_i-1][current_j-1].parent_j != current_j:
            path.append((current_i,current_j))
            direction.append(block_inf[current_i-1][current_j-1].dir)
            #update current position to its parent
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
        
        #set the start block's costs to 0
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
        
       
        while open_list:       #while there are nodes to process
            best_block=heapq.heappop(open_list)     #get block with lowest f cost
            i,j=best_block[1],best_block[2]
            visited_blocks[i- 1][j-1]=True          #mark block as visited
            
            possible_moves= [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for move in possible_moves:
                next_i=i+move[0]
                next_j=j+move[1]
                
                
                if self.is_safe(next_i,next_j) and self.snake_body_collision(next_i, next_j, self.snake.body):
                    if visited_blocks[next_i-1][next_j-1]: continue   #skip visited blocks already

                    if self.fruit_eaten(next_i, next_j, fruit_pos):   #if the move reaches the fruit
                        block_inf[next_i-1][next_j-1].parent_i = i
                        block_inf[next_i-1][next_j-1].parent_j = j
                        block_inf[next_i-1][next_j-1].dir = move
                        self.reconstruct_path(block_inf, fruit_pos)
                        fruit_found = True
                        return 

                    
                    else:       #calculate costs for this block
                        g_new=block_inf[i-1][j-1].g+1.0
                        h_new=self.h_value_calculation(next_i,next_j,fruit_pos)
                        f_new=g_new+h_new
                        
                        #update the block if a better path is found
                        if block_inf[next_i-1][next_j-1].f==float("inf") or block_inf[next_i-1][next_j-1].f>f_new:
                            heapq.heappush(open_list,(f_new,next_i,next_j))
                            block_inf[next_i-1][next_j-1].f=f_new
                            block_inf[next_i-1][next_j-1].g=g_new
                            block_inf[next_i-1][next_j-1].h=h_new
                            block_inf[next_i-1][next_j-1].parent_i=i
                            block_inf[next_i-1][next_j-1].parent_j=j
                            block_inf[next_i-1][next_j-1].dir=move
                    
        if not fruit_found:  #no path found
            return True     
    
    #designing a backuo path finding strategy if the optimal path is not available
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
    
    def calculate_free_space(self, i, j):     #calculate free space around a given position for when there is no optimal path to reach the fruit right awat
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

    def check_fruit_pos(self):    #varify if the fruit's position overlaps with snake's body
        for block in self.snake.body:
            if self.fruit.pos == block:
                return False

        return True
    
    def check_pepper_pos(self):  #varify if the pepper's position overlaps with snake's body or fruit's position
        for block in self.snake.body:
            if self.bonus.pos == block or self.bonus.pos==self.fruit.pos:
                return False

        return True

    def draw_path(self):        #draw the path tha snake is going to follow from A* algorithm
        self.final_path = self.path
        if self.final_path != None:
            for point in self.final_path[:]:
                
                path_rect = pygame.Rect(int((point[0])*40), int((point[1])*40), 40, 40)
                pygame.draw.circle(game_screen, "Red", ((int((point[0]+0.5)*40), int((point[1]+0.5)*40))), 5)

    def draw_elements(self):   #draw all the elements(snake,fruits,score,pepper)
        self.count_down += 1   #as a simple timer to manage the duration of temporary visual effects in the game
        
        score_texts={
            "apple":"+5",
            "strawberry":"+5",
            "pineapple":"+10",
            "blueberry":"+10",
        }
        
        if self.eaten:
            fruit_score = game_font_3.render(score_texts[self.eaten], True, text_color)
            fruit_score_rect = fruit_score.get_rect(center=(int(self.snake.body[0].x * 40), int(self.snake.body[0].y * 40) - 20))
            game_screen.blit(fruit_score, fruit_score_rect)
         
        if self.mango_bonus:
            self.mango_count_down += 1
            #displaying mango bonus massage
            mango_eaten = game_font_1.render("+15; Mango has been eaten!", True, text_color)
            mango_eaten_rect = mango_eaten.get_rect(center = (440, 110))
            game_screen.blit(mango_eaten, mango_eaten_rect)
        
        if self.boom_display_time > 0:   #draw explosion effect when pepper is eaten
             
            if self.snake.direction == Vector2(1, 0) or Vector2(-1,0):   #horizontal movement
                boom_rect = self.boom_image.get_rect(center=(int(self.snake.body[0].x * 40) + 40, int(self.snake.body[0].y * 40)-40)) 
            elif self.snake.direction == Vector2(0, -1) or Vector2(0,1):   #vertical movement
                boom_rect = self.boom_image.get_rect(center=(int(self.snake.body[0].x * 40)-60, int(self.snake.body[0].y * 40)))  

            game_screen.blit(self.boom_image, boom_rect)
            self.boom_display_time-=1
             
        self.draw_path()
        self.fruit.draw_fruit()
        
        if not ai_state:    #draw pepper only in non-ai mode
            if self.bonus.bonus_index == 1: self.bonus.draw_bonus()

        if self.bonus.bonus_index == 2: self.bonus.draw_bonus()    #draw mango randomly both in ai and player mode
        self.snake.draw_snake()

        bonus_text = game_font_1.render("Warning: Bonus is finishing!", True, text_color)
        bonus_text_rect = bonus_text.get_rect(center=(440, 100))
        
        if self.bonus_count_down >=3:
            game_screen.blit(bonus_text, bonus_text_rect)

        if self.count_down > 30: 
            self.eaten = None
            self.count_down = 0
            
        if self.mango_count_down > 60:  #dactivate mango bonus after 60 cycles 
            self.mango_bonus = False
            self.mango_count_down = 0

        if tutorial:
            game_screen.blit(home, home_rect)
        
    
    #hanndle collisions between snake, fruits, pepper and wall
    def check_collision(self): 
        global ai_state, blinking_speed, snake_color
        prev_blinking_speed = blinking_speed
        prev_snake_color = snake_color
        
        snake_head_rect = pygame.Rect(int(self.snake.body[0].x * 40), int(self.snake.body[0].y * 40), 40, 40)
    
        if snake_head_rect.colliderect(self.fruit.rect):    #check if the snake eats the fruit
            if ai_state and not tutorial: 
                self.bonus_count_down += 1
                if self.bonus_count_down >= 5:
                    self.bonus_count_down = 0
                    self.path = None
                    pygame.time.set_timer(update_screen, difficulty)
                    ai_state = False
                    blinking_speed = prev_blinking_speed
                    self.snake.snake_color = prev_snake_color
            
            #add to the score and snake length based on th fruit that is eaten        
            if self.fruit.fruit_index == 0: 
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

            #randomize fruit and pepper positions
            self.fruit.randomize()
            self.bonus.index_randomize()
            
            while not self.check_fruit_pos():
                self.fruit.randomize()

            while not self.check_pepper_pos():
                self.bonus.randomize()
            
            self.snake.play_eating_sound()
            
            if ai_state:   #recompute ai path after eating the fruit
                self.path = None  # Clear the path
                self.ai_search(tuple(self.snake.body[0]), tuple(self.best_goal()))


        if snake_head_rect.colliderect(self.bonus.rect): #AI should enter here
            if self.bonus.bonus_index == 1:
                self.score += 15

                self.boom_display_time=120
                
                for _ in range(3): self.snake.add_block()  #add 3 blocks to snake's body
                
                self.bonus.randomize()
                self.bonus.index_randomize()
                self.snake.pepper_sound.play()
                
                while not self.check_pepper_pos():
                    self.bonus.randomize()
                ai_state = True
                pygame.time.set_timer(update_screen, 80)
                prev_blinking_speed = blinking_speed
                blinking_speed = 100
                prev_snake_color = snake_color
                self.snake.snake_color = "Red"
            
            elif self.bonus.bonus_index == 2:
                self.mango_bonus = True   #activate mango bonus
                self.score += 15          
                for _ in range(3): self.snake.add_block()  #add 3 blocks to snake's body
                
                self.bonus.randomize()
                self.bonus.index_randomize()
                while not self.check_pepper_pos():
                    self.bonus.randomize()
                self.snake.mango_sound.play()

 
        
    def play_botton_click(self):
        self.button_click_sound.play()

    def best_goal(self):  #determine the best target(mango or other fruits) for the snake based on its distance to target
        
        if self.bonus.bonus_index == 2:
            scores = {
                0: 5,
                1 : 5,
                2 :10,
                3 :10,
                4 :15
            }
            
            #calculate bonus point for mango based on its score and h value
            bonus_point = 15 /self.h_value_calculation(int(self.snake.body[0].x), int(self.snake.body[0].y), self.bonus.pos)
            #calculate bonus point for other fruits
            fruit_point = scores[self.fruit.fruit_index] / self.h_value_calculation(int(self.snake.body[0].x), int(self.snake.body[0].y), self.fruit.pos)

            if bonus_point > fruit_point:   #choose the best target based on their points
                return self.bonus.pos
        return self.fruit.pos  
        
    def snake_moving_ai(self):
        
        self.snake.last_body = self.snake.body[:]
        
        if not self.ai_search(tuple(self.snake.body[0]), tuple(self.best_goal())):
            self.directions = self.direction
            
            if self.directions and len(self.directions) > 0:
                self.snake.direction = Vector2(self.directions.pop(0)) #set the snake's direction to the next step of path
                self.snake.last_body = self.snake.body[:]
                
                if self.snake.new_block==True:     #check if the snake has grown by eating a fruit
                    prev_body=self.snake.body[:]
                    prev_body.insert(0,prev_body[0]+self.snake.direction) #a new head is added
                    new_body=prev_body
                    self.snake.body=new_body[:]   #update the snake's body with thenew block
                    self.snake.new_block = False
                    
                else:                                #if there is no collisio with fruit yet
                    prev_body=self.snake.body[:-1]   #move the snake by removing the tail and adding a nnew head
                    prev_body.insert(0,prev_body[0]+self.snake.direction)
                    new_body=prev_body
                    self.snake.body=new_body[:]
                    
        else:       #use a backup path finding strategy if no optimal path is found
            best_move = self.backup_path(tuple(self.snake.body[0]))
            
            if best_move:  #if backup strategy worked, move the snake i the best move direction
                self.snake.direction = Vector2(best_move)
                prev_body=self.snake.body[:-1]
                prev_body.insert(0,prev_body[0]+self.snake.direction)
                new_body=prev_body
                self.snake.body=new_body[:]
                self.ai_search(tuple(self.snake.body[0]), tuple(self.best_goal()))
            
            else:        #continue moving in the new direction if no valid path exists
                prev_body=self.snake.body[:-1]
                prev_body.insert(0,prev_body[0]+self.snake.direction)
                new_body=prev_body
                self.snake.body=new_body[:]
                self.ai_search(tuple(self.snake.body[0]), tuple(self.best_goal()))

                
class Fruits:
    def __init__(self):
        
        #load fruit images and scale them
        self.apple = pygame.image.load("Project/Snake-game-project/apple1.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (40, 40))
        
        self.strawberry = pygame.image.load("Project/Snake-game-project/strawberry.png").convert_alpha()
        self.strawberry= pygame.transform.scale(self.strawberry, (32, 40))
        
        self.pineapple = pygame.image.load("Project/Snake-game-project/pineapple.png").convert_alpha()
        self.pineapple = pygame.transform.scale(self.pineapple, (27, 40))
        
        self.blueberry = pygame.image.load("Project/Snake-game-project/blueberry.png").convert_alpha()
        self.blueberry = pygame.transform.scale(self.blueberry, (40, 40))
        

        #set initial fruit positions and index
        self.x= random.randint(1,19)
        self.y= random.randint(1,19)
        self.pos=Vector2(self.x,self.y)
        self.rect = pygame.Rect(-1, -1, 1, 1)   #rec for collision detection
        self.fruit_index = 0   #determines the type of fruit which is going to display

    def draw_fruit(self):       
        fruit = [self.apple, self.strawberry, self.pineapple, self.blueberry]
        surf = fruit[self.fruit_index]
        
        #set the rect for the chosen fruit for its collision detection
        self.rect = surf.get_rect(center = (int((self.pos.x + 0.5)*40), int((self.pos.y+0.5)*40)))
        game_screen.blit(surf, self.rect)   #draw the fruit on the game screen
        
    def randomize(self):
        #choose the fruit type that is going to display
        #fruits with higher score has a bit less chance to display on the screen
        self.fruit_index = random.choices([0,1,2,3],weights=[25,25,20,20])[0]
        self.x= random.randint(1,20)
        self.y= random.randint(1, 20)
        self.pos=Vector2(self.x,self.y)

        
class Snake:
    #load the different phases of snake's eyes( to show its blinking) and its tongue and scale them 
    def __init__(self, snake_color):
        open_eyes = pygame.image.load("Project/Snake-game-project/eyes3.png").convert_alpha()
        open_eyes_scaled = pygame.transform.scale(open_eyes, (40, 40))

        close_eyes = pygame.image.load("Project/Snake-game-project/eye_closed.png").convert_alpha()
        close_eyes_scaled = pygame.transform.scale(close_eyes, (40, 40))         
        
        tongue = pygame.image.load("Project/Snake-game-project/tongue.png").convert_alpha()
        tongue_scaled = pygame.transform.scale(tongue, (40, 40))

        end_eye = pygame.image.load("Project/Snake-game-project/end_eye.png")
    
        #initialize snake's body with 3 blocks
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)  #snake initially is moving to the right
        self.last_body = None
        self.new_block=False
        self.eyes = [open_eyes_scaled, close_eyes_scaled]
        self.eyes_index = 0
        self.end_eyes = pygame.transform.scale(end_eye, (40, 40))
        self.tongue = tongue_scaled
        self.tongue_index = 0
        self.snake_color = snake_color
        
        #load sound effects for various actions
        self.eating_sound=pygame.mixer.Sound("Project/Snake-game-project/apple-munch-40169 (mp3cut.net).mp3")
        self.hitting_wall_sound=pygame.mixer.Sound("Project/Snake-game-project/hitting-wall-85571 (mp3cut.net).mp3")
        self.self_hitting_sound=pygame.mixer.Sound("Project/Snake-game-project/self-hitting-230542.mp3")
        self.game_over_sound=pygame.mixer.Sound("Project/Snake-game-project/game-over-89697.mp3")
        self.pepper_sound=pygame.mixer.Sound("Project/Snake-game-project/supernatural-explosion-104295.mp3")
        self.mango_sound=pygame.mixer.Sound("Project/Snake-game-project/sound-effect-twinklesparkle-115095.mp3")
        
    def draw_snake(self):    #draw the snake on the game screen
        
        for index, block in enumerate(self.body):
            x=int(block.x *40)
            y=int(block.y*40)
            block_rect=pygame.Rect(x,y,40,40)

            
            if index == 0:  # Head of the snake               
                # Determine which corners to round based on direction
                if self.direction == Vector2(1, 0):  # Moving right
                    pygame.draw.rect(game_screen, self.snake_color, block_rect, border_top_right_radius=10, border_bottom_right_radius= 10)  # Top-right corner
                    #draw eyes on the snake's head
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
                
                #cycle through eye animations(blinking and hitting the wall phase)
                if int(self.eyes_index) == 0: self.eyes_index += 0.02
                else: self.eyes_index += 0.05
                if self.eyes_index > 2: self.eyes_index = 0

                #cycle through tongue animations
                self.tongue_index += 0.02
                if self.tongue_index > 2: self.tongue_index = 0

        
            elif index <len(self.body)-1:  # Other blocks without rounded corners
                pygame.draw.rect(game_screen, self.snake_color, block_rect) 
            
            else:  #tail block
                prev_block=self.body[index-1]
                direction=block-prev_block
                
                if direction==pygame.Vector2(1,0):  #moving right
                    pygame.draw.circle(game_screen, self.snake_color, (x, y + 20), 20)  # Rounded tail
                
                elif direction==pygame.Vector2(-1,0):  #moving left
                    pygame.draw.circle(game_screen, self.snake_color, (x + 40, y + 20), 20)
                
                elif direction==pygame.Vector2(0,1):  #moving down
                    pygame.draw.circle(game_screen, self.snake_color, (x + 20, y), 20)
                
                elif direction==pygame.Vector2(0,-1):  #moving up
                    pygame.draw.circle(game_screen, self.snake_color, (x + 20, y + 40), 20)
                
    def draw_end_snake(self):
        for index, block in enumerate(self.body):
            x=int(block.x*40)
            y=int(block.y*40)
            block_rect=pygame.Rect(x,y,40,40)
            
            if index == 0:              
                if self.direction == Vector2(1, 0): 
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
                    
    def undo(self):  #undo the snake's last move when collision happen
        self.body = self.last_body  #reset the body to its previous state


    def snake_moving(self):
        self.last_body = self.body[:]  #save the current body if undoing is needed
        
        if self.new_block: #add a new block at the front if a fruit was eaten
            prev_body=self.body[:]
            prev_body.insert(0,prev_body[0]+self.direction) #extendig the head
            new_body=prev_body
            self.body=new_body[:] 
            self.new_block = False
            
        else:  #normal moving/ no fruit was eaten
            prev_body=self.body[:-1]  #remove the tail
            prev_body.insert(0,prev_body[0]+self.direction) #move the head
            new_body=prev_body
            self.body=new_body[:] #update the body


            
            
    def add_block(self):  #for when a fruit was eaten
        self.new_block=True
        
    #play sound effects    
    def play_eating_sound(self):
        self.eating_sound.play()
        
    def play_hitting_wall(self):
        self.hitting_wall_sound.play()
        
    def play_self_hitting(self):
        self.self_hitting_sound.play()
        
    def play_game_over(self):
        self.game_over_sound.play()


class Bonus:
    def __init__(self):
        #upload and scale the bonus image
        self.pepper = pygame.image.load("Project/Snake-game-project/pepper.png").convert_alpha()
        self.pepper = pygame.transform.scale(self.pepper, (27, 40))

        self.mango = pygame.image.load("Project/Snake-game-project/mango.png").convert_alpha()
        self.mango = pygame.transform.scale(self.mango, (40, 40))

        self.x= random.randint(1,19)
        self.y= random.randint(1,19)
        self.pos=Vector2(self.x,self.y)
        self.rect = pygame.Rect(-1, -1, 1, 1)  #preholder rect for collisionn
        self.bonus_index = 0

    def draw_bonus(self):
        #determine to display which bous based on their index
        if self.bonus_index == 1: 
            self.rect = self.pepper.get_rect(center = (int((self.pos.x + 0.5)*40), int((self.pos.y+0.5)*40)))
            game_screen.blit(self.pepper, self.rect) #draw the pepper on the screen
        
        elif self.bonus_index == 2:
            self.rect = self.mango.get_rect(center = (int((self.pos.x + 0.5)*40), int((self.pos.y+0.5)*40)))
            game_screen.blit(self.mango, self.rect) #draw the mango on the screen

    def index_randomize(self):
        self.bonus_index = random.randint(0,8)   #chooose the random index for the pepper( the pepper is going to display only if 1 was selected)
        
    def randomize(self):
        self.x= random.randint(1,20)
        self.y= random.randint(1,19)
        self.pos=Vector2(self.x,self.y)
        

# set game settings(background, snake color setting, speed and etc...)
def settings():
    global snake_color, background, difficulty, game_state, text_color, blinking_speed, light_bg, night_bg

    #in the first part we are going to display labels, icons and define scaled rects and positions for them in the setting screen
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

    #define bottons for starting the game and returning to the home page
    start = game_font_2.render("Start", True, "Black")
    start2_rect = pygame.Rect(540, 760, 200, 100)

    home = game_font_2.render("Home Page", True, "Black")
    home_rect = pygame.Rect(140, 760, 200, 100)

    #setting screen loop
    while True:
        game_screen.fill("#bbff86")  #fill the screen with a light green background
        game_screen.blit(background_text, background_text_rect)  #display background

        #display selection icons :
        
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
        
        #process events for interactivity
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                #control background selection
                if light_bg_icon_rect.collidepoint(event.pos):
                    selected_bg_index = 0
                    background = pygame.transform.scale(light_bg, (800, 800))
                    text_color = "Black"

                if night_bg_icon_rect.collidepoint(event.pos):
                    selected_bg_index = 1
                    background = pygame.transform.scale(night_bg, (800, 800))
                    text_color = "White"

                #control snake's color selection
                if snake_green.collidepoint(event.pos):
                    selected_color_index = 0
                    snake_color = "#5a6f19"     #Green

                if snake_yellow.collidepoint(event.pos):
                    selected_color_index = 1
                    snake_color = "#f5ce18"     #Yellow
                
                if snake_blue.collidepoint(event.pos):
                    selected_color_index = 2
                    snake_color = "#23d4df"     #Blue
                    
                #control speeed selection
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

                #starting the game botton in the setting screen
                if start2_rect.collidepoint(event.pos):
                    main.play_botton_click()
                    game_over_sound_played=False  #control the sounds and game over part to not show up
                    game_over_start_time=None
                    pygame.mixer.music.stop()
                    ai_state=False
                    return True  #start the game
                
                #returning to home page botton
                if home_rect.collidepoint(event.pos):
                    main.play_botton_click()
                    background = default_background
                    snake_color = "#5a6f19"
                    text_color = "Black"
                    difficulty = 150
                    blinking_speed = 60
                    return False  #return to home page
                
        #draw selected items in setting screen with red borders        
        pygame.draw.rect(game_screen, "Red", selected_bg[selected_bg_index], width= 3)
        pygame.draw.rect(game_screen, "Red", selected_color[selected_color_index], width= 3)
        game_screen.blit(selected_speed[selected_speed_index], selected_speed_rect[selected_speed_index])




        pygame.display.update()
                
#iitialize global game states
game_state = False
start_page = True
tutorial = False
ai_state = False


def check_game_over(main):
    global game_state
    #check for collision with the snake's own body
    for block in main.snake.body[1:]:
        if block == main.snake.body[0]:
            main.snake.play_self_hitting()  #play self hitting collision sound
            game_state = False   #end the game
    
    #check for collision with the walll
    if not 1<= main.snake.body[0].y < 21 or not 1<= main.snake.body[0].x < 21:
        main.snake.play_hitting_wall()  #play wall hitting collsion sound
        game_state = False


pygame.mixer.pre_init(44100,-16,2,512)   #pre initialize soundtrack setting

pygame.init()   #initialize pygame
pygame.mixer.init()
pygame.mixer.music.load("Project/Snake-game-project/Sneaky-Snitch(chosic.com).mp3")

#game screen setup
game_screen=pygame.display.set_mode((880,880),pygame.RESIZABLE | pygame.SCALED)   #pygame.scaled is added to prevent full screen problems
pygame.display.set_caption("Snake")
surface=pygame.Surface((400,400))

#load backgrounds
light_bg = pygame.image.load("Project/Snake-game-project/bg4.png").convert_alpha()
night_bg = pygame.image.load("Project/Snake-game-project/night4.jpeg").convert_alpha()
default_background = pygame.transform.scale(light_bg, (800, 800))

#default settings
snake_color = "#5a6f19"    #default snake color(green)
background = default_background   
difficulty = 150
blinking_speed = 60
text_color = "Black"

#create a clock object to control the game's timing and frame rate
clock=pygame.time.Clock()

#Fonts
game_font = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 150) #Name of the game
game_font_1 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 50) #Our brand
game_font_2 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 40) #keys
game_font_3 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 20) #scores 
game_font_4 = pygame.font.Font("Project/Snake-game-project/JungleAdventurer.ttf", 100) #game_over_scores 


#Start Page setup
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

#set home botton to put in tutorial screen
home = pygame.image.load("Project/Snake-game-project/home.png")
home = pygame.transform.scale(home, (40, 40))
home_rect = home.get_rect(center=(440, 860))

#create bottons with shadows
def add_buttomn(screen, rect, text, rect_color = "White", shadow_color = "#979797"):
    shadow_rect = pygame.Rect(rect.x + 5, rect.y + 5, 200, 100)
    text_rect = text.get_rect(center= (rect.center))
    pygame.draw.rect(screen, shadow_color, shadow_rect)
    pygame.draw.rect(screen, rect_color, rect)
    game_screen.blit(text, text_rect)

update_screen=pygame.USEREVENT
pygame.time.set_timer(update_screen,150)  #set up a timer event that triggers every 150ms



main=Main(snake_color)

#display score on the game screen
def display_score(main):
    score = main.score  #get the current score from thr main game 
    score_text = game_font_3.render(f"Score: {score}", True, "White")
    score_text_rect = score_text.get_rect(midleft = (60, 20))
    game_screen.blit(score_text, score_text_rect)


game_over_start_time=None
game_over_sound_played=False

tutorial_speed = 90  #set tutorial speed



#main game loop( it runs until the game ends)
while True:
    if not game_state:  #check if the game is not in the play
        if not start_page:
            main.snake.undo()
            main.snake.draw_end_snake()  #draw the snake in its final state
            
            if game_over_start_time is None:   #game over page after collision with itself or wall
                game_over_start_time=pygame.time.get_ticks()  #record the time when gameover starts
                
            elapsed_time=pygame.time.get_ticks()-game_over_start_time
            
            if elapsed_time>=1000:   #display gameover screen after 1s delay (to avoid the sound effects of collision and game over to be mixed)
                if not game_over_sound_played:
                    main.snake.play_game_over()
                    game_over_sound_played=True   #mark the game over sound as played
                    
                #create the game over text ,score and bottons
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
                
            for event in pygame.event.get():  #handle events during gameover screen
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  #restart the game when space key is pressed
                        game_state = True
                        main = Main(snake_color)   #create a new main game object
                        game_over_sound_played=False   #reset sound flag 
                        game_over_start_time=None     #reset timer
                        start_page = False      #switch to main game state


                if event.type == pygame.MOUSEBUTTONDOWN:   #home botton click event
                    if home_page_click_rect.collidepoint(event.pos):
                        main.play_botton_click()
                        background = default_background
                        snake_color = "#5a6f19"
                        text_color = "Black"
                        game_over_sound_played = False
                        game_over_start_time = None
                        ai_state = False
                        tutorial = False
                        difficulty = 150
                        blinking_speed = 60
                        game_state = False
                        main.score =0
                        start_page = True    #return to start page
       
        #start page (before game starts)       
        else:
            
            if not pygame.mixer.music.get_busy():   #play background music if not playing already
                pygame.mixer.music.play(-1)         #put the background music in a loop

            #create start game screen title and bottons
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
                    if start_rect.collidepoint(event.pos):    #if start botton is clicked
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
                        if settings():                        #show settig page
                            game_state = True
                            main = Main(snake_color)
                            start_page = False
                        
                        else:
                            game_state = False
                            start_page = True       #stay at the start page
                            
                    elif tutorial_rect.collidepoint(event.pos):   #if tutorial botton is clicked
                        pygame.time.set_timer(update_screen, tutorial_speed)    #set update timer for tutorial
                        main.play_botton_click()
                        pygame.mixer.music.stop()     #stop background music for tutorial
                        tutorial = True
                        game_state = True
                        start_page = False
                        ai_state = True
                        main = Main(snake_color)




    #main game loop when the game is running
    else:     
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == update_screen:  #update event for game progress
                main.update()
                
            #keyboard setting to move the snake
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  #move right
                    if main.snake.direction.x !=-1:
                        main.snake.direction=Vector2(1,0)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:   #move left
                    if main.snake.direction.x !=1:
                        main.snake.direction=Vector2(-1,0)
                if event.key == pygame.K_UP or event.key == pygame.K_w:     #move up
                    if main.snake.direction.y !=1 :
                        main.snake.direction=Vector2(0,-1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:    #move down
                    if main.snake.direction.y !=-1:
                        main.snake.direction=Vector2(0,1)
                        
                if event.key == pygame.K_ESCAPE:    #return to start page(esc key)
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
                if home_rect.collidepoint(event.pos):   #if home botton is clicked
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
                    
        #fill the game screen with selected background color            
        game_screen.fill("#005e20")
        back_rect = background.get_rect(topleft = (40, 40))   #set a position for background
        #display the background and current score
        game_screen.blit(background, back_rect)    
        display_score(main)    

        #check if the game is over
        check_game_over(main)
        if game_state: main.draw_elements()  
    
    pygame.display.update()
    
    
    clock.tick(blinking_speed)   #control the game's format rate