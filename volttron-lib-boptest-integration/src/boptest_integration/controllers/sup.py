# -*- coding: utf-8 -*-
"""
This module implements a supervisory controller for room temperature set points
specifically for testcase2.

"""

from .controller import Controller


class SupController(Controller):

    def __init__(self, u=None):
        if not u:
            u = {
                'oveTSetRooHea_u': 22 + 273.15,
                'oveTSetRooHea_activate': 1,
                'oveTSetRooCoo_u': 23 + 273.15,
                'oveTSetRooCoo_activate': 1
            }
        super().__init__(u=u)

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

        return self._u
