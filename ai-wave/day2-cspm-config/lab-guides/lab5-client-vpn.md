#### 실습 Client VPN — AWS Client VPN 엔드포인트 구성

#### 목표
상호 인증(Mutual Authentication) 방식으로 AWS Client VPN 엔드포인트를 생성하고, 클라이언트에서 VPC 및 인터넷에 접속되는 것까지 확인한다.

#### 사전 준비
- Client VPN 엔드포인트로 작업하는 데 필요한 IAM 권한
- 인증서를 AWS Certificate Manager(ACM)로 가져오는 데 필요한 권한
- 서브넷 1개 이상 + 인터넷 게이트웨이가 있는 VPC (서브넷 라우팅 테이블에 IGW 경로 포함)
- OpenVPN easy-rsa 유틸리티 설치 환경

#### Step 1. 서버 · 클라이언트 인증서 및 키 생성

```bash
git clone https://github.com/OpenVPN/easy-rsa.git
cd easy-rsa/easyrsa3
./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa build-server-full server nopass
./easyrsa build-client-full client1.domain.tld nopass
```

생성된 인증서(`server.crt`, `server.key`, `ca.crt` 등)를 안전한 곳에 보관합니다.

#### Step 2. 인증서를 ACM에 업로드

1. AWS Certificate Manager 콘솔 이동
2. 서버 인증서 + 개인 키(및 CA 인증서) 가져오기
3. Client VPN 엔드포인트를 생성할 리전과 **동일한 리전**에 업로드해야 함

#### Step 3. Client VPN 엔드포인트 생성

1. VPC 콘솔 → **Client VPN Endpoints** → **Create Client VPN endpoint**
2. 이름 태그·설명 입력(선택)
3. **클라이언트 IPv4 CIDR**: 클라이언트에 할당할 IP 대역 지정 (최소 /22, 최대 /12, 생성 후 변경 불가)
4. **서버 인증서 ARN**: Step 2에서 업로드한 서버 인증서 선택
5. **인증 옵션**: "상호 인증 사용" 선택 → 클라이언트 인증서 ARN 지정
   - 서버·클라이언트 인증서가 같은 CA로 발급됐다면 서버 인증서 ARN을 양쪽 다 지정 가능
6. 나머지 기본값 유지 → **Create Client VPN endpoint**

생성 직후 상태는 `pending-associate`입니다.

#### Step 4. 대상 네트워크(Target Network) 연결

1. 생성한 Client VPN 엔드포인트 선택 → **Target network associations** → **Associate target network**
2. VPC와 서브넷 선택 → **Associate target network**

첫 서브넷 연결 시 자동으로 벌어지는 일:
- 엔드포인트 상태가 `available`로 변경 (단, 아직 권한 부여 규칙 없으면 VPC 리소스 접근은 불가)
- VPC 로컬 라우팅이 Client VPN 라우팅 테이블에 자동 추가
- VPC 기본 보안 그룹이 엔드포인트에 자동 적용

#### Step 5. VPC에 대한 권한 부여 규칙(Authorization Rule) 추가

1. **Authorization rules** → **Add authorization rule**
2. 대상 네트워크(Destination network)에 VPC의 IPv4 CIDR 입력
3. "모든 사용자에게 액세스 허용" 선택 → 추가

#### Step 6. 인터넷 액세스 제공 (선택)

1. **Route Table** → **Create Route** → 대상 `0.0.0.0/0`, 서브넷 ID 지정
2. **Authorization rules**에 `0.0.0.0/0` 대상으로 규칙 추가

#### Step 7. 보안 그룹 요구 사항 확인

- 트래픽을 라우팅하는 서브넷의 보안 그룹이 인터넷으로의 아웃바운드 트래픽 허용해야 함
- VPC 리소스의 보안 그룹에 Client VPN 엔드포인트로부터의 접근을 허용하는 규칙 필요

#### Step 8. 클라이언트 구성 파일 다운로드 및 준비

1. 엔드포인트 선택 → **Download client configuration**
2. 텍스트 편집기로 열어서 `<cert></cert>`, `<key></key>` 태그 추가
3. 각각 클라이언트 인증서(`.crt`)와 개인 키(`.key`) 내용을 붙여넣기
4. 저장

#### Step 9. Client VPN 엔드포인트에 연결

1. AWS 제공 VPN Client(또는 다른 OpenVPN 기반 클라이언트) 설치
2. Step 8에서 준비한 구성 파일 가져오기(Import)
3. 연결 → 성공 시 VPC 내부 리소스 및 인터넷 접근 확인

---

#### 트러블슈팅

**Endpoint 생성 시 인증서 오류**
ACM에 서버 인증서가 없거나, 인증 유형(상호 인증)과 맞지 않는 인증서를 지정한 경우입니다. 상호 인증에는 반드시 서버 인증서가 필요합니다.

**연결은 되는데 VPC 리소스에 접근이 안 됨**
Authorization Rule이 없거나, 대상 CIDR 범위가 실제 리소스 대역과 일치하지 않는 경우입니다.

**클라이언트가 인터넷에도 접속이 안 됨**
Full-tunnel 모드인데 라우트나 보안 그룹에서 아웃바운드가 막혀 있는 경우입니다. Split-tunnel 여부와 Step 7의 보안 그룹 설정을 확인하세요.

**특정 사용자만 연결이 거부됨**
해당 클라이언트 인증서가 취소(revoke)되었거나 CRL(인증서 해지 목록)에 등록된 경우입니다.

#### 참고
[1] AWS Client VPN 시작하기: https://docs.aws.amazon.com/ko_kr/vpn/latest/clientvpn-admin/cvpn-getting-started.html

[2] AWS Client VPN 상호 인증: https://docs.aws.amazon.com/ko_kr/vpn/latest/clientvpn-admin/mutual.html
