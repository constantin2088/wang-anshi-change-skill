import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_dependencies import analyze
class TaskToolTests(unittest.TestCase):
 def sample(self):return json.loads((ROOT/'examples/tool-input.json').read_text(encoding='utf-8'))
 def test_shared_precondition_before_steps(self):self.assertEqual(analyze(self.sample())['dependency_order'],['授权','试点','复核'])
 def test_missing_precondition_stops(self):
  p=self.sample();p['nodes'][1]['depends']=['lost']
  with self.assertRaises(ValueError):analyze(p)
 def test_cycle_stops(self):
  p=self.sample();p['nodes'][0]['depends']=['复核']
  with self.assertRaises(ValueError):analyze(p)
 def test_duplicate_node_stops(self):
  p=self.sample();p['nodes'].append(p['nodes'][0])
  with self.assertRaises(ValueError):analyze(p)
 def test_parallel_tasks_can_share_input(self):
  p=self.sample();p['nodes'].append({'id':'反馈','depends':['授权']});r=analyze(p)['dependency_order'];self.assertLess(r.index('授权'),r.index('反馈'))

if __name__=='__main__':unittest.main()
