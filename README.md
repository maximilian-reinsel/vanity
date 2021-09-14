# vanity

## Table of contents

- [Introduction](#introduction)
- [Setup](#setup)
- [Usage](#usage)
- [Contribute](#contribute)

## Introduction

**Vanity** is a tool for generating vanity license plates.

## Setup

Install conda (through [anaconda](https://docs.anaconda.com/anaconda/install/) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)), then run:

```sh
conda env create -f conda.yaml
conda activate vanity
```

This will install all necessary dependencies.

## Usage

To use the tool, run:
```sh
python src/license_explorer.py
```

Here's some example output:
```
Enter word to start:BREAD
Enter max distance to output: 1
DISTANCE 0
         Option(word='BREAD', distance=0)
DISTANCE 1
         Option(word='8READ', distance=1)
         Option(word='BAKERY', distance=1)
         Option(word='BR3AD', distance=1)
         Option(word='BRAD', distance=1)
         Option(word='BRE4D', distance=1)
         Option(word='BRED', distance=1)
         Option(word='LOAF', distance=1)
```

## Contribute

If you add any dependencies, make sure to export the changes:

```sh
conda env export -n vanity --from-history | grep -v "prefix" > conda.yaml
```