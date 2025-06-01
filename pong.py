import pygame, sys, random
 
pygame.init()

mode_selected = False
is_single_player = False
 
WIDTH, HEIGHT = 1280, 720
 
SCORE_FONT = pygame.font.SysFont("Consolas", int(WIDTH/20))
TEXT_FONT = pygame.font.SysFont("Consolas", int(WIDTH/50))
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()

while not mode_selected:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                is_single_player = True
                mode_selected = True
            elif event.key == pygame.K_2:
                is_single_player = False
                mode_selected = True
    
    SCREEN.fill("black")
    title_text = TEXT_FONT.render("Press 1 for Single Player or 2 for Two Players", True, "white")
    SCREEN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/2))
    pygame.display.update()
    CLOCK.tick(60)
 
# Pong Paddles!
player_left = pygame.Rect(110, HEIGHT/2-50, 10, 100)
player_right = pygame.Rect(WIDTH-110, HEIGHT/2-50, 10, 100)
player_left_score, player_right_score = 0,0

# Pong Ball
ball = pygame.Rect(WIDTH/2-10, HEIGHT/2-10, 20, 20)
x_speed, y_speed = 1,1

# Checking for winner
def check_winner(left_score, right_score):
    if left_score >= 11 and (left_score - right_score) >= 2:
        return "Left"
    elif right_score >= 11 and (right_score - left_score) >= 2:
        return "Right"
    else:
        return None

# Winner screen
def handle_winner(winner_text, font, screen):
    text = font.render(f"{winner_text} Player Wins!", True, "yellow")
    prompt = font.render("Press Q to Quit or Press R to Restart The Game!", True, "yellow")
    screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2))
    screen.blit(prompt, (WIDTH/2 - prompt.get_width()/2, HEIGHT/2+20))
    pygame.display.update()

    game_paused = True
    while game_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # Quit
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_r: # Play again
                    return False
                else:
                    pass
    return True

# Game Loop
while True:
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_w]:
        if player_left.top > 0:
            player_left.top -= 2
    if keys_pressed[pygame.K_s]:
        if player_left.bottom < HEIGHT:
            player_left.bottom += 2
    
    if is_single_player:
        if player_right.y < ball.y:
            player_right.top += 1
        if player_right.bottom > ball.y:
            player_right.bottom -= 1
    else:
        if keys_pressed[pygame.K_UP]:
            if player_right.top > 0:
                player_right.top -= 2
        if keys_pressed[pygame.K_DOWN]:
            if player_right.bottom < HEIGHT:
                player_right.bottom += 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if ball.y >= HEIGHT:
        y_speed = -1
    if ball.y <= 0:
        y_speed = 1
    
    # Ball passes left side
    if ball.x <= 0:
        player_right_score += 1
        SCREEN.fill("black")
        player_left_score_text = SCORE_FONT.render(str(player_left_score), True, "blue")
        player_right_score_text = SCORE_FONT.render(str(player_right_score), True, "red")
        SCREEN.blit(player_left_score_text, (WIDTH/2-75, 50))
        SCREEN.blit(player_right_score_text, (WIDTH/2+75, 50))
        pygame.display.update()

        winner = check_winner(player_left_score, player_right_score)
        if winner == "Right":
            if not handle_winner(winner, TEXT_FONT, SCREEN):
                player_left_score = 0
                player_right_score = 0
                ball.center = (WIDTH/2, HEIGHT/2)
                x_speed, y_speed = random.choice([1,-1]), random.choice([1,-1])

        ball.center = (WIDTH/2, HEIGHT/2)
        x_speed, y_speed = random.choice([1,-1]), random.choice([1,-1])

    # Ball passes right side
    if ball.x >= WIDTH:
        player_left_score += 1
        SCREEN.fill("black")
        player_left_score_text = SCORE_FONT.render(str(player_left_score), True, "blue")
        player_right_score_text = SCORE_FONT.render(str(player_right_score), True, "red")
        SCREEN.blit(player_left_score_text, (WIDTH/2-75, 50))
        SCREEN.blit(player_right_score_text, (WIDTH/2+75, 50))
        pygame.display.update()
        winner = check_winner(player_left_score, player_right_score)
        if winner == "Left":
            if not handle_winner(winner, TEXT_FONT, SCREEN):
                player_left_score = 0
                player_right_score = 0
                ball.center = (WIDTH/2, HEIGHT/2)
                x_speed, y_speed = random.choice([1,-1]), random.choice([1,-1])

        ball.center = (WIDTH/2, HEIGHT/2)
        x_speed, y_speed = random.choice([1,-1]), random.choice([1,-1])

    if player_right.x - ball.width <= ball.x <= player_right.x and ball.y in range(player_right.top-ball.width, player_right.bottom+ball.width):
        x_speed = -1
    if player_left.x - ball.width <= ball.x <= player_left.x and ball.y in range(player_left.top-ball.width, player_left.bottom+ball.width):
        x_speed = 1

    player_left_score_text = SCORE_FONT.render(str(player_left_score), True, "blue")
    player_right_score_text = SCORE_FONT.render(str(player_right_score), True, "red")

    ball.x += x_speed * 2
    ball.y += y_speed * 2
    SCREEN.fill("black")

    pygame.draw.rect(SCREEN, "blue", player_left)
    pygame.draw.rect(SCREEN, "red", player_right)
    pygame.draw.circle(SCREEN, "white", ball.center, 10)

    SCREEN.blit(player_left_score_text, (WIDTH/2-75, 50))
    SCREEN.blit(player_right_score_text, (WIDTH/2+75, 50))

    pygame.display.update()
    CLOCK.tick(300)