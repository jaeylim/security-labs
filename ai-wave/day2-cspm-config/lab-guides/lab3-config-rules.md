### 실습 ③ Config Rules 적용 실습

#### 목표

3개의 AWS Managed Config Rule을 직접 등록하여 계정 내 IAM·S3 설정 상태를 점검하고, Non-Compliant 리소스를 식별하는 CSPM 워크플로우를 체험한다.

#### 참고

`shared/config-rules/managed-rules-reference.md` 참고

### 사전 준비

#### 1. AWS Config 활성화 확인

1. AWS Config 콘솔 이동
2. 아직 설정 안 되어 있으면 **Get started** → 기본값(모든 리소스 기록)으로 활성화
3. 이미 활성화되어 있으면 Dashboard에서 상태만 확인

> Config Recorder가 켜져 있어야 Rule 평가 자체가 동작합니다. 활성화 직후에는 리소스 인벤토리를 만드는 데 몇 분 정도 걸릴 수 있습니다.

#### 2. 평가용 테스트 리소스 준비

Rule을 등록해도 대상 리소스가 없으면 결과가 비어있어 실습 효과가 떨어집니다. 아래 정도는 미리 만들어두는 것을 추천합니다.

1. **IAM 사용자 2개 이상**
   - 콘솔 액세스 권한이 있는 사용자 1명은 **MFA 미설정 상태로 남겨두기** (mfa-enabled 규칙에서 Non-Compliant로 잡히게 하기 위함)
2. **S3 버킷 1개**
   - 이름: `demo-config-bucket-<임의문자열>`
   - 기본 설정(퍼블릭 차단 ON) 그대로 두면 Compliant로 나옴 — 대조군으로 활용
   - (선택) 별도 테스트 버킷 하나는 **Block Public Access를 의도적으로 끄기** → Non-Compliant 사례로 활용

> 실제 루트 계정 액세스 키를 새로 발급하지 마세요. 루트 액세스 키 규칙은 "현재 계정 상태"를 그대로 평가하는 것으로 충분합니다.

---

#### Step 1. IAM MFA 활성화 규칙 등록

1. AWS Config 콘솔 → **Rules** → **Add rule**
2. **AWS managed rule** 선택 → 검색창에 `mfa-enabled-for-iam-console-access` 입력 후 선택
3. Trigger type: `Periodic` 기본값 그대로 → **Save**
4. 규칙 저장 후 자동 평가 시작 (또는 **Re-evaluate** 클릭해서 즉시 실행)

#### Step 2. 루트 액세스 키 점검 규칙 등록

1. **Add rule** → AWS managed rule 검색창에 `root-account-mfa-enabled` 또는 `iam-root-access-key-check` 입력 후 선택
2. 기본 설정 그대로 **Save**
3. 평가 결과 확인 (루트 계정에 액세스 키가 없으면 Compliant로 나오는 것이 정상이며, 이 경우도 실습 결과로 유효함)

#### Step 3. S3 퍼블릭 액세스 차단 규칙 등록

1. **Add rule** → 검색창에 `s3-bucket-public-read-prohibited` 입력 후 선택
2. **Save**
3. 같은 방식으로 `s3-bucket-public-write-prohibited`도 추가 등록
4. Non-Compliant 리소스가 있다면(사전 준비에서 퍼블릭으로 열어둔 버킷) 목록에 표시되는지 확인

#### Step 4. 결과 확인

1. AWS Config 콘솔 → **Rules** 목록에서 규칙별 **Compliance status** 확인
2. 규칙 클릭 → **Resources in scope** 탭에서 Compliant / Non-Compliant 리소스 목록 상세 확인
3. (선택) Non-Compliant 항목 클릭 → **Compliance timeline**에서 언제부터 미준수 상태였는지 이력 확인

> 규칙 등록 직후에는 평가가 `Not applicable` 또는 `Evaluating`으로 잠시 표시될 수 있습니다. 1~2분 후 새로고침하면 정상적으로 Compliant/Non-Compliant 결과가 나타납니다.

#### 주의사항

- Config Rule은 계정 전체 리소스를 대상으로 평가하므로, 실습 계정에 이미 존재하는 다른 리소스도 함께 평가 대상에 포함됩니다.
- 루트 액세스 키 규칙 테스트를 위해 실제로 루트 액세스 키를 새로 발급하지 마세요 — 루트 액세스 키는 발급 자체가 보안 위험입니다.
- 실습 종료 후 계속 사용하지 않을 규칙/테스트 리소스(특히 퍼블릭으로 열어둔 S3 버킷)는 정리하는 것을 권장합니다.
