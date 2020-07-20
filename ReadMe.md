# Machine Learning for Meme Analysis
> Work in progress project for learning how to detect and track memes online.

**Badges**
- build status

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)

## Table of Contents

- [Installation](#installation)
- [Scrape Memes](#scrape)
- [Extract Metadata](#extract)
- [Image Clustering](#image)
- [FAQ](#faq)
- [Support](#support)
- [License](#license)




## Installation

- Python 3.6 or higher

### Setup

> update and install this package first

```shell
$ brew update
$ brew install pandas
```
---
## Features
## Scrape Memes
## Extract Metadata
  > EXIF, IPTC, 8BIM, ICC
  
  > Add user-defined tags in the exiftool_config file for exiftool. 
  
  ![alt-text](https://github.com/elsa-k-donovan/Meme-Analysis/blob/master/exiftool_config.png)
  - There will be an additional metadata tag "Platform" which will be added to all images used in the Meme Viewer. This will be used to easily distinguish which memes came from which platform. 
  - Step 1: Run the [get_all_metadata.py](https://github.com/elsa-k-donovan/Meme-Analysis/blob/master/get_all_metadata.py) which will extract all metadata from your image directory, so that you can decide which tags to focus on. 
  - After this, run the [get_img_metadata.py](https://github.com/elsa-k-donovan/Meme-Analysis/blob/master/get_img_metadata.py) to import the metadata of images in a directory into a new csv file.
## Image Clustering




Python scripts included were used to parse data from csv and tsv files. 

Memes Pipeline project cloned from @zsavvas
[https://github.com/zsavvas/memes_pipeline]

## Meme Viewer

> Using OpenFrameworks for Mac v0.11.0 Using the Visual Studio Code template, which is only available in v0.11.0.
> Later opened my project made with v0.11.0 in the downgraded OpenFrameworks v0.10.0 in order to fix an ofxJSON compatibility issue.
- download ofxJSON and add it to your addons folder for openframeworks.
- change tsnePath in file to that of your JSON which has your coordinate points and your image filepaths.

> If any weird errors show up remember to use "Clean DEBUG" command. That solves most small issues. 
> If any additional openFrameworks error occur, open the c_cpp_properties.json file and make sure all paths are correct.
> Code --> Preferences --> Settings --> C++

---

