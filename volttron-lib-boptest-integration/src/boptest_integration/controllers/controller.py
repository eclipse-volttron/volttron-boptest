# -*- coding: utf-8 -*-
"""
This module contains a generic controller class that is used to instantiate
concrete controller, found in pid.py, pidTwoZones.py, and sup.py.

"""

import sys
import importlib
import pandas as pd


class Controller:
    def __init__(self, u: dict = None, forecast_parameters: dict = None):
        """Controller object that instantiates concrete controller methods.

        Parameters
        ----------
        u : dict
                Defines the control input to be used for the next step.
                {<input_name> : <input_value>}
        forecast_parameters: dict
            {'point_names':[<string>],
             'horizon': <int>,
             'interval': <int>}
        """

        self._u = u
        self._forecast_parameters = forecast_parameters
        if forecast_parameters:
            self.use_forecast = True
        else:
            self.use_forecast = False

    def get_initialize(self, u):
        """Initialize the control input u.

        Parameters
        ----------
        u

        Returns
        -------
        u : dict
            Defines the control input to be used for the next step.
            {<input_name> : <input_value>}

        """
        return self._u

    def compute_control(self, y, forecasts):
        """Compute the control input from the measurement.

            Parameters
            ----------
            y : dict
                Contains the current values of the measurements.
                {<measurement_name>:<measurement_value>}
            forecasts : structure depends on controller, optional
                Forecasts used to calculate control.
                Default is None.

            Returns
            -------
            u : dict
                Defines the control input to be used for the next step.
                {<input_name> : <input_value>}

            """
        pass
        # TODO: forecasts should not be part of the control. Refactor it out
        # Note: only pidTwoZones use forecasts as part of the update_forecasts, but only to validate config

    def get_forecast_parameters(self):
        """Get forecast parameters within the controller.

        Returns
        -------
        forecast_parameters: dict
            {'point_names':[<string>],
             'horizon': <int>,
             'interval': <int>}

        """
        return self._forecast_parameters

    def update_forecasts(self, forecast_data: dict, forecasts: pd.DataFrame):
        """Update forecast_store within the controller.

        This controller only uses the first timestep of the forecast for upper
        and lower temperature limits.


        Parameters
        ----------
        forecast_data: dict
            Dictionary of arrays with forecast data from BOPTEST
            {<point_name1: [<data>]}
        forecasts: DataFrame
            DataFrame of forecast values used over time.

        Returns
        -------
        forecasts: DataFrame
            Updated DataFrame of forcast values used over time.

        """
        pass
        # TODO: this method is not essential, consider refactoring it out.
        # Note: only pidTwoZones use forecasts as part of the update_forecasts, but only for formatting purpose


