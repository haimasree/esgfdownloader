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
):
    desired_interval = pd.Interval(start_year, end_year, closed="both")
    with open(input_file, "r") as input_file_handle, open(
        output_file, "w"
    ) as output_file_handle:
        match = False
        for line in input_file_handle:
            stripped_line = line.rstrip()
            if stripped_line == START_PATTERN:
                match = True
                print("Starting the filtering process")
            elif stripped_line == END_PATTERN:
                match = False
                print("Ending the filtering process")
            if match:
                output = filter_by_year(stripped_line, line, desired_interval)
                if output != "NOLINE":
                    output_file_handle.write(line)
                else:
                    print(f"{stripped_line} is not part of the given years")
            else:
                output_file_handle.write(line)


@click.command()
@click.argument("input_file", type=click.Path(exists=True, readable=True))
@click.option(
    "-o",
    "--output",
    "output_file",
    type=click.Path(),
    required=False,
)
@click.argument("start_year", required=True, type=click.INT)
@click.argument("end_year", required=True, type=click.INT)
def filter_cli(
    input_file: click.Path,
    output_file: Optional[click.Path],
    start_year: click.INT,
    end_year: click.INT,
):
    input_file = Path(input_file)
    if output_file is None:
        output_file = Path(f"filtered-{input_file.stem}{input_file.suffixes[-1]}")
    filter_and_write(
        input_file=input_file,
        output_file=output_file,
        start_year=start_year,
        end_year=end_year,
    )
    print(f"Filtering {input_file}, {output_file}, {start_year} and {end_year}")


if __name__ == "__main__":
    filter_cli()
