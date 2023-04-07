# scheduling-bazaar
Package to simulate space-ground scheduling schemes. 

This project will be used to find contacts, or "visible" passes, for ground stations and satellites. 
The contacts will be used to answer scheduling questions for a network of ground stations. 


# Prerequisites

* numpy
* ephem
* orbit
* intervaltree
* iso8601

`conda env update -f environment.yml`

Uses `direnv` tool to manage shell setup.


# Git LFS
The `data/` directory is a submodule which stores generated data for testing.
That submodule uses [Git Large File Storage](https://git-lfs.github.com/) and its use requires installation of a Git extension, see the link for more information.

Checkout by `git submodule update --init`

# satbazaar

A package to analyze stations, observations and TLEs from SatNOGS.

## Configuration

See satbazaar.cfg-dist

## Usage
```
usage: get-observations.py [-h] [--create] [--fetch | --no-fetch] [--pages MAX_EXTRA_PAGES] [--retry-unknown] [--retry-observer] [--reverse] [--idstart IDSTART] [--idend IDEND]
                           [--start START] [--end END]
                           observations.db

positional arguments:
  observations.db       Database of observations

options:
  -h, --help            show this help message and exit
  --create              Create the DB if it doesn't exist
  --fetch, --no-fetch   Fetch new observations (default: True)
  --pages MAX_EXTRA_PAGES
                        Extra pages to fetch (default: [50])
  --retry-unknown       Retry fetching obs. with "unknown" status
  --retry-observer      Retry fetching obs. with null "observer" field
  --reverse             Retry obs by descending ID
  --idstart IDSTART     First obs ID to inspect when retrying
  --idend IDEND         Last obs ID to inspect when retrying
  --start START         Obs beginning after this datetime (RFC3339)
  --end END             Obs ending before this datetime (RFC3339)
```

## Task: Fetch observations of one specific day

```
/python-files/get-observations.py --create --fetch --start 2023-04-04 --end 2023-04-05 ../../data/all/observations.db --pages 186
```
