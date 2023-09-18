cursor_color = False

def setup(no_color: bool):
    global cursor_color
    cursor_color = not no_color

def move_up():
    print("\033[F", end="")

def erase():
    print("\033[2K\r", end="")

def red():
    if cursor_color:
        print("\033[31m", end="")

def green():
    if cursor_color:
        print("\033[32m", end="")

def yellow():
    if cursor_color:
        print("\033[33m", end="")

def blue():
    if cursor_color:
        print("\033[34m", end="")

def reset():
    print("\033[0m", end="")