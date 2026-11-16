import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))

import utils
from utils import Colors, check_root, run_command, print_color

def test_colors_attributes():
    assert Colors.HEADER == '\033[95m'
    assert Colors.OKGREEN == '\033[92m'
    assert Colors.FAIL == '\033[91m'
    assert Colors.ENDC == '\033[0m'
    assert Colors.BOLD == '\033[1m'

def test_check_root():
    with patch('os.geteuid', return_value=0):
        assert check_root() is True
    with patch('os.geteuid', return_value=1000):
        assert check_root() is False

def test_run_command_success():
    res = run_command("echo test", shell=True, capture_output=True)
    assert res.returncode == 0
    assert "test" in res.stdout

def test_print_color(capsys):
    print_color("Hello", color=Colors.OKGREEN)
    captured = capsys.readouterr()
    assert f"{Colors.OKGREEN}Hello{Colors.ENDC}\n" == captured.out
