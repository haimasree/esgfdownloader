from pathlib import Path
from typing import Optional

import click


def filter_and_write(
    input_file: Path, output_file: Path, start_year: int, end_year: int
):
    print("Entered a function")


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
def filter_by_year(
    input_file: click.Path,
    output_file: Optional[click.Path],
    start_year: click.INT,
    end_year: click.INT,
):
    input_file = Path(input_file)
    if output_file is None:
        output_file = f"filtered-{input_file.stem}{input_file.suffixes[-1]}"
    filter_and_write(
        input_file=input_file,
        output_file=output_file,
        start_year=start_year,
        end_year=end_year,
    )
    print(f"Hello world with {input_file}, {output_file}, {start_year} and {end_year}")


if __name__ == "__main__":
    filter_by_year()
