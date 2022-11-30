from typing import Optional, List
from pathlib import Path

import click

START_PATTERN = 'download_files="$(cat <<EOF--dataset.file.url.chksum_type.chksum'
END_PATTERN = 'EOF--dataset.file.url.chksum_type.chksum'
STR_PATTERN = "SHA256"

def split_and_write(input_file: Path, output_files: List[Path]) -> None:
    with open(input_file, "r") as input_file_handle:
        match = False
        count = 0
        for index, line in enumerate(input_file_handle):
            stripped_line = line.rstrip()
            if stripped_line == START_PATTERN:
                count = index + 1 # +1 is to account that urls start from the next line
                print("Starting the matching process")
            elif stripped_line == END_PATTERN:
                count = index - count # Technically its index-1-count+1 
                print("Ending the matching process")
                break
    print(f"Number of urls = {count}")
            # if match:
            #     output = filter_by_year(stripped_line, line, desired_interval)
            #     if output != "NOLINE":
            #         output_file_handle.write(line)
            #     else:
            #         print(f"{stripped_line} is not part of the given years")
            # else:
            #     output_file_handle.write(line)


    

@click.command()
@click.argument("input_file", type=click.Path(exists=True, readable=True))
@click.argument("number_of_splits", required=True, type=click.INT)
def split_cli(input_file: click.Path, number_of_splits: click.INT):
    input_file = Path(input_file)
    output_files = []
    # output_files = [Path(f"filtered-{input_file.stem}-{n}{input_file.suffixes[-1]}").touch(exist_ok=True) for n in range(number_of_splits)]
    split_and_write(
        input_file=input_file,
        output_files=output_files,
    )


if __name__ == "__main__":
    split_cli()
