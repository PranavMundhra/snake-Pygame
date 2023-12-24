import pygame
import sys
import random
import csv

pygame.init()

width = 500
height = 350
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
snake_x = 390
snake_y = 240
snake = [pygame.Rect(snake_x, snake_y, 10, 10)]
food_x = 0
food_y = 0
font = pygame.font.Font("PixelifySans-VariableFont_wght.ttf" , 15)
font1 = pygame.font.Font("PixelifySans-VariableFont_wght.ttf" , 30)
score = 0
score_text = font.render("Score: "+str(score), True, (211,211,211))

# Generates coordinates of the food
def food_coordinates():
    while True:
        food_x = random.randint(0, width - 10)
        food_y = random.randint(0, height - 10)
        food_rect = pygame.Rect(food_x, food_y, 10, 10)
        if not any(segment.colliderect(food_rect) for segment in snake):
            return food_x, food_y
def read_high_score():
    try:
        with open('high_score.csv', mode='r') as file:
            reader = csv.reader(file)
            high_score = int(next(reader)[0])
            return high_score
    except FileNotFoundError:
        return 0
def write_high_score(score):
    with open('high_score.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([score])

food_x, food_y = food_coordinates()
food = pygame.Rect(food_x, food_y, 10, 10)
clock = pygame.time.Clock()
move_x = 0
move_y = 0
high_score = read_high_score()
high_score_text = font.render("High Score: "+str(high_score), True, (211,211,211))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and move_x == 0:
                move_x = -10
                move_y = 0
            elif event.key == pygame.K_RIGHT and move_x == 0:
                move_x = 10
                move_y = 0
            elif event.key == pygame.K_UP and move_y == 0:
                move_x = 0
                move_y = -10
            elif event.key == pygame.K_DOWN and move_y == 0:
                move_x = 0
                move_y = 10

    new_head = pygame.Rect(snake[0].x + move_x, snake[0].y + move_y, 10, 10)

    # Teleport snake when it reaches window boundaries
    if new_head.x >= width:
        new_head.x = 0
    elif new_head.x < 0:
        new_head.x = width - 10
    elif new_head.y >= height:
        new_head.y = 0
    elif new_head.y < 0:
        new_head.y = height - 10

    snake.insert(0, new_head)

    # Checks collision with food
    if new_head.colliderect(food):
        food_x, food_y = food_coordinates()
        food.x = food_x
        food.y = food_y
        score += 1
    else:
        snake.pop()  # Remove the tail segment if no food is eaten

    # Check collision with self (if head touches any part of the body)
    # Check collision with self (if head touches any part of the body)
    for segment in snake[1:]:
        if new_head.colliderect(segment):
            game_over = True  # Flag to display game over message
            while game_over:
                end_text = font1.render("Game Over! Score: " + str(score), True, (211, 211, 211))
                window.blit(end_text, (95, 135))
                if high_score < score:
                    write_high_score(score)  # Update the high score with the current score
                    high_score = score  # Update high_score variable
                    high_score_text = font.render("High Score: " + str(high_score), True, (211, 211, 211))  # Update high score text
                    break
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            pygame.quit()
                            sys.exit()

   
    score_text = font.render("Score: " + str(score), True, (211, 211, 211))
    window.fill((0, 0, 0))  # Fill the window with black color
    window.blit(score_text, (5,20))
    window.blit(high_score_text, (5,5))
    pygame.draw.rect(window, (250, 0, 0), food)  # Draw food
    # Draw snake
    for segment in snake:
        pygame.draw.rect(window, (0, 255, 0), segment)

    clock.tick(20)  # Set the maximum FPS
    pygame.display.update()

pygame.quit()
sys.exit()
