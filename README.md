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

There are currently two supported ways to split - splits the urls into n (almost) equal parts or splits into two groups of variables where each group can include multiple variables. Both options can not be used together
- Splits the urls into n (almost) equal parts. Outputs n files which only differ in the selection of the urls 
  
  - `splitter ./data -o ./result -ns 3`
    - create a directory called `result` if not present and output 3 (number of desired splits provided by -ns flag) files prefixed with `split` for each input file `wget-*.sh` in `data/` 
  - `splitter ./data -ns 3` 
    - create a directory called `split` if not present and output 3 files (number of desired splits provided by -ns flag) prefixed with `split` for each input file `wget-*.sh` in `data/`

- Splits the urls into two groups based on variables. Outputs 2 files which only differ in the selection of the urls.
  
  - `splitter ./data -o ./result -g1 vas -g2 ta`
    - create a directory called `result` if not present and output two files prefixed with `split` and suffixed with group variable name for each input file `wget-*.sh` in `data/`
  - For using multiple variables for each group use the following syntax
    - `splitter ./data -o ./result -g1 vas -g1 psl -g2 ta -g2 ua -g2 zg`
    - Suffix of the resulting files will be like so - `split-*-vas_psl.sh`, `split-*-ta_ua_zg.sh`


You can use the output files as you would use the original wget files

## For running the tests:

### Install test specific dependencies
```
py -m pip install .[tests]
```

### Run the tests

```
pytest
```

### TODO:

Add the tests to CI

## TODO:

Combine both these tools