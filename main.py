import pygame
import sys
import random
from pygame.math import Vector2


class Main:
    
    def __init__(self, snake_color):
        self.snake=Snake(snake_color)
        self.fruit=Fruits()
        self.score = 0
        
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
            self.score += 5
            self.fruit.randomize() 
            self.snake.add_block()
            for block in self.snake.body:
                if self.fruit.pos == block:
                    self.fruit.randomize()
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
        self.x= random.randint(1,19)
        self.y= random.randint(1,19)
        self.pos=Vector2(self.x,self.y)
        self.rect = pygame.Rect(-1, -1, 1, 1)
        
    def draw_fruit(self):
        apple = pygame.image.load("Project/Snake-game-project/apple1.png").convert_alpha()
        scaled_apple = pygame.transform.scale(apple, (40, 40))
        self.rect = scaled_apple.get_rect(topleft = (int(self.pos.x*40), int(self.pos.y*40)))
        game_screen.blit(scaled_apple, self.rect)
        
    def randomize(self):
        self.x= random.randint(1,20)
        self.y= random.randint(1,20)
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


            else:  # Other blocks without rounded corners
                pygame.draw.rect(game_screen, self.snake_color, block_rect) 
            
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

            else:  # Other blocks without rounded corners
                pygame.draw.rect(game_screen, self.snake_color, block_rect) 


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



def settings():
    global snake_color, background, difficulty, game_state, text_color

    background_text = game_font_2.render("Background", True, "Black")
    background_text_rect = background_text.get_rect(center=(440, 60))


    light_bg = pygame.image.load("Project/Snake-game-project/background.png").convert_alpha()
    light_bg = pygame.transform.scale(light_bg, (120, 120))
    light_bg_rect = light_bg.get_rect(center= (300, 160))

    night_bg = pygame.image.load("Project/Snake-game-project/night2.jpg").convert_alpha()
    night_bg = pygame.transform.scale(night_bg, (120, 120))
    night_bg_rect = night_bg.get_rect(center= (580, 160))

    selected_light_bg = pygame.Rect(light_bg_rect.topleft[0]- 3, light_bg_rect.topleft[1] -3, 126, 126)
    selected_night_bg = pygame.Rect(night_bg_rect.topleft[0]- 3, night_bg_rect.topleft[1] -3, 126, 126)
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

        game_screen.blit(light_bg, light_bg_rect)
        game_screen.blit(night_bg, night_bg_rect)

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
                if light_bg_rect.collidepoint(event.pos):
                    selected_bg_index = 0
                    background = pygame.transform.scale(light_bg, (800, 800))
                    text_color = "Black"

                if night_bg_rect.collidepoint(event.pos):
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
                    difficulty = 10

                if medium_rect.collidepoint(event.pos):
                    selected_speed_index = 1
                    difficulty = 60

                if fast_rect.collidepoint(event.pos):
                    selected_speed_index = 2
                    difficulty = 200

                if start2_rect.collidepoint(event.pos):
                    return True
                
                if home_rect.collidepoint(event.pos):
                    background = pygame.transform.scale(light_bg, (800, 800))
                    snake_color = "#5a6f19"
                    text_color = "Black"
                    difficulty = 60
                    return False
                
        pygame.draw.rect(game_screen, "Red", selected_bg[selected_bg_index], width= 3)
        pygame.draw.rect(game_screen, "Red", selected_color[selected_color_index], width= 3)
        game_screen.blit(selected_speed[selected_speed_index], selected_speed_rect[selected_speed_index])




        pygame.display.update()
                

    



game_state = False


def check_game_over(main):
    global game_state
    for block in main.snake.body[1:]:
        if block == main.snake.body[0]:
            game_state = False
    if not 1<= main.snake.body[0].y < 21 or not 1<= main.snake.body[0].x < 21:
        game_state = False

pygame.init()
game_screen=pygame.display.set_mode((880,880))
pygame.display.set_caption("Snake")
surface=pygame.Surface((400,400))
background = pygame.image.load("Project/Snake-game-project/background.png").convert_alpha()
default_background = pygame.transform.scale(background, (800, 800))

snake_color = "#5a6f19"
background = pygame.image.load("Project/Snake-game-project/background.png").convert_alpha()
background = pygame.transform.scale(background, (800, 800))
difficulty = 60
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


while True:
    if not game_state:
        if main.score != 0:
            main.snake.undo()
            main.snake.draw_end_snake()
            #Gameover Page
            game_over_title = game_font.render("Game Over!", True, text_color)
            game_over_rect = game_over_title.get_rect(center= (440, 240))

            restart = game_font_1.render("Press space to restart", True, text_color)
            restart_rect = restart.get_rect(center=(440, 540))

            home_page = game_font_2.render("Home Page", True, "Black")
            home_page_click_rect = pygame.Rect(340, 590, 200, 100)

            last_score_text = game_font_4.render(f"Score: {main.score}", True, text_color)
            last_score_rect = last_score_text.get_rect(center= (440, 390))
            game_screen.blit(last_score_text, last_score_rect)
            game_screen.blit(game_over_title, game_over_rect)
            game_screen.blit(restart, restart_rect)
            add_buttomn(game_screen, home_page_click_rect, home_page)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = True
                        main = Main(snake_color)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_page_click_rect.collidepoint(event.pos):
                        background = default_background
                        snake_color = "#5a6f19"
                        text_color = "Black"
                        difficulty = 60
                        game_state = False
                        main.score =0
        else:

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
                        if settings():
                            game_state = True
                            main = Main(snake_color)
                        
                        else:
                            game_state = False
                            main.score = 0

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
                    
                
        game_screen.fill("#005e20")
        game_screen.blit(background, (40, 40))    
        display_score(main)    
        #game_screen.fill((20,120,150))
        check_game_over(main)
        if game_state: main.draw_elements()  
    
    pygame.display.update()
    
    
    clock.tick(difficulty)