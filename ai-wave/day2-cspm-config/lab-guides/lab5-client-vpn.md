#### Client VPN 실습 

---

#### 0단계. 시작 전 환경 확인

#### 0-1. git 설치 확인 (Windows는 Git Bash 사용)
1. [git-scm.com](https://git-scm.com/download/win) 접속 → Windows용 설치 파일 다운로드 → 설치 (전부 기본값으로 Next 눌러도 됨)
2. 설치 후 **시작 메뉴 → "Git Bash"** 검색해서 실행
3. Git Bash 창에 아래 입력해서 버전 나오면 정상:
```bash
git --version
```

#### 0-2. 사용할 VPC·서브넷 확인
1. AWS 콘솔 검색창에 **VPC** 입력 → 이동
2. 좌측 메뉴 **Your VPCs** 클릭 → 사용할 VPC의 **VPC ID**와 **IPv4 CIDR**(예: `10.0.0.0/16`)를 메모장에 적어두기
3. 좌측 메뉴 **Subnets** 클릭 → 그 VPC 소속 서브넷 하나 선택 → **Subnet ID** 메모
4. 좌측 메뉴 **Internet Gateways** 클릭 → 그 VPC에 연결된 IGW가 있는지 확인 (State: Attached)
   - 없다면: **Create internet gateway** → 생성 → 체크박스 선택 → **Actions → Attach to VPC** → 해당 VPC 선택
5. **Route Tables** 클릭 → 그 서브넷에 연결된 라우팅 테이블 선택 → **Routes** 탭에서 `0.0.0.0/0 → igw-xxxxx` 경로가 있는지 확인
   - 없다면: **Edit routes** → **Add route** → Destination `0.0.0.0/0`, Target에서 방금 확인한 IGW 선택 → **Save changes**

#### 0-3. 테스트할 EC2 인스턴스 준비 (연결 확인용)
- 테스트 인스턴스가 이 VPC에 있다면 그대로 사용 가능
- 없다면 이 VPC의 서브넷에 t3.micro 인스턴스 하나 새로 생성 (Public IP는 Disable로 둬도 무방)
- 인스턴스 상세 화면에서 **프라이빗 IPv4 주소**(예: `10.0.1.25`)를 메모장에 적어두기 — 나중에 ping 테스트용

---

#### 1단계. 서버·클라이언트 인증서 생성 (Git Bash)

Git Bash를 열고 원하는 작업 폴더로 이동한 뒤(예: 바탕화면):

```bash
cd ~/Desktop

# 1. easy-rsa 다운로드
git clone https://github.com/OpenVPN/easy-rsa.git
```
→ 실행하면 여러 줄의 다운로드 로그가 뜨고, 마지막에 `Resolving deltas: 100%` 같은 문구가 나오면 성공.

```bash
cd easy-rsa/easyrsa3
```

```bash
# 2. PKI 초기화
./easyrsa init-pki
```
→ `init-pki complete...` 메시지가 뜨면 성공. `pki` 폴더가 생성됩니다.

```bash
# 3. CA(인증기관) 생성
./easyrsa build-ca nopass
```
→ `Common Name` 입력하라고 뜨면 그냥 **Enter** (기본값 `Easy-RSA CA` 사용). 마지막에 `CA creation complete...` 뜨면 성공.

```bash
# 4. 서버 인증서 생성
./easyrsa build-server-full server nopass
```
→ 중간에 `Confirm request details: type 'yes'` 라고 뜨면 **yes** 입력 후 Enter. `Certificate created at...` 뜨면 성공.

```bash
# 5. 클라이언트 인증서 생성
./easyrsa build-client-full client1.domain.tld nopass
```
→ 마찬가지로 `yes` 입력. `Certificate created at...` 뜨면 성공.

#### 생성 확인
```bash
ls pki/ca.crt pki/issued/server.crt pki/private/server.key pki/issued/client1.domain.tld.crt pki/private/client1.domain.tld.key
```
→ 5개 파일 경로가 전부 에러 없이 출력되면 정상입니다.

#### 파일 내용 빠르게 복사하는 법 (다음 단계에서 필요)
```bash
cat pki/ca.crt
```
→ 출력된 내용을 **`-----BEGIN CERTIFICATE-----`부터 `-----END CERTIFICATE-----`까지 전체** 마우스로 드래그해서 복사(Ctrl+C 또는 우클릭 → Copy)

같은 방식으로 아래 파일들도 각각 `cat` 명령으로 내용을 확인·복사할 수 있습니다:
```bash
cat pki/issued/server.crt
cat pki/private/server.key
cat pki/issued/client1.domain.tld.crt
cat pki/private/client1.domain.tld.key
```

---

#### 2단계. ACM에 서버 인증서 업로드

1. AWS 콘솔 검색창에 **Certificate Manager** 입력 → 이동
2. **우측 상단 리전이 서울(ap-northeast-2)인지 확인** (다르면 여기서 이후 모든 게 안 보임)
3. **가져오기(Import a certificate)** 버튼 클릭
4. **인증서 본문(Certificate body)** 칸에 → 1단계에서 복사한 `server.crt` 내용 붙여넣기
5. **인증서 프라이빗 키(Certificate private key)** 칸에 → `server.key` 내용 붙여넣기
6. **인증서 체인(Certificate chain)** 칸에 → `ca.crt` 내용 붙여넣기
7. **다음** 클릭 → 태그는 생략하고 **검토 및 가져오기** → **가져오기** 클릭
8. 인증서 목록 화면으로 돌아오면, 방금 업로드한 항목의 **식별자(ARN)** 클릭 → 전체 ARN 문자열 복사해서 메모장에 저장 (`arn:aws:acm:ap-northeast-2:...`로 시작하는 긴 문자열)

> 클라이언트 인증서까지 별도로 올리고 싶으면 위 과정을 클라이언트 인증서(`client1.domain.tld.crt`, 프라이빗 키, 체인은 동일한 `ca.crt`)로 한 번 더 반복하세요. 귀찮으면 생략하고 3단계에서 서버 인증서 ARN을 그대로 재사용해도 됩니다.

---

#### 3단계. Client VPN 엔드포인트 생성

1. AWS 콘솔 검색창에 **VPC** 입력 → 이동
2. 좌측 메뉴 맨 아래쪽 **Client VPN Endpoints** 클릭
3. **Create Client VPN endpoint** 클릭
4. 아래 표대로 입력:

| 필드 | 입력값 |
|---|---|
| Name tag | `my-client-vpn` |
| Description | (생략 가능) |
| Client IPv4 CIDR | `10.100.0.0/22` |
| Server certificate ARN | 2단계에서 복사한 ARN 붙여넣기(드롭다운에서 선택) |
| Use mutual authentication | 체크 |
| Client certificate ARN | 서버와 동일한 ARN(또는 별도 업로드한 클라이언트 인증서 ARN) |
| DNS servers | 비워둠 (기본 VPC DNS 사용) |
| Transport Protocol | UDP (기본값) |
| Enable split-tunnel | 체크 안 함 (Full-tunnel, 인터넷까지 확인하려면) |

5. 맨 아래 **Create Client VPN endpoint** 클릭
6. 생성된 엔드포인트를 클릭 → **Client VPN Endpoint ID**(`cvpn-endpoint-xxxx`)와 **State**(`Pending associate`) 확인

---

#### 4단계. 대상 네트워크 연결

1. 엔드포인트 선택 → **Target network associations** 탭 → **Associate target network**
2. **VPC**: 0단계에서 확인한 VPC 선택
3. **Choose a subnet to associate**: 0단계에서 확인한 서브넷 선택
4. **Associate target network** 클릭
5. 화면 새로고침(⟳ 아이콘)하면서 **State**가 `Associating` → `Available`로 바뀔 때까지 대기 (보통 2~5분)

---

#### 5단계. 권한 부여 규칙 추가 (VPC 접근)

1. **Authorization rules** 탭 → **Add authorization rule**
2. **Destination network to enable access**: 0단계에서 메모한 VPC CIDR 입력 (예: `10.0.0.0/16`)
3. **Grant access to**: **Allow access to all users**
4. **Add authorization rule** 클릭

---

#### 6단계. 인터넷 액세스 추가

1. **Route Table** 탭 → **Create Route**
2. **Route destination**: `0.0.0.0/0`
3. **Subnet ID for target network association**: 4단계에서 연결한 서브넷 선택
4. **Create Route** 클릭
5. 다시 **Authorization rules** 탭 → **Add authorization rule**
6. **Destination network**: `0.0.0.0/0`, **Grant access to**: Allow access to all users → **Add authorization rule**

---

#### 7단계. 보안 그룹 확인

1. VPC 콘솔 → **Security Groups**
2. 사용 중인 VPC의 **default** 보안 그룹 클릭
3. **Inbound rules** 탭 → 규칙이 없으면 **Edit inbound rules** → **Add rule**:
   - Type: **All ICMP - IPv4** (ping 테스트를 위해 필요)
   - Source: 3단계에서 지정한 **Client IPv4 CIDR** (`10.100.0.0/22`)
   - **Save rules**
4. **Outbound rules** 탭 → `0.0.0.0/0` 전체 허용 규칙이 이미 있는지 확인 (기본 보안 그룹은 보통 있음)

> 이 ICMP 규칙이 없으면 VPN은 연결돼도 ping이 응답하지 않습니다. 꼭 확인하세요.

---

#### 8단계. 클라이언트 구성 파일 준비

1. Client VPN Endpoints 화면에서 엔드포인트 선택 → **Download client configuration** 클릭 → `downloaded-client-config.ovpn` 파일이 다운로드 폴더에 저장됨
2. 이 파일을 **메모장(또는 VS Code)으로 열기** — 더블클릭하면 다른 프로그램으로 열릴 수 있으니, 파일 우클릭 → **연결 프로그램 → 메모장** 선택
3. 파일 맨 아래로 스크롤 → 새 줄에 다음 형식으로 추가:

```
<cert>
(1단계에서 cat으로 확인한 client1.domain.tld.crt 내용 전체 붙여넣기)
</cert>

<key>
(1단계에서 cat으로 확인한 client1.domain.tld.key 내용 전체 붙여넣기)
</key>
```

4. **Ctrl+S**로 저장 (파일 형식은 "모든 파일", 확장자 `.ovpn` 그대로 유지)

---

#### 9단계. AWS VPN Client 설치 및 연결 (Windows)

1. [AWS VPN Client 다운로드 페이지](https://aws.amazon.com/vpn/client-vpn-download/) 접속 → **Windows (64-bit)** 설치 파일 다운로드
2. 다운로드한 `.msi` 파일 더블클릭 → 설치 마법사 전부 **Next → Next → Install → Finish**
3. 설치 후 **AWS VPN Client** 실행 (관리자 권한 요청 뜨면 **예** 클릭)
4. 상단 메뉴 **File → Manage Profiles**
5. **Add Profile** 클릭
6. **Display Name**: `my-vpn` (자유롭게)
7. **VPN Configuration File**: **Browse** → 8단계에서 저장한 `.ovpn` 파일 선택
8. **Add Profile** 클릭 → Manage Profiles 창 닫기
9. 메인 화면에서 방금 만든 프로필 선택된 상태로 **Connect** 버튼 클릭
10. 몇 초 후 **"Connected"** 문구와 함께 초록불이 뜨면 연결 성공

---

#### 10단계. Windows `ipconfig`로 실제 연결 확인

### 10-1. 연결 전 상태 미리 확인 (선택이지만 추천)
VPN 연결하기 **전**에 cmd 창을 하나 열어서 기준선을 봐두면 비교하기 쉽습니다.

1. **시작 메뉴 → "cmd" 검색 → 명령 프롬프트 실행**
2. 아래 입력:
```
ipconfig
```
3. 화면에 나오는 어댑터 목록을 한 번 훑어봅니다 (Wi-Fi, 이더넷 등만 보일 것)

### 10-2. VPN 연결 후 확인
1. 9단계에서 **AWS VPN Client로 Connect** 완료한 상태에서
2. cmd 창에 다시 입력:
```
ipconfig
```
3. **새로운 어댑터가 하나 추가되어 있어야 합니다.** 보통 이렇게 보입니다:

```
Ethernet adapter Ethernet 5:   (또는 "AWS VPN Client" 관련 이름)

   Connection-specific DNS Suffix  . :
   IPv4 Address. . . . . . . . . . . : 10.100.0.6
   Subnet Mask . . . . . . . . . . . : 255.255.252.0
   Default Gateway . . . . . . . . . :
```

**확인 포인트**
- **IPv4 Address**가 3단계에서 지정한 **Client IPv4 CIDR (`10.100.0.0/22`) 범위 안의 IP**로 할당되어 있으면 → VPN 터널이 정상적으로 만들어진 것입니다.
- 이 어댑터가 안 보이면 → AWS VPN Client 화면에서 "Connected" 상태인지 다시 확인하고, 안 되어 있으면 재연결 시도

#### 10-3. 상세 정보로 한 번 더 확인 (선택)
```
ipconfig /all
```
→ 방금 그 어댑터 항목에서 **Description**에 "AWS VPN Client" 또는 "TAP-Windows Adapter" 같은 이름이 포함되어 있으면 확실

### 10-4. 실제 VPC 리소스로 ping 테스트
0-3단계에서 메모해둔 EC2 프라이빗 IP로 ping을 보내봅니다:
```
ping 10.0.1.25
```
(위 IP는 예시이며, 실제 메모해둔 EC2 프라이빗 IP로 바꿔서 입력)

**성공 시 화면:**
```
10.0.1.25에서 응답: 바이트=32 시간=5ms TTL=255
10.0.1.25에서 응답: 바이트=32 시간=4ms TTL=255
...
```
→ 이게 뜨면 **VPN을 통해 VPC 내부 리소스까지 실제로 도달**하는 것이 증명된 것입니다.

**실패 시 (요청 시간 초과 등)** → 아래 트러블슈팅 표 확인

#### 10-5. 인터넷 접속도 되는지 확인 (6단계까지 했다면)
```
ping 8.8.8.8
```
또는 그냥 브라우저에서 아무 사이트나 접속해보기 — 정상 로딩되면 인터넷 라우팅까지 성공.

#### 10-6. 경로 확인 (선택, 있어보이는 추가 데모)
```
tracert 10.0.1.25
```
→ 첫 번째 홉이 VPN 어댑터의 게이트웨이를 거쳐 나가는 게 보이면, 트래픽이 실제로 VPN 터널을 통과하고 있다는 증거

---

#### 전체 흐름 요약

1. `ipconfig` (연결 전)
2. AWS VPN Client Connect 클릭 → "Connected" 
3. `ipconfig` (연결 후, 새 어댑터+IP 확인) 
4. `ping <EC2 프라이빗 IP>` 성공 화면 캡처

---


| ping은 되는데 인터넷은 안 됨 | 6단계(0.0.0.0/0 라우트 + 권한 규칙) 둘 다 했는지, 서브넷의 보안 그룹 아웃바운드가 막혀있지 않은지 확인 |
