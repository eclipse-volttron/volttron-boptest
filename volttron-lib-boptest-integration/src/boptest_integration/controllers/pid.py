# -*- coding: utf-8 -*-
"""
This module implements a simple P controller of heater power control specifically
for testcase1.

"""

from .controller import Controller


class PidController(Controller):

    def __init__(self, u=None):
        if not u:
            u = {
                'oveAct_u': 0,
                'oveAct_activate': 1
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

        # Controller parameters
        LowerSetp = 273.15 + 20
        UpperSetp = 273.15 + 23
        k_p = 2000

        # print(f"========= y {y}")

        # Compute control
        if y['TRooAir_y'] < LowerSetp:
            e = LowerSetp - y['TRooAir_y']
        elif y['TRooAir_y'] > UpperSetp:
            e = UpperSetp - y['TRooAir_y']
        else:
            e = 0

        value = k_p * e
        u = {
            'oveAct_u': value,
            'oveAct_activate': 1
        }

        return u

