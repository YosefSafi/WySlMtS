import pytest
from wyslmts.utils import success_print, info_print, error_exit
from typer import Exit

def test_utils_output(capsys):
    success_print("Success message")
    captured = capsys.readouterr()
    assert "Success:" in captured.out
    assert "Success message" in captured.out

    info_print("Info message")
    captured = capsys.readouterr()
    assert "Info:" in captured.out
    assert "Info message" in captured.out

def test_error_exit():
    with pytest.raises(Exit) as excinfo:
        error_exit("Critical error")
    assert excinfo.value.exit_code == 1
