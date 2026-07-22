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

#####
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
