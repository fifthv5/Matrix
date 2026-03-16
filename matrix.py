#!/usr/bin/env python3
import curses
import random

def matrix_effect(stdscr):
    # --- Configuration ---
    MESSAGE = "SYSTEM FAILURE: REALITY NOT FOUND"
    
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(60)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)   # Head / Message
    curses.init_pair(2, 46, -1)                  # Bright Green
    curses.init_pair(3, 34, -1)                  # Dim Green
    curses.init_pair(4, 22, -1)                  # Darkest Green

    height, width = stdscr.getmaxyx()
    
    # Initialize columns: [y_pos, counter, speed_delay, trail_length]
    columns = [[random.randint(-height, 0), 0, random.randint(1, 3), random.randint(10, 25)] for _ in range(width)]
    chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890"

    # Pre-calculate message position (Center)
    msg_y = height // 2
    msg_x_start = (width // 2) - (len(MESSAGE) // 2)
    
    # Store the "frozen" state of the message characters
    message_map = {} # (y, x) -> char

    while True:
        new_h, new_w = stdscr.getmaxyx()
        if new_h != height or new_w != width:
            height, width = new_h, new_w
            msg_y = height // 2
            msg_x_start = (width // 2) - (len(MESSAGE) // 2)
            stdscr.clear()

        stdscr.erase()

        for x, col in enumerate(columns):
            y, counter, delay, length = col
            
            for i in range(length):
                char_y = y - i
                if 0 <= char_y < height:
                    # CHECK: Is this coordinate part of our message?
                    is_msg_area = (char_y == msg_y and msg_x_start <= x < msg_x_start + len(MESSAGE))
                    
                    if is_msg_area:
                        # If the rain has reached or passed this point, "reveal" the letter
                        char = MESSAGE[x - msg_x_start]
                        color = curses.color_pair(1) | curses.A_BOLD
                    else:
                        # Normal rain logic
                        if i == 0:
                            color = curses.color_pair(1) | curses.A_BOLD
                        elif i < length * 0.4:
                            color = curses.color_pair(2)
                        else:
                            color = curses.color_pair(4)
                        char = random.choice(chars)

                    try:
                        if x < width - 1:
                            stdscr.addch(char_y, x, char, color)
                    except curses.error:
                        pass

            # Movement Logic
            columns[x][1] += 1
            if columns[x][1] >= delay:
                columns[x][0] += 1
                columns[x][1] = 0

            if y - length > height:
                columns[x][0] = 0

        stdscr.refresh()
        if stdscr.getch() != -1:
            break

if __name__ == "__main__":
    try:
        curses.wrapper(matrix_effect)
    except KeyboardInterrupt:
        pass
