from pathlib import Path
from typing import Optional

import click
import pandas as pd

START_PATTERN = "#These are the embedded files to be downloaded"
END_PATTERN = "# ESG_HOME should point to the directory containing ESG credentials."
STR_PATTERN = "SHA256"


def filter_by_year(
    stripped_line: str, original_line: str, desired_interval: pd.Interval
) -> str:
    if not stripped_line:
        return original_line
    elif STR_PATTERN not in stripped_line:
        return original_line
    else:
        interval = stripped_line.split(" ")[0][-21:-4]
        start, end = interval.split("-")
        start = int(start[0:4])
        end = int(end[0:4])
        if desired_interval.overlaps(pd.Interval(start, end, closed="both")):
            return original_line
        else:
            return "NOLINE"


def filter_and_write(
    input_file: Path, output_file: Path, start_year: int, end_year: int
) -> None:
    desired_interval = pd.Interval(start_year, end_year, closed="both")
    with open(input_file, "r") as input_file_handle, open(
        output_file, "w", newline="\n"
    ) as output_file_handle:
        match = False
        for line in input_file_handle:
            stripped_line = line.rstrip()
            if stripped_line == START_PATTERN:
                match = True
            elif stripped_line == END_PATTERN:
                match = False
            if match:
                output = filter_by_year(stripped_line, line, desired_interval)
                if output != "NOLINE":
                    output_file_handle.write(line)
                # else:
                #     print(f"{stripped_line} is not part of the given years")
            else:
                output_file_handle.write(line)


@click.command()
@click.argument("input_filedir", type=click.Path(exists=True, readable=True))
@click.option(
    "-o",
    "--output",
    "output_filedir",
    type=click.Path(),
    required=False,
)
@click.argument("start_year", required=True, type=click.INT)
@click.argument("end_year", required=True, type=click.INT)
def filter_cli(
    input_filedir: click.Path,
    output_filedir: Optional[click.Path],
    start_year: click.INT,
    end_year: click.INT,
):
    input_filedir = Path(input_filedir)
    if output_filedir is None:
        output_filedir = input_filedir.parent / "filtered"
    else:
        output_filedir = Path(output_filedir)
    output_filedir.mkdir(exist_ok=True)
    for input_file in input_filedir.rglob("wget-*.sh"):
        output_file = Path(
            output_filedir / f"filtered-{input_file.stem}{input_file.suffixes[-1]}"
        )
        print(f"Running filter {input_file} {output_file} {start_year} {end_year}")
        filter_and_write(
            input_file=input_file,
            output_file=output_file,
            start_year=start_year,
            end_year=end_year,
        )


if __name__ == "__main__":
    filter_cli()
