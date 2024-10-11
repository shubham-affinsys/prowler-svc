from datetime import datetime

from prowler.config.config import prowler_version
from prowler.lib.outputs.finding import Finding
from tests.providers.aws.utils import AWS_ACCOUNT_NUMBER, AWS_REGION_EU_WEST_1


def generate_finding_output(
    status: str = "PASS",
    status_extended: str = "",
    severity: str = "high",
    muted: bool = False,
    account_uid: str = AWS_ACCOUNT_NUMBER,
    account_name: str = AWS_ACCOUNT_NUMBER,
    region: str = AWS_REGION_EU_WEST_1,
    resource_details: str = "",
    resource_uid: str = "",
    resource_name: str = "",
    resource_tags: dict = {},
    compliance: dict = {"test-compliance": "test-compliance"},
    timestamp: datetime = None,
    provider: str = "aws",
    partition: str = "aws",
    description: str = "check description",
    risk: str = "test-risk",
    related_url: str = "test-url",
    remediation_recommendation_text: str = "",
    remediation_recommendation_url: str = "",
    remediation_code_nativeiac: str = "",
    remediation_code_terraform: str = "",
    remediation_code_cli: str = "",
    remediation_code_other: str = "",
    categories: str = "test-category",
    depends_on: str = "test-dependency",
    related_to: str = "test-related-to",
    notes: str = "test-notes",
    service_name: str = "test-service",
    check_id: str = "test-check-id",
    check_title: str = "test-check-id",
    check_type: str = "test-type",
) -> Finding:
    return Finding(
        auth_method="profile: default",
        timestamp=timestamp if timestamp else datetime.now(),
        account_uid=account_uid,
        account_name=account_name,
        account_email="",
        account_organization_uid="test-organization-id",
        account_organization_name="test-organization",
        account_tags={"test-tag": "test-value"},
        finding_uid="test-unique-finding",
        provider=provider,
        check_id=check_id,
        check_title=check_title,
        check_type=check_type,
        status=status,
        status_extended=status_extended,
        muted=muted,
        service_name=service_name,
        subservice_name="",
        severity=severity,
        resource_type="test-resource",
        resource_uid=resource_uid,
        resource_name=resource_name,
        resource_details=resource_details,
        resource_tags=resource_tags,
        partition=partition,
        region=region,
        description=description,
        risk=risk,
        related_url=related_url,
        remediation_recommendation_text=remediation_recommendation_text,
        remediation_recommendation_url=remediation_recommendation_url,
        remediation_code_nativeiac=remediation_code_nativeiac,
        remediation_code_terraform=remediation_code_terraform,
        remediation_code_cli=remediation_code_cli,
        remediation_code_other=remediation_code_other,
        compliance=compliance,
        categories=categories,
        depends_on=depends_on,
        related_to=related_to,
        notes=notes,
        prowler_version=prowler_version,
    )
