#!/usr/bin/bash

CURRENT_DIR=`pwd`
WORK_DIR=`mktemp -d`
cd "$WORK_DIR"
git clone https://gitlab.com/librespacefoundation/satnogs/satnogs-client/
cd satnogs-client
git tag --format "%(refname:strip=2) %(taggerdate:iso-strict)" | sort > releases_part1.csv
git tag --format "%(refname:strip=2) %(committerdate:iso-strict)" | sort > releases_part2.csv
cat releases_part1.csv releases_part2.csv | awk  '$2!=""' | sort > "$CURRENT_DIR/official_releases.csv"
cd "$CURRENT_DIR"
rm -rf "$WORK_DIR"
echo "Output written to ./official_releases.csv"
