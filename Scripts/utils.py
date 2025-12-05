
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Matching fish "br" colors roughly
    BRRED = '\033[91m'
    BRGREEN = '\033[92m'
    BRYELLOW = '\033[93m'
    BRBLUE = '\033[94m'
    BRMAGENTA = '\033[95m'
    BRCYAN = '\033[96m'
    BRWHITE = '\033[97m'
    BRBLACK = '\033[90m'
    BRGREY = '\033[90m' # Often mapped to bright black
    WHITE = '\033[97m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    GREY = '\033[37m' # Light gray
    NORMAL = ENDC

import os
import sys
import subprocess
import time
import shutil

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_color(text, color=Colors.NORMAL, end='\n'):
    print(f"{color}{text}{Colors.ENDC}", end=end)

def typewriter(text, delay=0.05, color=Colors.NORMAL):
    print(color, end='')
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Colors.ENDC)

def loading_bar(chars=20, delay=0.05, char='█', prefix='', suffix=''):
    if prefix:
        print(prefix, end='')
    for _ in range(chars):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if suffix:
        print(suffix)
    else:
        print()

def run_command(command, shell=True, check=False, capture_output=False):
    """
    Runs a shell command.
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=check,
            text=True,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return e

def get_input(prompt, color=Colors.BRRED):
    print_color(prompt, color=color, end='')
    return input()

def check_root():
    if os.geteuid() != 0:
        return False
    return True
