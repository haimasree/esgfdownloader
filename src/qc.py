from typing import Optional
from pathlib import Path
import shutil

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

    allfilenames = [
        [input_file.name for input_file in inputdir.rglob("*.*")]
        for inputdir in inputdirlist
    ]
    common_filenames = set.intersection(*[set(filenames) for filenames in allfilenames])

    uniquefilelist = {}
    for inputdir in inputdirlist:
        for input_file in inputdir.rglob("*.*"):
            if input_file.name in common_filenames:
                if input_file.name not in uniquefilelist:
                    uniquefilelist[input_file.name] = {
                        "path": input_file.resolve(),
                        "size": input_file.stat().st_size,
                    }
                elif (
                    uniquefilelist[input_file.name]["size"] < input_file.stat().st_size
                ):
                    uniquefilelist[input_file.name] = {
                        "path": input_file.resolve(),
                        "size": input_file.stat().st_size,
                    }

    for filename, fileinfo in uniquefilelist.items():
        shutil.copyfile(fileinfo["path"], outputdir / filename)


if __name__ == "__main__":
    qc_cli()
