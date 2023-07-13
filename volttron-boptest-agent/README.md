# boptest-agent

The volttron-boptest-agent utilizes the volttron-lib-boptest-integration library to perform simulation control and
benchmark tasks.

BOPTEST is designed to facilitate
the performance evaluation and benchmarking of building control strategies, which
contains these key components:

1. Run-Time Environment (RTE): Deployed with Docker and accessed with a RESTful HTTP API, use the RTE to set up tests,
   control building emulators, access data, and report KPIs.

1. Test Case Repository: A collection of ready-to-use building emulators representing a range of building types and HVAC
   systems.

1. Key Performance Indicator (KPI) Reporting: A set of KPIs is calculated by the the RTE using data from the building
   emulator being controlled.

For more information, please visit [IBPSA Project 1 - BOPTEST](https://github.com/ibpsa/project1-boptest).

# Prerequisites

* Python 3 (tested with Python3.10)
* Linux OS (tested with Ubuntu 22.04)

## Python

<details>
<summary>To install specific Python version (e.g., Python 3.10), we recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```shell
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.10
pyenv install 3.10

# make it available globally
pyenv global system 3.10
```

</details>

# Quick-start

### Setup environment and VOLTTRON platform

The following recipe walks through the steps to install and demonstrate basic usage of "volttron-boptest" agent.

1. Create and activate a virtual environment.

   It is recommended to use a virtual environment for installing volttron.

    ```shell
    python -m venv env
    source env/bin/activate
    
    pip install volttron
    ```

1. Install volttron and start the platform.

   > **Note**:
   > According to the [volttron-core#README](https://github.com/eclipse-volttron/volttron-core#readme), setup
   VOLTTRON_HOME
   > environment variable is mandatory:
   > ... if you have/had in the past, a monolithic VOLTTRON version that used the default VOLTTRON_HOME
   > $HOME/.volttron. This modular version of VOLTTRON cannot work with volttron_home used by monolithic version of
   > VOLTTRON(version 8.3 or earlier)

    ```shell
    # Setup environment variable `VOLTTRON_HOME`
    export VOLTTRON_HOME=<path-to-volttron_home-dir>
    
    # Start platform with output going to volttron.log
    volttron -vv -l volttron.log &
    ```

### Setup the boptest simulation server locally.

In order to demonstrate the basic usage of volttron-boptest-agent, we need to setup the boptest simulation server.

(Please see more details about boptest quick-start
at [Quick-Start to Deploy a Test Case](https://github.com/ibpsa/project1-boptest#quick-start-to-deploy-a-test-case))

1. Download [IBPSA Project 1 - BOPTEST](https://github.com/ibpsa/project1-boptest) repository to <boptest_repo>. For
   demo purpose, let boptest_repo be `/tmp/project1-boptest`.

   ```shell
   git clone https://github.com/ibpsa/project1-boptest /tmp/project1-boptest
   ```

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

   (Optional) Verify with `docker-compose version` to verify the installation
   ```shell
   (env) kefei@ubuntu-22:~/sandbox/volttron-boptest$ docker-compose version
   docker-compose version 1.29.2, build unknown
   docker-py version: 5.0.3
   CPython version: 3.10.6
   OpenSSL version: OpenSSL 3.0.2 15 Mar 2022

   ```

1. Build and deploy a test case.

   The basic command to start a test case is by using `TESTCASE=<testcase_name> docker-compose up`.

   For demo purpose, we will build and deploy testcase1, for avialbe testcases please
   see [testcases/](https://github.com/ibpsa/project1-boptest/tree/master/testcases)
   ```shell
   (env) kefei@ubuntu-22:~/sandbox/volttron-boptest$ TESTCASE=testcase1 docker-compose --file /tmp/project1-boptest/docker-compose.yml up
   Creating network "boptest-net" with the default driver
   Creating project1-boptest_boptest_1 ... done
   Attaching to project1-boptest_boptest_1
   boptest_1 | 07/13/2023 09:59:42 PM UTC root INFO Control step set successfully.
   boptest_1 | 07/13/2023 09:59:42 PM UTC root INFO Test simulation initialized successfully to 0.0s with warmup period of
   0.0s.
   boptest_1 | 07/13/2023 09:59:42 PM UTC root INFO Test case scenario was set successfully.
   ...
   boptest_1  |  * Debug mode: off
   boptest_1  | 07/13/2023 09:59:42 PM UTC werkzeug            INFO         * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
   ```
   Or use detach mode
   ```shell
   (env) kefei@ubuntu-22:~/sandbox/volttron-boptest$ TESTCASE=testcase1 docker-compose --file /tmp/project1-boptest/docker-compose.yml up --detach 
   Starting project1-boptest_boptest_1 ... done
   ```

   Note: Use `docker-compose down` to shut down the service.

### Install volttron boptest agent

1. Install the "volttron-boptest" dependency.

   There are two options to install volttron-boptest. You can install this library using the version on PyPi or install
   it from the source code (`git clone` might be required.)
   Note: the `vctl install` command in the following step can handle dependency installation using pypi. However, in
   this demo we demonstrate what is happening under the neath the hood by separating the dependency installation and
   agent registry
   steps.

    ```shell
    # option 1: install from pypi
    pip install volttron-boptest
    
    # option 2: install from the source code (Note: `-e` option to use editable mode, useful for development.)
    pip install [-e] <path-to-the-source-code-root>/volttron-boptest/
    ```

1. Install and start the "volttron-boptest" agent.

   Prepare the default config files:

    ```shell
    # Create config file place holders
    mkdir config
    touch config/boptest_integration-agent-config.json
    ```

   Edit the `testcase1_config.yml` as follows:
    ```yaml
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
    ```

   Please see [examples/](examples) for other example config files.

   Use `vctl install` command to register to the volttron home path.
   Note: for demo purposes and reproducibility, we assign vip-identity as "volttron_boptest_agent", but you can choose
   any other valid agent identity as desired.

    ```shell
    vctl install volttron-boptest --agent-config <path-to-agent-config> \
   --vip-identity volttron_boptest_agent \
   --start
    ```

   Observe Data

   The volttron-boptest agent publishes events on the message bus. To see these events in the Volttron log file, install
   a [Listener Agent](https://pypi.org/project/volttron-listener/):

    ```
    vctl install volttron-listener --start
    ```

(Optional) Use `vctl stauts` to verify the installation

   ```shell
   (env) kefei@ubuntu-22:~/sandbox/volttron-boptest$ vctl status
   UUID   AGENT                        IDENTITY                     TAG PRIORITY STATUS          HEALTH 
   a      volttron-boptest-agent-0.0.1 volttron_boptest_agent                    running [59108] GOOD
   2      volttron-listener-0.2.0rc0   volttron-listener-0.2.0rc0_1              running [59096] GOOD
   ```

1. (optional) Inspect the volttron.log file

   <details>
   <summary> Within the volttron.log, we should see similar logs as follows</summary>

   ```shell
    # Create config file place holders
   KPI RESULTS 
   -----------
   2023-07-13 18:27:51,124 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: emis_tot: 0.2147137757521314 KgCO2/m$^2$
   2023-07-13 18:27:51,174 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: ener_tot: 1.073568878760657 kWh/m$^2$
   2023-07-13 18:27:51,223 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: idis_tot: 508.47225004790033 ppmh/zone
   2023-07-13 18:27:51,280 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: pdih_tot: None kW/m$^2$
   2023-07-13 18:27:51,330 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: pele_tot: None kW/m$^2$
   2023-07-13 18:27:51,381 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: pgas_tot: 0.09615811655434148 kW/m$^2$
   2023-07-13 18:27:51,436 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: tdis_tot: 5.316029375566828 Kh/zone
   2023-07-13 18:27:51,494 (volttron-boptest-agent-0.0.1 59108) root(186) INFO: time_rat: 0.001856946445725582 s/s
   2023-07-13 18:27:51,550 (volttron-boptest-agent-0.0.1 59108) root(202) INFO: ======== run workflow completed.======
   2023-07-13 18:27:51,553 (volttron-boptest-agent-0.0.1 59108) <stdout>(0) INFO: ["======= kpi {'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': 1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, 'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': 5.316029375566828, 'time_rat': 0.001856946445725582}"]
   2023-07-13 18:27:51,558 (volttron-boptest-agent-0.0.1 59108) root(129) INFO: =========== refactoring onstart
   2023-07-13 18:27:52,067 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,071 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,073 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,074 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,075 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,076 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,078 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,079 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,081 (volttron-listener-0.2.0rc0 59096) listener.agent(104) INFO: Peer: pubsub, Sender: volttron_boptest_agent:, Bus: , Topic: PNNL/BUILDING/UNIT/kpi, Headers: {'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
   ("{'cost_tot': 0.075149821513246, 'emis_tot': 0.2147137757521314, 'ener_tot': "
    "1.073568878760657, 'idis_tot': 508.47225004790033, 'pdih_tot': None, "
    "'pele_tot': None, 'pgas_tot': 0.09615811655434148, 'tdis_tot': "
    "5.316029375566828, 'time_rat': 0.001856946445725582}")
   2023-07-13 18:27:52,084 (volttron-boptest-agent-0.0.1 59108) root(305) INFO: ======== onstart completed.======
   ```

   </details>

# Development

Please see the following for contributing
guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).

Please see the following helpful guide
about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)

# Disclaimer Notice

This material was prepared as an account of work sponsored by an agency of the
United States Government. Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or any
information, apparatus, product, software, or process disclosed, or represents
that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.
