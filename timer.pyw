# TODO:
#  - Add optional 2 second delay
#  - Render best solve
#  - Remove last solve
#  - Add colors to timer

import pygame as pg
import time

from func import *
from settings import *


pg.init()
pg.font.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

roboto_medium = pg.font.Font("./Roboto/Roboto-Medium.ttf", int(HEIGHT * 0.25))
roboto_medium_small = pg.font.Font("./Roboto/Roboto-Medium.ttf", int(HEIGHT * 0.05))
roboto_light = pg.font.Font("./Roboto/Roboto-Light.ttf", int(HEIGHT * 0.1))
roboto_light_small = pg.font.Font("./Roboto/Roboto-Light.ttf", int(HEIGHT * 0.05))

timer_text = ""
milli_seconds_passed = 0
scramble = generate_scramble(SCRAMBLE_LENGTH)

running = True
timer_running = False

click_counter = 0
past_solves = []
past_solves = load_file(SAVE_FILE)

while running:
    # Update
    t = clock.tick(60) # 60 fps
    if timer_running:
        milli_seconds_passed += t

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if click_counter == 2:
                    timer_running = False
                click_counter += 1
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                if click_counter == 1:
                    timer_running = True
                click_counter += 1
                if click_counter == 4:
                    # Stopping timer
                    click_counter = 0
                    past_solves.append(milli_seconds_passed)
                    milli_seconds_passed = 0
                    scramble = generate_scramble(SCRAMBLE_LENGTH)

    
    timer_text = timer_to_str(milli_seconds_passed)
    # Draw
    screen.fill(BG)
    timer_surf = roboto_medium.render(timer_text, True, WHITE)
    timer_size = roboto_medium.size(timer_text)
    render_history(screen, past_solves, roboto_light)
    render_avgs(screen, past_solves, roboto_light_small, roboto_medium_small)

    scramble_surf = roboto_medium_small.render(scramble, True, WHITE)
    scramble_size = roboto_medium_small.size(scramble)

    screen.blit(timer_surf, ((WIDTH - timer_size[0]) / 2, 0))
    screen.blit(scramble_surf, ((WIDTH - scramble_size[0]) / 2, HEIGHT * 0.25 + 5))

    pg.display.flip()

with open(SAVE_FILE, "w") as f:
    f.write(str(past_solves))
pg.quit()