"""
GuardDuty Finding 발생 시 EC2 인스턴스를 격리용 보안 그룹으로 자동 교체하는
Lambda 예시 코드.

트리거: EventBridge 규칙 (GuardDuty Finding, severity >= 7 등 조건)
사전 준비: 아웃바운드가 차단된 격리 전용 보안 그룹(ex.sg-isolation0001)을 미리 생성
"""

import boto3

ISOLATION_SG_ID = "sg-isolation0001"  # 실제 환경의 격리용 SG ID로 교체


def lambda_handler(event, context):
    detail = event["detail"]
    instance_id = detail["resource"]["instanceDetails"]["instanceId"]

    ec2 = boto3.client("ec2")

    # 격리 전용 보안 그룹으로 교체 (기존 SG 제거)
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=[ISOLATION_SG_ID],
    )

    return {
        "status": "isolated",
        "instance": instance_id,
    }
