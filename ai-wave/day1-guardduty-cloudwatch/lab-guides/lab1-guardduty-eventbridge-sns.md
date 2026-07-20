# 실습 ① GuardDuty → EventBridge → SNS 알림 파이프라인

## 목표
GuardDuty Finding 발생 시 EventBridge를 통해 SNS로 자동 알림이 전달되는 탐지-알림 파이프라인을 구축한다.

## 사전 준비
- IAM 권한: GuardDuty, EventBridge, SNS 관련 권한 보유 계정
- 알림 수신용 이메일 주소

## Step 1. GuardDuty 활성화
1. GuardDuty 콘솔 이동
2. [지금 시작하기] 클릭 → 계정 단위 활성화
3. 활성화 확인 (Summary 화면에서 상태 확인)

<img width="800" alt="GuardDuty 활성화 화면" src="https://github.com/user-attachments/assets/6c97cc18-deef-4cff-b7d9-7dc80c9e17a5" />

## Step 2. Sample Finding 생성
1. GuardDuty 콘솔 → 설정(Settings)
2. [Sample findings 생성] 클릭
3. Findings 목록에서 테스트용 Finding 확인

> 스크린샷: `screenshots/lab1-step2-sample-finding.png`

## Step 3. EventBridge 규칙 생성
1. EventBridge 콘솔 → 규칙 생성
2. 이벤트 패턴: GuardDuty Finding 심각도 조건 지정 (예: severity >= 7)
3. 대상(Target)은 다음 단계에서 SNS로 연결

> 스크린샷: `screenshots/lab1-step3-eventbridge-rule.png`

## Step 4. SNS 주제 연결 및 알림 확인
1. SNS 주제 생성 및 이메일 구독 등록
2. EventBridge 대상으로 SNS 주제 지정
3. Sample Finding 재생성 후 이메일 수신 확인

> 스크린샷: `screenshots/lab1-step4-sns-notification.png`

## 실무 연계 노트
FocusAI PCI-DSS 증적 작업에서 구축한 GuardDuty → EventBridge → SNS 파이프라인과 동일한 구조. 규정 준수 환경에서는 이 알림 흐름 자체가 모니터링 통제(Control) 증적 자료로 활용된다.
