import sys
import os
import pytest
from unittest.mock import patch, MagicMock, call

# Add Scripts to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))

import expac_master
from utils import Colors

@pytest.fixture
def mock_user():
    with patch('getpass.getuser', return_value='testuser') as m:
        yield m

def test_expac_missing(mock_user):
    with patch('shutil.which', return_value=None):
        with patch('expac_master.print_color') as mock_print:
            expac_master.main()
            mock_print.assert_called_with("CRITICAL: 'expac' MISSING.", Colors.RED)

def test_draw_splash(mock_user):
    with patch('expac_master.clear_screen') as mock_clear, \
         patch('expac_master.print_color') as mock_print, \
         patch('expac_master.loading_bar') as mock_loading, \
         patch('expac_master.time.sleep') as mock_sleep:
        expac_master.draw_splash()
        assert mock_clear.called
        assert mock_print.called
        assert mock_loading.call_count == 3
        # Verify user is in splash
        mock_print.assert_any_call("      [ SYSTEM IDENTITY: testuser ] [ ARCHITECTURE: HASWELL ]", Colors.BRBLACK)
        mock_print.assert_any_call("  > WELCOME BACK, testuser.", Colors.BRRED)

def test_draw_header():
    with patch('expac_master.clear_screen') as mock_clear, \
         patch('expac_master.print_color') as mock_print:
        expac_master.draw_header()
        assert mock_clear.called
        assert mock_print.called

def test_draw_footer(mock_user):
    with patch('socket.gethostname', return_value='test-host'), \
         patch('subprocess.getoutput', return_value='5.15.0-test'), \
         patch('expac_master.print_color') as mock_print:
        expac_master.draw_footer()

        hostname = 'test-host'
        kernel = '5.15.0-test'
        user = 'testuser'
        expected = f"║  NODE: {hostname:<15}  ::  KERNEL: {kernel:<15}  ::  USER: {user:<8} ║"
        mock_print.assert_any_call(expected, Colors.BRBLACK)

@patch('shutil.which', return_value='/usr/bin/expac')
@patch('expac_master.draw_splash')
@patch('expac_master.draw_header')
@patch('expac_master.draw_footer')
@patch('expac_master.get_input')
@patch('expac_master.clear_screen')
@patch('expac_master.time.sleep')
@patch('subprocess.run')
@patch('subprocess.check_output')
@patch('subprocess.Popen')
def test_main_menu_options(mock_popen, mock_check_output, mock_run, mock_sleep, mock_clear, mock_get_input, mock_footer, mock_header, mock_splash, mock_which):
    # Test sequence of inputs: 1, 2, 3, 4, 5 (target exists), 5 (target doesn't), 0 (exit)
    mock_get_input.side_effect = ['1', '', '2', '', '3', '', '4', '', '5', 'test-pkg', '', '5', 'unknown-pkg', '', '0']

    # For option 1 (MATRIX STREAM)
    mock_check_output.return_value = "pkg1|repo1|dep1|opt1\n"
    mock_popen_instance = mock_popen.return_value
    mock_popen_instance.communicate.return_value = (b"", b"")

    mock_run.side_effect = [
        MagicMock(returncode=0), # Option 2
        MagicMock(returncode=0), # Option 3
        MagicMock(returncode=0), # Option 4
        MagicMock(returncode=0), # Option 5: pacman -Qq test-pkg
        MagicMock(returncode=0), # Option 5: expac -H M ...
        MagicMock(returncode=1), # Option 5: pacman -Qq unknown-pkg
    ]

    expac_master.main()

    # Verify calls
    assert mock_splash.called
    assert mock_header.call_count == 7 # 1 initial + 6 from loop (after 1, 2, 3, 4, 5, 5)

    # Option 1: MATRIX STREAM
    mock_check_output.assert_any_call("expac -l ', ' '%n|%r|%N|%o' | sort", shell=True, text=True)
    mock_popen.assert_called_with(["column", "-t", "-s", "|"], stdin=expac_master.subprocess.PIPE)

    # Option 2: BLOAT HUNTER
    mock_run.assert_any_call("expac -H M '%m\t%n' | sort -h -r | head -50", shell=True)

    # Option 3: TIMELINE LOG
    mock_run.assert_any_call("expac --timefmt='%Y-%m-%d %T' '%l\\t%n' | sort | tail -20", shell=True)

    # Option 4: INTRUDER SCAN
    mock_run.assert_any_call("expac '%n\t[%r]' | grep -v -E 'core|extra' | sort", shell=True)

    # Option 5: TARGET INSPECTOR (exists)
    mock_run.assert_any_call(["pacman", "-Qq", "test-pkg"], stdout=expac_master.subprocess.DEVNULL, stderr=expac_master.subprocess.DEVNULL)

    # Option 5: TARGET INSPECTOR (doesn't exist)
    mock_run.assert_any_call(["pacman", "-Qq", "unknown-pkg"], stdout=expac_master.subprocess.DEVNULL, stderr=expac_master.subprocess.DEVNULL)

def test_main_invalid_command(mock_user):
    with patch('shutil.which', return_value='/usr/bin/expac'), \
         patch('expac_master.draw_splash'), \
         patch('expac_master.draw_header'), \
         patch('expac_master.draw_footer'), \
         patch('expac_master.get_input', side_effect=['invalid', '0']), \
         patch('expac_master.clear_screen'), \
         patch('expac_master.time.sleep'), \
         patch('expac_master.print_color') as mock_print:
        expac_master.main()
        mock_print.assert_any_call("  >> INVALID COMMAND.", Colors.RED)
