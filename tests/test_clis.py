from click.testing import CliRunner
from pathlib import Path
import pytest

from src import esgffilterbyyear, splitter


@pytest.fixture
def runner():
    runner = CliRunner()
    yield runner


def get_parts(filename):
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


def test_cli_correct_use_split(runner):
    test_dir = Path(__file__).resolve().parent
    input_dir = test_dir / "data"
    output_dir = test_dir / "split"
    result = runner.invoke(
        splitter.split_cli,
        [str(input_dir), "3"],
    )
    assert result.exit_code == 0
    output_filenames = [
        output_dir / f"split-wget-{pattern}-{n}.sh"
        for n in range(3)
        for pattern in ["20220725055633", "test"]
    ]
    for output_filename in output_filenames:
        assert output_filename.exists()
        output_filename.unlink()
