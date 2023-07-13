from boptest_integration.interface import Interface

CONFIG = {
    "testcase_name": "testcase2",
    "initialize":  # for GET/initialize
        {
            "start_time": 0,
            "warmup_period": 0
        },
    "scenario": None,
    "step": 3600,
    "length": 172800,

    "controller":
        {
            "type": "sup",  # currently support "pid", "sup", pidTwoZones"
            "u":
                {
                    'oveTSetRooHea_u': 295.15,  # 22 + 273.15
                    'oveTSetRooHea_activate': 1,
                    'oveTSetRooCoo_u': 296.15,  # 23 + 273.15
                    'oveTSetRooCoo_activate': 1
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
