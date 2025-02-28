# Copyright (C) 2017-2022 Battelle Memorial Institute
# file: dsoStub.py

import json
import helics

import logging as log

from tesp_support.helpers import load_json_case
from tesp_support.helpers import parse_mva


def dso_make_stub(casename):
    log.info('Reading configuration...')
    ppc = load_json_case(casename + '.json', True)
    port = str(ppc['port'])
    nd = ppc['FNCS'].shape[0]

    # write player helics config.json file for load and generator players
    players = ppc["players"]
    for idx in range(len(players)):
        player = ppc[players[idx]]
        jsonfile = player[0] + '_player_h.json'
        yp = open(jsonfile, 'w')
        print('{', file=yp)
        print('  "name": "' + player[0] + 'player",', file=yp)
        print('  "period": 15.0,', file=yp)
        print('  "publications": [', file=yp)
        if player[8]:
            # load
            comma = ","
            for i in range(nd):
                bs = str(i + 1)
                print('    {', file=yp)
                print('      "global": false,', file=yp)
                print('      "key": "' + player[0] + '_load_' + bs + '",', file=yp)
                print('      "type": "string"', file=yp)
                print('    },', file=yp)
                print('    {', file=yp)
                print('      "global": false,', file=yp)
                print('      "key": "' + player[0] + "_ld_hist_" + bs + '",', file=yp)
                print('      "type": "string"', file=yp)
                if nd == i+1:
                    comma = ""
                print('    }' + comma, file=yp)
            print('  ]', file=yp)
            print('}', file=yp)
        else:
            # power
            brace = False
            genFuel = ppc['genfuel']
            for i in range(len(genFuel)):
                if genFuel[i][0] in ppc['renewables']:
                    idx = str(genFuel[i][2])
                    if player[6]:
                        if brace:
                            print('    },', file=yp)
                        print('    {', file=yp)
                        print('      "global": false,', file=yp)
                        print('      "key": "' + player[0] + '_power_' + idx + '",', file=yp)
                        print('      "type": "string"', file=yp)
                        brace = True
                    if player[7]:
                        if brace:
                            print('    },', file=yp)
                        print('    {', file=yp)
                        print('      "global": false,', file=yp)
                        print('      "key": "' + player[0] + '_pwr_hist_' + idx + '",', file=yp)
                        print('      "type": "string"', file=yp)
                        brace = True
            print('    }', file=yp)
            print('  ]', file=yp)
            print('}', file=yp)

        yp.close()

    yp = open('dso_h.json', 'w')
    print('{', file=yp)
    print('  "name": "dsostub",', file=yp)
    print('  "period": 15.0,', file=yp)
    print('  "publications": [', file=yp)
    comma = ","
    for i in range(nd):
        bs = str(i + 1)
        print('    {', file=yp)
        print('      "global": false,', file=yp)
        print('      "key": "rt_bid_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "global": false,', file=yp)
        print('      "key": "da_bid_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        if nd == i + 1:
            comma = ""
        print('    }' + comma, file=yp)
    print('  ],', file=yp)
    print('  "subscriptions": [', file=yp)
    comma = ","
    for i in range(nd):
        bs = str(i + 1)
        print('    {', file=yp)
        print('      "name": "SUBSTATION_' + bs + '",', file=yp)
        print('      "key": "refplayer/ref_load_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "SUBHISTORY_' + bs + '",', file=yp)
        print('      "key": "refplayer/ref_ld_hist_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "IND_LOAD_' + bs + '",', file=yp)
        print('      "key": "indplayer/ind_load_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "IND_LD_HIST_' + bs + '",', file=yp)
        print('      "key": "indplayer/ind_ld_hist_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "LMP_DA_Bus_' + bs + '",', file=yp)
        print('      "key": "pypower/lmp_da_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "LMP_RT_Bus_' + bs + '",', file=yp)
        print('      "key": "pypower/lmp_rt_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "cleared_q_rt_' + bs + '",', file=yp)
        print('      "key": "pypower/cleared_q_rt_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "cleared_q_da_' + bs + '",', file=yp)
        print('      "key": "pypower/cleared_q_da_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "V_Bus_' + bs + '",', file=yp)
        print('      "key": "pypower/three_phase_voltage_' + bs + '",', file=yp)
        print('      "type": "double"', file=yp)
        if nd == i + 1:
            comma = ""
        print('    }' + comma, file=yp)
    print('  ]', file=yp)
    print('}', file=yp)
    yp.close()

    yp = open('tso_h.json', 'w')
    print('{', file=yp)
    print('  "name": "pypower",', file=yp)
    print('  "period": 15,', file=yp)
    print('  "publications": [', file=yp)
    comma = ","
    for i in range(nd):
        bs = str(i + 1)
        print('    {', file=yp)
        print('      "global": false,', file=yp)
        print('      "key": "lmp_rt_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "global": false,', file=yp)
        print('      "key": "lmp_da_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "global": false,', file=yp)
        print('      "key": "cleared_q_rt_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "global": false,', file=yp)
        print('      "key": "cleared_q_da_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "global": false,', file=yp)
        print('      "key": "three_phase_voltage_' + bs + '",', file=yp)
        print('      "type": "double"', file=yp)
        if nd == i + 1:
            comma = ""
        print('    }' + comma, file=yp)
    print('  ],', file=yp)

    print('  "subscriptions": [', file=yp)
    for i in range(nd):
        bs = str(i + 1)
        print('    {', file=yp)
        print('      "name": "DA_BID_' + bs + '",', file=yp)
        print('      "key": "dsostub/da_bid_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "RT_BID_' + bs + '",', file=yp)
        print('      "key": "dsostub/rt_bid_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "REF_LOAD_' + bs + '",', file=yp)
        print('      "key": "refplayer/ref_load_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "REF_LD_HIST_' + bs + '",', file=yp)
        print('      "key": "refplayer/ref_ld_hist_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "GLD_LOAD_' + bs + '",', file=yp)
        print('      "key": "gldplayer/gld_load_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        print('    },', file=yp)
        print('    {', file=yp)
        print('      "name": "GLD_LD_HIST_' + bs + '",', file=yp)
        print('      "key": "gldplayer/gld_ld_hist_' + bs + '",', file=yp)
        print('      "type": "string"', file=yp)
        if nd != i + 1:
            print('    },', file=yp)
    if ppc['genPower']:
        genFuel = ppc['genfuel']
        for i in range(len(genFuel)):
            if genFuel[i][0] in ppc['renewables']:
                idx = str(genFuel[i][2])
                for plyr in ["genMn", "genForecastHr"]:
                    player = ppc[plyr]
                    if player[6] and not player[8]:
                        print('    },', file=yp)
                        print('    {', file=yp)
                        print('      "name": "' + player[0].upper() + '_POWER_' + idx + '",', file=yp)
                        print('      "key": "' + player[0] + 'player/' + player[0] + '_power_' + idx + '",', file=yp)
                        print('      "type": "string"', file=yp)
                    if player[7] and not player[8]:
                        print('    },', file=yp)
                        print('    {', file=yp)
                        print('      "name": "' + player[0].upper() + '_PWR_HIST_' + idx + '",', file=yp)
                        print('      "key": "' + player[0] + 'player/' + player[0] + '_pwr_hist_' + idx + '",', file=yp)
                        print('      "type": "string"', file=yp)
        print('    }' + comma, file=yp)
    print('  ]', file=yp)
    print('}', file=yp)
    yp.close()


def dso_loop(casename):
    ts = 0
    rt_period = 300
    da_period = 43200  # 86400
    tnext_rt = -30  # start the real time bid
    tnext_da = (10 * 3600) - 15  # start the day ahead bid
    power_factor = 0.57  # roughly 30 deg

    logger = log.getLogger()
    # logger.setLevel(log.DEBUG)
    logger.setLevel(log.INFO)
    # logger.setLevel(log.WARNING)

    log.info('Reading configuration...')
    ppc = load_json_case(casename + '.json', True)

    tmax = int(ppc['Tmax'])
    dt = int(ppc['dt'])
    bWantMarket = ppc['priceSensLoad']
    fncs_bus = ppc['FNCS']
    nd = fncs_bus.shape[0]
    dsoList = [1, 2, 3, 4, 5, 6, 7, 8]

    gld_bus = {}  # key on bus number
    for i in range(nd):
        busnum = i + 1
        gld_bus[busnum] = {
            'dalmp': {}, 'rtlmp': 0, 'v': 0,
            'p': 0, 'q': 0, 'p_hist': {},
            'p_i': 0, 'q_i': 0, 'p_i_hist': {}
        }

    log.info("Initialize HELICS dso federate")
    hFed = helics.helicsCreateValueFederateFromConfig("./dso_h.json")
    fedName = helics.helicsFederateGetName(hFed)
    subCount = helics.helicsFederateGetInputCount(hFed)
    pubCount = helics.helicsFederateGetPublicationCount(hFed)
    log.info('Federate name: ' + fedName)
    log.info('Subscription count: ' + str(subCount))
    log.info('Publications count: ' + str(pubCount))
    log.info('Starting HELICS dso federate')
    helics.helicsFederateEnterExecutingMode(hFed)

    while ts <= tmax:
        # see another example for helics integration at fncsPYPOWER.py
        for t in range(subCount):
            sub = helics.helicsFederateGetInputByIndex(hFed, t)
            key = helics.helicsSubscriptionGetKey(sub)
            topic = key.upper().split('/')[1]
            # log.info("HELICS subscription index: " + str(t) + ", key: " + key + ", topic: " + topic)
            if helics.helicsInputIsUpdated(sub):
                val = helics.helicsInputGetString(sub)
                # get voltages and LMPs from the TSO
                if 'LMP_DT_' in topic:
                    busnum = int(topic[7:])
                    # gld_bus[busnum]['dalmp'] = float(val)
                elif 'LMP_RT_' in topic:
                    busnum = int(topic[7:])
                    # gld_bus[busnum]['rtlmp'] = float(val)
                elif 'V_Bus_' in topic:
                    busnum = int(topic[6:])
                    # gld_bus[busnum]['v'] = float(val)
                elif 'REF_LOAD_' in topic:  # gridlabd - residential/commercial
                    busnum = int(topic[9:])
                    p, q = parse_mva(val)
                    # log.info('at ' + str(ts) + " " + topic + " " + val)
                    gld_bus[busnum]['p'] = p  # MW active
                    gld_bus[busnum]['q'] = q  # MW reactive
                elif 'REF_LD_HIST_' in topic:  # gridlabd - residential/commercial
                    busnum = int(topic[12:])
                    # log.info('at ' + str(ts) + " " + topic + val)
                    gld_bus[busnum]['p_hist'] = json.loads(val)  # MW active
                elif 'IND_LOAD_' in topic:
                    busnum = int(topic[9:])
                    p, q = parse_mva(val)
                    # log.info('at ' + str(ts) + " " + topic + " " + val)
                    gld_bus[busnum]['p_i'] = p  # MW
                    gld_bus[busnum]['q_i'] = q  # MW
                elif 'IND_LD_HIST_' in topic:
                    busnum = int(topic[12:])
                    # log.info('at ' + str(ts) + " " + topic + val)
                    gld_bus[busnum]['p_i_hist'] = json.loads(val)  # MW active

        # bid into the day-ahead market for each bus
        # as with real-time market, half the hourly load will be unresponsive and half responsive
        # the bid curve is also fixed
        # however, we will add some noise to the day-ahead bid
        if ts >= tnext_da:
            for row in fncs_bus:
                busnum = int(row[0])
                if busnum in dsoList:
                    da_bid = {
                        'unresp_mw': [],
                        'resp_max_mw': [],
                        'resp_c2': [],
                        'resp_c1': [],
                        'resp_c0': [],
                        'resp_deg': []
                    }
                    for i in range(24):
                        p = gld_bus[busnum]['p_hist'][24 + i]  # + gld_bus[busnum]['p_i_hist'][24+i]
                        da_bid['unresp_mw'].append(p)
                        da_bid['resp_max_mw'].append(0.0)
                        da_bid['resp_c2'].append(0.0)
                        da_bid['resp_c1'].append(0.0)
                        da_bid['resp_c0'].append(0.0)
                        da_bid['resp_deg'].append(0)

                    # this is what the tso8stub.yaml expects to receive from a dso auction
                    log.info('Day-Ahead bid for DSO stub at' + str(ts) + ' = ' + str(da_bid))
                    pub = helics.helicsFederateGetPublication(hFed, 'da_bid_' + str(busnum))
                    helics.helicsPublicationPublishString(pub, json.dumps(da_bid))
            tnext_da += da_period

        # update the bid, and publish simulated load as unresponsive + cleared_responsive
        if ts >= tnext_rt:
            for row in fncs_bus:
                busnum = int(row[0])
                if busnum in dsoList:
                    p = gld_bus[busnum]['p']  # + gld_bus[busnum]['p_i']
                    rt_bid = {
                        'unresp_mw': p,
                        'resp_max_mw': 0.0,
                        'resp_c2': 0.0,
                        'resp_c1': 0.0,
                        'resp_c0': 0.0,
                        'resp_deg': 0
                    }
                    if bWantMarket:
                        rt_bid['unresp_mw'] = p * 0.95
                        rt_bid['resp_max_mw'] = p * 0.05
                        rt_bid['resp_c2'] = 0.05
                        rt_bid['resp_c1'] = 60.0
                        rt_bid['resp_c0'] = 0.0
                        rt_bid['resp_deg'] = 0

                    # this is what the tso8stub.yaml expects to receive from a dso auction
                    log.info('Real Time bid for DSO stub at ' + str(ts) + ' = ' + str(rt_bid))
                    pub = helics.helicsFederateGetPublication(hFed, 'rt_bid_' + str(busnum))
                    helics.helicsPublicationPublishString(pub, json.dumps(rt_bid))

            tnext_rt += rt_period

        # request the next time step, if necessary
        if ts >= tmax:
            log.info('breaking out at ' + str(ts))
            break
        ts = int(helics.helicsFederateRequestTime(hFed, min(ts + dt, tmax)))

    # ======================================================
    log.info('Finalizing HELICS dso federate')
    helics.helicsFederateDestroy(hFed)


if __name__ == "__main__":
    dso_make_stub('./case_config')
    # dso_loop('./generate_case_config')
