### 실습 ② Lambda 자동 대응 코드 시연

#### 목표
GuardDuty Finding 발생 시 Lambda가 자동으로 1차 대응(리소스 격리)을 수행하는 흐름을 이해하고 EventBridge Target 연결을 확인한다.

#### 코드
`shared/lambda-snippets/isolate-ec2-on-finding.py` 참고

#### Step 1. Lambda 함수 생성
1. Lambda 콘솔 → 함수 생성 (Python 3.x 런타임)
2. `shared/lambda-snippets/isolate-ec2-on-finding.py` 코드 붙여넣기
3. 실행 역할에 `ec2:ModifyInstanceAttribute` 권한 부여

#### Step 2. EventBridge Target 연결
1. 실습①에서 만든 EventBridge 규칙의 Target에 Lambda 함수 추가
2. 테스트 이벤트로 트리거 확인

#### 주의사항
- 예시 코드의 `sg-isolation0001`은 격리 전용 보안 그룹 ID이며, 실제 환경에서는 사전에 아웃바운드가 차단된 격리용 SG를 미리 생성해두어야 한다.
- 실습 환경에서는 실제 운영 인스턴스에 적용하지 말고 테스트 인스턴스로 검증할 것.
