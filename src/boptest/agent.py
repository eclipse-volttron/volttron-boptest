from __future__ import  annotations
# -*- coding: utf-8 -*- {{{
# ===----------------------------------------------------------------------===
#
#                 Installable Component of Eclipse VOLTTRON
#
# ===----------------------------------------------------------------------===
#
# Copyright 2022 Battelle Memorial Institute
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# ===----------------------------------------------------------------------===

from pathlib import Path
from pprint import pformat
from typing import Callable, Dict

from volttron.client.messaging import (headers)
from volttron.utils import (format_timestamp, get_aware_utc_now, load_config,
                            setup_logging, vip_main)

import logging
import sys
import gevent

from dnp3_python.dnp3station.outstation_new import MyOutStationNew
from pydnp3 import opendnp3
from volttron.client.vip.agent import Agent, Core, RPC
import subprocess
from volttron import utils
from .boptest_integration import BopTestSimIntegrationLocal
import time
import numpy as np


setup_logging()
_log = logging.getLogger(__name__)
__version__ = "1.0"


# def boptest_example(config_path, **kwargs) -> BopTestAgent:
#     """Parses the Agent configuration and returns an instance of
#     the agent created using that configuration.
#
#     :param config_path: Path to a configuration file.
#
#     :type config_path: str
#     :returns: BopTestAgent
#     :rtype: BopTestAgent
#     """
#     _log.debug("CONFIG PATH: {}".format(config_path))
#     try:
#         config = utils.load_config(config_path)
#     except Exception:
#         config = {}
#     #_log.debug("CONFIG: {}".format(config))
#     if not config:
#         _log.info("Using Agent defaults for starting configuration.")
#
#     return BopTestAgent(config, **kwargs)


class BopTestAgent(Agent):
    """This is class is a subclass of the Volttron Agent;
        This agent is an implementation of a DNP3 outstation;
        The agent overrides @Core.receiver methods to modify agent life cycle behavior;
        The agent exposes @RPC.export as public interface utilizing RPC calls.
    """

    def __init__(self, config_path: str, **kwargs) -> None:
        super().__init__(enable_web=True, **kwargs)

        self.bp_sim = BopTestSimIntegrationLocal()
        self.config: "json" = self._parse_config(config_path)
        # TODO: design config template
        # TODO: create config data class (with validation)
        #  logging.debug(f"================ config: {self.config}")

        # Init the result data
        self._results = None
        self._kpi = None
        # self._custom_kpi_result = None
        self._forecasts = None

        self._is_onstart_completed = False



    # @staticmethod
    # def boptest_up(testcase: str, docker_compose_file_path: str, is_verbose: bool = True) -> str:
    #     """
    #     EXAMPLE
    #     boptest_up(testcase="testcase1", docker_compose_file_path="/home/kefei/project/project1-boptest/docker-compose.yml")
    #     """
    #     if is_verbose:
    #         verbose = "--verbose"
    #     else:
    #         verbose = ""
    #     cmd = f"TESTCASE={testcase} docker-compose {verbose} -f {docker_compose_file_path} up -d"
    #     res = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE)
    #     return res.stdout.decode("utf-8")

    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.
        Usually not needed if using the configuration store.
        """
        pass
        logging.info("=========== Starting Boptest agent onstart")  # TODO: get rid of this

        # GET TEST INFORMATION
        # -------------------------------------------------------------------------
        logging.info('\nTEST CASE INFORMATION\n---------------------')
        # Retrieve testcase name from REST API
        name = self.bp_sim.get_name()
        logging.info('Name:\t\t\t\t{0}'.format(name))
        # Retrieve a list of inputs (controllable points) for the model from REST API
        inputs = self.bp_sim.get_inputs(keys_only=False)
        logging.info('Control Inputs:\t\t\t{0}'.format(inputs))
        # Retrieve a list of measurements (outputs) for the model from REST API
        measurements = self.bp_sim.get_measurements(keys_only=False)
        logging.info('Measurements:\t\t\t{0}'.format(measurements))
        # Get the default simulation timestep for the model for simulation run
        step_def = self.bp_sim.get_step()
        logging.info('Default Control Step:\t{0}'.format(step_def))

        # # IF ANY CUSTOM KPI CALCULATION, DEFINE STRUCTURES
        # # ------------------------------------------------
        # custom_kpis = []  # Initialize customized kpi calculation list
        # custom_kpi_result = {}  # Initialize tracking of customized kpi calculation results
        # if customized_kpi_config is not None:
        #     with open(customized_kpi_config) as f:
        #         config = json.load(f, object_pairs_hook=collections.OrderedDict)
        #     for key in config.keys():
        #         custom_kpis.append(CustomKPI(config[key]))
        #         custom_kpi_result[CustomKPI(config[key]).name] = []
        # custom_kpi_result['time'] = []

        # RUN TEST CASE
        # -------------------------------------------------------------------------
        # Record real starting time
        start = time.time()
        # Initialize test case
        print('Initializing test case simulation.')
        scenario = None
        if scenario is not None:  # TODO: add scenario setup methods
            # # Initialize test with a scenario time period
            # res = check_response(requests.put('{0}/scenario'.format(url), json=scenario))['time_period']
            # print(res)
            # # Record test simulation start time
            # start_time = int(res['time'])
            # # Set final time and total time steps to be very large since scenario defines length
            # final_time = np.inf
            # total_time_steps = int((365 * 24 * 3600) / step)
            pass
        else:
            # Initialize test with a specified start time and warmup period

            # DONE: refactor the following, e.g., start_time, warmup_period, etc. to config process
            # start_time = 0  # used in GET/initialize
            # warmup_period = 0  # used in GET/initialize
            # length = 24 * 3600  # intermediate variable to calculate total_time_steps.
            # step = 300  # step length
            start_time = self.config.get("initialize").get("start_time")  # used in GET/initialize
            warmup_period = self.config.get("initialize").get("warmup_period")  # used in GET/initialize
            length = self.config.get("length")  # intermediate variable to calculate total_time_steps.
            # TODO: investigate what happen if length is not a multiplication of steps (affected by PUT/results)
            step = self.config.get("step")  # step length
            res = self.bp_sim.put_initialize(start_time=start_time, warmup_period=warmup_period)
            logging.info("RESULT: {}".format(res))
            # Set final time and total time steps according to specified length (seconds)
            final_time = start_time + length
            total_time_steps = int(length / step)  # calculate number of timesteps, i.e., number of advance
        if res:
            logging.info('Successfully initialized the simulation')
        logging.info('\nRunning test case...')
        # Set simulation time step
        res = self.bp_sim.put_step(step=step)

        # Initialize input to simulation from controller
        # u = controller.initialize()
        u = self.config.get("controller").get("u")
        # Initialize forecast storage structure
        forecasts = None
        res = self.bp_sim.get_scenario()
        logging.info("RESULT: {}".format(res))

        # Simulation Loop
        for t in range(total_time_steps):
            # Advance simulation with control input value(s)
            y = self.bp_sim.post_advance(data=u)
            # If simulation is complete break simulation loop
            if not y:
                break
            # If custom KPIs are configured, compute the KPIs
            # TODO: develop customer-kpis feature
            # for kpi in custom_kpis:
            #     kpi.processing_data(y)  # Process data as needed for custom KPI
            #     custom_kpi_value = kpi.calculation()  # Calculate custom KPI value
            #     custom_kpi_result[kpi.name].append(round(custom_kpi_value, 2))  # Track custom KPI value
            #     print('KPI:\t{0}:\t{1}'.format(kpi.name, round(custom_kpi_value, 2)))  # Print custom KPI value
            # custom_kpi_result['time'].append(y['time'])  # Track custom KPI calculation time
            # If controller needs a forecast, get the forecast data and provide the forecast to the controller
            # TODO: develop forecast feature
            # if controller.use_forecast:
            # if self.config.get("controller").get("use_forecast"):
            #     # Retrieve forecast from restful API
            #     forecast_parameters = controller.get_forecast_parameters()
            #     forecast_data = check_response(requests.put('{0}/forecast'.format(url), json=forecast_parameters))
            #     # Use forecast data to update controller-specific forecast data
            #     forecasts = controller.update_forecasts(forecast_data, forecasts)
            # else:
            #     forecasts = None
            # # Compute control signal input to simulation for the next timestep
            # u = controller.compute_control(y, forecasts)
        logging.info('\nTest case complete.')
        logging.info('Elapsed time of test was {0} seconds.'.format(time.time() - start))

        # VIEW RESULTS
        # -------------------------------------------------------------------------
        # Report KPIs
        kpi = self.bp_sim.get_kpi()
        logging.info('\nKPI RESULTS \n-----------')
        for key in kpi.keys():
            if key == 'ener_tot':
                unit = 'kWh/m$^2$'
            elif key == 'pele_tot':
                unit = 'kW/m$^2$'
            elif key == 'pgas_tot':
                unit = 'kW/m$^2$'
            elif key == 'pdih_tot':
                unit = 'kW/m$^2$'
            elif key == 'tdis_tot':
                unit = 'Kh/zone'
            elif key == 'idis_tot':
                unit = 'ppmh/zone'
            elif key == 'cost_tot':
                unit = 'Euro or \$/m$^2$'
            elif key == 'emis_tot':
                unit = 'KgCO2/m$^2$'
            elif key == 'time_rat':
                unit = 's/s'
            else:
                unit = None
            logging.info('{0}: {1} {2}'.format(key, kpi[key], unit))

            # POST PROCESS RESULTS
            # -------------------------------------------------------------------------
            # Get result data
            points = list(measurements.keys()) + list(inputs.keys())
            res = self.bp_sim.put_results(point_names=points, start_time=start_time, final_time=final_time)

            # return kpi, res, custom_kpi_result, forecasts  # TODO: originally publish these
            # TODO: refactor topic value to config
            default_prefix = "PNNL/BUILDING/UNIT/"
            self.vip.pubsub.publish(peer='pubsub', topic=default_prefix + "kpi", message=str(kpi))
            # self.vip.pubsub.publish(peer='pubsub', topic=default_prefix + "result", message=str(res))
            # TODO: publish custom_kpi_result forecasts

            # Store the result data
            self._results = res
            self._kpi = kpi
            # self._custom_kpi_result = custom_kpi_result
            self._forecasts = forecasts

            self._is_onstart_completed = True




        # Example publish to pubsub
        # self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")
        #
        # # Example RPC call
        # # self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        # pass
        # self._create_subscriptions(self.setting2)

    def _parse_config(self, config_path: str) -> Dict:
        """Parses the agent's configuration file.

        :param config_path: The path to the configuration file
        :return: The configuration
        """
        # TODO: added capability to configuration based on tabular config file (e.g., csv)
        try:
            config = load_config(config_path)
        except NameError as err:
            _log.exception(err)
            raise err
        except Exception as err:
            _log.error("Error loading configuration: {}".format(err))
            config = {}
        # print(f"============= def _parse_config config {config}")
        if not config:
            raise Exception("Configuration cannot be empty.")
        return config

    @RPC.export
    def rpc_dummy(self) -> str:
        """
        For testing rpc call
        """
        return "This is a dummy rpc call"

    # TODO: verify if onstart hook needs to finish first before evoke rpc call.
    @RPC.export
    def get_kpi_results(self):
        if self._is_onstart_completed:
            return self._kpi
        else:
            logging.info("Onstart process not finished")
            return

    @RPC.export
    def get_simulation_results(self):
        if self._is_onstart_completed:
            return self._results
        else:
            logging.info("Onstart process not finished")
            return


def main():
    """Main method called to start the agent."""
    vip_main(BopTestAgent)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
