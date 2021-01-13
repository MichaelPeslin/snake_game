from time import sleep
from random import randrange
import pygame
import sys

# Window size
FRAME_SIZE_X = 720
FRAME_SIZE_Y = 480

# Colors
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
SCORE_FONT = (255, 255, 255)

# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
DIFFICULTY = {
    'easy': 10,
    'medium': 25,
    'hard': 40
}


class Game:
    def __init__(self, level=DIFFICULTY['easy']):
        """
        Init class variables for game
        :param level: set difficulty of game
        """
        self.game = pygame
        # FPS (frames per second) controller
        self.fps = self.game.time.Clock()
        # Difficulty
        self.level = level
        # Init Snake and Food instances
        self.snake = Snake()
        self.food = Food()
        self.snake_data, self.new_food = self.snake(food_location=self.food.food_location).values()
        self.food_data = self.food(
            snake_body=self.snake_data,
            new_food=self.new_food
        )
        # Init window object
        self.window = None
        # Init Score class instance
        self.score = Score()

    def __init_game(self):
        """
        Function to start the game. Init window, set size and while loop for turn repetition
        """
        if self.game:
            self.game.init()
            self.game.display.set_caption('Snake')
            self.window = self.game.display.set_mode(size=(FRAME_SIZE_X, FRAME_SIZE_Y))

        while True:
            for event in self.game.event.get():
                if event.type == self.game.QUIT:
                    self.__exit_game()
                # If any keyboard button is pressed down
                elif event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_ESCAPE:
                        self.__exit_game()
                    else:
                        if event.key == self.game.K_UP or event.key == ord('w'):
                            self.snake.change_direction(new_direction='UP')
                        if event.key == self.game.K_DOWN or event.key == ord('s'):
                            self.snake.change_direction(new_direction='DOWN')
                        if event.key == self.game.K_LEFT or event.key == ord('a'):
                            self.snake.change_direction(new_direction='LEFT')
                        if event.key == self.game.K_RIGHT or event.key == ord('d'):
                            self.snake.change_direction(new_direction='RIGHT')
            # Change coordinates
            self.__turn()
            # Check game over conditions
            self.__check_game_over()
            # Draw stage
            self.__draw_stage()
            # Draw Snake
            self.__draw_snake()
            # Draw food
            self.__draw_food()
            # Draw score
            self.__draw_score(self.score())
            # Refresh game screen
            self.game.display.update()
            # Refresh rate
            self.fps.tick(self.level)

    def __turn(self):
        """
        Main action of game, calculation of coordinates for Snakes and Food
        """
        self.snake_data, self.new_food = self.snake(food_location=self.food_data).values()
        self.food_data = self.food(snake_body=self.snake_data, new_food=self.new_food)
        if self.new_food:
            self.score.increase_score()

    def __draw_stage(self):
        """
        Drawing background
        """
        self.window.fill(BACKGROUND_COLOR)

    def __draw_snake(self):
        """
        Drawing Snake coordinates
        """
        for body_part in self.snake_data:
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            self.game.draw.rect(self.window, SNAKE_COLOR, self.game.Rect(body_part[0], body_part[1], 10, 10))

    def __draw_food(self):
        """
        Drawing food
        """
        self.game.draw.rect(self.window, FOOD_COLOR, self.game.Rect(self.food_data[0], self.food_data[1], 10, 10))

    def __draw_game_over(self):
        """
        Drawing message of game over case
        """
        my_font = self.game.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU LOST', True, FOOD_COLOR)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (FRAME_SIZE_X / 2, FRAME_SIZE_Y / 4)
        self.window.fill(BACKGROUND_COLOR)
        self.window.blit(game_over_surface, game_over_rect)
        self.game.display.flip()
        sleep(3)
        self.game.quit()
        sys.exit()

    def __draw_score(self, score):
        """
        Drawing score on windows screen
        :param score: Score value
        """
        SCORE_FONT = self.game.font.SysFont('times new roman', 20)
        score_surface = SCORE_FONT.render('Score : ' + str(score), True, SNAKE_COLOR)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (FRAME_SIZE_X / 2, 15)
        self.window.blit(score_surface, score_rect)

    def __check_game_over(self):
        """
        Check conditions of game over case:
        1. Head crushed window border
        2. Head crushed itself body
        """
        snake_head = self.snake_data[0]
        if snake_head[0] < 0 or snake_head[0] > FRAME_SIZE_X - 10:
            self.__draw_game_over()
        elif snake_head[1] < 0 or snake_head[1] > FRAME_SIZE_Y - 10:
            self.__draw_game_over()
        # Snake's head crashed itself body
        for block in self.snake_data[1:]:
            if snake_head[0] == block[0] and snake_head[1] == block[1]:
                self.__draw_game_over()

    def __exit_game(self):
        """
        Finish game and close window
        """
        self.game.quit()
        sys.exit()

    def run(self):
        """
        Launch Snake Game
        """
        self.__init_game()


class Snake:
    def __init__(self):
        """
        Init default snake params
        """
        self.snake_head_pos = [100, 50]
        self.snake_body = [
            self.snake_head_pos,
            [self.snake_head_pos[0] - 10, self.snake_head_pos[1]],
            [self.snake_head_pos[0] - 20, self.snake_head_pos[1]]
        ]
        self.snake_direction = 'RIGHT'
        self.ate_food = False

    def change_direction(self, new_direction: str):
        """
        Change snake direction. Making sure the snake cannot move in the opposite direction instantaneously
        :param new_direction: String parameter with one of 4 directions ['DOWN', 'UP', 'LEFT', 'RIGHT']
        """
        if new_direction == 'UP' and self.snake_direction != 'DOWN':
            self.snake_direction = 'UP'
        if new_direction == 'DOWN' and self.snake_direction != 'UP':
            self.snake_direction = 'DOWN'
        if new_direction == 'LEFT' and self.snake_direction != 'RIGHT':
            self.snake_direction = 'LEFT'
        if new_direction == 'RIGHT' and self.snake_direction != 'LEFT':
            self.snake_direction = 'RIGHT'

    def __move(self):
        """
        Moving the snake to next position
        :return: Snake body coordinates
        """
        self.snake_head_pos = self.__recount_head()
        self.snake_body.pop()
        self.ate_food = False
        return self.snake_body.insert(0, self.snake_head_pos)

    def __growth(self):
        """
        Increase snake body when snake ate food
        :return: Snake body coordinates
        """
        self.snake_head_pos = self.__recount_head()
        self.ate_food = True
        return self.snake_body.insert(0, self.snake_head_pos)

    def __can_eat(self, food_location: list):
        """
        Check on this turn snake can eat food
        :param food_location: food coordinates
        :return: Boolean True or False
        """
        return self.snake_head_pos == food_location

    def __recount_head(self):
        """
        Count the snake head position to next step
        :return: Snake head coordinates
        """
        if self.snake_direction == 'UP':
            return [self.snake_head_pos[0], self.snake_head_pos[1] - 10]
        elif self.snake_direction == 'DOWN':
            return [self.snake_head_pos[0], self.snake_head_pos[1] + 10]
        elif self.snake_direction == 'LEFT':
            return [self.snake_head_pos[0] - 10, self.snake_head_pos[1]]
        elif self.snake_direction == 'RIGHT':
            return [self.snake_head_pos[0] + 10, self.snake_head_pos[1]]

    def __call__(self, food_location: list):
        """
        Call function on each tern. Check Snake can eat Food, do necessary action
        :param food_location: Food coordinates
        :return: dictionary with two params: data - list of Snake coordinates and ate - Boolean result, food was eaten
        or not
        """
        if self.__can_eat(food_location=food_location):
            self.__growth()
        else:
            self.__move()
        return {
            'data': self.snake_body,
            'ate': self.ate_food
        }


class Food:
    def __init__(self):
        """
        Init default food params
        """
        self.food_location = self.generate_location(snake_body=[
            [100, 50],
            [90, 50],
            [80, 50]
        ])
        self.food_was_eaten = False

    def generate_location(self, snake_body: list):
        """
        Generate food new coordinates into window frame, except Snake body location
        :param snake_body: Snake body coordinates
        :return: New Food coordinates
        """
        generation = [randrange(1, (FRAME_SIZE_X//10)) * 10, randrange(1, (FRAME_SIZE_Y//10)) * 10]
        if generation in snake_body:
            generation = self.generate_location(snake_body)
        return generation

    def __call__(self, snake_body: list, new_food: bool):
        """
        Call function on each tern. Check Food was eaten, if it's true, create new one
        :param snake_body: Snake body coordinates
        :param new_food: Boolean, contains answer Food was eaten or not
        :return: Food location coordinates
        """
        if new_food:
            self.food_location = self.generate_location(snake_body=snake_body)
        return self.food_location


class Score:
    def __init__(self):
        """
        Init Score default value
        """
        self.score = 0

    def increase_score(self):
        """
        Increase Score value by 10
        """
        self.score += 10

    def __call__(self):
        """
        :return: Return Score value
        """
        return self.score


