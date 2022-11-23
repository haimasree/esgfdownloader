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

1. `filter data/wget-20221026075853.sh -o data/output.sh 2014 2018` # will output to data/output.sh
2. `filter data/wget-20221026075853.sh 2014 2018` # will output to  filtered-wget-20221026075853.sh

You can use the output files as you would use the original wget files
