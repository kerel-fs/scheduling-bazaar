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

# satbazaar2

A package to download observations and demoddata from SatNOGS.

## Installation

```sh
git clone https://github.com/wiredlab/scheduling-bazaar
cd scheduling-bazaar
uv pip sync
```

## Getting started

### Create empty databases
```sh
get-observations --create --no-fetch observations.db demoddata.db
```

### Fetch observations & demoddata
```sh
get-observations observations.db demoddata.db
```

### Fetch observations only

To skip the download of demoddata, you can pass an empty string as second positional argument:

```sh
get-observations observations.db ""
```

### Fetch observations for a specified time range

```sh
START_DATE="$(date --date "2 days ago" --rfc-3339=seconds)"
END_DATE="$(date --date "1 day ago" --rfc-3339=seconds)"
get-observations --pages 2 --fetch --start "$START_DATE" --end "$END_DATE" observations.db demoddata.db
```
