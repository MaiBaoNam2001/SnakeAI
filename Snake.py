import pygame
import random
import time
import os

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 400

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

SNAKE_BLOCK = 10
SNAKE_SPEED = 15

message_font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 15)

def show_your_score(score):
	score_view = score_font.render("Your Score: {}".format(score), True, WHITE)
	display.blit(score_view, [0, 0])

def show_message(message):
	message_view = message_font.render(message, True, YELLOW)
	message_rect = message_view.get_rect(center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))
	display.blit(message_view, message_rect)

def show_snake(snake_block, snake_list):
	for node in snake_list:
		pygame.draw.rect(display, GREEN, [node[0], node[1], SNAKE_BLOCK, SNAKE_BLOCK])

def show_food(food_x, food_y):
	pygame.draw.ellipse(display, RED, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

def game_loop():
	game_over = False
	game_close = False

	snake_x = DISPLAY_WIDTH / 2
	snake_y = DISPLAY_HEIGHT / 2

	snake_x_change = 0
	snake_y_change = 0

	snake_list = []
	length_of_snake = 1

	food_x = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
	food_y = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

	while not game_over:
		while game_close:
			display.fill(BLACK)
			show_message("You Lost! Press P-Play Again or Q-Quit")
			show_your_score(length_of_snake - 1)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						game_loop()
					if event.key == pygame.K_q:
						game_over = True
						game_close = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					snake_x_change = - SNAKE_BLOCK
					snake_y_change = 0
				elif event.key == pygame.K_RIGHT:
					snake_x_change = SNAKE_BLOCK
					snake_y_change = 0
				elif event.key == pygame.K_UP:
					snake_x_change = 0
					snake_y_change = - SNAKE_BLOCK
				elif event.key == pygame.K_DOWN:
					snake_x_change = 0
					snake_y_change = SNAKE_BLOCK

		if snake_x >= DISPLAY_WIDTH or snake_x < 0 or snake_y >= DISPLAY_HEIGHT or snake_y < 0:
			game_close = True

		snake_x += snake_x_change
		snake_y += snake_y_change

		display.fill(BLACK)
		show_food(food_x, food_y)

		snake_head = []
		snake_head.append(snake_x)
		snake_head.append(snake_y)
		snake_list.append(snake_head)

		if len(snake_list) > length_of_snake:
			del snake_list[0]

		for node in snake_list[:-1]:
			if node == snake_head:
				game_close = True

		show_snake(SNAKE_BLOCK, snake_list)
		show_your_score(length_of_snake - 1)
		pygame.display.update()

		if snake_x == food_x and snake_y == food_y:
			food_x = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
			food_y = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
			length_of_snake += 1

		clock.tick(SNAKE_SPEED)

	pygame.quit()
	os._exit(1)

game_loop()