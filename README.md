# MOT2VOC
Scripts to convert from MOTChallenge dataset to VOC like dataset

## Preparation
1. First of all, clone the code
```
git clone https://github.com/agirbau/MOT2VOC.git
```

2. Install the requisites:
```
pip install -r requirements.txt
```

This script has been tested for python3.5 (remember that 2.7 is not longer supported in 2020!)

3. Finally download the MOTChallenge data:
    Download [MOT17Det](https://motchallenge.net/data/MOT17Det.zip) and unzip
    ```
    wget https://motchallenge.net/data/MOT17Det.zip -P your/path/to/the/MOT/dataset
    ```
    ```
    cd your/path/to/the/MOT/dataset
    unzip MOT17Det.zip
    cd -
    ```

## Usage
Simply pass as an argument the MOTDet path and the path where the VOC-like dataset will be generated. 
```
python MOT_to_VOC.py --mot_path your/path/to/the/MOT/dataset --voc_path your/path/to/the/VOC/dataset
```

As an example:

```
python MOT_to_VOC.py --mot_path /imatge/agirbau/work/MOT/MOT17/MOT17Det --voc_path /imatge/agirbau/work/MOT/MOT17/MOT17_voc
```

The dataset structure will be the same as the original MOTChallenge dataset, but the `gt` folder will contain an XML file per frame instead of a global `gt.txt` file.


As an example for reading the VOC-like data there's a visualization script that shows the ground truth for a sequence:
```
python MOT_VOC_visualization.py --voc_path --voc_path your/path/to/the/VOC/dataset/train/MOT-sequence
```

As an example:

```
python MOT_VOC_visualization.py --voc_path /mnt/7C1A87F757CA1344/datasets/MOT17/MOT17_voc/train/MOT17-04 
```
