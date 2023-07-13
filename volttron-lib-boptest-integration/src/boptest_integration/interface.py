from boptest_integration.boptest_integration import BopTestSimIntegrationLocal
import logging
import time
import numpy as np
from .controllers import PidController, SupController, PidTwoZonesController

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Interface:
    """Interface for workflow control
    """

    def __init__(self, config: dict, **kwargs) -> None:

        self.bp_sim = BopTestSimIntegrationLocal()
        self.config: dict = config
        # TODO: design config template
        # TODO: create config data class (with validation)
        logger.debug(f"================ config: {self.config}")

        # Init the result data
        self._results = None
        self._kpi = None
        # self._custom_kpi_result = None
        self._forecasts = None

    def run_workflow(self):
        """
        run workflow
        """
        pass
        logging.info("=========== run_workflow")

        # GET TEST INFORMATION
        # -------------------------------------------------------------------------
        logger.info('\nTEST CASE INFORMATION\n---------------------')
        # Retrieve testcase name from REST API
        name = self.bp_sim.get_name()
        logger.info('Name:\t\t\t\t{0}'.format(name))
        # check if running the proper testcase
        testcase_name = self.config.get("testcase_name")
        if name != testcase_name:
            raise ValueError(fr"Running testcase `{name}` inconsistent with config testcase_name `{testcase_name}`.")
        # Retrieve a list of inputs (controllable points) for the model from REST API
        inputs = self.bp_sim.get_inputs(keys_only=False)
        logger.info('Control Inputs:\t\t\t{0}'.format(inputs))
        # Retrieve a list of measurements (outputs) for the model from REST API
        measurements = self.bp_sim.get_measurements(keys_only=False)
        logger.info('Measurements:\t\t\t{0}'.format(measurements))
        # Get the default simulation timestep for the model for simulation run
        step_def = self.bp_sim.get_step()
        logger.info('Default Control Step:\t{0}'.format(step_def))

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
        logger.info('Initializing test case simulation.')
        # TODO: investigate what happen if length is not a multiplication of steps (affected by PUT/results)
        # TODO: handle very large length, e.g., 365 * 24 * 3600
        length = self.config.get("length")  # intermediate variable to calculate total_time_steps.

        step = self.config.get("step")  # step length
        scenario = self.config.get("scenario")  # e.g., {"time_period": "test_day","electricity_price": "dynamic"}
        if scenario is not None:
            # Initialize test with a scenario time period
            res = self.bp_sim.put_scenario(**scenario)
            logging.info('Scenario:\t\t\t{0}'.format(res))
            # Record test simulation start time
            start_time = int(res["time_period"]['time'])  # Note: the schema can be subjective to Boptest versions.
            # Set final time and total time steps to be very large since scenario defines length
            final_time = np.inf
            total_time_steps = int(length / step)
        else:
            # Initialize test with a specified start time and warmup period
            start_time = self.config.get("initialize").get("start_time")  # used in GET/initialize
            warmup_period = self.config.get("initialize").get("warmup_period")  # used in GET/initialize

            res = self.bp_sim.put_initialize(start_time=start_time, warmup_period=warmup_period)
            logging.info("RESULT: {}".format(res))
            # Set final time and total time steps according to specified length (seconds)
            final_time = start_time + length
            total_time_steps = int(length / step)  # calculate number of timesteps, i.e., number of advance
        if res:
            logging.info('Successfully initialized the simulation')
        logger.info('\nRunning test case...')
        # Set simulation time step
        res = self.bp_sim.put_step(step=step)

        # Load controller info
        # type (currently support pid, sup, pidTwoZones)
        controller_type = self.config.get("controller").get("type")
        # Initialize input to simulation from controller
        u = self.config.get("controller").get("u")
        # Initialize forecast storage structure
        forecast_data = self.config.get("controller").get("forecast_parameters")

        if controller_type == "pid":
            controller = PidController(u=u)
        elif controller_type == "sup":
            controller = SupController(u=u)
        elif controller_type == "pidTwoZones":
            controller = PidTwoZonesController(u=u, forecast_parameters=forecast_data)
        else:
            error_msg = "controller type needs to be one of ['pid', 'sup', 'pidTwoZones']"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # init using scenario endpoint
        # res = self.bp_sim.get_scenario()
        # logging.info("RESULT: {}".format(res))

        # Simulation Loop
        custom_kpi_result = None
        forecasts = None
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
            if controller.use_forecast:
                # Retrieve forecast from restful API
                forecast_parameters = controller.get_forecast_parameters()
                # forecast_data = check_response(requests.put('{0}/forecast'.format(url), json=forecast_parameters))
                forecast_data = self.bp_sim.put_forecast(**forecast_parameters)
                # Use forecast data to update controller-specific forecast data
                forecasts = controller.update_forecasts(forecast_data=forecast_data, forecasts=forecasts)
            else:
                forecasts = None
            # Compute control signal input to simulation for the next timestep
            u = controller.compute_control(y, forecasts)
        logger.info('\nTest case complete.')
        logger.info('Elapsed time of test was {0} seconds.'.format(time.time() - start))

        # VIEW RESULTS
        # -------------------------------------------------------------------------
        # Report KPIs
        kpi = self.bp_sim.get_kpi()
        logger.info('\nKPI RESULTS \n-----------')
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

            # # Store the result data
            # self._results = res
            # self._kpi = kpi
            # # self._custom_kpi_result = custom_kpi_result
            # self._forecasts = forecasts
            #
            # self._is_onstart_completed = True

        logger.info("======== run workflow completed.======")

        return kpi, res, forecasts, custom_kpi_result  # Note: originally publish these
