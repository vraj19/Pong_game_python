# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
paddle1_vel,paddle2_vel = 0,0
score1, score2 = 0,0
di = RIGHT

# initialize ball_pos and ball_vel for new bal in middle of table

ball_pos = [0, 0]
ball_vel = [0, 0]

# if direction is RIGHT, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos, ball_vel, di # these are vectors stored as lists
    ball_vel = [(random.randrange(120, 240))/60, -(random.randrange(60, 180))/60]
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    di = direction    
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    spawn_ball(di)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
           
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1]- 20 <= 0 or (HEIGHT - ball_pos[1]) == 20 :
        ball_vel[1] = -ball_vel[1]
     
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) or (WIDTH - BALL_RADIUS - PAD_WIDTH - 1 <= ball_pos[0]):
        if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) and ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]-0.1*ball_vel[0]
        elif (WIDTH - BALL_RADIUS - PAD_WIDTH - 1 <= ball_pos[0]) and ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]-0.1*ball_vel[0]   
        else:
            if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
                score2 += 1
                spawn_ball(RIGHT)
            elif WIDTH - BALL_RADIUS - PAD_WIDTH - 1 <= ball_pos[0]:
                score1 += 1
                spawn_ball(LEFT)
                
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Yellow", "Black")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos >= 0 and paddle1_pos <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    elif paddle1_pos < 0:
        paddle1_pos = -paddle1_pos
    elif paddle1_pos > HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT
        paddle1_pos -= paddle1_vel
    
    if paddle2_pos >= 0 and paddle2_pos <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    elif paddle2_pos < 0:
        paddle2_pos = -paddle2_pos
    elif paddle2_pos > HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT
        paddle2_pos -= paddle2_vel    
  
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos], [0, paddle1_pos + PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + PAD_HEIGHT], [PAD_WIDTH, paddle1_pos]], 1, 'Yellow', 'Black')
    canvas.draw_polygon([[WIDTH, paddle2_pos], [WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos]], 1, 'Yellow', 'Black')
       
    # draw scores
    canvas.draw_text(str(score1), [150,40], 48, "White")
    canvas.draw_text(str(score2), [450,40], 48, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 8
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -8
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 8
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -8
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background('Grey')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("RESTART", new_game)

# start frame
new_game()
frame.start()
