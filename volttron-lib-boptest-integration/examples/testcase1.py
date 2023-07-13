from boptest_integration.interface import Interface

CONFIG = {
    "initialize":  # for GET/initialize
        {
            "start_time": 0,
            "warmup_period": 0
        },
    "scenario": None,
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


def main():
    config: dict = CONFIG
    interface = Interface(config=config)
    kpi, res, forecasts, custom_kpi_result = interface.run_workflow()
    print(f"======= kpi {kpi}")


if __name__ == "__main__":
    main()
