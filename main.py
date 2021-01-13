# This is a sample Python script.

from main.game import Game, DIFFICULTY

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    snake = Game(level=DIFFICULTY['easy'])
    snake.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
