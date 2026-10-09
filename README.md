# 정비 시간창 스케줄러

정비 작업의 선행조건·기술자 스킬·운영 금지 시간·공용 작업장 제약을 만족하는 결정적 일정을 생성합니다.

## 핵심 기능

우선순위와 ID로 순서를 고정합니다. 선행 종료·기술자·공용 작업장 가용성 중 가장 늦은 시점부터 시작하고 금지 시간과 겹치면 뒤로 이동합니다.

## 설치·실행

Python 3.10 이상, 외부 패키지·유료 API·장비 연결이 필요 없습니다.

~~~bash
git clone https://github.com/MetaSonGi/maintenance-window-scheduler.git
cd maintenance-window-scheduler
python -m pip install -r requirements.txt
python main.py
python main.py --input sample-input.json --html result.html
python -m unittest -v
~~~

example-report.html 또는 result.html을 브라우저에서 열 수 있습니다. CDN과 서버 없이 동작하며 문자열은 HTML escape됩니다.

## 입출력 예제

[sample-input.json](sample-input.json), [example-output.json](example-output.json), [example-report.html](example-report.html)을 포함합니다.

~~~json
{
  "horizon_h": 12,
  "blocked": [
    [
      4,
      6
    ]
  ],
  "technicians": [
    {
      "id": "kim",
      "skills": [
        "electrical"
      ]
    },
    {
      "id": "lee",
      "skills": [
        "mechanical",
        "inspection"
      ]
    }
  ],
  "tasks": [
    {
      "id": "lockout",
      "skill": "electrical",
      "duration_h": 1,
      "priority": 1
    },
    {
      "id": "bearing",
      "skill": "mechanical",
      "duration_h": 3,
      "depends_on": [
        "lockout"
      ],
      "priority": 2
    },
    {
      "id": "inspect",
      "skill": "inspection",
      "duration_h": 1,
      "depends_on": [
        "bearing"
      ],
      "priority": 3
    }
  ]
}
~~~

출력 미리보기:

~~~text
{
  "schedule": [
    {
      "task_id": "lockout",
      "technician": "kim",
      "start_h": 0,
      "end_h": 1
    },
    {
      "task_id": "bearing",
      "technician": "lee",
      "start_h": 1,
      "end_h": 4
    },
    {
      "task_id": "inspect",
      "technician": "lee",
      "start_h": 6,
      "end_h": 7
    }
  ],
  "unscheduled": [],
  "complete": true,
  "assumptions": [
    "single_shared_bay",
    "non_preemptive"
  ]
}

~~~

## 설계 판단

우선순위와 ID로 순서를 고정합니다. 선행 종료·기술자·공용 작업장 가용성 중 가장 늦은 시점부터 시작하고 금지 시간과 겹치면 뒤로 이동합니다. JSON 입출력으로 Python 작업 큐, Nest.js 자동화, XR/WebGL 모니터링 앞단에 연결할 수 있습니다. 실제 장비 상태는 변경하지 않습니다.

## 한계

최적해가 아닌 greedy 기준선입니다. 이동시간, 부품 재고, 교대, 여러 작업장, 위험도 최적화는 없습니다. 가상의 경력, 논문 성능, 모델 재현, 실물 제조 검증을 주장하지 않습니다.

## 검증·근거

정상·경계·오류 테스트 4개를 실행했습니다. [VALIDATION.txt](VALIDATION.txt)와 [TRENDS.md](TRENDS.md)에 결과와 근거를 구분했습니다.

실행 기준일: 2026-10-10 (Asia/Seoul). 기존 저장소를 수정하지 않은 독립 프로그램입니다.
