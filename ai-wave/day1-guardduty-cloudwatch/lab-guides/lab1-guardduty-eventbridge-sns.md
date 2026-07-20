### 실습 ① GuardDuty → EventBridge → SNS 알림 파이프라인

#### 목표
GuardDuty Finding 발생 시 EventBridge를 통해 SNS로 자동 알림이 전달되는 탐지-알림 파이프라인을 구축한다.

#### 사전 준비
- IAM 권한: GuardDuty, EventBridge, SNS 관련 권한 보유 계정
- 알림 수신용 이메일 주소

#### Step 1. GuardDuty 활성화
1. GuardDuty 콘솔 이동
2. [지금 시작하기] 클릭 → 계정 단위 활성화
3. 활성화 확인 (Summary 화면에서 상태 확인)

<img width="500" alt="image" src="https://github.com/user-attachments/assets/966cdd85-674a-4381-85b1-f45b263da3f7" />


#### Step 2. Sample Finding 생성
1. GuardDuty 콘솔 → 설정(Settings)
2. [Sample findings 생성] 클릭
3. Findings 목록에서 테스트용 Finding 확인

<img width="500" alt="image" src="https://github.com/user-attachments/assets/6b90d2bd-2d82-4d27-b086-584abe6e967a" />


#### Step 3. SNS 생성
1. SNS 콘솔 → Topics → Create topic (Standard 타입)
2. 주제 이름 지정 후 생성
3. Create subscription → Protocol: Email → 알림 받을 이메일 주소 입력
4. 받은 확인 메일에서 [Confirm subscription] 클릭 (이거 안 하면 알림 안 옴!)

<img width="500" alt="image" src="https://github.com/user-attachments/assets/fd42c1db-62e8-444e-b013-43a35aacb06f" />



#### Step 4. EventBridge 규칙 생성 (Enhanced Builder 기준)
1. 왼쪽 "Events" 탭이 선택된 상태에서, AWS SERVICE EVENTS 클릭해서 펼치기
2. 검색창에 GuardDuty 입력 → GuardDuty 선택
3. 이벤트 타입 목록에서 GuardDuty Finding 선택
4. 그걸 가운데 "Triggering Events" 박스 위로 드래그해서 놓기 (또는 클릭해서 추가)
5. 박스에 이벤트가 들어가면, 오른쪽에 세부 패턴 편집 화면이 열려요 — 여기서 Event pattern (filter) 부분에 심각도 조건(예: severity >= 7)을 추가

Step 5. SNS를 Target으로 연결
1. 왼쪽 상단 "Targets" 탭으로 전환
2. 목록에서 SNS topic 찾기 (또는 검색창에 SNS 입력)
3. 오른쪽 "Targets" 박스로 드래그해서 놓기
4. 미리 만들어둔 SNS 주제(Topic ARN) 선택

#### 실무 연계 노트
PCI-DSS 증적 작업에서 구축한 GuardDuty → EventBridge → SNS 파이프라인과 동일한 구조. 규정 준수 환경에서는 이 알림 흐름 자체가 모니터링 통제(Control) 증적 자료로 활용된다.
