.. _boptest-agent:

==========
Boptest Agent
==========

The goal of the Building Optimization Testing Framework (BOPTEST) is to enable benchmarking of control
strategies for building and district energy systems, with a particular focus on heating, ventilation,
and air-conditioning (HVAC). For more information about Boptest Simulation Suite, please refer to `BOPTEST User Guide <https://ibpsa.github.io/project1-boptest/docs-userguide/index.html>`_.


The Boptest agent is an implementation of VOLTTRON Boptest integration library utilizing the VOLTTRON agent framework
to interact with the boptest server.

Requirements
============

the Boptest Agent can be installed in an activated environment with:

.. code-block:: bash

    pip install volttron-boptest

.. note::
    The current version of the Boptest Agent is developed and tested against boptest `v0.4.0 <https://github.com/ibpsa/project1-boptest/releases/tag/v0.4.0>`_.
    Running boptest simulation of different version might lead unexpected outcomes.

Agent Configuration Example
============

The users need to specify the boptest agent config file to define simulation workflow behavior.
The basic simulation workflow include the following stages: configuration, initialize, advance, output results.
BOPTEST consists of several building emulators and boundary conditions (so-called “test cases”) that
are made rapidly and repeatably accessible for control by test controllers through a developed run-time environment (RTE).
There are several workflow examples available at `/examples <https://github.com/eclipse-volttron/volttron-boptest/tree/main/volttron-boptest-agent/examples>`_.
(Note: the example usecase must match the test case that is running.)

In this section, we will dive deeper into the `/examples/testcase1.config <https://github.com/eclipse-volttron/volttron-boptest/blob/main/volttron-boptest-agent/examples/testcase1.config>`_. example.

.. code-block:: json
    :linenos:

    {
      "testcase_name": "testcase1",
      "initialize":  # for GET/initialize
      {
        "start_time": 0,
        "warmup_period": 0
      },
      "scenario": null,
      "step": 300,
      "length": 86400,

      "controller":
      {
        "type": "pid",  # currently support "pid", "sup", pidTwoZones"
        "u":
        {
          "oveAct_u": 0,
          "oveAct_activate": 1
        }
      }

    }


The configuration is a dictionary include the following sections:

* testcase_name:
    * Name of the boptest testcase.
    * Please see `Test Cases <https://ibpsa.github.io/project1-boptest/testcases/index.html>`_. for more inforamtion.
* initialize:
    * Initialize simulation to a start time using a specified warmup period. Also resets point data history and KPI calculations. Arguments for the PUT/initialize endpoint.
    * Arguments are "start_time" and "warmup_period". Both accept float values.
    * Note: only either "intialize" or "scenario" should be configured. (Left the other one undefined or set to "None")
* scenario:
    * Set current test scenario. Setting time_period results in similar behavior to PUT /initialize, except uses a pre-determined start time and warmup period as defined within BOPTEST according to the selected scenario. Arguments for the PUT/scenario endpoint.
    * Arguments are "time_period" and "electricity_price". Both accept string values.
    * An example can be found in `/examples/testcase1_scenario.py <https://github.com/eclipse-volttron/volttron-boptest/blob/main/volttron-boptest-agent/examples/testcase1_scenario.config>`_.
    * Note: only either "intialize" or "scenario" should be configured. (Left the other one undefined or set to "None")
* step:
    * This is the amount of simulation time (in second) that will pass when the next control step is taken. API wrapper for the PUT/step endpoint.
    * Accepts float values.
    * Note: the step configuration only affects the granularity of the PUT/results when  step shorter than 30 seconds, in which case you'll get the results at the time intervals used by integration when simulating. Otherwise the PUT/results will always have a resolution 0f 30 seconds. See more details at https://github.com/ibpsa/project1-boptest/issues/439
* length:
    * The duration of the simulation scenario in seconds.
    * Accepts float values.
* controller:
    * The configuration for the controllers module, which contains several concrete controller class to interfact with the Boptest simulation testcases.
    * Arguments are
        * type: controller types, which accepts strings, currently support "pid" (for testcase1), "sup" (for testcase2), pidTwoZones" (for testcase 3) controller types. Users can define their own controlers.
        * u: initial inputs. Note the accepted inputs are testcase-specific, and the user can use the "GET/inputs" entry point to query the available control signal input point names (u) and metadata.

