"""정비 작업의 선행조건·기술자 스킬·운영 금지 시간·공용 작업장 제약을 만족하는 결정적 일정을 생성합니다."""
import argparse,html,json,math
from pathlib import Path
def finite(v,n,minimum=None):
 if type(v) not in (int,float) or not math.isfinite(v):raise ValueError(n+": finite number required")
 if minimum is not None and v<minimum:raise ValueError(n+": below minimum")
 return v
def report(x,t):
 p=html.escape(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
 return '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+html.escape(t)+'</title><style>body{font:16px/1.6 system-ui;max-width:1000px;margin:30px auto;padding:20px;background:#101b2b;color:#eef7ff}pre{background:#192b40;padding:22px;border-radius:12px;white-space:pre-wrap}h1{color:#79e3c2}</style><h1>'+html.escape(t)+'</h1><p>오프라인 합성 예제 · 실물 장비 연결 없음</p><pre>'+p+'</pre>'
def cli(fn,title):
 p=argparse.ArgumentParser();p.add_argument("--input",default=str(Path(__file__).with_name("sample-input.json")));p.add_argument("--html");a=p.parse_args()
 try:
  x=fn(json.loads(Path(a.input).read_text(encoding="utf-8")))
  if a.html:Path(a.html).write_text(report(x,title),encoding="utf-8")
  print(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
 except (ValueError,KeyError,TypeError) as e:p.exit(2,"input error: "+str(e)+"\n")

def run(d):
 horizon=finite(d["horizon_h"],"horizon_h",0);blocked=[tuple(x) for x in d.get("blocked",[])];techs=d["technicians"];tasks={t["id"]:t for t in d["tasks"]}
 if len(tasks)!=len(d["tasks"]):raise ValueError("duplicate task ID")
 done={};schedule=[];remaining=set(tasks);bay=0
 while remaining:
  ready=sorted((tasks[i] for i in remaining if all(x in done for x in tasks[i].get("depends_on",[]))),key=lambda t:(t.get("priority",999),t["id"]))
  if not ready:return {"schedule":schedule,"unscheduled":[{"id":i,"reason":"dependency_cycle_or_missing"} for i in sorted(remaining)],"complete":False}
  progress=False
  for task in ready:
   dur=finite(task["duration_h"],"duration_h",0)
   if dur<=0:raise ValueError("duration_h must be positive")
   cand=[];dep=max((done[x] for x in task.get("depends_on",[])),default=0)
   for tech in techs:
    if task["skill"] not in tech["skills"]:continue
    start=max(dep,bay,tech.get("_free",0))
    while any(start<b and start+dur>a for a,b in blocked):
     start=max(b for a,b in blocked if start<b and start+dur>a)
    if start+dur<=horizon:cand.append((start,tech["id"],tech))
   if not cand:continue
   start,tid,tech=min(cand);end=start+dur;tech["_free"]=end;bay=end;done[task["id"]]=end;remaining.remove(task["id"]);progress=True
   schedule.append({"task_id":task["id"],"technician":tid,"start_h":start,"end_h":end})
  if not progress:
   return {"schedule":schedule,"unscheduled":[{"id":i,"reason":"no_feasible_skill_or_window"} for i in sorted(remaining)],"complete":False}
 for t in techs:t.pop("_free",None)
 return {"schedule":schedule,"unscheduled":[],"complete":True,"assumptions":["single_shared_bay","non_preemptive"]}

if __name__=="__main__":cli(run,'정비 시간창 스케줄러')
