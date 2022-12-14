import re
from typing import List, Optional
from pathlib import Path

import numpy as np
import click

START_PATTERN = 'download_files="$(cat <<EOF--dataset.file.url.chksum_type.chksum'
END_PATTERN = "EOF--dataset.file.url.chksum_type.chksum"
STR_PATTERN = "SHA256"

# TODO: Add a chunk version for files which can not be loaded into memory
def splitbygroup_and_write(
    input_file: Path, output_files: List[Path], group1: List, group2: List
) -> None:
    with open(input_file, "r") as input_file_handle:
        content = (
            input_file_handle.read()
        )  # Assuming the file is large enough to be loaded into memory
    start_template = content.split(START_PATTERN)[0]
    urls = content.split(END_PATTERN)[
        1
    ]  # Not 0 because END_PATTERN is part of START_PATTERN
    urls = urls.split("\n")[
        1:-1
    ]  # There is an empty string at the begnining and end of the list which will be added back later
    end_template = content.split(END_PATTERN)[2]
    group_url_list = [
        [url for url in urls for variable in disjoint_group if f"{variable}_" in url]
        for disjoint_group in [group1, group2]
    ]

    for index, group_urls in enumerate(group_url_list):
        with open(output_files[index], "w", newline="\n") as output_file_handle:
            output_file_handle.write(start_template)
            output_file_handle.write(START_PATTERN)
            output_file_handle.write("\n")
            output_file_handle.write("\n".join(group_urls))
            output_file_handle.write("\n")
            output_file_handle.write(END_PATTERN)
            output_file_handle.write(end_template)


def splitbynumber_and_write(
    input_file: Path, output_files: List[Path], number_of_splits: int
) -> None:
    with open(input_file, "r") as input_file_handle:
        content = (
            input_file_handle.read()
        )  # Assuming the file is large enough to be loaded into memory
    start_template = content.split(START_PATTERN)[0]
    urls = content.split(END_PATTERN)[
        1
    ]  # Not 0 because END_PATTERN is part of START_PATTERN
    urls = urls.split("\n")[
        1:-1
    ]  # There is an empty string at the begnining and end of the list which will be added back later
    end_template = content.split(END_PATTERN)[2]
    url_sublist = np.array_split(urls, number_of_splits)
    assert len(url_sublist) == number_of_splits
    for index in range(number_of_splits):
        with open(output_files[index], "w", newline="\n") as output_file_handle:
            output_file_handle.write(start_template)
            output_file_handle.write(START_PATTERN)
            output_file_handle.write("\n")
            output_file_handle.write("\n".join(url_sublist[index]))
            output_file_handle.write("\n")
            output_file_handle.write(END_PATTERN)
            output_file_handle.write(end_template)


@click.command()
@click.argument("input_filedir", type=click.Path(exists=True, readable=True))
@click.option(
    "-o",
    "--output",
    "output_filedir",
    type=click.Path(),
    required=False,
)
@click.option("--number_of_splits", "-ns", type=click.INT)
@click.option("--group1", "-g1", multiple=True)
@click.option("--group2", "-g2", multiple=True)
def split_cli(
    input_filedir: click.Path,
    output_filedir: Optional[click.Path],
    number_of_splits: Optional[click.INT],
    group1: Optional[str],
    group2: Optional[str],
) -> None:
    if not (group1 and group2) and number_of_splits is None:
        raise click.BadParameter(
            "Please specify atleast two sets of variable groups or a number of split files"
        )
    elif (group1 and group2) and number_of_splits is not None:
        raise click.BadParameter(
            "Please specify either two sets of variable groups or a number of split files - not both"
        )
    if group1 and group2:
        group1 = list(group1)
        group2 = list(group2)
    input_filedir = Path(input_filedir)
    if output_filedir is None:
        output_filedir = input_filedir.parent / "split"
    else:
        output_filedir = Path(output_filedir)
    output_filedir.mkdir(exist_ok=True)
    for input_file in input_filedir.rglob("wget-*.sh"):
        if group1 and group2:
            print(
                f"Splitting {input_file} into 2 files and writing to {output_filedir}"
            )
            output_files = [
                Path(
                    output_filedir
                    / f"split-{input_file.stem}-{'_'.join(group)}{input_file.suffixes[-1]}"
                )
                for group in [group1, group2]
            ]
            splitbygroup_and_write(
                input_file=input_file,
                output_files=output_files,
                group1=group1,
                group2=group2,
            )
        else:
            print(
                f"Splitting {input_file} into {number_of_splits} files and writing to {output_filedir}"
            )
            output_files = [
                Path(
                    output_filedir
                    / f"split-{input_file.stem}-{n}{input_file.suffixes[-1]}"
                )
                for n in range(number_of_splits)
            ]
            splitbynumber_and_write(
                input_file=input_file,
                output_files=output_files,
                number_of_splits=number_of_splits,
            )


if __name__ == "__main__":
    split_cli()
