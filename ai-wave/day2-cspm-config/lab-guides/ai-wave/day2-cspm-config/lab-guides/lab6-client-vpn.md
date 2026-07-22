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
