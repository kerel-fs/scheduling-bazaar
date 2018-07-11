# This file contains the different scheduling method definitions to be used
# when simulating.
import random


def random_scheduler(passes, clients, satellites, debug=False):
    """Randomly schedules passes on the given clients (which are already
    instantiated with the desired client type).

    passes - candidate passes for scheduling.
    clients - dict of ground stations to use.
    debug - Boolean.  Print out status markers for each.
    """
    passes = random.sample(passes, len(passes))
    for pd in passes:
        # create a request
        r = pass2request(pd, satellites)
        offer = clients[pd.data.gs].request(r)
        if debug is True:
            if offer['status'] == 'accept':
                print('*', end='', flush=True)
            else:
                print('.', end='', flush=True)
    if debug is True:
        print()
    return clients


def first_start_scheduler(passes, clients, satellites, debug=False):
    """Makes requests to stations in order of start time.

    passes - candidate passes for scheduling.
    clients - dict of ground stations to use.
    debug - Boolean.  Print out status markers for each pass.

    Returns updated clients with filled calendars.
    """
    # TODO: what is the sort key?
    for pd in sorted(passes):
        r = pass2request(pd, satellites)
        offer = clients[pd.data.gs].request(r)
        if debug is True:
            if offer['status'] == 'accept':
                print('*', end='', flush=True)
            else:
                print('.', end='', flush=True)
    if debug is True:
        print()
    return clients

# def max_gs_el(passes, clients, debug=False):


# def max_sat_el(passes, clients, debug=False):


def pass2request(pd, satellites):
    """Take a pass (as returned from db.getpasses() and construct a request
    dict for the Network to send to a Client.

    The bounty is SNC (SatNOGS Credits) with an amount set to the pass duration
    in seconds.

    When transmitted over a network, this is then converted to JSON.
    """

    d = pd.data
    job = {'id': random.randrange(2**16),  # fake an ID number
           'start': d.start.isoformat(),
           'end': d.end.isoformat(),
           'ground_station': d.gs,
           'tle0': satellites[d.norad]['tle'][0],
           'tle1': satellites[d.norad]['tle'][1],
           'tle2': satellites[d.norad]['tle'][2],
           'frequency': -1,
           'mode': 'null',
           'transmitter': 'asdfasdasdfadsf',
           }
    duration = (d.end - d.start).total_seconds()
    bounty = [{'currency': 'SNC', 'amount': duration}]

    request = {'job': job,
               'bounty': bounty,
               'status': 'initial',
               }
    return request


