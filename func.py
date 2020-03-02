import pygame as pg

from settings import *

def timer_to_str(milli_seconds):
    output = ""
    if milli_seconds / 1000 / 60 > 1:
        output += str(int(milli_seconds / 1000 / 60))
        output += ":"
    minutes = str(int(milli_seconds / 1000) % 60)
    if len(minutes) == 1:
        minutes = "0" + minutes
    output += minutes
    output += ":"
    m = str(int(milli_seconds) % 1000)
    if len(m) == 2:
        m = "0" + m
    if len(m) == 1:
        m = "00" + m
    output += m
    return output

def render_history(surf, past_solves, font, color=(255, 255, 255)):
    last5 = reversed(past_solves[-5:])
    for i, solve in enumerate(last5):
        time_surf = font.render(timer_to_str(solve), True, color)
        surf.blit(time_surf, (WIDTH * 0.08, HEIGHT * 0.35 + HEIGHT * 0.1 * i))

def render_avgs(surf, past_solves, font1, font2, color=(255, 255, 255)):
    if len(past_solves) == 0:
        return
    last5      = past_solves[-5:]
    last12     = past_solves[-12:]
    last_total = past_solves[:]
    mean5      = float(sum(last5)) / len(last5)
    mean12     = float(sum(last12)) / len(last12)
    mean_total = float(sum(last_total)) / len(last_total)
    if len(last_total) <= 2:
        avg5 = mean5
        avg12 = mean12
        avg_total = mean_total
    else:
        avg5      = float(sum(last5) - min(last5) - max(last5)) / (len(last5) - 2)
        avg12     = float(sum(last12) - min(last12) - max(last12)) / (len(last12) - 2)
        avg_total = float(sum(last_total) - min(last_total) - max(last_total)) / (len(last_total) - 2)
    
    last_col = ["", "Last 5:", "Last 12:", "Total:"]
    mean_col = f"Mean\n{timer_to_str(mean5)}\n{timer_to_str(mean12)}\n{timer_to_str(mean_total)}"
    mean_col = mean_col.split("\n")
    avg_col = f"Average\n{timer_to_str(avg5)}\n{timer_to_str(avg12)}\n{timer_to_str(avg_total)}"
    avg_col = avg_col.split("\n")
    biggest_last = font2.size(last_col[0])[0]
    biggest_mean = font1.size(mean_col[0])[0]
    biggest_avg  = font1.size(avg_col[0])[0]
    for i, last in enumerate(last_col):
        size = font2.size(last)[0]
        if size > biggest_last:
            biggest_last = size
        time_surf = font2.render(last, True, color)
        surf.blit(time_surf, (WIDTH * 0.4, HEIGHT * 0.35 + 40 * i))
    for i, mean in enumerate(mean_col):
        if i == 0:
            size = font2.size(mean)[0]
            if size > biggest_mean:
                biggest_mean = size
            time_surf = font2.render(mean, True, color)
        else:
            size = font1.size(mean)[0]
            if size > biggest_mean:
                biggest_mean = size
            time_surf = font1.render(mean, True, color)
        surf.blit(time_surf, (WIDTH * 0.4 + biggest_last + 10, HEIGHT * 0.35 + 40 * i))
    for i, avg in enumerate(avg_col):
        if i == 0:
            size = font2.size(avg)[0]
            if size > biggest_avg:
                biggest_avg = size
            time_surf = font2.render(avg, True, color)
        else:
            size = font1.size(avg)[0]
            if size > biggest_avg:
                biggest_avg = size
            time_surf = font1.render(avg, True, color)
        surf.blit(time_surf, (WIDTH * 0.4 + biggest_last + biggest_mean + 20, HEIGHT * 0.35 + 40 * i))

def load_file(path):
    output = []
    try:
        with open(path) as f:
            contents = f.read().strip()
    except FileNotFoundError:
        return []
    
    contents = contents[1:-1].split(", ")
    output = list(map(int, contents))

    return output