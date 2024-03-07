import pygame
import random
import logging
import sys

# Configure logging
logging.basicConfig(filename='game.log', level=logging.DEBUG)

class FighterEnemy:
    def __init__(self, screen_width, screen_height):
        self.width = 50
        self.height = 50
        self.image = pygame.image.load('fighter.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.speed = 2
        self.spawn_delay = 2000  # milliseconds
        self.last_spawn_time = pygame.time.get_ticks()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies = []

    def spawn(self):
        if pygame.time.get_ticks() - self.last_spawn_time > self.spawn_delay:
            enemy_x = random.randint(0, self.screen_width - self.width)
            enemy_y = -self.height
            self.enemies.append([enemy_x, enemy_y])
            self.last_spawn_time = pygame.time.get_ticks()

    def move(self):
        for enemy in self.enemies:
            enemy[1] += self.speed

    def draw(self, screen):
        for enemy in self.enemies:
            screen.blit(self.image, (enemy[0], enemy[1]))


def game(screen):
    try:
        # Load the background image and scale it to match the screen dimensions
        background_img = pygame.image.load('background.png').convert()
        background_img = pygame.transform.scale(background_img, screen.get_size())

        # Load the explosion images
        player_explosion_img = pygame.image.load('explosion.png')
        player_explosion_img = pygame.transform.scale(player_explosion_img, (50, 50))
        enemy_explosion_img = pygame.image.load('enemyexplosion.png')
        enemy_explosion_img = pygame.transform.scale(enemy_explosion_img, (50, 50))

        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Player
        player_width = 50
        player_height = 50
        player_img = pygame.image.load('player.png')
        player_img = pygame.transform.scale(player_img, (player_width, player_height))
        player_x = screen.get_width() // 2 - player_width // 2
        player_y = screen.get_height() - player_height - 10
        player_speed = 10  # Increased player speed

        # Movement flags
        move_left = False
        move_right = False

        # Enemies
        enemy_width = 50
        enemy_height = 50
        enemy_img = pygame.image.load('enemy.png')
        enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
        enemy_speed = 3
        enemies = []
        enemy_spawn_delay = 1000  # milliseconds
        last_enemy_spawn_time = pygame.time.get_ticks()

        # Fighter Enemies
        fighter_enemy = FighterEnemy(screen.get_width(), screen.get_height())

        # Bullets
        bullet_width = 5
        bullet_height = 15
        bullet_img = pygame.Surface((bullet_width, bullet_height))
        bullet_img.fill(WHITE)
        bullet_speed = 7
        bullets = []

        # Fonts
        font = pygame.font.Font(None, 20)  # Adjust font size

        # Score
        score = 0

        # Timer
        game_duration = 30  # 30 seconds
        start_time = pygame.time.get_ticks()

        # Game loop
        clock = pygame.time.Clock()
        running = True
        while running:
            # Calculate elapsed time
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds

            # Check if game time has elapsed
            if elapsed_time >= game_duration:
                # Player wins
                return True, score

            # Draw background
            screen.blit(background_img, (0, 0))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, score
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_left = True
                    elif event.key == pygame.K_RIGHT:
                        move_right = True
                    elif event.key == pygame.K_SPACE:
                        bullet_x = player_x + player_width // 2 - bullet_width // 2
                        bullet_y = player_y
                        bullets.append([bullet_x, bullet_y])
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move_left = False
                    elif event.key == pygame.K_RIGHT:
                        move_right = False

            # Update player position based on movement flags
            if move_left and player_x > 0:
                player_x -= player_speed
            if move_right and player_x < screen.get_width() - player_width:
                player_x += player_speed

            # Spawn enemies
            if pygame.time.get_ticks() - last_enemy_spawn_time > enemy_spawn_delay:
                enemy_x = random.randint(0, screen.get_width() - enemy_width)
                enemy_y = -enemy_height
                enemies.append([enemy_x, enemy_y])
                last_enemy_spawn_time = pygame.time.get_ticks()

            # Spawn fighter enemies
            fighter_enemy.spawn()

            # Move enemies
            for enemy in enemies:
                enemy[1] += enemy_speed
                screen.blit(enemy_img, (enemy[0], enemy[1]))

            # Move fighter enemies
            fighter_enemy.move()
            fighter_enemy.draw(screen)

            # Move bullets
            for bullet in bullets:
                bullet[1] -= bullet_speed
                screen.blit(bullet_img, (bullet[0], bullet[1]))

            # Check for collisions between player and enemies
            for enemy in enemies:
                if (player_x < enemy[0] + enemy_width and
                        player_x + player_width > enemy[0] and
                        player_y < enemy[1] + enemy_height and
                        player_y + player_height > enemy[1]):
                    # Collision detected with player and enemy, display both explosions
                    screen.blit(player_explosion_img, (player_x, player_y))
                    screen.blit(enemy_explosion_img, (enemy[0], enemy[1]))
                    pygame.display.flip()
                    pygame.time.delay(2000)  # Delay to show explosions
                    # Player loses
                    return False, score

            # Check for collisions between player and fighter enemies
            for enemy in fighter_enemy.enemies:
                if (player_x < enemy[0] + fighter_enemy.width and
                        player_x + player_width > enemy[0] and
                        player_y < enemy[1] + fighter_enemy.height and
                        player_y + player_height > enemy[1]):
                    # Collision detected with player and fighter enemy, display both explosions
                    screen.blit(player_explosion_img, (player_x, player_y))
                    screen.blit(enemy_explosion_img, (enemy[0], enemy[1]))
                    pygame.display.flip()
                    pygame.time.delay(2000)  # Delay to show explosions
                    # Player loses
                    return False, score

            # Check if any enemy ship touches the bottom of the screen
            for enemy in enemies:
                if enemy[1] >= screen.get_height():
                    # Enemy ship touched the bottom of the screen, player loses
                    return False, score

            # Check if any fighter enemy ship touches the bottom of the screen
            for enemy in fighter_enemy.enemies:
                if enemy[1] >= screen.get_height():
                    # Fighter enemy ship touched the bottom of the screen, player loses
                    return False, score

            # Collision detection between bullets and enemies
            for enemy in enemies:
                for bullet in bullets:
                    if (bullet[1] < enemy[1] + enemy_height and
                            bullet[1] > enemy[1] and
                            bullet[0] > enemy[0] and
                            bullet[0] < enemy[0] + enemy_width):
                        # Bullet hit the enemy
                        score += 1
                        enemies.remove(enemy)
                        bullets.remove(bullet)

            # Collision detection between bullets and fighter enemies
            for enemy in fighter_enemy.enemies:
                for bullet in bullets:
                    if (bullet[1] < enemy[1] + fighter_enemy.height and
                            bullet[1] > enemy[1] and
                            bullet[0] > enemy[0] and
                            bullet[0] < enemy[0] + fighter_enemy.width):
                        # Bullet hit the fighter enemy
                        score += 2
                        fighter_enemy.enemies.remove(enemy)
                        bullets.remove(bullet)

            # Display score
            score_text = font.render("Score: " + str(score), True, WHITE)
            screen.blit(score_text, (10, 10))

            # Display remaining time
            time_left = game_duration - elapsed_time
            time_text = font.render("Time: " + str(int(time_left)), True, WHITE)
            screen.blit(time_text, (screen.get_width() - 150, 10))

            # Player
            screen.blit(player_img, (player_x, player_y))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

    except Exception as e:
        # Log the exception
        logging.exception("An error occurred: %s", e)
        return False, 0


def main():
    try:
        # Initialize pygame
        pygame.init()

        # Set up the screen
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Starship Shooter")

        while True:
            # Display game introduction
            intro_text = [
                "The year is 2050. Earth, once a thriving planet, has fallen under attack by a ruthless alien civilization known as the Xerons.",
                "They have unleashed a devastating assault, laying waste to cities and decimating humanity's defenses.",
                "Amidst the chaos, you are the last remaining pilot of the Earth Federation's elite squadron.",
                "As the sole survivor, you embark on a desperate mission to repel the Xeron invasion and save what remains of humanity.",
                "To protect earth, you must prevent the enemy ships from reaching the bottom of the screen for 30 seconds.",
                "Press SPACEBAR to start the game..."
            ]

            # Render introduction text
            font = pygame.font.Font(None, 20)  # Adjust font size
            intro_rendered_texts = []
            line_spacing = 25  # Adjust line spacing
            max_lines = 16  # Limit number of lines to fit within the box
            for i, line in enumerate(intro_text):
                if i >= max_lines:
                    break
                text_surface = font.render(line, True, (255, 255, 255))
                intro_rendered_texts.append(text_surface)

            # Calculate total height of the intro text
            total_intro_height = len(intro_rendered_texts) * line_spacing

            # Calculate starting y position to center the text vertically
            intro_y = (screen_height - total_intro_height) // 2

            # Render introduction text
            screen.fill((0, 0, 0))
            for i, text_surface in enumerate(intro_rendered_texts):
                text_x = (screen_width - text_surface.get_width()) // 2  # Center horizontally
                screen.blit(text_surface, (text_x, intro_y + i * line_spacing))
            pygame.display.flip()

            # Wait for spacebar input to start the game
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        break
                else:
                    continue
                break

            # Start the game
            player_won, score = game(screen)

            # Display appropriate message based on game result
            if player_won:
                message = "You saved earth. Press Y to try again. To quit, press N."
            else:
                message = "You've failed to protect earth. To try again, press Y. To quit, press N."

            # Render message text
            message_text = font.render(message, True, (255, 255, 255))
            message_x = (screen_width - message_text.get_width()) // 2
            message_y = (screen_height - message_text.get_height()) // 2

            # Display message text
            screen.fill((0, 0, 0))
            screen.blit(message_text, (message_x, message_y))
            pygame.display.flip()

            # Wait for player input to restart or quit the game
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            break
                        elif event.key == pygame.K_n:
                            pygame.quit()
                            sys.exit()
                else:
                    continue
                break

    finally:
        # Quit pygame
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
