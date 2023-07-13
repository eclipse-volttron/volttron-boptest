from boptest_integration.interface import Interface

CONFIG = {
    "testcase_name": "testcase1",
    "initialize": None,
    "scenario":
        {
            "time_period": "test_day",
            "electricity_price": "dynamic"
        },
    "step": 300,
    "length": 1728000,

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
