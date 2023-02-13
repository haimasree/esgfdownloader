from typing import Optional
from pathlib import Path

import click


@click.command()
@click.option(
    "-i",
    "--input",
    "inputdirlist",
    type=click.Path(exists=True, readable=True),
    required=True,
    multiple=True,
)
@click.option(
    "-o",
    "--output",
    "outputdir",
    type=click.Path(),
    required=False,
)
def qc_cli(
    inputdirlist: click.Path,
    outputdir: Optional[click.Path],
) -> None:
    if not inputdirlist:
        raise click.BadParameter("Please specify one or more input directory")
    if inputdirlist:
        inputdirlist = list(inputdirlist)
    inputdirlist = [Path(inputdir) for inputdir in inputdirlist]
    if outputdir is None:
        outputdir = inputdirlist[0].parent / "qc"
    else:
        outputdir = Path(outputdir)
    outputdir.mkdir(exist_ok=True)


if __name__ == "__main__":
    qc_cli()
