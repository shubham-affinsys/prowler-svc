from argparse import Namespace
from datetime import datetime
from os import environ

from freezegun import freeze_time
from mock import MagicMock, patch

from prowler.config.config import (
    default_config_file_path,
    default_fixer_config_file_path,
    load_and_validate_config_file,
)
from prowler.providers.gcp.gcp_provider import GcpProvider
from prowler.providers.gcp.models import GCPIdentityInfo, GCPProject


class TestGCPProvider:
    def test_gcp_provider(self):
        project_id = []
        excluded_project_id = []
        list_project_id = False
        credentials_file = ""
        impersonate_service_account = ""
        audit_config = load_and_validate_config_file("gcp", default_config_file_path)
        fixer_config = load_and_validate_config_file(
            "gcp", default_fixer_config_file_path
        )

        projects = {
            "test-project": GCPProject(
                number="55555555",
                id="project/55555555",
                name="test-project",
                labels={"test": "value"},
                lifecycle_state="",
            )
        }

        mocked_service = MagicMock()

        mocked_service.projects.list.return_value = MagicMock(
            execute=MagicMock(return_value={"projects": projects})
        )

        with patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.setup_session",
            return_value=(None, "test-project"),
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.get_projects",
            return_value=projects,
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.update_projects_with_organizations",
            return_value=None,
        ), patch(
            "prowler.providers.gcp.gcp_provider.discovery.build",
            return_value=mocked_service,
        ):
            gcp_provider = GcpProvider(
                project_id,
                excluded_project_id,
                credentials_file,
                impersonate_service_account,
                list_project_id,
                audit_config=audit_config,
                fixer_config=fixer_config,
            )
            assert gcp_provider.session is None
            assert gcp_provider.project_ids == ["test-project"]
            assert gcp_provider.projects == projects
            assert gcp_provider.default_project_id == "test-project"
            assert gcp_provider.identity == GCPIdentityInfo(profile="default")
            assert gcp_provider.audit_config == {"shodan_api_key": None}

    @freeze_time(datetime.today())
    def test_is_project_matching(self):
        arguments = Namespace()
        arguments.project_id = []
        arguments.excluded_project_id = []
        arguments.list_project_id = False
        arguments.credentials_file = ""
        arguments.impersonate_service_account = ""
        arguments.config_file = default_config_file_path
        arguments.fixer_config = default_fixer_config_file_path

        # Output options
        arguments.status = []
        arguments.output_formats = ["csv"]
        arguments.output_directory = "output_test_directory"
        arguments.verbose = True
        arguments.only_logs = False
        arguments.unix_timestamp = False
        arguments.shodan = "test-api-key"

        projects = {
            "test-project": GCPProject(
                number="55555555",
                id="project/55555555",
                name="test-project",
                labels={"test": "value"},
                lifecycle_state="",
            )
        }

        mocked_service = MagicMock()

        mocked_service.projects.list.return_value = MagicMock(
            execute=MagicMock(return_value={"projects": projects})
        )
        with patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.setup_session",
            return_value=(None, None),
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.get_projects",
            return_value=projects,
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.update_projects_with_organizations",
            return_value=None,
        ), patch(
            "prowler.providers.gcp.gcp_provider.discovery.build",
            return_value=mocked_service,
        ):
            gcp_provider = GcpProvider(
                arguments.project_id,
                arguments.excluded_project_id,
                arguments.credentials_file,
                arguments.impersonate_service_account,
                arguments.list_project_id,
                arguments.config_file,
                arguments.fixer_config,
            )

            input_project = "sys-*"
            project_to_match = "sys-12345678"
            assert gcp_provider.is_project_matching(input_project, project_to_match)
            input_project = "*prowler"
            project_to_match = "test-prowler"
            assert gcp_provider.is_project_matching(input_project, project_to_match)
            input_project = "test-project"
            project_to_match = "test-project"
            assert gcp_provider.is_project_matching(input_project, project_to_match)
            input_project = "*test*"
            project_to_match = "prowler-test-project"
            assert gcp_provider.is_project_matching(input_project, project_to_match)
            input_project = "prowler-test-project"
            project_to_match = "prowler-test"
            assert not gcp_provider.is_project_matching(input_project, project_to_match)

    def test_setup_session_with_credentials_file_no_impersonate(self):
        mocked_credentials = MagicMock()

        mocked_credentials.refresh.return_value = None
        mocked_credentials._service_account_email = "test-service-account-email"

        arguments = Namespace()
        arguments.project_id = []
        arguments.excluded_project_id = []
        arguments.list_project_id = False
        arguments.credentials_file = "test_credentials_file"
        arguments.impersonate_service_account = ""
        arguments.config_file = default_config_file_path
        arguments.fixer_config = default_fixer_config_file_path

        projects = {
            "test-project": GCPProject(
                number="55555555",
                id="project/55555555",
                name="test-project",
                labels={"test": "value"},
                lifecycle_state="",
            )
        }

        mocked_service = MagicMock()

        mocked_service.projects.list.return_value = MagicMock(
            execute=MagicMock(return_value={"projects": projects})
        )
        with patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.get_projects",
            return_value=projects,
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.update_projects_with_organizations",
            return_value=None,
        ), patch(
            "os.path.abspath",
            return_value="test_credentials_file",
        ), patch(
            "prowler.providers.gcp.gcp_provider.default",
            return_value=(mocked_credentials, MagicMock()),
        ), patch(
            "prowler.providers.gcp.gcp_provider.discovery.build",
            return_value=mocked_service,
        ):
            gcp_provider = GcpProvider(
                arguments.project_id,
                arguments.excluded_project_id,
                arguments.credentials_file,
                arguments.impersonate_service_account,
                arguments.list_project_id,
                arguments.config_file,
                arguments.fixer_config,
            )
            assert environ["GOOGLE_APPLICATION_CREDENTIALS"] == "test_credentials_file"
            assert gcp_provider.session is not None
            assert gcp_provider.identity.profile == "test-service-account-email"

    def test_setup_session_with_credentials_file_and_impersonate(self):
        mocked_credentials = MagicMock()

        mocked_credentials.refresh.return_value = None
        mocked_credentials._service_account_email = "test-service-account-email"

        arguments = Namespace()
        arguments.project_id = []
        arguments.excluded_project_id = []
        arguments.list_project_id = False
        arguments.credentials_file = "test_credentials_file"
        arguments.impersonate_service_account = "test-impersonate-service-account"
        arguments.config_file = default_config_file_path
        arguments.fixer_config = default_fixer_config_file_path

        projects = {
            "test-project": GCPProject(
                number="55555555",
                id="project/55555555",
                name="test-project",
                labels={"test": "value"},
                lifecycle_state="",
            )
        }

        mocked_service = MagicMock()

        mocked_service.projects.list.return_value = MagicMock(
            execute=MagicMock(return_value={"projects": projects})
        )
        with patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.get_projects",
            return_value=projects,
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.update_projects_with_organizations",
            return_value=None,
        ), patch(
            "os.path.abspath",
            return_value="test_credentials_file",
        ), patch(
            "prowler.providers.gcp.gcp_provider.default",
            return_value=(mocked_credentials, MagicMock()),
        ), patch(
            "prowler.providers.gcp.gcp_provider.discovery.build",
            return_value=mocked_service,
        ):
            gcp_provider = GcpProvider(
                arguments.project_id,
                arguments.excluded_project_id,
                arguments.credentials_file,
                arguments.impersonate_service_account,
                arguments.list_project_id,
                arguments.config_file,
                arguments.fixer_config,
            )
            assert environ["GOOGLE_APPLICATION_CREDENTIALS"] == "test_credentials_file"
            assert gcp_provider.session is not None
            assert (
                gcp_provider.session.service_account_email
                == "test-impersonate-service-account"
            )
            assert gcp_provider.identity.profile == "default"
            assert (
                gcp_provider.impersonated_service_account
                == "test-impersonate-service-account"
            )

    def test_print_credentials_default_options(self, capsys):
        mocked_credentials = MagicMock()

        mocked_credentials.refresh.return_value = None
        mocked_credentials._service_account_email = "test-service-account-email"

        arguments = Namespace()
        arguments.project_id = []
        arguments.excluded_project_id = []
        arguments.list_project_id = False
        arguments.credentials_file = "test_credentials_file"
        arguments.impersonate_service_account = ""
        arguments.config_file = default_config_file_path
        arguments.fixer_config = default_fixer_config_file_path

        projects = {
            "test-project": GCPProject(
                number="55555555",
                id="project/55555555",
                name="test-project",
                labels={"test": "value"},
                lifecycle_state="",
            )
        }

        mocked_service = MagicMock()

        mocked_service.projects.list.return_value = MagicMock(
            execute=MagicMock(return_value={"projects": projects})
        )
        with patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.get_projects",
            return_value=projects,
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.update_projects_with_organizations",
            return_value=None,
        ), patch(
            "os.path.abspath",
            return_value="test_credentials_file",
        ), patch(
            "prowler.providers.gcp.gcp_provider.default",
            return_value=(mocked_credentials, MagicMock()),
        ), patch(
            "prowler.providers.gcp.gcp_provider.discovery.build",
            return_value=mocked_service,
        ):
            gcp_provider = GcpProvider(
                arguments.project_id,
                arguments.excluded_project_id,
                arguments.credentials_file,
                arguments.impersonate_service_account,
                arguments.list_project_id,
                arguments.config_file,
                arguments.fixer_config,
            )
            gcp_provider.print_credentials()
            captured = capsys.readouterr()
            assert "Using the GCP credentials below:" in captured.out
            assert (
                "GCP Account:" in captured.out
                and "test-service-account-email" in captured.out
            )
            assert "GCP Project IDs:" in captured.out and "test-project" in captured.out
            assert "Impersonated Service Account" not in captured.out
            assert "Excluded GCP Project IDs" not in captured.out

    def test_print_credentials_impersonated_service_account(self, capsys):
        mocked_credentials = MagicMock()

        mocked_credentials.refresh.return_value = None
        mocked_credentials._service_account_email = "test-service-account-email"

        arguments = Namespace()
        arguments.project_id = []
        arguments.excluded_project_id = []
        arguments.list_project_id = False
        arguments.credentials_file = "test_credentials_file"
        arguments.impersonate_service_account = "test-impersonate-service-account"
        arguments.config_file = default_config_file_path
        arguments.fixer_config = default_fixer_config_file_path

        projects = {
            "test-project": GCPProject(
                number="55555555",
                id="project/55555555",
                name="test-project",
                labels={"test": "value"},
                lifecycle_state="",
            )
        }

        mocked_service = MagicMock()

        mocked_service.projects.list.return_value = MagicMock(
            execute=MagicMock(return_value={"projects": projects})
        )
        with patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.get_projects",
            return_value=projects,
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.update_projects_with_organizations",
            return_value=None,
        ), patch(
            "os.path.abspath",
            return_value="test_credentials_file",
        ), patch(
            "prowler.providers.gcp.gcp_provider.default",
            return_value=(mocked_credentials, MagicMock()),
        ), patch(
            "prowler.providers.gcp.gcp_provider.discovery.build",
            return_value=mocked_service,
        ):
            gcp_provider = GcpProvider(
                arguments.project_id,
                arguments.excluded_project_id,
                arguments.credentials_file,
                arguments.impersonate_service_account,
                arguments.list_project_id,
                arguments.config_file,
                arguments.fixer_config,
            )
            gcp_provider.print_credentials()
            captured = capsys.readouterr()
            assert "Using the GCP credentials below:" in captured.out
            assert "GCP Account:" in captured.out and "default" in captured.out
            assert "GCP Project IDs:" in captured.out and "test-project" in captured.out
            assert (
                "Impersonated Service Account:" in captured.out
                and "test-impersonate-service-account" in captured.out
            )
            assert "Excluded GCP Project IDs" not in captured.out

    def test_print_credentials_excluded_project_ids(self, capsys):
        mocked_credentials = MagicMock()

        mocked_credentials.refresh.return_value = None
        mocked_credentials._service_account_email = "test-service-account-email"

        arguments = Namespace()
        arguments.project_id = []
        arguments.excluded_project_id = ["test-excluded-project"]
        arguments.list_project_id = False
        arguments.credentials_file = "test_credentials_file"
        arguments.impersonate_service_account = ""
        arguments.config_file = default_config_file_path
        arguments.fixer_config = default_fixer_config_file_path

        projects = {
            "test-project": GCPProject(
                number="55555555",
                id="project/55555555",
                name="test-project",
                labels={"test": "value"},
                lifecycle_state="",
            ),
            "test-excluded-project": GCPProject(
                number="12345678",
                id="project/12345678",
                name="test-excluded-project",
                labels={"test": "value"},
                lifecycle_state="",
            ),
        }

        mocked_service = MagicMock()

        mocked_service.projects.list.return_value = MagicMock(
            execute=MagicMock(return_value={"projects": projects})
        )

        with patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.get_projects",
            return_value=projects,
        ), patch(
            "prowler.providers.gcp.gcp_provider.GcpProvider.update_projects_with_organizations",
            return_value=None,
        ), patch(
            "os.path.abspath",
            return_value="test_credentials_file",
        ), patch(
            "prowler.providers.gcp.gcp_provider.default",
            return_value=(mocked_credentials, MagicMock()),
        ), patch(
            "prowler.providers.gcp.gcp_provider.discovery.build",
            return_value=mocked_service,
        ):
            gcp_provider = GcpProvider(
                arguments.project_id,
                arguments.excluded_project_id,
                arguments.credentials_file,
                arguments.impersonate_service_account,
                arguments.list_project_id,
                arguments.config_file,
                arguments.fixer_config,
            )
            gcp_provider.print_credentials()
            captured = capsys.readouterr()
            assert "Using the GCP credentials below:" in captured.out
            assert (
                "GCP Account:" in captured.out
                and "test-service-account-email" in captured.out
            )
            assert "GCP Project IDs:" in captured.out and "test-project" in captured.out
            assert "Impersonated Service Account" not in captured.out
            assert (
                "Excluded GCP Project IDs:" in captured.out
                and "test-excluded-project" in captured.out
            )
