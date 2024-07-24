import snakegame3
import sys
import random

# Initialize pygame
snakegame3.init()
# Constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
GRID_COLOR = (50, 50, 50)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = SNAKE_COLOR

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * CELL_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = snakegame3.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            snakegame3.draw.rect(surface, self.color, r)
            snakegame3.draw.rect(surface, GRID_COLOR, r, 1)

    def handle_keys(self):
        for event in snakegame3.event.get():
            if event.type == snakegame3.QUIT:
                snakegame3.quit()
                sys.exit()
            elif event.type == snakegame3.KEYDOWN:
                if event.key == snakegame3.K_UP:
                    self.turn(UP)
                elif event.key == snakegame3.K_DOWN:
                    self.turn(DOWN)
                elif event.key == snakegame3.K_LEFT:
                    self.turn(LEFT)
                elif event.key == snakegame3.K_RIGHT:
                    self.turn(RIGHT)

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE, random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)

    def draw(self, surface):
        r = snakegame3.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        snakegame3.draw.rect(surface, self.color, r)
        snakegame3.draw.rect(surface, GRID_COLOR, r, 1)

# Main function
def main():
    clock = snakegame3.time.Clock()
    screen = snakegame3.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = snakegame3.Surface(screen.get_size())
    surface = surface.convert()
    snake = Snake()
    food = Food()

    while True:
        for event in snakegame3.event.get():
            if event.type == snakegame3.QUIT:
                snakegame3.quit()
                sys.exit()
            elif event.type == snakegame3.KEYDOWN:
                if event.key == snakegame3.K_ESCAPE:
                    snakegame3.quit()
                    sys.exit()
                snake.handle_keys()

        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        surface.fill(GRID_COLOR)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        snakegame3.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
