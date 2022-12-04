## Installation instructions

### Clone 
```git clone https://github.com/haimasree/esgfdownloader.git```

### Virtual env package manager - conda
```
cd esgfdownloader
conda env create -f env.yml
conda activate filteresgf
python -m pip install .
```


## Usage of the filter tool:

1. `filter ./data -o ./result 2014 2018` # will create a directory called `result` if not present and output one file prefixed with `filtered` for each input file `wget-*.sh` in `data/` 

2. `filter ./data 2014 2018` # will create a directory called `filtered` if not present and output one file prefixed with `filtered` for each input file `wget-*.sh` in `data/` 

You can use the output files as you would use the original wget files


## Usage of the split tool:

Splits the urls into n (almost) equal parts. Outputs n files which only differ in the selection of the urls

`splitter ./data -o ./result 3` # will create a directory called `result` if not present and output one file prefixed with `split` for each input file `wget-*.sh` in `data/` 
`splitter ./data 3` # will create a directory called `split` if not present and output one file prefixed with `split` for each input file `wget-*.sh` in `data/`

You can use the output files as you would use the original wget files

## TODO:

Combine both these tools