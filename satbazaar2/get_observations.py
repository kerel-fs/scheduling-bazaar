#!/usr/bin/env python3

"""
Utility to get observations from a SatNOGS Network server and store in a local
SQLite3 database.
"""

import argparse
import os
import sys

from .observations import ObservationsDB
from .observations import fetch_new
from .observations import retry_unknown
from .observations import retry_observer_null


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db', metavar='OBSERVATIONS_DB',
                        help='Database of observations')
    parser.add_argument('demoddata_db', metavar='DEMODDATA_DB',
                        help='Database of demodulated frames')
    parser.add_argument('--create', action='store_true', default=False,
                        help="Create the DB if it doesn't exist")
    parser.add_argument('--fetch', action=argparse.BooleanOptionalAction,
                        dest='fetch_new', default=True,
                        help='Fetch new observations')
    parser.add_argument('--pages', nargs=1, dest='MAX_EXTRA_PAGES',
                        type=int, default=[50],
                        help='Extra pages to fetch (default: %(default)s)')
    parser.add_argument('--retry-unknown',
                        action='store_true',
                        dest='retry_unknown', default=False,
                        help='Retry fetching obs. with "unknown" status')
    parser.add_argument('--retry-observer',
                        action='store_true',
                        dest='retry_observer_null', default=False,
                        help='Retry fetching obs. with null "observer" field')
    parser.add_argument('--reverse',
                        action='store_true', default=False,
                        help='Retry obs by descending ID')
    parser.add_argument('--idstart', action='store', type=int,
                        help='First obs ID to inspect when retrying')
    parser.add_argument('--idend', action='store', type=int,
                        help='Last obs ID to inspect when retrying')
    parser.add_argument('--start', action='store', type=str,
                        help='Obs beginning after this datetime (RFC3339)')
    parser.add_argument('--end', action='store', type=str,
                        help='Obs ending before this datetime (RFC3339)')

    # just for developing script
    # import requests_cache
    # requests_cache.install_cache(expire_after=60*60)

    opts = parser.parse_args()

    parameters = {}
    if opts.start:
        parameters['start'] = opts.start

    if opts.end:
        parameters['end'] = opts.end

    if not (os.path.isfile(opts.db) or opts.create):
        print(f"Error: Cannot open observation database, no such file: '{opts.db}'")
        sys.exit(1)

    if opts.demoddata_db == '':
        # Don't fetch demoddata
        print('INFO: DEMODDATA_DB is empty, no telemetry frames will be fetched.')
        opts.demoddata_db = None
    else:
        if not (os.path.isfile(opts.demoddata_db) or opts.create):
            print(f"Error: Cannot open demoddata database, no such file: '{opts.demoddata_db}'")
            sys.exit(1)

    observations = ObservationsDB(opts.db, opts.demoddata_db)

    try:
        if opts.fetch_new:
            pages = opts.MAX_EXTRA_PAGES[0]

            fetch_new(observations, pages, params=parameters)

        if opts.retry_unknown:
            retry_unknown(observations,
                          reverse=opts.reverse,
                          idstart=opts.idstart,
                          idend=opts.idend)

        if opts.retry_observer_null:
            retry_observer_null(observations,
                          reverse=opts.reverse,
                          idstart=opts.idstart,
                          idend=opts.idend)

    except KeyboardInterrupt:
        print('Cancelled by user, exiting.')

    # print('Finished getting new/updated obs.')
