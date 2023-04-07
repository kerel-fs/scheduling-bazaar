#!/bin/bash

YEAR="2020";
DAY="4";

for MONTH in {7..6};
do
    DATE=$(printf "%4d-%02d-%02d" $YEAR $MONTH $DAY);
    DATE2=$(printf "%4d-%02d-%02d" $YEAR $MONTH $((DAY + 1)));

    SECONDS=0;
    echo -n "Fetching $DATE...";
    CMD="./python-files/get-observations.py --create --fetch --start $DATE --end $DATE2 ../../data/all/observations.db";
    $CMD > "./$DATE.log";
    ELAPSED_SECONDS=$SECONDS;

    DURATION="$(TZ=UTC0 printf '%(%H:%M:%S)T\n' $ELAPSED_SECONDS)";
    echo " Done. Duration: $DURATION";

    sleep 60;
done
