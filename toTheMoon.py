import pygame, time, random
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOUR = (6, 4, 99)
TIME = 0.25     # the lower the time the greater the speed

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/moon.png").convert() 
        self.x = SIZE * 3 
        self.y = SIZE * 3 

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 14) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/resizedDog.png").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    def increase_length(self): 
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'
    
    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i -1]
            self.y[i] = self.y[i -1]

        # update head
        if self.direction == 'up':
            self.y[0] -= SIZE 
        elif self.direction == 'down':
            self.y[0] += SIZE
        elif self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE 
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("To the Moon!")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 600))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/One Cosmos Royalty Free Sci-Fi Background Music (No Copyright).mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/resizedSpace.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background() 
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move() 
        
        # snake colliding with itself
        for i in range(4, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise 'Collision occured'

        # snake colliding with border
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 600):
            self.play_sound('crash')
            raise 'Out of bound'

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1= font.render(f"Game is over: Your score is {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(line1, (180, 240))
        line2 = font.render(f"To play again press ENTER. To exit press ESCAPE.", True, (200, 200, 200))
        self.surface.blit(line2, (180, 275))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
            running = True
            pause = False

            while running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False

                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            pause = False

                        if not pause:
    
                            if event.key == K_UP:
                                self.snake.move_up()
                                
                            elif event.key == K_DOWN:
                                self.snake.move_down()

                            elif event.key == K_LEFT:
                                self.snake.move_left()

                            elif event.key == K_RIGHT:
                                self.snake.move_right()

                    elif event.type == QUIT:
                        running = False
                
                try:
                    if not pause:
                        self.play()
                except Exception as e:
                    self.show_game_over()
                    pause = True
                    self.reset()

                time.sleep(TIME) 

if __name__ == "__main__":
    game = Game()
    game.run()

 