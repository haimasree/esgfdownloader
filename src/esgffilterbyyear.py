from pathlib import Path
from typing import Optional

import click


@click.command()
@click.argument("input_file", type=click.Path(exists=True, readable=True))
@click.option(
    "-o",
    "--output",
    "output_file",
    type=click.Path(exists=True, readable=True),
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
    if output_file is None:
        output_file = f"filtered-{Path(input_file).stem}{Path(input_file).suffixes[-1]}"
    print(f"Hello world with {input_file}, {output_file}, {start_year} and {end_year}")


if __name__ == "__main__":
    filter_by_year()
