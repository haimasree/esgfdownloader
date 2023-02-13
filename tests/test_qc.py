from click.testing import CliRunner
from pathlib import Path

import pytest

from src import qc


@pytest.fixture
def runner():
    runner = CliRunner()
    yield runner


def is_same(filename1, filename2):
    with open(filename1, "rb") as file_handle1, open(filename2, "rb") as file_handle2:
        return file_handle1.read() == file_handle2.read()


def test_qc_invalidcli(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    invalid_input_dir = test_dir / "invalid"
    result = runner.invoke(
        qc.qc_cli,
        [],
    )
    assert result.exit_code == 2
    assert "Missing option '-i' / '--input'" in result.output
    result = runner.invoke(qc.qc_cli, ["-i", str(invalid_input_dir)])
    assert result.exit_code == 2
    assert "does not exist" in result.output


def test_cli_correct_use_qc(runner):
    test_dir = (
        Path(__file__).resolve().parent / "data" / "cmiphist_results_example25012023"
    )
    inputdirlist = [
        test_dir / "1",
        test_dir / "2",
    ]
    outputdir = test_dir / "qc"
    result = runner.invoke(
        qc.qc_cli,
        ["-i", str(inputdirlist[0]), "-i", str(inputdirlist[1])],
    )
    assert result.exit_code == 0
    outputfilenames = [output_file.name for output_file in outputdir.rglob("*.*")]
    assert sorted(outputfilenames) == sorted(
        [
            "uas_day_CanESM5_historical_r17i1p1f1_gn_18500101-20141231.nc",
            "uas_day_CanESM5_historical_r20i1p1f1_gn_18500101-20141231.nc",
            "vas_day_CanESM5_historical_r19i1p1f1_gn_18500101-20141231.nc",
            "vas_day_CanESM5_historical_r4i1p1f1_gn_18500101-20141231.nc",
        ]
    )
    for output_file in outputdir.rglob("*.*"):
        output_file.unlink()
    outputdir.rmdir()


def test_cli_correct_use_qc_customoutput(runner, tmp_path):
    test_dir = (
        Path(__file__).resolve().parent / "data" / "cmiphist_results_example25012023"
    )
    inputdirlist = [
        test_dir / "1",
        test_dir / "2",
    ]
    outputdir = tmp_path / "result"
    outputdir.mkdir()
    result = runner.invoke(
        qc.qc_cli,
        ["-i", str(inputdirlist[0]), "-i", str(inputdirlist[1]), "-o", str(outputdir)],
    )
    assert result.exit_code == 0
    outputfilenames = [output_file.name for output_file in outputdir.rglob("*.*")]
    assert sorted(outputfilenames) == sorted(
        [
            "uas_day_CanESM5_historical_r17i1p1f1_gn_18500101-20141231.nc",
            "uas_day_CanESM5_historical_r20i1p1f1_gn_18500101-20141231.nc",
            "vas_day_CanESM5_historical_r19i1p1f1_gn_18500101-20141231.nc",
            "vas_day_CanESM5_historical_r4i1p1f1_gn_18500101-20141231.nc",
        ]
    )
    for output_file in outputdir.rglob("*.*"):
        output_file.unlink()
    outputdir.rmdir()


def test_cli_correct_use_qc_match(runner, tmp_path):
    test_dir = (
        Path(__file__).resolve().parent / "data" / "cmiphist_results_example25012023"
    )
    inputdirlist = [
        test_dir / "1",
        test_dir / "2",
    ]
    outputdir = tmp_path / "result"
    outputdir.mkdir()
    result = runner.invoke(
        qc.qc_cli,
        ["-i", str(inputdirlist[0]), "-i", str(inputdirlist[1]), "-o", str(outputdir)],
    )
    assert result.exit_code == 0
    outputfilenames = [output_file.name for output_file in outputdir.rglob("*.*")]

    assert is_same(outputdir / outputfilenames[0], inputdirlist[1] / outputfilenames[0])
    assert is_same(outputdir / outputfilenames[1], inputdirlist[1] / outputfilenames[1])
    assert is_same(outputdir / outputfilenames[2], inputdirlist[0] / outputfilenames[2])
    assert is_same(outputdir / outputfilenames[3], inputdirlist[1] / outputfilenames[3])

    assert not is_same(
        outputdir / outputfilenames[0], inputdirlist[0] / outputfilenames[0]
    )
    assert not is_same(
        outputdir / outputfilenames[1], inputdirlist[0] / outputfilenames[1]
    )
    assert not is_same(
        outputdir / outputfilenames[2], inputdirlist[1] / outputfilenames[2]
    )
    assert not is_same(
        outputdir / outputfilenames[3], inputdirlist[0] / outputfilenames[3]
    )

    for output_file in outputdir.rglob("*.*"):
        output_file.unlink()
    outputdir.rmdir()
