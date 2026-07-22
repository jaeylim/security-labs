#### 1. cloudshell에서 인증서 생성

```
git clone https://github.com/OpenVPN/easy-rsa.git
cd easy-rsa/easyrsa3
./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa build-server-full server nopass
./easyrsa build-client-full client1.domain.tld nopass
```

#### 2. ACM에 바로 업로드
#####서버인증서
```
aws acm import-certificate \
  --certificate fileb://pki/issued/server.crt \
  --private-key fileb://pki/private/server.key \
  --certificate-chain fileb://pki/ca.crt
```
#####클라이언트 인증서
```
aws acm import-certificate \
  --certificate fileb://pki/issued/client1.domain.tld.crt \
  --private-key fileb://pki/private/client1.domain.tld.key \
  --certificate-chain fileb://pki/ca.crt
```
<img width="800" alt="image" src="https://github.com/user-attachments/assets/f04a06b5-196c-4e5f-988c-93f080f62eea" />

##### 22. ACM에 직접 업로드
1. Certificate body 칸에 붙여넣을 것:
```
bash
cat pki/issued/server.crt
```
2. Certificate private key 칸에 붙여넣을 것:
```
bash
cat pki/private/server.key
```

3. Certificate chain 칸에 붙여넣을 것:
```
bash
cat pki/ca.crt
```

#### 3. client 인증서 업로드
cat pki/issued/client1.domain.tld.crt
cat pki/private/client1.domain.tld.key --> 오류 발생시 "cat pki/private/client1.domain.tld.key | tr -d '\r'"

→ 나온 내용 그대로 ACM에 또 한 번 Import (본문/키 칸에 붙여넣고 체인은 ca.crt 그대로 재사용).

#### 4. VPN 설정 값
```
Details

Name: client-vpn-endpoint-01 (그대로 둬도 됨)
Description: 비워둠

Network infrastructure

Association type: Virtual Private Cloud (VPC) (이미 선택됨, 그대로)
VPC ID: 본인 VPC 선택 (jylim-vpc 등 아까 보이던 그거)
Security group IDs: 비워둠 (기본 SG 자동 적용됨)

IP address

Endpoint IP address type: IPv4 (Dual stack 말고 IPv4로 바꾸세요)
Traffic IP address type: IPv4
Client IPv4 CIDR: 10.100.0.0/22

Authentication

Server certificate ARN: 드롭다운에서 방금 만든 인증서 선택
Use mutual authentication 체크
체크하면 나오는 Client certificate ARN: 같은 인증서 선택
Use user-based authentication: 체크 안 함
```

#### 5. Target Network 연결
1) 방금 만든 Endpoint 클릭 → Target network associations 탭 → Associate target network
2) VPC 선택 → 서브넷 선택 → Associate target network
3) State가 Available로 바뀔 때까지 대기

#### 6. Authorization Rule 추가
1) Authorization rules 탭 → Add authorization rule
2) Destination network: VPC CIDR (10.0.0.0/16)
3) Grant access to: Allow access to all users
4) Add

#### 7. 보안 그룹 ICMP 허용 (ping 테스트용)
1) VPC 콘솔 → Security Groups
2) Inbound rules → Edit → Add rule
3) Type: All ICMP - IPv4, Source: 10.100.0.0/22
4) Save

#### 8.클라이언트 파일 준비 + 연결
Endpoint 화면 → Download client configuration
메모장으로 열기 → 맨 아래 추가:
<cert>
(cat pki/issued/client1.domain.tld.crt 내용)
</cert>
<key>
(cat pki/private/client1.domain.tld.key 내용)
</key>
