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
@click.option(
    "-m",
    "--move",
    "movedir",
    type=click.Path(),
    required=False,
)
def qc_cli(
    inputdirlist: click.Path,
    outputdir: Optional[click.Path],
    movedir: Optional[click.Path],
) -> None:
    if not inputdirlist:
        raise click.BadParameter("Please specify one or more input directory")
    if movedir is not None and outputdir is not None:
        raise click.BadParameter(
            "Please specify only one option - move \
zero size or smaller non zero size files or copy over the non zero \
files with maximum size"
        )
    if movedir is None and outputdir is None:
        print(
            "Since no option is specified we are resorting to default - \
copy over the non zero files with maximum size to qc"
        )
    if inputdirlist:
        inputdirlist = list(inputdirlist)
    inputdirlist = [Path(inputdir) for inputdir in inputdirlist]

    # TODO: Sort this logic out because both movedir and outputdir
    # are getting created
    if movedir is not None:
        movedir = Path(movedir)
        movedir.mkdir(exist_ok=True)
    else:
        if outputdir is None:
            outputdir = inputdirlist[0].parent / "qc"
        outputdir = Path(outputdir)
        outputdir.mkdir(exist_ok=True)

    allfilenames = [
        [input_file.name for input_file in inputdir.rglob("*.nc")]
        for inputdir in inputdirlist
    ]
    common_filenames = set.intersection(*[set(filenames) for filenames in allfilenames])
    uniquefilelist = {}

    if movedir is not None:
        for inputdir in inputdirlist:
            for input_file in inputdir.rglob("*.nc"):
                if input_file.name in common_filenames:
                    if input_file.name not in uniquefilelist:
                        uniquefilelist[input_file.name] = {
                            "path": input_file.resolve(),
                            "size": input_file.stat().st_size,
                        }
                    elif (
                        uniquefilelist[input_file.name]["size"]
                        < input_file.stat().st_size
                    ):
                        shutil.move(
                            uniquefilelist[input_file.name]["path"],
                            movedir / input_file.name,
                        )
                        uniquefilelist[input_file.name] = {
                            "path": input_file.resolve(),
                            "size": input_file.stat().st_size,
                        }
    else:
        for inputdir in inputdirlist:
            for input_file in inputdir.rglob("*.nc"):
                if input_file.name in common_filenames:
                    if input_file.name not in uniquefilelist:
                        uniquefilelist[input_file.name] = {
                            "path": input_file.resolve(),
                            "size": input_file.stat().st_size,
                        }
                    elif (
                        uniquefilelist[input_file.name]["size"]
                        < input_file.stat().st_size
                    ):
                        uniquefilelist[input_file.name] = {
                            "path": input_file.resolve(),
                            "size": input_file.stat().st_size,
                        }

        for filename, fileinfo in uniquefilelist.items():
            if fileinfo["size"] == 0:
                print(f"No input folder contains non zero {filename}")
            else:
                shutil.copyfile(fileinfo["path"], outputdir / filename)


if __name__ == "__main__":
    qc_cli()
