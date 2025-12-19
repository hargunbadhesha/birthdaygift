import pygame
import sys

# ------------ CONFIG ------------
WIDTH, HEIGHT = 900, 500
FPS = 60

BALL_SPEED_IN = -9   # towards batsman
BALL_SPEED_OUT_X = 8 # after hit
BALL_SPEED_OUT_Y = -6

BG_COLOR = (20, 120, 20)  # backup if bg image fails

# ------------ INIT ------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cricket Love Animation 🏏❤️")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arial", 36, bold=True)
font_med = pygame.font.SysFont("arial", 24, bold=True)

# ------------ LOAD ASSETS ------------
def load_and_scale(path, width=None, height=None):
    try:
        img = pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"Error loading {path}: {e}")
        # fallback: colored rect
        img = pygame.Surface((100, 100), pygame.SRCALPHA)
        img.fill((255, 0, 0, 180))
    if width or height:
        orig_w, orig_h = img.get_size()
        if width and not height:
            scale = width / orig_w
            height = int(orig_h * scale)
        elif height and not width:
            scale = height / orig_h
            width = int(orig_w * scale)
        img = pygame.transform.smoothscale(img, (width, height))
    return img

bg = load_and_scale("assets/stadium_bg.png", width=WIDTH)

batsman_img = load_and_scale("assets/batsman.png", height=180)
bowler_img = load_and_scale("assets/bowler.png", height=170)
gf_img = load_and_scale("assets/girlfriend.png", height=120)
ball_img = load_and_scale("assets/ball.png", height=25)

# ------------ POSITIONS ------------
# Ground line reference (just visual)
GROUND_Y = 330

# Batsman on left-ish
batsman_rect = batsman_img.get_rect()
batsman_rect.midbottom = (260, GROUND_Y)

# Bowler on right
bowler_rect = bowler_img.get_rect()
bowler_rect.midbottom = (700, GROUND_Y)

# Girlfriend in stands (top-left-ish)
gf_rect = gf_img.get_rect()
gf_rect.midtop = (130, 80)

# Ball starts near bowler's hand
ball_rect = ball_img.get_rect()
ball_rect.center = (bowler_rect.centerx - 40, bowler_rect.centery - 40)

ball_vx = BALL_SPEED_IN
ball_vy = 0

hit = False
cheer = False
cheer_timer = 0  # frames after hit

# ------------ TEXT ------------
bf_name = "Karan"     # change this
gf_name = "Hargun"    # change this if you want

def draw_text_center(text, font, color, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)

# ------------ MAIN LOOP ------------
def main():
    global hit, cheer, cheer_timer, ball_vx, ball_vy

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --------- UPDATE LOGIC ---------
        if not hit:
            # Ball moving towards batsman
            ball_rect.x += ball_vx
            ball_rect.y += ball_vy

            # Simple "contact" detection: when ball reaches batsman's x
            contact_x = batsman_rect.centerx - 10
            if ball_rect.centerx <= contact_x:
                hit = True
                cheer = True
                cheer_timer = 0
                ball_vx = BALL_SPEED_OUT_X
                ball_vy = BALL_SPEED_OUT_Y

        else:
            # After hit - ball flying for SIX
            ball_rect.x += ball_vx
            ball_rect.y += ball_vy
            ball_vy += 0.2  # gravity-ish

            cheer_timer += 1

        # Reset if ball goes off screen (loop animation)
        if ball_rect.right < 0 or ball_rect.top > HEIGHT + 50:
            hit = False
            cheer = False
            cheer_timer = 0
            ball_rect.center = (bowler_rect.centerx - 40, bowler_rect.centery - 40)
            ball_vx = BALL_SPEED_IN
            ball_vy = 0

        # --------- DRAW ---------
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(BG_COLOR)

        # Ground line
        pygame.draw.line(screen, (200, 230, 200), (0, GROUND_Y + 5), (WIDTH, GROUND_Y + 5), 4)

        # Crowd-ish background stripe
        pygame.draw.rect(screen, (40, 40, 60), (0, 0, WIDTH, 150))

        # Draw girlfriend (cheering)
        if cheer and cheer_timer % 20 < 10:
            # simple "bounce" effect
            offset_y = -10
        else:
            offset_y = 0
        gf_draw_rect = gf_rect.copy()
        gf_draw_rect.y += offset_y
        screen.blit(gf_img, gf_draw_rect)

        # Draw bowler & batsman
        screen.blit(bowler_img, bowler_rect)
        screen.blit(batsman_img, batsman_rect)

        # Draw ball
        screen.blit(ball_img, ball_rect)

        # Names / labels
        draw_text_center(f"{bf_name} at the crease 🏏", font_med, (255, 255, 255), 30)
        draw_text_center(f"{gf_name} cheering from the stands 💛", font_med, (255, 255, 0), 60)

        # If hit, show SIX
        if hit:
            draw_text_center("SIX!!! 🎉", font_big, (255, 215, 0), 120)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
