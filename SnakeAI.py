import pygame
import time
import random
import os

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

WIDTH = 25
HEIGHT = 15
FIELD_SIZE = WIDTH * HEIGHT
HEAD = 0

FOOD = 0
UNDEFINED = (WIDTH + 1) * (HEIGHT + 1)
SNAKE = 2 * UNDEFINED

LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH

ERROR = -2333
MOVE = [LEFT, RIGHT, UP, DOWN]

SNAKE_BLOCK = 20
SNAKE_SPEED = 60 #30

MESSAGE_FONT = pygame.font.SysFont("bahnschrift", 20)
SCORE_FONT = pygame.font.SysFont("comicsansms", 15)

display = pygame.display.set_mode((SNAKE_BLOCK * WIDTH, SNAKE_BLOCK * HEIGHT))
pygame.display.set_caption("Snake AI")
clock = pygame.time.Clock()

def show_score(score):
	score_view = SCORE_FONT.render("Your Score: {}".format(score), True, WHITE)
	display.blit(score_view, [0, 0])

def show_message(message):
	message_view = MESSAGE_FONT.render(message, True, YELLOW)
	message_rect = message_view.get_rect(center = ((SNAKE_BLOCK * WIDTH) / 2, (SNAKE_BLOCK * HEIGHT) / 2))
	display.blit(message_view, message_rect)

def initial_game():
	global board, snake, snake_size
	global template_board, template_snake, template_snake_size
	global food, best_move

	board = [0] * FIELD_SIZE
	snake = [0] * (FIELD_SIZE + 1)
	snake[HEAD] = 1 * WIDTH + 1
	snake_size = 1

	template_board = [0] * FIELD_SIZE
	template_snake = [0] * (FIELD_SIZE + 1)
	template_snake[HEAD] = 1 * WIDTH + 1
	template_snake_size = 1

	food_x = random.randint(0, WIDTH - 1)
	food_y = random.randint(0, HEIGHT - 1)
	food = food_y * WIDTH + food_x
	best_move = ERROR

def place_new_food():
	global food, snake_size, snake
	cell_free = False
	while not cell_free:
		food_x = random.randint(0, WIDTH - 1)
		food_y = random.randint(0, HEIGHT - 1)
		food = food_y * WIDTH + food_x
		cell_free = is_cell_free(food, snake_size, snake)

def is_cell_free(index, pygame_size, pygame_snake):
	return not (index in pygame_snake[:pygame_size])

def draw_entities():
	global snake, snake_size, food
	for index in snake[:snake_size]:
		pygame.draw.rect(display, GREEN, [SNAKE_BLOCK * (index % WIDTH), SNAKE_BLOCK * (index // WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])
	pygame.draw.ellipse(display, RED, [SNAKE_BLOCK * (food % WIDTH), SNAKE_BLOCK * (food // WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])

def is_move_possible(index, move):
	flag = False
	if move == LEFT:
		flag = True if index % WIDTH > 0 else False
	elif move == RIGHT:
		flag = True if index % WIDTH < (WIDTH - 1) else False
	elif move == UP:
		flag = True if index > (WIDTH - 1) else False
	elif move == DOWN:
		flag = True if index < (FIELD_SIZE - WIDTH) else False
	return flag

def board_BFS(pygame_food, pygame_snake, pygame_board):
	queue = []
	queue.append(pygame_food)
	inqueue = [0] * FIELD_SIZE
	found = False
	while len(queue) != 0:
		index = int(queue.pop(0))
		if inqueue[index] == 1:
			continue
		inqueue[index] = 1
		for i in range(len(MOVE)):
			if is_move_possible(index, MOVE[i]):
				if index + MOVE[i] == pygame_snake[HEAD]:
					found = True
				if pygame_board[index + MOVE[i]] < SNAKE:
					if pygame_board[index + MOVE[i]] > pygame_board[index] + 1:
						pygame_board[index + MOVE[i]] = pygame_board[index] + 1
					if inqueue[index + MOVE[i]] == 0:
						queue.append(index + MOVE[i])
	return found

def is_tail_reachable():
	global template_board, template_snake, template_snake_size, food
	template_board[template_snake[template_snake_size - 1]] = FOOD
	template_board[food] = SNAKE
	result = board_BFS(template_snake[template_snake_size - 1], template_snake, template_board)
	for i in range(len(MOVE)):
		if is_move_possible(template_snake[HEAD], MOVE[i]) and template_snake[HEAD] + MOVE[i] == template_snake[template_snake_size - 1] and template_snake_size > 3:
			result = False
	return result

def shift_array(array, size):
	for i in range(size, 0, -1):
		array[i] = array[i - 1]

def make_move(move):
	global snake, board, snake_size, score
	shift_array(snake, snake_size)
	snake[HEAD] += move
	p = snake[HEAD]
	if snake[HEAD] == food:
		board[snake[HEAD]] = SNAKE
		snake_size += 1
		if snake_size < FIELD_SIZE: place_new_food()
	else:
		board[snake[HEAD]] = SNAKE
		board[snake[snake_size]] = UNDEFINED

def reset_board(pygame_snake, pygame_size, pygame_board):
	for i in range(FIELD_SIZE):
		if i == food:
			pygame_board[i] = FOOD
		elif is_cell_free(i, pygame_size, pygame_snake):
			pygame_board[i] = UNDEFINED
		else:
			pygame_board[i] = SNAKE

def virtual_shortest_move():
	global snake, board, snake_size, template_snake, template_board, template_snake_size, food
	template_snake_size = snake_size
	template_snake = snake[:]
	template_board = board[:]
	reset_board(template_snake, template_snake_size, template_board)
	food_eated = False
	while not food_eated:
		board_BFS(food, template_snake, template_board)
		move = choose_shortest_safe_move(template_snake, template_board)
		shift_array(template_snake, template_snake_size)
		template_snake[HEAD] += move
		if template_snake[HEAD] == food:
			template_snake_size += 1
			reset_board(template_snake, template_snake_size, template_board)
			template_board[food] = SNAKE
			food_eated = True
		else:
			template_board[template_snake[HEAD]] = SNAKE
			template_board[template_snake[template_snake_size]] = UNDEFINED

def choose_shortest_safe_move(pygame_snake, pygame_board):
	best_move = ERROR
	min = SNAKE
	for i in range(len(MOVE)):
		if is_move_possible(pygame_snake[HEAD], MOVE[i]) and pygame_board[pygame_snake[HEAD] + MOVE[i]] < min:
			min = pygame_board[pygame_snake[HEAD] + MOVE[i]]
			best_move = MOVE[i]
	return best_move

def choose_longest_safe_move(pygame_snake, pygame_board):
	best_move = ERROR
	max = -1
	for i in range(len(MOVE)):
		if is_move_possible(pygame_snake[HEAD], MOVE[i]) and pygame_board[pygame_snake[HEAD] + MOVE[i]] < UNDEFINED and pygame_board[pygame_snake[HEAD] + MOVE[i]] > max:
			max = pygame_board[pygame_snake[HEAD] + MOVE[i]]
			best_move = MOVE[i]
	return best_move

def follow_tail():
	global template_board, template_snake, template_snake_size, food
	template_snake_size = snake_size
	template_snake = snake[:]
	reset_board(template_snake, template_snake_size, template_board)
	template_board[template_snake[template_snake_size - 1]] = FOOD
	template_board[food] = SNAKE
	board_BFS(template_snake[template_snake_size - 1], template_snake, template_board)
	template_board[template_snake[template_snake_size - 1]] = SNAKE
	return choose_longest_safe_move(template_snake, template_board)

def find_safe_way():
	global snake, board
	safe_move = ERROR
	virtual_shortest_move()
	if is_tail_reachable():
		return choose_shortest_safe_move(snake, board)
	safe_move = follow_tail()
	return safe_move

def any_possible_move():
	global snake, snake_size, board, food
	best_move = ERROR
	reset_board(snake, snake_size, board)
	board_BFS(food, snake, board)
	min = SNAKE
	for i in range(len(MOVE)):
		if is_move_possible(snake[HEAD], MOVE[i]) and board[snake[HEAD] + MOVE[i]] < min:
			min = board[snake[HEAD] + MOVE[i]]
			best_move = MOVE[i]
	return best_move

def game_loop():
	game_over = False
	game_close = False

	initial_game()

	while not game_over:
		while game_close:
			display.fill(BLACK)
			show_message("You Lost! Press P-Play Again or Q-Quit")
			show_score(snake_size - 1)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
						game_over = True
						game_close = False
					if event.key == pygame.K_p:
						game_loop()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_over = True

		reset_board(snake, snake_size, board)

		if board_BFS(food, snake, board):
			best_move = find_safe_way()
		else:
			best_move = follow_tail()

		if best_move == ERROR:
			best_move = any_possible_move()

		if best_move != ERROR:
			make_move(best_move)
		else:
			game_close = True

		display.fill(BLACK)
		draw_entities()
		show_score(snake_size - 1)
		pygame.display.update()

		clock.tick(SNAKE_SPEED)

	pygame.quit()
	os._exit(1)

game_loop()
