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
conda env update -f conda.yaml --prune
conda activate vanity
```

This will install all necessary dependencies.

## Usage

To use the tool, run:
```sh
python src/vanity.py bread --dmv
```

Here's some example output:
```
Checking results against the CA DMV...
DISTANCE 0
         BREAD 🚫
DISTANCE 1
         8READ ✅   BAKERY 🚫  BR3AD 🚫   BRAD 🚫    BRE4D ✅   BRED 🚫    LOAF 🚫
DISTANCE 2
         1OAF ✅    8AKERY ✅  8R3AD ✅   8RAD ✅    8RE4D ✅   8RED ✅    B4KERY 🚫  BAK3RY ✅  BAKE 🚫    BAKED 🚫
         BAKING 🚫  BAKRY 🚫   BARD 🚫    BKERY ✅   BR34D ✅   BR3D ✅    BR4D 🚫    BRD 🚫     BUN 🚫     LAF 🚫
         LO4F ✅    LOF 🚫     RAD 🚫     REARED 🚫  ROAST 🚫
DISTANCE 3
         1AF 🚫     1O4F ✅    1OF 🚫     84KERY ✅  8AK3RY ✅  8AKE ✅    8AKED 🚫   8AKING ✅  8AKRY ✅   8ARD ✅
         8KERY ✅   8R34D ✅   8R3D ✅    8R4D ✅    8RD ✅     8UN ✅     B4K3RY ✅  B4KE 🚫    B4KED ✅   B4KING 🚫
         B4KRY ✅   B4RD ✅    BAK1NG ✅  BAK3 ✅    BAK3D ✅   BAKD 🚫    BAKIN9 ✅  BAKNG 🚫   BK3RY ✅   BKE 🚫
         BKED ✅    BKING 🚫   BKRY ✅    BN 🚫      COOK 🚫    COOKING 🚫 FDR 🚫     KEPT 🚫    L4F ✅     LF 🚫
         POET 🚫    R3ARED ✅  R4D ✅     RARED 🚫   RAST ✅    RD 🚫      RE4RED ✅  REAR3D ✅  REARD ✅   RERED ✅
         RO4ST ✅   ROA5T ✅   ROAS7 ✅   ROST 🚫    STEAK 🚫
```

You can omit the `--dmv` flag to skip querying the DMV,
and you can include the `--no-emoji` flag to suppress emojis.

To check a single license plate, use the `-d 0` option to skip the search.

```sh
% python src/vanity.py bread --dmv -d 0
Checking results against the CA DMV...
DISTANCE 0
         BREAD 🚫
```

To see options, run:
```sh
python src/vanity.py -h
```

## Contribute

If you add any dependencies, make sure to export the changes:

```sh
conda env export -n vanity --from-history | grep -v "prefix" > conda.yaml
```
