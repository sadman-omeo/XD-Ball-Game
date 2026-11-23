from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import time

# Global Variables
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500

# Diamond Variables
dmnd_x, dmnd_y = 250, 350
dmnd_size = 12
dmnd_color = (1.0, 1.0, 1.0)

# Catcher Variables
catcher_x = 250
catcher_y = 15
catcher_width = 100
catcher_height = 15
# Catcher Movement
catcher_speed = 20

# Game State
is_paused = False
score = 0
game_over = False

# Cheat Mode
cheat_mode = False

# Diamond Movement
dmnd_speed = 100
dmnd_acceleration = 5

last_time = time.time()


# Find Zone
def FindZone(x1, y1, x2, y2):
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
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

# Convert Any Zone to Zone 0
def convert_to_zone0(x, y, zone):

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

    elif zone == 7:
        return x, -y


# Convert Zone 0 Back to Original Zone
def convert_to_origin(x, y, zone):

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

    elif zone == 7:
        return x, -y


def draw_points(x, y):
    glPointSize(2)          # Set pixel size of the point (default = 1)
    glBegin(GL_POINTS)      # Start drawing points
    glVertex2f(x, y)        # Specify the (x, y) coordinate of the point
    glEnd()                 # Finish drawing


# Midpoint Line Drawing Algorithm
def draw_line(x1, y1, x2, y2):

    x1 = int(round(x1)) 
    y1 = int(round(y1))
    x2 = int(round(x2)) 
    y2 = int(round(y2))

    zone = FindZone(x1, y1, x2, y2)

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    y = y1

    for x in range(x1, x2 + 1):
        px, py = convert_to_origin(x, y, zone)
        draw_points(px, py)

        if d > 0:
            d = d + incNE
            y = y + 1
        else:
            d = d + incE


# Draw Diamond
def draw_diamond():

    glColor3f(dmnd_color[0], dmnd_color[1], dmnd_color[2])

    draw_line(dmnd_x, dmnd_y + dmnd_size,
             dmnd_x + dmnd_size, dmnd_y)

    draw_line(dmnd_x + dmnd_size, dmnd_y,
             dmnd_x, dmnd_y - dmnd_size)

    draw_line(dmnd_x, dmnd_y - dmnd_size,
             dmnd_x - dmnd_size, dmnd_y)

    draw_line(dmnd_x - dmnd_size, dmnd_y,
             dmnd_x, dmnd_y + dmnd_size)


# Generate New Diamond
def spawn_diamond():
    global dmnd_x, dmnd_y, dmnd_color

    dmnd_x = random.randint(dmnd_size, WINDOW_WIDTH - dmnd_size)
    dmnd_y = WINDOW_HEIGHT - 55

    colors = [
        (1.0, 1.0, 0.0),
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 1.0),
        (0.0, 1.0, 0.0),
        (1.0, 0.5, 0.0),
        (1.0, 0.4, 0.6)
    ]

    dmnd_color = random.choice(colors)


# Restart Game
def restart_game():
    global score, game_over, is_paused
    global dmnd_speed, catcher_x, last_time
    global cheat_mode

    score = 0
    game_over = False
    is_paused = False
    cheat_mode = False

    dmnd_speed = 100
    catcher_x = WINDOW_WIDTH / 2

    last_time = time.time()

    spawn_diamond()

    print("Starting Over")


# Draw Catcher
def draw_catcher():
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    top_left = catcher_x - catcher_width // 2
    top_right = catcher_x + catcher_width // 2

    bottom_left = top_left + 10
    bottom_right = top_right - 10

    top_y = catcher_y + catcher_height
    bottom_y = catcher_y

    draw_line(top_left, top_y, top_right, top_y)
    draw_line(top_right, top_y, bottom_right, bottom_y)
    draw_line(bottom_right, bottom_y, bottom_left, bottom_y)
    draw_line(bottom_left, bottom_y, top_left, top_y)


# Draw Control Buttons
def draw_buttons():

    # Restart Button (Teal)
    glColor3f(0.0, 1.0, 1.0)

    draw_line(20, 470, 45, 470)
    draw_line(20, 470, 32, 482)
    draw_line(20, 470, 32, 458)

    # Play/Pause Button (Amber)
    glColor3f(1.0, 0.7, 0.0)

    if is_paused:
        # Play Icon
        draw_line(245, 460, 245, 480)
        draw_line(245, 480, 263, 470)
        draw_line(263, 470, 245, 460)

    else:
        # Pause Icon
        draw_line(245, 460, 245, 480)
        draw_line(255, 460, 255, 480)

    # Exit Button (Red)
    glColor3f(1.0, 0.0, 0.0)

    draw_line(460, 460, 480, 480)
    draw_line(460, 480, 480, 460)


# AABB Collision Detection
def has_collided(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
        return True


# Check Diamond and Catcher Collision
def check_collision():

    diamond_box = (dmnd_x - dmnd_size, dmnd_y - dmnd_size, dmnd_size * 2, dmnd_size * 2)
    catcher_box = (catcher_x - catcher_width / 2, catcher_y, catcher_width, catcher_height)

    return has_collided(diamond_box, catcher_box)


# Special Key Listener
def special_key_listener(key, x, y):
    global catcher_x

    if is_paused or game_over or cheat_mode:
        return

    if key == GLUT_KEY_LEFT:
        catcher_x -= catcher_speed

    elif key == GLUT_KEY_RIGHT:
        catcher_x += catcher_speed

    # Keep catcher inside the window
    if catcher_x - catcher_width / 2 < 0:
        catcher_x = catcher_width / 2

    if catcher_x + catcher_width / 2 > WINDOW_WIDTH:
        catcher_x = WINDOW_WIDTH - catcher_width / 2

    glutPostRedisplay()

# Mouse Listener
def mouse_listener(button, state, x, y):
    global is_paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        mouse_x = x
        mouse_y = WINDOW_HEIGHT - y

        # Restart Button
        if 10 <= mouse_x <= 55 and 450 <= mouse_y <= 490:
            restart_game()

        # Play/Pause Button
        elif 230 <= mouse_x <= 275 and 450 <= mouse_y <= 490:
            if not game_over:
                is_paused = not is_paused

        # Exit Button
        elif 450 <= mouse_x <= 490 and 450 <= mouse_y <= 490:
            print("Goodbye! Final Score:", score)
            glutLeaveMainLoop()
            return

        glutPostRedisplay()


# Keyboard Listener
def keyboard_listener(key, x, y):
    global cheat_mode

    if key == b'c' or key == b'C':
        if not game_over:
            cheat_mode = not cheat_mode

            if cheat_mode:
                print("Cheat Mode Activated")
            else:
                print("Cheat Mode Deactivated")

    glutPostRedisplay()


# Automatic Catcher Movement
def move_catcher_to_diamond(delta_time):
    global catcher_x

    target_x = dmnd_x

    # Keep catcher inside the screen
    if target_x < catcher_width / 2:
        target_x = catcher_width / 2

    elif target_x > WINDOW_WIDTH - catcher_width / 2:
        target_x = WINDOW_WIDTH - catcher_width / 2

    distance = target_x - catcher_x

    # Estimate time before diamond reaches catcher
    remaining_height = dmnd_y - dmnd_size - (catcher_y + catcher_height)

    if remaining_height < 1:
        remaining_height = 1

    time_left = remaining_height / dmnd_speed

    # Increase catcher speed when necessary
    auto_speed = max(600, abs(distance) * 2 / max(time_left, 0.001))

    movement = auto_speed * delta_time

    if distance > 0:
        catcher_x += min(distance, movement)

    elif distance < 0:
        catcher_x -= min(-distance, movement)






# Projection Setup
def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, 0, 1)
    glMatrixMode(GL_MODELVIEW)


# Display Function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    # Drawing functions will be added here

    if not game_over:
        draw_diamond()

    draw_catcher()
    draw_buttons()

    glutSwapBuffers()


# Animation Function
def animate():
    global dmnd_y, dmnd_speed, last_time
    global score, game_over

    curr_time = time.time()
    delta_time = curr_time - last_time
    last_time = curr_time



    if not is_paused and not game_over:

        prev_dmnd_y = dmnd_y
        # Move diamond downward
        dmnd_y -= dmnd_speed * delta_time
        
        # Gradually increase falling speed    
        dmnd_speed += dmnd_acceleration * delta_time

        # Automatic catcher movement
        if cheat_mode:
            move_catcher_to_diamond(delta_time)

        # Check horizontal overlap
        horizontal_overlap = (dmnd_x + dmnd_size > catcher_x - catcher_width / 2 
            and dmnd_x - dmnd_size < catcher_x + catcher_width / 2
        )

        # Check if diamond crosses the catcher between frames
        crossed_catcher = (prev_dmnd_y - dmnd_size >= catcher_y + catcher_height
            and dmnd_y - dmnd_size <= catcher_y + catcher_height
        )

        # Check collision
        if check_collision() or (crossed_catcher and horizontal_overlap):
            score += 1
            print("Score:", score)

            spawn_diamond()

        # Check if diamond is missed
        elif dmnd_y + dmnd_size < catcher_y:
            game_over = True
            print("Game Over! Final Score:", score)

    glutPostRedisplay()


# Main Function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")

    spawn_diamond()

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


if __name__ == "__main__":
    main()