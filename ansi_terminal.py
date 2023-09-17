def move_up():
    print("\033[F", end="")

def erase():
    print("\033[2K\r", end="")

def red():
    print("\033[31m", end="")

def green():
    print("\033[32m", end="")

def yellow():
    print("\033[33m", end="")

def reset():
    print("\033[0m", end="")