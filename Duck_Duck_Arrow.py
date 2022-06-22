# Imports the two modules pygame and random
import pygame
import random

# Imports some functions from the module pygame to use in the future code
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Creates variables for the width and height of the screen
screen_width = 800
screen_height = 600

# Creates a variable giving the variable 'red' the value of the color red in rgb
red = (213, 50, 80)

# Assigns two variables x and y coordinates for the location of the score
score_x = 0
score_y = 0

# Sets up the screen assigning it a width and height, creates a background using an imported image, and gives a title to the window
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('bg.jpg')
pygame.display.set_caption('Duck, Duck, Arrow')

# Creates a clock to control the frame rate then initilizes pygame
clock = pygame.time.Clock()
pygame.init()

# Creates a variable that sets the inital score to 0 and sets the score's font to comic sans
score_value = 0
score_font = pygame.font.SysFont("comicsansms", 20)

# Defines a score function that holds a variable which shows what will be displayed on the screen and then displays it on the screen 
def show_score(x, y):
    score = score_font.render("Score :" + str(score_value), True, red)
    screen.blit(score, (x, y))

# Defines a player object using sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("air_balloon.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        # Allows the player to start with 3 lives
        self.lives = 3

    # defines a function then resets the player to (0,0) after colliding with an arrow
    def reset(self):
        # reset the player
        self.rect.center = (0, 0)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -4)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 4)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-4, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(4, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height - 80:
            self.rect.bottom = screen_height - 80

# Defines an arrow object using sprite
class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super(Arrow, self).__init__()
        self.surf = pygame.image.load("arrow.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, screen_width),
                random.randint(screen_height, screen_height),
            )
        )
        self.speed = random.randint(5, 15)

    # Move the sprite based on speed
    # Remove the sprite when it passes the top edge of the screen
    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < 0:
            self.kill()

# Defines a duck object using sprite
class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super(Duck, self).__init__()
        self.surf = pygame.image.load("duck.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height ),
            )
        )

    # defines a function that controls the direction the duck moves and removes the duck after it leaves the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom >= screen_height - 80:
            self.kill()

# Defines an archer object using sprite
class Archer(pygame.sprite.Sprite):
    def __init__(self):
        super(Archer, self).__init__()
        self.surf = pygame.image.load("archer.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )

    # Defines a function that moves the archer left
    # The function also kills the object after it leaves the left edge of the screen and only creates archers at the bottom of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
             self.kill()
        if self.rect.top <= screen_height - 60:
            self.rect.top = screen_height - 60

# Defines a cloud object using sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height ),
            )
        )

    # Defines a function that moves the clouds left, 
    # destroys them after leaving the left edge of the screen, 
    # and prevents them from generating at the bottom of the display
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom >= screen_height - 80:
            self.kill()

# Creates custom events for each object, assigning it a unique integer and controlling the speed at which they are created
add_duck = pygame.USEREVENT + 1
pygame.time.set_timer(add_duck, 5000)
ADDARROW = pygame.USEREVENT + 2
pygame.time.set_timer(ADDARROW, 400)
ADDARCHER = pygame.USEREVENT + 3
pygame.time.set_timer(ADDARCHER, 700)
ADDCLOUD = pygame.USEREVENT + 4
pygame.time.set_timer(ADDCLOUD, 1000)

# Creates player
player = Player()

# Creates groups to hold duck sprites, arrow sprites, archer sprites, cloud sprites, and all sprites
ducks = pygame.sprite.Group()
arrows = pygame.sprite.Group()
archers = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# sets running to true
running = True

# Main loop that runs the game
while running:
    # transfers the backgroud image on the screen at coordinates (0,0)
    screen.blit(background, (0, 0))

    # Examines and goes through every event in the queue
    for event in pygame.event.get():
        #
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
                running = False

        # Add a new arrow
        elif event.type == ADDARROW:
            # Create the new arrow and add it to sprite groups
            new_arrow = Arrow()
            arrows.add(new_arrow)
            all_sprites.add(new_arrow)

        # Add a new duck
        elif event.type == add_duck:
            # Create the new duck and add it to sprite groups
            new_duck = Duck()
            ducks.add(new_duck)
            all_sprites.add(new_duck)

        # Add a new cloud
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        # Add a new Archer
        elif event.type == ADDARCHER:
            # Create the new archer and add it to sprite groups
            new_archer = Archer()
            archers.add(new_archer)
            all_sprites.add(new_archer)

    # Checks the users input and gets the keys that are pressed
    pressed_keys = pygame.key.get_pressed()

    # Updates the player sprite based on the keys that are pressed
    player.update(pressed_keys)

    # Updates the positions of the sprites
    ducks.update()
    arrows.update()
    archers.update()
    clouds.update()

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # If the player sprite collides with the ducks add a point to the score_value
    if pygame.sprite.spritecollideany(player, ducks):
            score_value += 1

    # If the player collides with the arrows, reset their position and remove a life
    if pygame.sprite.spritecollideany(player, arrows):
        player.reset()
        player.lives -= 1
    
    # If the player_lives get to 0, make running equal false and stop the game
    if player.lives == 0:
        running = False

    # Shows the score on the screen
    show_score(score_x, score_y)

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Flip the display
    pygame.display.flip()
 
    # Calculates number of milliseconds each frame takes
    clock.tick(30)
