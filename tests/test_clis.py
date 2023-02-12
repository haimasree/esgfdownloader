from click.testing import CliRunner
from pathlib import Path

import pytest
import numpy as np

from src import esgffilterbyyear, splitter


@pytest.fixture
def runner():
    runner = CliRunner()
    yield runner


def get_parts(filename):
    # TODO: Make this a separate function in splitter.py
    # TODO: Make this identical to the filter tool or make the filter tool identical to splitter
    with open(filename, "r") as input_file_handle:
        content = (
            input_file_handle.read()
        )  # Assuming the file is large enough to be loaded into memory
    start_template = content.split(splitter.START_PATTERN)[0]
    urls = content.split(splitter.END_PATTERN)[
        1
    ]  # Not 0 because END_PATTERN is part of START_PATTERN
    urls = urls.split("\n")[
        1:-1
    ]  # There is an empty string at the begnining and end of the list which will be added back later
    end_template = content.split(splitter.END_PATTERN)[2]
    return start_template, urls, end_template


def is_same(filename1, filename2):
    with open(filename1) as file_handle1, open(filename2) as file_handle2:
        return file_handle1.read() == file_handle2.read()


def test_cli_correct_use_filter(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = test_dir / "filtered"
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(input_dir), "1850", "2014"],
    )
    assert result.exit_code == 0
    output_file = output_dir / "filtered-wget-test.sh"
    input_file = input_dir / "wget-test.sh"
    assert output_file.exists()
    assert is_same(input_file, output_file)
    output_file.unlink()
    output_file = output_dir / "filtered-wget-20220725055633.sh"
    input_file = input_dir / "wget-20220725055633.sh"
    assert output_file.exists()
    assert is_same(input_file, output_file)
    output_file.unlink()


def test_cli_correct_use_filter_customoutput(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(input_dir), "-o", str(output_dir), "1850", "2014"],
    )
    assert result.exit_code == 0
    output_file = output_dir / "filtered-wget-test.sh"
    input_file = input_dir / "wget-test.sh"
    assert output_file.exists()
    assert is_same(input_file, output_file)
    output_file = output_dir / "filtered-wget-20220725055633.sh"
    input_file = input_dir / "wget-20220725055633.sh"
    assert output_file.exists()
    assert is_same(input_file, output_file)


def test_cli_correct_use_filter_match_result(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(input_dir), "-o", str(output_dir), "2008", "2012"],
    )
    assert result.exit_code == 0
    output_file = output_dir / "filtered-wget-20220725055633.sh"
    input_file = input_dir / "wget-20220725055633.sh"
    assert output_file.exists()
    start_template, _, end_template = get_parts(input_file)
    res_start_template, urls, res_end_template = get_parts(output_file)
    assert len(urls) == 16
    assert urls == [
        "'ta_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/ta/gn/v20190429/ta_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'SHA256' '67597c0c291d60f01df2a8f6d822b7759a3b77a578ee8726ac270fd44ac03f5b'",
        "'ta_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/ta/gn/v20190429/ta_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'SHA256' 'cd7a8b1d00659c2e13a0d7e36064dc5cb4e33b649555c27312999b28b2731dde'",
        "'ua_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/ua/gn/v20190429/ua_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'SHA256' '1c67cdbba4c520d96852c3e04668ccbab7cd816cebfff286c4eff0eb5874c299'",
        "'ua_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/ua/gn/v20190429/ua_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'SHA256' '0cc332f5eecef45fcded5ea1cd8d0b6be558069cdf4599089ecffedd9ab150f6'",
        "'va_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/va/gn/v20190429/va_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'SHA256' '4c8cf3f4fafa6f27dbb7efceff7fba9efc00982be3a857bd6aa5de70b6f4c040'",
        "'va_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/va/gn/v20190429/va_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'SHA256' '901f4c1a09633355e4deca02ff3ba81b31b5e6c04967838db19539af1f587526'",
        "'zg_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/zg/gn/v20190429/zg_day_CanESM5_historical_r10i1p1f1_gn_20010101-20101231.nc' 'SHA256' 'c83de59fc1b80970caa7cfbdce51803f95beee7d044f8468b8f4b87d64bee525'",
        "'zg_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r10i1p1f1/day/zg/gn/v20190429/zg_day_CanESM5_historical_r10i1p1f1_gn_20110101-20141231.nc' 'SHA256' '2d008fc7c818c168527508e50bc3838a127ae278226ada38ab30b4774548f84e'",
        "'ta_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/ta/gn/v20190429/ta_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'SHA256' 'a868584b0fb03b5407777396197927da5a07095d72eed089091cf166edfe38f7'",
        "'ta_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/ta/gn/v20190429/ta_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'SHA256' '66df2a3cc8ee804143da988d53bacfb2e3e2dec1a09bf2f914e6de6ba3130ad6'",
        "'ua_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/ua/gn/v20190429/ua_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'SHA256' 'e2466535acf4953c768cc99e60132cfee06e6a5799d8ee9f7485854e91b1b04c'",
        "'ua_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/ua/gn/v20190429/ua_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'SHA256' 'f8574323ec10470e971d8a20fcf881eb67a8ab50e79a10686b6686f541027d17'",
        "'va_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/va/gn/v20190429/va_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'SHA256' '022cb95c266d8649baefffb573268e1a7198f2152d00fce3256c5cfd5aa6c00a'",
        "'va_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/va/gn/v20190429/va_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'SHA256' '48cc22db3424f33bc8789384e7d66dd3ef5a066c9ebb8e2898321ef252a58495'",
        "'zg_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/zg/gn/v20190429/zg_day_CanESM5_historical_r11i1p1f1_gn_20010101-20101231.nc' 'SHA256' '0d204bb84b7941c669f62c5a921f0c14e215397e617284d5ea922c1e3a33ac72'",
        "'zg_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'http://crd-esgf-drc.ec.gc.ca/thredds/fileServer/esgC_dataroot/AR6/CMIP6/CMIP/CCCma/CanESM5/historical/r11i1p1f1/day/zg/gn/v20190429/zg_day_CanESM5_historical_r11i1p1f1_gn_20110101-20141231.nc' 'SHA256' '995ee23ce365cd6b5f547601cd28e24a167c0897aaecc090ddb126d70423f71b'",
    ]
    assert start_template == res_start_template
    assert end_template == res_end_template


def test_cli_correct_use_split_number(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = test_dir / "split"
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-ns", "3"],
    )
    assert result.exit_code == 0
    output_filenames = [
        output_dir / f"split-wget-{pattern}-{n}.sh"
        for n in range(3)
        for pattern in ["20220725055633", "test", "mpilr_r30_hist"]
    ]
    for output_filename in output_filenames:
        assert output_filename.exists()
        output_filename.unlink()


def test_cli_correct_use_split_link(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data" / "splitlink"
    output_dir = test_dir / "data" / "split"
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-nl", "16"],
    )
    assert result.exit_code == 0
    output_filenames = [output_dir / f"splitlink-wget-test-{n}.sh" for n in range(11)]
    output_filenames = [
        output_dir / f"splitlink-wget-20220725055633-{n}.sh" for n in range(9)
    ]
    for output_filename in output_filenames:
        assert output_filename.exists()
        output_filename.unlink()


def test_cli_correct_use_split_groups(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = test_dir / "split"
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-g1", "tas", "-g2", "ta"],
    )
    assert result.exit_code == 0
    output_filenames = [
        output_dir / f"split-wget-{pattern}-{group}.sh"
        for group in ["tas", "ta"]
        for pattern in ["20220725055633", "test", "mpilr_r30_hist"]
    ]
    for output_filename in output_filenames:
        assert output_filename.exists()
        output_filename.unlink()


def test_cli_correct_use_split_groups_customoutput_match(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data" / "splitgroup"
    output_dir = tmp_path / "result"
    output_dir.mkdir()

    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-o", str(output_dir), "-g1", "vas", "-g2", "va", "-g2", "ta"],
    )
    assert result.exit_code == 0
    output_filenames = [
        output_dir / f"split-wget-{pattern}-{group}.sh"
        for group in ["vas", "va_ta"]
        for pattern in ["mpilr_r30_hist"]
    ]
    input_file = input_dir / "wget-mpilr_r30_hist.sh"
    input_start_template, input_urls, input_end_template = get_parts(input_file)

    for index, output_filename in enumerate(output_filenames):
        output_start_template, output_urls, output_end_template = get_parts(
            output_filename
        )
        assert output_start_template == input_start_template
        assert output_end_template == input_end_template
        if index == 0:
            assert output_urls == [
                "'vas_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18500101-18691231.nc' 'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r30i1p1f1/day/zg/gn/v20210901/vas_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18500101-18691231.nc' 'SHA256' '6db5f6845de25b2787b219b466b46d87facdb183b7beed3a441ab4857bcb2e43'",
                "'vas_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18700101-18891231.nc' 'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r30i1p1f1/day/zg/gn/v20210901/vas_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18700101-18891231.nc' 'SHA256' 'd275f66ee9001e7779f496085d33bdf7f9e9705a9d4efd263c85877c50323264'",
            ]
        else:
            assert output_urls == [
                "'ta_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18500101-18691231.nc' 'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r30i1p1f1/day/ta/gn/v20210901/ta_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18500101-18691231.nc' 'SHA256' 'a1f0af64d321b7e6d8a16d3048dbb2231334f676c9f71a3aedfc18dece135d06'",
                "'ta_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18700101-18891231.nc' 'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r30i1p1f1/day/ta/gn/v20210901/ta_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18700101-18891231.nc' 'SHA256' '4fadb01522d60760fa8988f59d238e571138440bc2a45148888c9dc34980e8de'",
                "'va_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18700101-18891231.nc' 'http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r30i1p1f1/day/va/gn/v20210901/va_day_MPI-ESM1-2-LR_historical_r30i1p1f1_gn_18700101-18891231.nc' 'SHA256' '4d7fd7de3236723e55ff36d03059a327f261fd0b5ee86f5466956a10d41f5602'",
            ]
    for output_filename in output_filenames:
        assert output_filename.exists()
        output_filename.unlink()


def test_cli_correct_use_split_link_customoutput(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data" / "splitlink"
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-o", str(output_dir), "-nl", "16"],
    )
    assert result.exit_code == 0
    output_filenames = [output_dir / f"splitlink-wget-test-{n}.sh" for n in range(11)]
    output_filenames = [
        output_dir / f"splitlink-wget-20220725055633-{n}.sh" for n in range(9)
    ]
    for output_filename in output_filenames:
        assert output_filename.exists()
        output_filename.unlink()


def test_cli_correct_use_split_number_customoutput(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-o", str(output_dir), "-ns", "3"],
    )
    assert result.exit_code == 0
    output_filenames = [
        output_dir / f"split-wget-{pattern}-{n}.sh"
        for n in range(3)
        for pattern in ["20220725055633", "test"]
    ]
    for output_filename in output_filenames:
        assert output_filename.exists()


def test_cli_correct_use_split_number_match(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-o", str(output_dir), "-ns", "3"],
    )
    assert result.exit_code == 0
    input_file = input_dir / "wget-20220725055633.sh"
    output_filenames = [
        output_dir / f"split-wget-20220725055633-{n}.sh" for n in range(3)
    ]
    input_start_template, input_urls, input_end_template = get_parts(input_file)
    input_url_sublist = np.array_split(input_urls, 3)

    for n in range(3):
        output_start_template, output_urls, output_end_template = get_parts(
            output_filenames[n]
        )
        assert output_start_template == input_start_template
        assert output_end_template == input_end_template
        assert output_urls == list(input_url_sublist[n])


def test_cli_correct_use_split_link_match(runner, tmp_path):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = tmp_path / "result"
    output_dir.mkdir()
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-o", str(output_dir), "-nl", "16"],
    )
    assert result.exit_code == 0
    input_file = input_dir / "wget-20220725055633.sh"
    output_filenames = [
        output_dir / f"splitlink-wget-20220725055633-{n}.sh" for n in range(9)
    ]
    input_start_template, input_urls, input_end_template = get_parts(input_file)
    input_url_sublist = np.array_split(input_urls, 3)
    input_url_sublists = np.array_split(input_urls, range(16, len(input_urls), 16))
    for index, input_url_sublist in enumerate(input_url_sublists):
        output_start_template, output_urls, output_end_template = get_parts(
            output_filenames[index]
        )
        assert output_start_template == input_start_template
        assert output_end_template == input_end_template
        assert output_urls == list(input_url_sublist)


def test_filter_invalidcli(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    invalid_input_dir = test_dir / "invalid"
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [],
    )
    assert result.exit_code == 2
    assert "Missing argument 'INPUT_FILEDIR'" in result.output
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(invalid_input_dir)],
    )
    assert result.exit_code == 2
    assert "Error: Invalid value for 'INPUT_FILEDIR'" in result.output
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(input_dir)],
    )
    assert result.exit_code == 2
    assert "Missing argument 'START_YEAR'" in result.output
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(input_dir), "2018"],
    )
    assert result.exit_code == 2
    assert "Missing argument 'END_YEAR'" in result.output
    result = runner.invoke(
        esgffilterbyyear.filter_cli,
        [str(input_dir), "2018", "stringvalue"],
    )
    assert result.exit_code == 2
    assert "Invalid value for 'END_YEAR'" in result.output


def test_split_invalidcli(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    invalid_input_dir = test_dir / "invalid"
    result = runner.invoke(
        splitter.split_cli,
        [],
    )
    assert result.exit_code == 2
    assert "Missing argument 'INPUT_FILEDIR'" in result.output
    result = runner.invoke(
        splitter.split_cli,
        [str(invalid_input_dir)],
    )
    assert result.exit_code == 2
    assert "Error: Invalid value for 'INPUT_FILEDIR'" in result.output
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-ns"],
    )
    assert result.exit_code == 2
    assert "Error: Option '-ns' requires an argument" in result.output
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-ns", "stringvalue"],
    )
    assert result.exit_code == 2
    assert (
        "Invalid value for '--number_of_splits' / '-ns': 'stringvalue'" in result.output
    )
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-nl"],
    )
    assert result.exit_code == 2
    assert "Error: Option '-nl' requires an argument" in result.output
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-nl", "stringvalue"],
    )
    assert result.exit_code == 2
    assert (
        "Invalid value for '--number_of_links' / '-nl': 'stringvalue'" in result.output
    )
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-ns", "3", "-g1", "vas", "-g2", "ua", "-g2", "ta"],
    )
    assert result.exit_code == 2
    assert (
        "Invalid value: Please specify exactly one  of three split criterias - two sets of variable groups, \
a number of split files or a number of links in a file"
        in result.output
    )
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-nl", "3", "-g1", "vas", "-g2", "ua", "-g2", "ta"],
    )
    assert result.exit_code == 2
    assert (
        "Invalid value: Please specify exactly one  of three split criterias - two sets of variable groups, \
a number of split files or a number of links in a file"
        in result.output
    )
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "-ns", "3", "-nl", "3"],
    )
    assert result.exit_code == 2
    assert (
        "Invalid value: Please specify exactly one  of three split criterias - two sets of variable groups, \
a number of split files or a number of links in a file"
        in result.output
    )
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir)],
    )
    assert result.exit_code == 2
    assert "Usage: split-cli [OPTIONS] INPUT_FILEDIR" in result.output
