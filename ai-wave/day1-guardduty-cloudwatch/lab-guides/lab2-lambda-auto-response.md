### 실습 ② Lambda 자동 대응 코드 시연

#### 목표
GuardDuty Finding 발생 시 Lambda가 자동으로 1차 대응(리소스 격리)을 수행하는 흐름을 이해하고 EventBridge Target 연결을 확인한다.

#### 코드
`shared/lambda-snippets/isolate-ec2-on-finding.py` 참고

### 사전 준비 
#### 1. 격리용 보안 그룹(SG) 생성
1. VPC 콘솔 → Security Groups → **Create security group**
2. 이름: `sg-isolation-demo`
3. **인바운드 규칙: 없음 (기본값 유지)**
4. **아웃바운드 규칙:  없음 (기본값 유지)**
5. 생성 후 **보안 그룹 ID**를 메모해두기 (예: `sg-0123456789abcdef0`)


#### Step 1. Lambda 함수 생성
1. Lambda 콘솔 → 함수 생성
   - 함수 이름: `guardduty-auto-isolate`
   - 런타임: `Python 3.12` (또는 최신 버전)
3. `shared/lambda-snippets/isolate-ec2-on-finding.py` 코드 붙여넣기
4. 실행 역할에 `ec2:ModifyInstanceAttribute` 권한 부여 (또는 위에 생성한 역할 부여)
5. `ISOLATION_SG_ID` 값을 실제 생성한 격리용 SG ID로 교체
6. **Deploy** 클릭
---
#### step 1-1. Lambda 실행 역할(IAM Role)에 권한 추가
Lambda 함수용 실행 역할에 아래 정책을 인라인으로 추가합니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:ModifyInstanceAttribute",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

> 실습용이라 `Resource: "*"`로 단순화했지만, 실제 운영에서는 특정 VPC·태그 조건으로 범위를 좁히는 것이 안전합니다.

1. Lambda 함수(guardduty-auto-isolate) 화면 → Configuration 탭 → Permissions
2. Execution role 항목에 있는 역할 이름 클릭 (파란 링크, IAM 콘솔로 이동됨)
3. IAM 역할 화면 → Add permissions → Create inline policy
4. 상단 탭에서 JSON 선택
5. 캡처하신 JSON 그대로 붙여넣기
6. Next → 정책 이름 입력 (예: guardduty-lambda-ec2-modify) → Create policy


#### Step 2. EventBridge Target 연결 
1. 이전에 만든 EventBridge 규칙의 Target에 Lambda 함수 추가
2. 실행
  a. Lambda 함수 화면 → **Test** 탭
  b. 아래 샘플 이벤트를 붙여넣기 (GuardDuty Finding 이벤트 형식을 흉내낸 것):

```json
{
  "detail": {
    "resource": {
      "instanceDetails": {
        "instanceId": "i-0123456789abcdef0"
      }
    }
  }
}
```

> `i-0123456789abcdef0` 자리에는 실습용으로 미리 만들어둔 **테스트 EC2 인스턴스 ID**를 넣으세요. 절대 운영 중인 인스턴스 ID를 넣지 마세요.

  c. **Test** 클릭 → 실행 결과에 `"status": "isolated"` 나오면 성공
  <img width="700" alt="image" src="https://github.com/user-attachments/assets/4a0545e2-55de-4c43-ba14-1a414427cce2" />

  d. EC2 콘솔에서 해당 인스턴스의 보안 그룹이 `sg-isolation-demo`로 바뀌었는지 확인

이제 이 규칙에 이미 등록되어 있던 SNS Target과 Lambda Target이 동시에 실행되는 구조가 됩니다 (한 이벤트 → 알림 + 자동조치 둘 다)

#### 주의사항
- 예시 코드의 `sg-isolation0001`은 격리 전용 보안 그룹 ID이며, 실제 환경에서는 사전에 아웃바운드가 차단된 격리용 SG를 미리 생성해두어야 한다.
- 실습 환경에서는 실제 운영 인스턴스에 적용하지 말고 테스트 인스턴스로 검증할 것.
