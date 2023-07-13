"""
A demo to test dnp3-driver get_point method using rpc call.
Pre-requisite:
- install platform-driver
- configure dnp3-driver
- a dnp3 outstation/server is up and running
- platform-driver is up and running
"""
import os
import random
from volttron.client.vip.agent import build_agent
from time import sleep
import datetime


def main():
    a = build_agent()
    print(a)

    rs = a.vip.peerlist.list().get(5)
    print(datetime.datetime.now(), "rs: ", rs)

    # peer = "test-agent"
    # peer_method = "get_outstation_config"
    #
    # rs = a.vip.rpc.call(peer, peer_method, ).get(timeout=10)
    # print(datetime.datetime.now(), "rs: ", rs)

    peer = "volttron_boptest_agent"
    peer_method = "rpc_dummy"
    rs = a.vip.rpc.call(peer, peer_method).get(timeout=5)
    print(datetime.datetime.now(), "rs: ", rs)

    # peer = "volttron_boptest_agent"
    # peer_method = "get_kpi_results"
    # rs = a.vip.rpc.call(peer, peer_method).get(timeout=5)
    # print(datetime.datetime.now(), "rs: ", rs)
    #
    # peer = "volttron_boptest_agent"
    # peer_method = "get_simulation_results"
    # rs = a.vip.rpc.call(peer, peer_method).get(timeout=5)
    # # print(datetime.datetime.now(), "rs: ", rs)
    # #
    # import pandas as pd
    # rs_payload = rs["payload"]
    # # df_res = pd.DataFrame()
    # df_res = pd.DataFrame.from_dict(rs_payload)
    # df_res = df_res.set_index('time')
    # print(df_res)


if __name__ == "__main__":
    main()
