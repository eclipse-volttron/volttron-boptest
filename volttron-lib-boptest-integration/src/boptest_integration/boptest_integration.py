# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright 2020, Battelle Memorial Institute.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government. Neither the United States Government nor the
# United States Department of Energy, nor Battelle, nor any of their
# employees, nor any jurisdiction or organization that has cooperated in the
# development of these materials, makes any warranty, express or
# implied, or assumes any legal liability or responsibility for the accuracy,
# completeness, or usefulness or any information, apparatus, product,
# software, or process disclosed, or represents that its use would not infringe
# privately owned rights. Reference herein to any specific commercial product,
# process, or service by trade name, trademark, manufacturer, or otherwise
# does not necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by
# BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# }}}

import logging


import requests
import numpy as np

_log = logging.getLogger(__name__)
__version__ = '0.0.1'


class BopTestSimIntegrationLocal:
    """
    Wrapper on local boptest_integration simulation server
    """

    def __init__(self, url: str = None, start_time: float = None, warmup_period: float = None):
        if url is None:
            self.url = 'http://0.0.0.0:5000'
        else:
            self.url = url
        self.start_time: float = start_time
        self.warmup_period: float = warmup_period
        self.current_time: float = None
        self.is_scenario = False
        self.has_initialized = False

    def get_name(self) -> str:
        """
        Wrapper on GET/name
        """
        res = requests.get('{0}/name'.format(self.url)).json()['payload']
        return res.get('name')

    def put_initialize(self, start_time: float, warmup_period: float, payload_only=True) -> dict:
        """
        wrapper on PUT/initialize
        electricity_price in ["constant", "dynamic", "highly_dynamic"].
        time_period in ["peak_heat_day", "typical_heat_day", "typical_cool_day", "mix_day"].
        EXAMPLE:
        put_initialize(start_time=31*24*3600, warmup_period=7*24*3600)
        """
        self.has_initialized = True
        self.start_time = start_time
        self.current_time = start_time
        self.warmup_period = warmup_period
        if payload_only:
            res = requests.put('{0}/initialize'.format(self.url),
                               data={'start_time': start_time,
                                     'warmup_period': warmup_period}).json()['payload']
        else:
            res = requests.put('{0}/initialize'.format(self.url),
                               data={'start_time': start_time,
                                     'warmup_period': warmup_period}).json()
        return res

    def retrieve_time_info(self) -> dict:
        """
        retrieve start_time, warmup_period as dict
        EXAMPLE
        retrieve_time_info()
        >> {"start_time": 2678400.0, "warmup_period": 604800.0, "current_time": 2692800.0)
        """
        return {"start_time": self.start_time,
                "warmup_period": self.warmup_period,
                "current_time": self.current_time}

    def put_scenario(self, time_period: str, electricity_price: str, payload_only=True):
        """
        wrapper on PUT/scenario
        EXAMPLE:
        put_scenario(time_period="peak_heat_day", electricity_price="dynamic")
        """
        self.is_scenario = True
        if payload_only:
            res = requests.put('{0}/scenario'.format(self.url),
                               data={'time_period': time_period,
                                     'electricity_price': electricity_price}).json()['payload']
        else:
            res = requests.put('{0}/scenario'.format(self.url),
                               data={'time_period': time_period,
                                     'electricity_price': electricity_price}).json()
        return res

    def get_scenario(self):
        """
        wrapper on GET/scenario
        EXAMPLE:
        get_scenario()
        """
        if self.is_scenario:
            res = requests.get('{0}/scenario'.format(self.url)).json()
            return res
        else:
            return "scenario is NOT set."

    def get_measurements(self, keys_only=True):
        """
        wrapper on GET/measurements
        EXAMPLE:
        get_measurements(keys_only=True)
        >> dict_keys(['reaCO2RooAir_y', 'reaCOP_y', 'reaPFan_y', 'reaPHeaPum_y', ...
        """
        if keys_only:
            res = requests.get('{0}/measurements'.format(self.url), ).json()['payload'].keys()
            res = list(res)
        else:
            res = requests.get('{0}/measurements'.format(self.url), ).json()['payload']
        return res

    def get_inputs(self, keys_only=True):
        """
        wrapper on GET/inputs
        EXAMPLE:
        get_inputs(keys_only=True)
        >> dict_keys(['oveFan_activate', 'oveFan_u', 'oveHeaPumY_activate', 'oveHeaPumY_u', ...

        Note: The naming convention is such that the extension `_y` indicates a measurement point, `_u` indicates the value of an input which can be overwritten by a test controller, and `_activate` indicates the enabling (with value 0 or 1) of a test controller to overwrite the corresponding input value.
        Hence, `<varname>_u` is enabled for overwriting by the test controller when `<varname>_activate=1`.
        `weaSta_` indicates a measurement for a weather point, so that historical weather data can be easily retrieved.
        """
        if keys_only:
            res = requests.get('{0}/inputs'.format(self.url), ).json()['payload'].keys()
            res = list(res)
        else:
            res = requests.get('{0}/inputs'.format(self.url), ).json()['payload']
        return res

    def get_step(self, payload_only=True) -> float:
        """
        wrapper on GET/step
        EXAMPLE:
        get_step()
        >> 3600.0
        """
        if payload_only:
            res = requests.get('{0}/step'.format(self.url)).json()["payload"]
        else:
            res = requests.get('{0}/step'.format(self.url)).json()
        return res

    def put_step(self, step: float) -> float:
        """
        wrapper on PUT/step
        EXAMPLE:
        put_step(step=7200)
        >> <Response [200]>
        """
        res = requests.put('{0}/step'.format(self.url), data={'step': step})
        return res

    def post_advance(self, data: dict = None, payload_only=True):
        """
        wrapper on POST/advance
        EXAMPLE
        post_advance(self, data={'oveHeaPumY_u':0.5, 'oveHeaPumY_activate': 1})
        >> 'payload': {'oveFan_activate': 0.0, 'oveFa ...
        """
        res = None
        try:
            if payload_only:
                res = requests.post('{0}/advance'.format(self.url), data=data).json()["payload"]
                self.current_time = res.get("time")
            else:
                res = requests.post('{0}/advance'.format(self.url), data=data).json()
                self.current_time = res.get("payload").get("time")
        except Exception as e:
            print(e)
            print(f"===== data {data}")
            print(f"===== res {requests.post('{0}/advance'.format(self.url), data=data).json()}")
        return res

    def put_results(self, point_names: list, start_time: float = -np.inf, final_time: float = np.inf):
        """
        wrapper on PUT/results ('start_time':-np.inf, 'final_time':np.inf)

        Note:  the granularity of the results will always be 30 seconds unless you choose a step shorter
        than 30 seconds in which case you'll get the results at the time intervals used by integration when simulating.
        see https://github.com/ibpsa/project1-boptest/issues/439

        EXAMPLE
        put_results(point_names=['reaTZon_y'])
        >> {'message': "Queried results data successfully for point names [u'reaTZon_y'].",
        >> 'payload': {'reaTZon_y': [294.48313766898406], 'time': [2505600.0]}, 'status': 200}
        """
        args = {'point_names': point_names, 'start_time': start_time, 'final_time': final_time}
        res = requests.put('{0}/results'.format(self.url), data=args).json()
        return res

    def get_kpi(self, payload_only=True):
        """
        wrapper on GET/kpi
        EXAMPLE
        get_kpi()
        >> {'message': 'Queried KPIs successfully.', 'payload': {'cost_tot': 0.006980178107630843,
        >> 'emis_tot': 0.004598381633034914, 'ener_tot': 0.02 ...
        """
        if payload_only:
            res = requests.get('{0}/kpi'.format(self.url)).json()["payload"]
        else:
            res = requests.get('{0}/kpi'.format(self.url)).json()
        return res

    def get_forecast_points(self, keys_only=True):
        """
        wrapper on GET/forecast_points
        RETURN:
        <point_name>:                   // str, name of point
        {"Description": <value>,    // str, description of point
         "Unit": <value>,           // str, unit of point
         },
        Note: not every testcase has forecast capability (testcase3 has such capability)
        EXAMPLE
        get_forecast_points()
        >> ['EmissionsBiomassPower', 'EmissionsDistrictHeatingPower', 'EmissionsElectricPower', ...]
        """
        if keys_only:
            res = requests.get('{0}/forecast_points'.format(self.url)).json()['payload'].keys()
        else:
            res = requests.get('{0}/forecast_points'.format(self.url)).json()['payload']
        return res

    def put_forecast(self, point_names: list, horizon: float, interval: float, payload_only=True) -> dict:
        """
        wrapper on PUT/forecast
        RETURN:
            {
        "time":
            <values>,   // array of floats, time values at interval for horizon
        <point_name>:   // str, name of point
            <values>,   // array of floats, forecast values at interval for horizon
        ...
        }
        EXAMPLE:
        put_forecast(point_names=['LowerSetp[North]',
                                  'UpperSetp[North]',
                                  'LowerSetp[South]',
                                  'UpperSetp[South]'],
                    'horizon': 600,
                    'interval': 300)
        >> {'LowerSetp[North]': [294.15, 294.15, 294.15], 'LowerSetp[South]': [293.15, 293....
        """
        forecast_parameters: dict = {
            "point_names": point_names,
            "horizon": horizon,
            "interval": interval
        }
        if payload_only:
            res = requests.put('{0}/forecast'.format(self.url), json=forecast_parameters).json()['payload']
        else:
            res = requests.put('{0}/forecast'.format(self.url), json=forecast_parameters).json()
        return res





class BopTestSimIntegration:
    """
    The class is responsible for integration with BopTest simulation, mainly wrap on its RestAPI
    """

    def __init__(self):
        self.testid: str = ""

    def get_name_remote(self, url: str = None, testid: str = None) -> str:
        """
        Wrapper on GET/name for remote service
        """
        if url is None:
            url = 'http://api.boptest.net'
        if testid is None:
            testid = self.testid
        res = requests.get('{0}/name/{1}'.format(url, testid)).json()['payload']
        return res.get('name')

    def establish_remote_simulation(self, testcase: str = None, url: str = None):
        if testcase is None:
            testcase = 'bestest_hydronic_heat_pump'

        if url is None:
            url = 'http://api.boptest.net'

            # Select and start a new test case
        testid = \
            requests.post('{0}/testcases/{1}/select'.format(url, testcase)).json()['testid']
        self.testid = testid
        return testid


# TODO: clean up (moving into examples)
if __name__ == "__main__":
    bp_sim = BopTestSimIntegrationLocal()

    res = bp_sim.get_name()
    print(res)

    # res = BopTestSimIntegrationLocal().put_initialize(start_time=31 * 24 * 3600, warmup_period=7 * 24 * 3600)
    # print(res)

    # res = bp_sim.put_step(7200)
    # print(res)
    #
    # res = bp_sim.get_step()
    # print(res)

    res = bp_sim.put_initialize(start_time=31*24*3600, warmup_period=7*24*3600)
    print(res)
    # #
    # # from time import sleep
    # #
    # res = bp_sim.retrieve_time_info()
    # print(res)
    #
    # res = bp_sim.post_advance(data={'oveHeaPumY_u':0.5, 'oveHeaPumY_activate': 1})
    # print(res)
    #
    # res = bp_sim.retrieve_time_info()
    # print(res)
    #
    # res = bp_sim.put_results(["reaTZon_y"], start_time=29 * 3600 * 24, final_time=29 * 3600 * 24 + 10)
    # print(res)
    # print(res.keys())
    #
    # res = bp_sim.get_kpi()
    # print(res)

    scenario = {"time_period": "test_day", "electricity_price": "dynamic"}
    res = bp_sim.put_scenario(**scenario)
    print(res)

    print("========")
    print(bp_sim.retrieve_time_info())

