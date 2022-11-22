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
@click.argument("start_year", required=True, type=click.int)
@click.argument("end_year", required=True, type=click.int)
def filter_by_year(
    input_file: click.Path,
    output_file: Optional[click.Path],
    start_year: click.int,
    end_year: click.int,
):
    print("Hello world")


if __name__ == "__main__":
    filter_by_year()
