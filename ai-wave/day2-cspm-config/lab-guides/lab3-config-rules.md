# 실습 ③ Config Rules 적용 실습

## 목표
3개의 AWS Managed Config Rule을 직접 등록하여 계정 내 IAM·S3 설정 상태를 점검하고, Non-Compliant 리소스를 식별하는 CSPM 워크플로우를 체험한다.

## 사전 준비
- AWS Config 활성화된 계정
- IAM 사용자 몇 개 (MFA 미설정 상태 포함), 테스트용 S3 버킷

## Step 1. IAM MFA 활성화 규칙
- Rule: `mfa-enabled-for-iam-console-access`
1. AWS Config 콘솔 → 규칙 추가 → Managed Rule 검색
2. 규칙 추가 후 평가 실행
3. 콘솔 접근 IAM 사용자의 MFA 활성화 여부 확인

> 스크린샷: `screenshots/lab3-step1-mfa-rule.png`

## Step 2. 루트 계정 액세스 키 점검 규칙
- Rule: 루트 계정 액세스 키 관련 Managed Rule
1. 규칙 추가 및 평가 실행
2. 루트 액세스 키 존재 여부 결과 확인

> 스크린샷: `screenshots/lab3-step2-root-key-rule.png`

## Step 3. S3 퍼블릭 액세스 차단 규칙
- Rule: `s3-bucket-public-read-prohibited` / `s3-bucket-public-write-prohibited`
1. 규칙 추가 및 평가 실행
2. Non-Compliant 리소스(퍼블릭 버킷) 목록 확인

> 스크린샷: `screenshots/lab3-step3-s3-public-rule.png`

## Step 4. 결과 종합 확인
- AWS Config 대시보드에서 규칙별 Compliant/Non-Compliant 리소스 수 확인
- 필요 시 Security Hub와 연계해 통합 대시보드로 확인

## 참고
Managed Rule 이름 목록: `shared/config-rules/managed-rules-reference.md`
