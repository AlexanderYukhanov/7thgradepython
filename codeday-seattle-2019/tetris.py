import random
import time


WIDTH = 300
HEIGHT = 450
BOX = 15
PALETTE = [
    (0, 0, 0),
    (0, 200, 0),
    (0, 200, 200),
    (200, 200, 0),
    (0, 0, 200),
    (200, 0, 0)
]

# Create an empty cup
cup = [None,] * (HEIGHT // BOX)
for y in range(len(cup)):
    cup[y] = [0] * (WIDTH // BOX)
SHAPE_I = [
    [[1,1,1,1]],
    [
        [1],
        [1],
        [1],
        [1],
    ],
]

SHAPE_H = [
    [
    [1,1],
    [1,1]
    ],
]

SHAPE_TT = [
    [
    [1,1,1],
    [0,1,0],
    [0,1,0],
    ],

    [
    [1,0,0],
    [1,1,1],
    [1,0,0],
    ],

    [
    [0,1,0],
    [0,1,0],
    [1,1,1],
    ],

    [
    [0,0,1],
    [1,1,1],
    [0,0,1],
    ],
]

SHAPE_T = [
    [
        [1,1,1],
        [0,1,0],
    ],
    [
        [1,0],
        [1,1],
        [1,0]
    ],
    [
        [0,1,0],
        [1,1,1]
    ],
    [
        [0,1],
        [1,1],
        [0,1],
    ]
]

SHAPE_Z = [
    [
        [1,1,0],
        [0,1,1],
    ],
    [
        [0,1],
        [1,1],
        [1,0],
    ]
]

SHAPE_ZZ = [
    [
        [0,1,1],
        [1,1,0]
    ],
    [
        [1,0],
        [1,1],
        [0,1]
    ]
]

SHAPE_L = [
    [
        [1,1,1],
        [0,0,1],
    ],
    [
        [1,1],
        [1,0],
        [1,0],
    ],
    [
        [1,0,0],
        [1,1,1],
    ],
    [
        [0,1],
        [0,1],
        [1,1],
    ],
]

SHAPE_LL = [
    [
        [1,1,1],
        [1,0,0],
    ],
    [
        [1,0],
        [1,0],
        [1,1],
    ],
    [
        [0,0,1],
        [1,1,1],
    ],
    [
        [1,1],
        [0,1],
        [0,1],
    ],
]

SHAPES = [SHAPE_L, SHAPE_LL, SHAPE_I, SHAPE_T, SHAPE_TT, SHAPE_Z, SHAPE_ZZ, SHAPE_H]

rect = Rect((WIDTH // 2, 0), (BOX - 2, BOX - 2))

delay = 20
speed = 1

shape = random.choice(SHAPES)
state = 0
color = 1
score = 0
dx = 0
period = 0.5

def can_go_here(rc):
    """Checks if the current shape is allowed in this position
    """
    if rc.left < 0:
        return False
    try:
        view = shape[state]
        for y in range(len(view)):
            for x in range(len(view[y])):
                if view[y][x] == 0:
                    continue
                if cup[rc.top // BOX + y][rc.left // BOX + x] != 0:
                    return False
        return True
    except IndexError:
        return False


def draw_shape():
    """Draws the shape
    """
    view = shape[state]
    for y in range(len(view)):
        for x in range(len(view[y])):
            if view[y][x] == 0:
                continue
            screen.draw.filled_rect(rect.move(BOX * x + 1, BOX * y + 1), PALETTE[color])


def draw_cup():
    """Draws the cup
    """
    for y in range(len(cup)):
        for x in range(len(cup[y])):
            if cup[y][x] == 0:
                continue
            screen.draw.filled_rect(Rect((BOX * x + 1, BOX * y + 1), (BOX -2, BOX-2)), PALETTE[cup[y][x]])


def draw():
    """Draws the scene
    """
    screen.fill((10, 10, 10))
    if not can_go_here(rect):
        screen.draw.text("GAME OVER", midtop=(WIDTH // 2, 50), color="purple", fontsize=60)
        screen.draw.text("Your final score: {}".format(score), midtop=(WIDTH // 2, 100), fontsize=30, color="green")
        screen.draw.text("Press SPACE to restart", midbottom=(WIDTH // 2, HEIGHT), fontsize=30, color="white")
        return

    screen.blit('gb.jpg', (0, 0))
    draw_shape()
    draw_cup()
    screen.draw.text("Score: {0}".format(score), midtop=(WIDTH//2, 10), color="red", gcolor="purple", fontsize=30)

def on_key_down(key):
    global speed, state, dx, score
    if key == keys.LEFT:
        dx = -BOX
    elif key == keys.RIGHT:
        dx = BOX
    elif key == keys.DOWN:
        speed = 2
    elif key == keys.UP:
        old_state = state
        state +=1
        if state >= len(shape):
            state = 0
        if not can_go_here(rect):
            state = old_state
    elif key == keys.SPACE and not can_go_here(rect):
        # reset everything for the new game
        for y in range(len(cup)):
            for x in range(len(cup[y])):
                cup[y][x] = 0
        score = 0
        sounds.mix3.play()

def on_key_up(key):
    global speed
    global dx
    speed = 1
    dx = 0

last_move = time.time()
last_fall = time.time()
def update():
    global rect, speed, last_move, last_fall, rect, color, shape, state, cup, score

    if not can_go_here(rect):
        # the game is over
        sounds.mix3.stop()
        return

    # handle player's move
    if time.time() - last_move >= 0.1:
        if dx != 0:
            last_move = time.time()
        new_rect = rect.move(dx, 0)
        if can_go_here(new_rect):
            rect = new_rect

        if keyboard.DOWN:
            speed += 1

    # handle fallind down
    if time.time() - last_fall < period / speed:
        return
    last_fall = time.time()
    new_rect = rect.move(0, BOX)

    if can_go_here(new_rect):
        rect = new_rect
    else:
        # reached the ground, copy the shape to the cup
        view = shape[state]
        for y in range(len(view)):
            for x in range(len(view[y])):
                if view[y][x] == 0:
                    continue
                cup[rect.top // BOX + y][rect.left // BOX + x] = color
        score +=1

        # check if there are lines to delete
        for y in range(len(cup)):
            to_delete = True
            for x in range(len(cup[y])):
                if cup[y][x] == 0:
                    to_delete = False
            if to_delete:
               sounds.eep.play()# delete y element from the cup
               cup = cup [:y] + cup [y+1:]
               # add an epmpty line to the cup
               cup = [[0] * (WIDTH //BOX)] + cup
               score +=50
        # new shape
        rect = Rect((WIDTH // 2, 0), (BOX - 2, BOX - 2))
        shape = random.choice(SHAPES)
        state = random.randint(0, len(shape) - 1)
        color = random.randint(1, len(PALETTE) - 1)
        # set default speed
        speed = 1

sounds.mix3.play()
