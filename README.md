## Installation instructions

### Clone 
```git clone https://github.com/haimasree/esgfdownloader.git```

### Virtual env package manager - conda
```
conda env create -f env.yml
conda activate filteresgf
python -m pip install .
```


## Usage of the filter tool:

1. `filter data/wget-20221026075853.sh -o data/output.sh 2014 2018`
2. `filter data/wget-20221026075853.sh 2014 2018` # will output to  filtered-wget-20221026075853.sh
