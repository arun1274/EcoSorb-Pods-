import json
import unittest
from pathlib import Path
from ecosorb.planner import plan, rectangle_bounds, lawnmower
from ecosorb.simulator import simulate_pod

DATA=json.loads((Path(__file__).resolve().parents[1]/'data/sample_spill.json').read_text())

class TestPlanning(unittest.TestCase):
    def test_demo_area_and_mass(self):
        p=plan(DATA)
        self.assertEqual(p['area_m2'],7200)
        self.assertEqual(p['estimated_mass_kg'],612)
        self.assertEqual(p['estimated_cartridge_loads'],77)
        self.assertEqual(len(p['zones']),3)
    def test_zones_span_region(self):
        p=plan(DATA)
        self.assertEqual(p['zones'][0]['bounds_m'][0],0)
        self.assertEqual(p['zones'][-1]['bounds_m'][2],120)
        for zone in p['zones']:
            self.assertTrue(zone['waypoints_local_m'])
    def test_nonrectangle_rejected(self):
        with self.assertRaises(ValueError):
            rectangle_bounds([[0,0],[1,0],[0.5,1],[0,1]])
    def test_coordinates_not_gps(self):
        bad=dict(DATA, coordinate_system='WGS84')
        with self.assertRaises(ValueError):
            plan(bad)
    def test_bad_swath(self):
        with self.assertRaises(ValueError):
            lawnmower(0,0,4,4,0)

class TestTelemetry(unittest.TestCase):
    def test_battery_return(self):
        p=simulate_pod([[0,0]]*50)
        self.assertEqual(p['status'],'RETURN_LOW_BATTERY')
        self.assertGreaterEqual(p['final_battery_pct'],30)
    def test_cartridge_return(self):
        p=simulate_pod([[0,0]]*50,capacity_kg=1)
        self.assertEqual(p['status'],'RETURN_CARTRIDGE_FULL')
    def test_complete(self):
        p=simulate_pod([[0,0],[1,1]])
        self.assertEqual(p['status'],'MISSION_COMPLETE')

if __name__=='__main__':
    unittest.main()
