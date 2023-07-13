from boptest_integration.interface import Interface

CONFIG = {
    "testcase_name": "testcase3",
    "initialize":  # for GET/initialize
        {
            "start_time": 0,
            "warmup_period": 0
        },
    "scenario": None,
    "step": 300,
    "length": 172800,  # 48*3600

    "controller":
        {
            "type": "pidTwoZones",  # currently support "pid", "sup", pidTwoZones"
            "u":
                {
                    'oveActNor_u': 0,
                    'oveActNor_activate': 1,
                    'oveActSou_u': 0,
                    'oveActSou_activate': 1
                },
            "forecast_parameters":
                {
                    'point_names': ['LowerSetp[North]',
                                    'UpperSetp[North]',
                                    'LowerSetp[South]',
                                    'UpperSetp[South]'],
                    'horizon': 600,
                    'interval': 300
                }
        }

}


def main():
    config: dict = CONFIG
    interface = Interface(config=config)
    kpi, res, forecasts, custom_kpi_result = interface.run_workflow()
    print(f"======= kpi {kpi}")


if __name__ == "__main__":
    main()
