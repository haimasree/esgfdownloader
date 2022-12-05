from click.testing import CliRunner
from pathlib import Path
import pytest

from src import esgffilterbyyear


@pytest.fixture
def runner():
    runner = CliRunner()
    yield runner


def is_same(filename1, filename2):
    with open(filename1) as file_handle1, open(filename2) as file_handle2:
        return file_handle1.read() == file_handle2.read()


def test_cli_correct_use_filter(runner):
    test_dir = Path(__file__).resolve().parent
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(test_dir / "data"), "1850", "2014"],
    )
    assert result.exit_code == 0
    output_file = test_dir / "filtered" / "filtered-wget-test.sh"
    input_file = test_dir / "data" / "wget-test.sh"
    assert output_file.exists()
    assert is_same(input_file, output_file)
    output_file.unlink()

def test_cli_correct_use_filter_customoutput(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [
            str(test_dir / "data"), 
            "-o",
            str(output_dir),
            "1850", 
            "2014"
        ],
    )
    assert result.exit_code == 0
    output_file = output_dir / "filtered-wget-test.sh"
    input_file = test_dir / "data" / "wget-test.sh"
    assert output_file.exists()
    assert is_same(input_file, output_file)

def test_cli_correct_use_filter_customoutput(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [
            str(test_dir / "data"), 
            "-o",
            str(output_dir),
            "1850", 
            "2014"
        ],
    )
    assert result.exit_code == 0
    output_file = output_dir / "filtered-wget-test.sh"
    input_file = test_dir / "data" / "wget-test.sh"
    assert output_file.exists()
    assert is_same(input_file, output_file)