import json,unittest
from pathlib import Path
from main import *
class Tests(unittest.TestCase):
 def sample(self):return json.loads(Path(__file__).with_name("sample-input.json").read_text())

 def test_schedule(self):
  s=run(self.sample())["schedule"];self.assertEqual([x["task_id"] for x in s],["lockout","bearing","inspect"]);self.assertGreaterEqual(s[2]["start_h"],6)
 def test_skill(self):
  d=self.sample();d["tasks"][0]["skill"]="welding";self.assertFalse(run(d)["complete"])
 def test_cycle(self):
  d=self.sample();d["tasks"][0]["depends_on"]=["inspect"];self.assertFalse(run(d)["complete"])
 def test_duration(self):
  d=self.sample();d["tasks"][0]["duration_h"]=0
  with self.assertRaises(ValueError):run(d)

if __name__=="__main__":unittest.main()
