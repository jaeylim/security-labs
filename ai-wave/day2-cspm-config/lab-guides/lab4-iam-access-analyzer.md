#### 실습 IAM Access Analyzer — 미사용 권한 탐지

#### 목표
Unused Access Analyzer를 생성해, 실습 계정 IAM 사용자의 과도한(미사용) 권한을 실제로 확인한다.

#### 사전 준비
- IAM 또는 Access Analyzer 관련 권한 (실습 계정은 Admin이라 문제 없음)
- 분석 대상 IAM 사용자·역할이 계정에 1개 이상 존재

#### 왜 이 실습이 지금 상황에 잘 맞는가
- AWS Config와 무관 — SCP 이슈, 보안팀 승인 없이 바로 진행 가능
- Admin 권한이면 분석기 생성에 필요한 권한이 이미 충분함
- 실습 계정의 IAM 사용자가 전부 Admin인 상태 자체가 "IAM 과다권한" 오설정 사례를 실시간으로 보여주는 좋은 소재가 됨

#### Step 1. Unused Access Analyzer 생성

**콘솔에서:**
1. IAM 콘솔 → **Access Analyzer** → **Analyzers**
2. **Create analyzer** 클릭
3. Analyzer type: **Account unused access** 선택 → 조회 기간(기본 90일) 확인 후 생성

**CLI로 하려면:**
```bash
aws accessanalyzer create-analyzer \
  --analyzer-name my-unused-access-analyzer \
  --type ACCOUNT_UNUSED_ACCESS
```

#### Step 2. Findings 목록 확인

1. Analyzer 생성 후 잠시 대기 (초기 분석에 몇 분 소요될 수 있음)
2. **Findings** 탭에서 목록 확인
3. 개별 Finding 클릭 → 어떤 IAM 사용자/역할의 어떤 권한이 미사용인지 상세 확인

#### 참고 — Finding 유형 3가지
| Finding 유형 | 설명 |
|---|---|
| Unused roles | 지정 기간 동안 접근 활동이 없는 역할 |
| Unused access keys / passwords | 지정 기간 동안 사용되지 않은 자격 증명 |
| Unused permissions | 지정 기간 동안 사용하지 않은 서비스·작업 수준 권한 |

> **주의**: 오늘 막 만든 실습 계정이라 사용 이력이 거의 없어서, 거의 모든 권한이 "미사용"으로 잡히는 게 정상입니다. 이 경우 "기본 조회 기간(90일) 동안 활동이 없으면 미사용으로 판단한다"는 논리 자체를 이해하는 게 핵심입니다.

#### Step 3. (선택) External Access Analyzer도 함께 생성해보기

1. **Create analyzer** → Analyzer type: **Account** (External access, 무료) 선택
2. 외부 계정·엔터티에 공유된 리소스(S3 버킷, IAM 역할 등)가 있는지 확인

---

#### 정리 — 찾아낸 미사용 권한, 다음 단계는?

1. **콘솔에서 바로 삭제** — 미사용 역할·액세스 키·비밀번호는 콘솔의 빠른 링크로 즉시 삭제 가능
2. **정책 생성(Policy Generation)** — CloudTrail에 기록된 실제 사용 활동 기반으로, 꼭 필요한 권한만 담은 정책 자동 생성
3. **정책 검증(Policy Validation)** — 새 정책을 배포하기 전 IAM 모범 사례·보안 표준 부합 여부 자동 검증

#### 트러블슈팅

**Findings이 하나도 안 나와요**
Analyzer 생성 직후에는 초기 분석에 시간이 걸릴 수 있습니다. 몇 분 후 새로고침해보세요.

**모든 권한이 미사용으로 나와요**
계정을 막 생성해서 사용 이력이 없으면 정상적인 현상입니다. 실제 업무에서 며칠~몇 주 사용한 뒤 재분석하면 실제 사용 패턴이 반영됩니다.

**Unused Access Analyzer 생성 시 비용이 걱정돼요**
역할·사용자 1개당 월 $0.20 수준으로 소액입니다. External Access Analyzer는 무료입니다. 실습 후 필요 없으면 Analyzer를 삭제하세요.

#### 참고
[1] IAM Access Analyzer 개요: https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html
[2] IAM Access Analyzer 조사 결과: https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html
[3] IAM Access Analyzer 가격 정책: https://aws.amazon.com/iam/access-analyzer/pricing
