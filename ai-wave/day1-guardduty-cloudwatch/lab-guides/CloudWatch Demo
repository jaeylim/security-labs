#### step3. 샘플 로그 주입 (CLI)

##### cloudshell (콘솔에서 직접 입력)
```
aws logs put-log-events \
  --log-group-name /demo/login-events \
  --log-stream-name stream-1 \
  --log-events \
  "[
    {\"timestamp\": $(date +%s000), \"message\": \"{\\\"eventName\\\":\\\"ConsoleLogin\\\",\\\"sourceIPAddress\\\":\\\"203.0.113.10\\\",\\\"errorMessage\\\":\\\"Failed authentication\\\"}\"},
    {\"timestamp\": $(date +%s000), \"message\": \"{\\\"eventName\\\":\\\"ConsoleLogin\\\",\\\"sourceIPAddress\\\":\\\"203.0.113.10\\\",\\\"errorMessage\\\":\\\"Failed authentication\\\"}\"},
    {\"timestamp\": $(date +%s000), \"message\": \"{\\\"eventName\\\":\\\"ConsoleLogin\\\",\\\"sourceIPAddress\\\":\\\"198.51.100.5\\\",\\\"errorMessage\\\":\\\"Failed authentication\\\"}\"},
    {\"timestamp\": $(date +%s000), \"message\": \"{\\\"eventName\\\":\\\"ConsoleLogin\\\",\\\"sourceIPAddress\\\":\\\"198.51.100.5\\\",\\\"errorMessage\\\":\\\"Succeeded\\\"}\"}
  ]"
```

#### step4. Log Analytics 조회 결과 확인
```
fields @timestamp, sourceIPAddress, eventName, errorMessage
   | filter eventName = "ConsoleLogin" and errorMessage like /Failed/
   | stats count() as failCount by sourceIPAddress
   | sort failCount desc
```
