# AWS Config Managed Rule 참고 목록

교육에서 사용하는 Managed Rule과 목적 정리.

| Rule 이름 | 목적 |
|---|---|
| `mfa-enabled-for-iam-console-access` | 콘솔 접근 IAM 사용자의 MFA 활성화 여부 점검 |
| `iam-user-no-policies-check` | IAM 사용자에 정책이 직접 연결되어 있는지 점검 (그룹/역할 사용 권장) |
| `s3-bucket-public-read-prohibited` | S3 버킷의 퍼블릭 읽기 허용 여부 점검 |
| `s3-bucket-public-write-prohibited` | S3 버킷의 퍼블릭 쓰기 허용 여부 점검 |
| `root-account-mfa-enabled` | 루트 계정 MFA 활성화 여부 점검 |
| `iam-root-access-key-check` | 루트 계정 액세스 키 존재 여부 점검 |

## 평가 트리거 방식
- **Configuration changes**: 리소스 구성이 변경될 때마다 즉시 평가
- **Periodic**: 지정 주기(예: 24시간)마다 정기 평가

## Non-Compliant 발생 시 확장 아이디어
- EventBridge/SNS로 알림 연계
- SSM Automation Document로 자동 교정(Remediation) 연결
