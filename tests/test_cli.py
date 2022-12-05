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
    assert is_same(output_file, input_file)
    output_file.unlink()
