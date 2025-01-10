import pygame 
import random
pygame.init()

window_width = 800
window_height =600

screen = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption("Sliding Puzzle Game")

FPS = 10 #frames per seconds 
clock = pygame.time.Clock()

WHITE = ((255,255,255))
BLACK = ((0,0,0))
RED = ((255,0,0))
GREEN = ((0,255,0))
BLUE = ((0,0,255))
GREY = ((128,128,128))

bg = pygame.image.load("villa sliding game.jpg")
bg = pygame.transform.scale(bg, (800,600))
bg_rect = bg.get_rect()  #adds a border around the image
bg_rect.topleft = (0,0)  #can use this variable to make the image move on the screen

font_title = pygame.font.Font('Hello Avocado.ttf', 64)
font_content = pygame.font.Font('Hello Avocado.ttf', 30)

game_over_text = font_title.render('GAME OVER', True, WHITE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (window_width//2, window_height//2)

warning_text = font_content.render('This is just 1 puzzle, you need to solve more to get out!', True, WHITE)
warning_rect = warning_text.get_rect()
warning_rect.center = (window_width//2, window_height//2 + 50)

continue_text = font_content.render('Press ENTER to continue', True, WHITE)
continue_rect = continue_text.get_rect()
continue_rect.center = (window_width//2, window_height//2 + 150)

img_selected = None 
is_game_over = False

rows = 5
cols = 5
num_cells = rows*cols 

cell_width = window_width//rows
cell_height = window_height//cols

cells = []
#now i am gonna have to create a loop that loops 9 times coz in this case we have 9 pieces 
rand_indexes = list(range(0,num_cells))

for i in range(num_cells):
    x = (i%rows)*cell_width
    y = (i//cols)*cell_height
    rect = pygame.Rect(x,y,cell_width,cell_height)

    rand_pos = random.choice(rand_indexes)
    rand_indexes.remove(rand_pos) #this removes that position which has already been chosen once 

    cells.append({'rect':rect, 'border': WHITE, 'order': i, 'pos':rand_pos})
    # print(cells[i])

    #now i wanna show these images randomly, i dont want to show them according to their order
    #so i will add a random position so that images are shown according to that not according to their order 
    #so i wanna generate a random number between 0 to 8, and once that number is generated i dont want it to repeat 


running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_game_over:
            mouse_pos = pygame.mouse.get_pos()

            for cell in cells:
                rect = cell['rect']
                order = cell['order']

                if rect.collidepoint(mouse_pos):
                    # print(order)
                    if not img_selected:
                        img_selected = cell   #so now the img_selected contains the whole dictionary - cell 
                        cell['border'] = RED
                        #so its like - if the image is not selected, i wanna select it and then store its information in this variable - img_selected so that when i click the next image, i remember which image i had clicked earlier 
                    else:    #if i get to else part of the loop, it means i am about to select the next image; also i dont want to select the same image twice 
                        current_img = cell
                        if current_img['order'] != img_selected['order']:
                            temp = img_selected['pos']
                            cells[img_selected['order']]['pos'] = cells[current_img['order']]['pos']
                            cells[current_img['order']]['pos'] = temp

                            cells[img_selected['order']]['border'] = WHITE
                            img_selected = None 

                            is_game_over = True
                            for cell in cells:
                                if cell['order'] != cell['pos']:
                                    is_game_over = False
                                    print("game over")



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(WHITE)

    clock.tick(FPS)  #makes this loop run 10 times per second in all computers 
    # screen.blit(bg, bg_rect, (0,0,100,100))   #writing like this blits that small square on screen starting from x=0 and width=100, and starting from y=0 and height=100
    # screen.blit(bg, bg_rect, (400,300,100,100))
    if not is_game_over:
        for i, val in enumerate(cells):
            pos = cells[i]['pos']
            img_area = pygame.Rect(cells[pos]['rect'].x, cells[pos]['rect'].y, cell_width, cell_height)
            screen.blit(bg, cells[i]['rect'], img_area)
    
            pygame.draw.rect(screen, cells[i]['border'], cells[i]['rect'], 1)

    else:
        screen.blit(bg, bg_rect)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(warning_text, warning_rect)
        screen.blit(continue_text, continue_rect)
    pygame.display.update()