import pytest
from integrations.boptest_integration import BopTestSimIntegrationLocal


# @pytest.mark.skip(reason="for local testing. Assuming a local testcase is running")
class TestBopTestSimIntegrationLocal:
    """
    Testing BopTestSimIntegrationLocal
    """

    def test_init(self):
        boptest_sim = BopTestSimIntegrationLocal()
        print(boptest_sim)
        assert boptest_sim

    def test_get_name(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.get_name()
        print(res)
        assert res

    def test_put_initialize(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.put_initialize(start_time=31*24*3600, warmup_period=7*24*3600)
        print(res)
        assert res

    def test_retrieve_time_info(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.retrieve_time_info()
        print(res)
        res_1 = boptest_sim.put_initialize(start_time=31 * 24 * 3600, warmup_period=7 * 24 * 3600)
        res_2 = boptest_sim.retrieve_time_info()
        print(res_2)
        assert res
        assert res_2
        assert res != res_2

    def test_put_scenario(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.put_scenario(time_period="peak_heat_day", electricity_price="dynamic")
        print(res)
        assert res

    def test_get_scenario(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.get_scenario()
        print(res)
        assert res == "scenario is NOT set."
        res_1 = boptest_sim.put_initialize(start_time=31 * 24 * 3600, warmup_period=7 * 24 * 3600)
        res_2 = boptest_sim.retrieve_time_info()
        print(res_2)
        assert res_2 != res

    def test_get_measurements(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.get_measurements()
        print(res)
        assert res

    def test_get_inputs(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.get_inputs()
        print(res)
        assert res

    def test_get_step(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.get_step()
        print(res)
        assert res

    def test_put_step(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.put_step(7200)
        print(res)
        res_2 = boptest_sim.get_step()
        print(res_2)
        assert res_2 == 7200

    def test_post_advance(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.post_advance()
        print(res)
        assert res

        try:
            boptest_sim = BopTestSimIntegrationLocal()
            res = boptest_sim.post_advance(data={'oveHeaPumY_u':0.5, 'oveHeaPumY_activate': 1})
            print(res)
            assert res
        except Exception as e:
            print(e)

    def test_get_results(self):
        boptest_sim = BopTestSimIntegrationLocal()
        measures = boptest_sim.get_measurements()
        res = boptest_sim.get_results(point_names=[measures[0]])
        print(res)
        assert res

    def test_get_kpi(self):
        boptest_sim = BopTestSimIntegrationLocal()
        res = boptest_sim.get_kpi()
        print(res)
        assert res




