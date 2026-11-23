"""CSE423 Lab 02 - Catch the Diamonds!

Every visible shape is constructed with the eight-zone midpoint line-drawing
algorithm and GL_POINTS only. The OpenGL/GLUT calls are restricted to those
in the supplied demo programs and lab reference, with glutLeaveMainLoop()
explicitly allowed by the assignment's exit instructions.

Place this file next to the supplied OpenGL folder and run with Python.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time  # explicitly permitted by Assignment 2 for delta-time animation


# Coordinates have their origin at the lower-left corner of a 500x500 window.
WIDTH = 500
HEIGHT = 500

# Diamond: four line segments with a modest on-screen size.
DIAMOND_HALF_WIDTH = 10
DIAMOND_HALF_HEIGHT = 13

# Catcher: the four-sided trapezoid shown in the assignment.
CATCHER_TOP_HALF_WIDTH = 48
CATCHER_BOTTOM_HALF_WIDTH = 37
CATCHER_BOTTOM_Y = 16
CATCHER_TOP_Y = 29
CATCHER_STEP = 24

START_SPEED = 95.0            # pixels / second
ACCELERATION = 10.0           # pixels / second squared

catcher_x = WIDTH // 2
diamond_x = WIDTH // 2
diamond_y = HEIGHT - 20.0
diamond_color = (1.0, 1.0, 0.0)
score = 0
speed = START_SPEED
paused = False
game_over = False
cheat_mode = False
previous_time = time.time()
random_state = int(time.time() * 1000000) % 4294967296


def random_fraction():
    """Simple seeded pseudorandom generator; avoids importing extra libraries."""
    global random_state
    random_state = (1664525 * random_state + 1013904223) % 4294967296
    return random_state / 4294967296.0


# ------------------------ Midpoint line drawing ------------------------

def find_zone(x1, y1, x2, y2):
    """Identify the zone (0..7) of a directed line segment."""
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def convert_to_zone_zero(x, y, zone):
    """Reflect/swap a point into zone 0 using eight-way symmetry."""
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    else:  # zone 7
        return x, -y


def convert_from_zone_zero(x, y, zone):
    """Restore a midpoint pixel to the original line's zone."""
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    else:  # zone 7
        return x, -y


def midpoint_line(x1, y1, x2, y2):
    """Rasterize a line in any of 8 zones, using only GL_POINTS."""
    # Convert endpoints to integer pixel coordinates before rasterizing.
    x1, y1 = int(round(x1)), int(round(y1))
    x2, y2 = int(round(x2)), int(round(y2))

    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone_zero(x1, y1, zone)
    x2, y2 = convert_to_zone_zero(x2, y2, zone)

    # Ensure left-to-right traversal after the zone conversion.
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    increment_e = 2 * dy
    increment_ne = 2 * (dy - dx)

    x = x1
    y = y1
    glBegin(GL_POINTS)
    while x <= x2:
        original_x, original_y = convert_from_zone_zero(x, y, zone)
        glVertex2f(original_x, original_y)

        if d > 0:
            d += increment_ne
            y += 1
        else:
            d += increment_e
        x += 1
    glEnd()


# -------------------------- Shapes / drawing ---------------------------

def draw_diamond():
    glColor3f(diamond_color[0], diamond_color[1], diamond_color[2])
    x = int(round(diamond_x))
    y = int(round(diamond_y))
    midpoint_line(x, y + DIAMOND_HALF_HEIGHT, x + DIAMOND_HALF_WIDTH, y)
    midpoint_line(x + DIAMOND_HALF_WIDTH, y, x, y - DIAMOND_HALF_HEIGHT)
    midpoint_line(x, y - DIAMOND_HALF_HEIGHT, x - DIAMOND_HALF_WIDTH, y)
    midpoint_line(x - DIAMOND_HALF_WIDTH, y, x, y + DIAMOND_HALF_HEIGHT)


def draw_catcher():
    if game_over:
        glColor3f(1.0, 0.15, 0.2)  # red after losing
    else:
        glColor3f(1.0, 1.0, 1.0)  # usual white

    left_top = int(round(catcher_x - CATCHER_TOP_HALF_WIDTH))
    right_top = int(round(catcher_x + CATCHER_TOP_HALF_WIDTH))
    left_bottom = int(round(catcher_x - CATCHER_BOTTOM_HALF_WIDTH))
    right_bottom = int(round(catcher_x + CATCHER_BOTTOM_HALF_WIDTH))

    midpoint_line(left_top, CATCHER_TOP_Y, right_top, CATCHER_TOP_Y)
    midpoint_line(right_top, CATCHER_TOP_Y, right_bottom, CATCHER_BOTTOM_Y)
    midpoint_line(right_bottom, CATCHER_BOTTOM_Y, left_bottom, CATCHER_BOTTOM_Y)
    midpoint_line(left_bottom, CATCHER_BOTTOM_Y, left_top, CATCHER_TOP_Y)


def draw_buttons():
    # Restart: bright teal left-facing arrow (3 midpoint lines).
    glColor3f(0.0, 1.0, 0.9)
    midpoint_line(29, 470, 49, 485)
    midpoint_line(29, 470, 49, 455)
    midpoint_line(29, 470, 65, 470)

    # Middle: amber pause bars during play; play triangle while paused.
    glColor3f(1.0, 0.7, 0.1)
    if paused:
        midpoint_line(242, 455, 242, 485)
        midpoint_line(242, 485, 265, 470)
        midpoint_line(265, 470, 242, 455)
    else:
        midpoint_line(245, 455, 245, 485)
        midpoint_line(255, 455, 255, 485)

    # Exit: red X.
    glColor3f(1.0, 0.1, 0.2)
    midpoint_line(453, 455, 481, 485)
    midpoint_line(453, 485, 481, 455)


def display():
    """Only draw the current game state here; never change positions."""
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_buttons()
    draw_catcher()
    if not game_over:
        draw_diamond()
    glutSwapBuffers()


# -------------------------- Game mechanics -----------------------------

def new_diamond():
    global diamond_x, diamond_y, diamond_color
    left_limit = DIAMOND_HALF_WIDTH + 5
    right_limit = WIDTH - DIAMOND_HALF_WIDTH - 5
    diamond_x = left_limit + int(random_fraction() * (right_limit - left_limit + 1))
    diamond_y = float(HEIGHT - DIAMOND_HALF_HEIGHT - 5)
    # All 3 channels are relatively bright against the black background.
    diamond_color = (0.5 + 0.5 * random_fraction(),
                     0.5 + 0.5 * random_fraction(),
                     0.5 + 0.5 * random_fraction())


def restart_game():
    global score, catcher_x, speed, paused, game_over, cheat_mode, previous_time
    score = 0
    catcher_x = WIDTH // 2
    speed = START_SPEED
    paused = False
    game_over = False
    cheat_mode = False
    previous_time = time.time()
    new_diamond()
    print("Starting Over! Score:", score)
    glutPostRedisplay()


def has_collision():
    """AABB intersection as recommended in Assignment 2, page 13."""
    diamond_left = diamond_x - DIAMOND_HALF_WIDTH
    diamond_right = diamond_x + DIAMOND_HALF_WIDTH
    diamond_bottom = diamond_y - DIAMOND_HALF_HEIGHT
    diamond_top = diamond_y + DIAMOND_HALF_HEIGHT

    catcher_left = catcher_x - CATCHER_TOP_HALF_WIDTH
    catcher_right = catcher_x + CATCHER_TOP_HALF_WIDTH

    return (diamond_left < catcher_right and
            diamond_right > catcher_left and
            diamond_bottom < CATCHER_TOP_Y and
            diamond_top > CATCHER_BOTTOM_Y)


def move_catcher_automatically(dt):
    """Travel toward the falling diamond incrementally, not by teleporting."""
    global catcher_x
    distance = diamond_x - catcher_x
    if distance == 0:
        return

    # Calculate enough speed to arrive before the diamond reaches the bowl.
    # This adjusts to increasingly fast falling diamonds.
    time_left = (diamond_y - DIAMOND_HALF_HEIGHT - CATCHER_TOP_Y) / speed
    if time_left < dt:
        time_left = dt
    cheat_speed = 650.0
    necessary_speed = abs(distance) * 1.4 / time_left
    if necessary_speed > cheat_speed:
        cheat_speed = necessary_speed

    step = cheat_speed * dt
    if abs(distance) < step:
        step = abs(distance)
    if distance > 0:
        catcher_x += step
    else:
        catcher_x -= step

    # Keep the whole catcher within the display area.
    if catcher_x < CATCHER_TOP_HALF_WIDTH:
        catcher_x = CATCHER_TOP_HALF_WIDTH
    if catcher_x > WIDTH - CATCHER_TOP_HALF_WIDTH:
        catcher_x = WIDTH - CATCHER_TOP_HALF_WIDTH


def animate():
    """Only update positions and rules; time-based motion is FPS-independent."""
    global previous_time, diamond_y, speed, score, game_over
    current_time = time.time()
    dt = current_time - previous_time
    previous_time = current_time
    # Limit long jumps if the window is stalled or moved.
    if dt > 0.05:
        dt = 0.05
    if dt < 0:
        dt = 0

    if not paused and not game_over:
        if cheat_mode:
            move_catcher_automatically(dt)
        diamond_y -= speed * dt
        speed += ACCELERATION * dt

        if has_collision():
            score += 1
            print("Score:", score)
            new_diamond()
        elif diamond_y + DIAMOND_HALF_HEIGHT < CATCHER_BOTTOM_Y:
            game_over = True
            print("Game Over! Final Score:", score)

    glutPostRedisplay()


# ----------------------------- Input -----------------------------------

def special_keyboard(key, x, y):
    global catcher_x
    if game_over or paused or cheat_mode:
        return
    if key == GLUT_KEY_LEFT:
        catcher_x -= CATCHER_STEP
    elif key == GLUT_KEY_RIGHT:
        catcher_x += CATCHER_STEP

    if catcher_x < CATCHER_TOP_HALF_WIDTH:
        catcher_x = CATCHER_TOP_HALF_WIDTH
    if catcher_x > WIDTH - CATCHER_TOP_HALF_WIDTH:
        catcher_x = WIDTH - CATCHER_TOP_HALF_WIDTH
    glutPostRedisplay()


def keyboard(key, x, y):
    global cheat_mode
    if key == b'c' or key == b'C':
        if not game_over:
            cheat_mode = not cheat_mode
            if cheat_mode:
                print("Cheat Mode: ON")
            else:
                print("Cheat Mode: OFF")
            glutPostRedisplay()


def mouse(button, state, x, y):
    global paused, previous_time
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return

    # GLUT mouse y starts at the top; the game uses a bottom-left origin.
    game_y = HEIGHT - y
    if 445 <= game_y <= 493:
        if 15 <= x <= 78:
            restart_game()
        elif 218 <= x <= 280:
            if not game_over:
                paused = not paused
                previous_time = time.time()
                glutPostRedisplay()
        elif 430 <= x <= 493:
            print("Goodbye! Final Score:", score)
            glutLeaveMainLoop()  # explicitly permitted in Assignment 2 tips


# ---------------------------- Window -----------------------------------

def setup_projection():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds! - CSE423 Assignment 2")

    setup_projection()
    glClearColor(0, 0, 0, 1)
    glPointSize(2)

    new_diamond()
    print("Catch the Diamonds! | Left/Right: move | C: cheat | Top: restart/pause/exit")
    print("Score:", score)

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_keyboard)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMainLoop()


if __name__ == "__main__":
    main()
