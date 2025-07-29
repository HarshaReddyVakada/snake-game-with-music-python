import pygame
import random
import winsound  # Importing winsound for sound

# Initialize Pygame and mixer for music
pygame.init()
pygame.mixer.init()  # Initialize the mixer

# Load and play background music
music_path = r"C:\Users\ASUSG\OneDrive\ドキュメント\Desktop\snakegame\Nagini_Original_Song_#NBP_Creation(128k).mp3"
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # Play the music on a loop
    print("Background music is playing...")
except pygame.error as e:
    print(f"Error loading music file: {e}")
# Set up the game window (600x600)
width, height = 600, 600
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Harsha Snake Game Project")

# Load the Ironman background image
try:
    # Load the background image using raw string
    background_image = pygame.image.load(r"C:\Users\ASUSG\OneDrive\ドキュメント\Desktop\snakegame\ironman.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))  # Scale the image to fit the screen
except Exception as e:
    print(rf"C:\Users\ASUSG\OneDrive\Desktop\snakegame2.py\ironman.jpg: {e}")
    background_image = pygame.Surface((width, height))  # Fallback to a blank surface if the image fails to load
    background_image.fill((0, 0, 0))  # Fill with black

# Initial snake settings
snake_x, snake_y = width // 2, height // 2
snake_size = 10
snake_body = []
snake_length = 1

# Movement variables
velocity_x = 0
velocity_y = 0
snake_speed = 5  # Start with a slower speed

# Initial food position
food_x = random.randint(0, width - snake_size) // 10 * 10
food_y = random.randint(0, height - snake_size) // 10 * 10
food_size = 10

# Score and speed control
score = 0
speed_increase_threshold = 10  # Speed will increase every 10 food items
font = pygame.font.SysFont(None, 35)

# Score animation settings
score_animation_value = 0  # Used for animating the score

# Function to display the snake
def display_snake(snake_body):
    for index, (x, y) in enumerate(snake_body):
        # The head of the snake is yellow, and the rest of the body is white
        if index == len(snake_body) - 1:
            pygame.draw.rect(game_screen, (255, 255, 0), [x, y, snake_size, snake_size])  # Yellow head
        else:
            pygame.draw.rect(game_screen, (255, 255, 255), [x, y, snake_size, snake_size])  # White body

# Function to display food
def display_food(x, y):
    pygame.draw.rect(game_screen, (255, 0, 0), [x, y, food_size, food_size])

# Function to display the animated scoreboard
def display_custom_scoreboard(score, animation_value):
    # Display "SCORE" in orange
    score_label_font = pygame.font.SysFont(None, 35)
    score_label = score_label_font.render("SCORE:", True, (255, 165, 0))  # Orange color for "SCORE"
    game_screen.blit(score_label, [width - 180, 10])

    # Display score number in green with animation
    animated_font = pygame.font.SysFont(None, 35 + animation_value)
    score_number = animated_font.render(str(score), True, (0, 255, 0))  # Green color for the score number
    game_screen.blit(score_number, [width - 90, 10])  # Adjust position to align after the "SCORE"

# Function to display colorful corners
def display_colorful_corners():
    pygame.draw.rect(game_screen, (255, 0, 0), [0, 0, 20, 20])  # Top-left corner (red)
    pygame.draw.rect(game_screen, (0, 255, 0), [width - 20, 0, 20, 20])  # Top-right corner (green)
    pygame.draw.rect(game_screen, (0, 0, 255), [0, height - 20, 20, 20])  # Bottom-left corner (blue)
    pygame.draw.rect(game_screen, (255, 255, 0), [width - 20, height - 20, 20, 20])  # Bottom-right corner (yellow)

# Main game loop
running = True
try:
    while running:
        pygame.time.delay(int(150 / snake_speed))  # Control the frame rate, slower start with 150ms delay
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and velocity_x == 0:
                    velocity_x = -snake_speed
                    velocity_y = 0
                elif event.key == pygame.K_RIGHT and velocity_x == 0:
                    velocity_x = snake_speed
                    velocity_y = 0
                elif event.key == pygame.K_UP and velocity_y == 0:
                    velocity_x = 0
                    velocity_y = -snake_speed
                elif event.key == pygame.K_DOWN and velocity_y == 0:
                    velocity_x = 0
                    velocity_y = snake_speed

        # Update snake position
        snake_x += velocity_x
        snake_y += velocity_y

        # Wrap-around effect for the snake
        if snake_x < 0:
            snake_x = width - snake_size
        elif snake_x > width - snake_size:
            snake_x = 0
        if snake_y < 0:
            snake_y = height - snake_size
        elif snake_y > height - snake_size:
            snake_y = 0

        # Check if the snake eats the food
        if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
            score += 1
            snake_length += 1  # Increase snake length

            # Play beep sound when snake eats food
            winsound.Beep(1000, 200)  # Frequency (1000 Hz), Duration (200 ms)

            # Increase snake speed every 10 food items eaten
            if score % speed_increase_threshold == 0:
                snake_speed += 1  # Gradual speed increase after every 10 food items

            # Trigger score animation
            score_animation_value = 20  # Set a value to make the score "pop"

            # Respawn food at a new random location
            food_x = random.randint(0, width - snake_size) // 10 * 10
            food_y = random.randint(0, height - snake_size) // 10 * 10

        # Add new position of the snake's head to the snake body
        snake_body.append([snake_x, snake_y])

        # Ensure snake's length matches snake_length
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Clear screen
        game_screen.blit(background_image, (0, 0))  # Draw the background image

        # Draw snake and food
        display_snake(snake_body)
        display_food(food_x, food_y)

        # Display colorful corners
        display_colorful_corners()

        # Display animated scoreboard
        if score_animation_value > 0:
            score_animation_value -= 1  # Gradually decrease the animation value to create a "pop" effect
        display_custom_scoreboard(score, score_animation_value)

        # Update the display
        pygame.display.update()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    pygame.quit()  # Ensure Pygame quits properly
