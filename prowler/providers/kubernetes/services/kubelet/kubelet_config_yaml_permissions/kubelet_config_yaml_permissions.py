from prowler.lib.check.models import Check, Check_Report_Kubernetes
from prowler.lib.utils.utils import get_file_permissions
from prowler.providers.kubernetes.services.core.core_client import core_client


class kubelet_config_yaml_permissions(Check):
    def execute(self) -> Check_Report_Kubernetes:
        findings = []
        for node in core_client.nodes.values():
            report = Check_Report_Kubernetes(self.metadata())
            report.namespace = node.namespace
            report.resource_name = node.name
            report.resource_id = node.uid
            # It can only be checked if Prowler is being executed inside a worker node or if the file is the default one
            if node.inside:
                if not get_file_permissions("/var/lib/kubelet/config.yaml"):
                    report.status = "MANUAL"
                    report.status_extended = f"Kubelet config.yaml file not found in Node {node.name}, please verify kubelet config.yaml file permissions manually."
                else:
                    report.status = "PASS"
                    report.status_extended = f"kubelet config.yaml file permissions are set to 600 or more restrictive in Node {node.name}."
                    if get_file_permissions("/var/lib/kubelet/config.yaml") > 0o600:
                        report.status = "FAIL"
                        report.status_extended = f"kubelet config.yaml file permissions are not set to 600 or more restrictive in Node {node.name}."
            else:
                report.status = "MANUAL"
                report.status_extended = f"Prowler is not being executed inside Node {node.name}, please verify kubelet config.yaml file permissions manually."
            findings.append(report)
        return findings
