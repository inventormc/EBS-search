# Online Search Tool for Graphical Patterns in Electronic Band Structures

This repository hosts the code and a test case for the paper [arXiv:1710.11611](https://arxiv.org/abs/1710.11611). Tested with Python 3.6.5.

To see the tool in action, register for free at: [omdb.diracmaterials.org](https://omdb.diracmaterials.org)

## Installation
```
pip install -r requirements.txt
```

## Example
This repository contains a data folder with VASP calculations, you can add more calculations here. Each folder represents a single material. Next, to create an ANN (approximate nearest neighbours) index, run:
```
python create_index.py --dataset folder --band_index -1 --width 0.4 --dimensions 16 --trees 10
```

```
python search.py --band_index -1 --width 0.4 --dimensions 16
```
The following plot should appear:
![Search Result Dirac crossing](misc/crossing_search_result.png)

## Test
TODO