### Security Labs

클라우드 보안 교육 커리큘럼 및 실습 자료 모음.

#### AI Security Wave 1기 (CJ올리브네트웍스)
`ai-wave/`
AWS GuardDuty/CloudWatch 기반 위협 탐지와 AWS Config 기반 CSPM 교육 과정.

- `ai-wave/day1-guardduty-cloudwatch/` — 1일차: 이상 징후 탐지
- `ai-wave/day2-cspm-config/` — 2일차: 설정 관리(CSPM)

## Shared
`shared/`
과정 간 재사용 가능한 공통 자료 (Lambda 스니펫, Config Rule 예시, 아키텍처 다이어그램).

---

각 day 폴더 구조:
```
ai-wave/dayN-*/
├── slides/          # 교육 PPT
└──  lab-guides/       # 실습 가이드 (마크다운)
```

새 과정이 추가되면 `ai-wave/`와 같은 레벨에 새 과정 폴더(예: `next-course/`)를 만들고, 공통으로 재사용 가능한 자료는 `shared/`에 포함시킬 예정입니다.
