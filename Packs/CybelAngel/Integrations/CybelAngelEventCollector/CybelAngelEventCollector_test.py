import random

from unittest.mock import MagicMock
from CybelAngelEventCollector import DATE_FORMAT, Client
from CommonServerPython import *
import pytest


TEST_URL = "https://test.com/api"


@pytest.fixture()
def client() -> Client:
    return Client(
        TEST_URL,
        client_id="1234",
        client_secret="1234",
        verify=False,
        proxy=False,
    )


def load_test_data(file_name):
    with open(f"test_data/{file_name}.json") as file:
        return json.load(file)


class HttpRequestsMocker:
    def __init__(self, num_of_events: int):
        self.num_of_events = num_of_events
        self.num_of_calls = 0

    def valid_http_request_side_effect(self, method: str, url_suffix: str = "", params: Dict | None = None, **kwargs):
        if method == "GET" and url_suffix == "/api/v2/reports":
            start_date = params.get("start-date")
            events = create_events(1, amount_of_events=self.num_of_events, start_date=start_date)
            return create_mocked_response(events)
        if method == "POST" and kwargs.get("full_url") == "https://auth.cybelangel.com/oauth/token":
            return {"access_token": "new_access_token"}
        return None

    def expired_token_http_request_side_effect(
        self, method: str, url_suffix: Optional[str] = None, params: Dict | None = None, **kwargs
    ):
        if method == "GET" and url_suffix == "/api/v2/reports":
            if self.num_of_calls == 0:
                self.num_of_calls += 1
                return create_mocked_response([], status_code=401)
            start_date = params.get("start-date")
            return create_events(1, amount_of_events=self.num_of_events, start_date=start_date)
        if method == "POST" and kwargs.get("full_url") == "https://auth.cybelangel.com/oauth/token":
            return {"access_token": "new_access_token"}
        return None


def create_events(start_id: int, amount_of_events: int, start_date: str) -> Dict[str, List[Dict]]:
    events = [
        {
            "id": i,
            "updated_at": (dateparser.parse(start_date) + timedelta(seconds=i)).strftime(DATE_FORMAT),
        }
        for i in range(start_id, start_id + amount_of_events)
    ]
    random.shuffle(events)
    return {"reports": events}


def create_mocked_response(response: List[Dict] | Dict, status_code: int = 200) -> requests.Response:
    mocked_response = requests.Response()
    mocked_response._content = json.dumps(response).encode("utf-8")
    mocked_response.status_code = status_code
    return mocked_response


def test_http_request_token_expired(client: Client, mocker):
    """
    Given:
     - expired token from integration context

    When:
     - retrieving events by a http-request

    Then:
     - make sure token is replaced with a new access token
     - make sure events are still returned even when token has expired
    """
    http_mocker = HttpRequestsMocker(1)
    mocker.patch.object(client, "_http_request", side_effect=http_mocker.expired_token_http_request_side_effect)
    mocker.patch.object(demisto, "getIntegrationContext", return_value={"access_token": "old_access_token"})
    set_integration_context_mocker: MagicMock = mocker.patch.object(demisto, "setIntegrationContext")

    result = client.http_request(method="GET", url_suffix="/api/v2/reports", params={"start-date": "2021-01-10T00:00:00"})
    events = result["reports"]
    assert len(events) == 1
    assert set_integration_context_mocker.call_args[0][0] == {"access_token": "new_access_token"}


def test_the_test_module(mocker):
    """
    Given:
     - valid credentials

    When:
     - running the test-module

    Then:
     - make sure "ok" is returned
    """
    import CybelAngelEventCollector

    return_results_mocker: MagicMock = mocker.patch.object(CybelAngelEventCollector, "return_results")
    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )
    mocker.patch.object(demisto, "command", return_value="test-module")

    http_mocker = HttpRequestsMocker(100)

    mocker.patch.object(CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.valid_http_request_side_effect)

    CybelAngelEventCollector.main()
    assert return_results_mocker.called
    assert return_results_mocker.call_args[0][0] == "ok"


def test_fetch_events_no_last_run(mocker):
    """
    Given:
     - no last run (first time of the fetch)

    When:
     - running the fetch-events

    Then:
     - make sure events are sent into xsiam
     - make sure all the 100 events are fetched
     - make sure last run is updated
    """
    import CybelAngelEventCollector

    send_events_mocker: MagicMock = mocker.patch.object(CybelAngelEventCollector, "send_events_to_xsiam")
    set_last_run_mocker: MagicMock = mocker.patch.object(demisto, "setLastRun", return_value={})
    mocker.patch.object(demisto, "getLastRun", return_value={})
    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )

    mocker.patch.object(demisto, "command", return_value="fetch-events")

    http_mocker = HttpRequestsMocker(100)

    mocker.patch.object(CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.valid_http_request_side_effect)

    CybelAngelEventCollector.main()
    assert send_events_mocker.called
    fetched_events = send_events_mocker.call_args[0][0]
    assert len(fetched_events) == 100

    assert set_last_run_mocker.called
    last_run = set_last_run_mocker.call_args[0][0]
    assert last_run[CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME] == fetched_events[-1]["_time"]
    assert last_run[CybelAngelEventCollector.LastRun.LATEST_FETCHED_REPORTS_IDS][0] == fetched_events[-1]["id"]


def test_fetch_events_token_expired(mocker):
    """
    Given:
     - token that has expired

    When:
     - running the fetch-events

    Then:
     - make sure events are sent into xsiam
     - make sure all the 100 events are fetched
     - make sure last run is updated
     - make sure the new access token is getting into the integration context
    """
    import CybelAngelEventCollector

    send_events_mocker: MagicMock = mocker.patch.object(CybelAngelEventCollector, "send_events_to_xsiam")
    set_last_run_mocker: MagicMock = mocker.patch.object(demisto, "setLastRun", return_value={})
    mocker.patch.object(demisto, "getLastRun", return_value={})
    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )
    mocker.patch.object(demisto, "command", return_value="fetch-events")
    mocker.patch.object(demisto, "getIntegrationContext", return_value={"access_token": "old_access_token"})
    set_integration_context_mocker: MagicMock = mocker.patch.object(demisto, "setIntegrationContext")

    http_mocker = HttpRequestsMocker(100)

    mocker.patch.object(
        CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.expired_token_http_request_side_effect
    )

    CybelAngelEventCollector.main()
    assert send_events_mocker.called
    fetched_events = send_events_mocker.call_args[0][0]
    assert len(fetched_events) == 100

    assert set_last_run_mocker.called
    last_run = set_last_run_mocker.call_args[0][0]
    assert last_run[CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME] == fetched_events[-1]["_time"]
    assert last_run[CybelAngelEventCollector.LastRun.LATEST_FETCHED_REPORTS_IDS][0] == fetched_events[-1]["id"]

    assert set_integration_context_mocker.call_args[0][0] == {"access_token": "new_access_token"}


def test_fetch_events_with_last_run(mocker):
    """
    Given:
     - last run of fetched events IDs [1, 2]

    When:
     - running the fetch-events

    Then:
     - make sure events are sent into xsiam
     - make sure all the 98 events are fetched, the rest were not fetched because they were fetched in previous fetch
     - make sure last run is updated
    """
    import CybelAngelEventCollector

    send_events_mocker: MagicMock = mocker.patch.object(CybelAngelEventCollector, "send_events_to_xsiam")
    set_last_run_mocker: MagicMock = mocker.patch.object(demisto, "setLastRun", return_value={})
    mocker.patch.object(
        demisto,
        "getLastRun",
        return_value={
            CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME: "2024-02-29T13:48:32",
            CybelAngelEventCollector.LastRun.LATEST_FETCHED_REPORTS_IDS: [1, 2],
        },
    )
    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )
    mocker.patch.object(demisto, "command", return_value="fetch-events")

    http_mocker = HttpRequestsMocker(100)

    mocker.patch.object(CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.valid_http_request_side_effect)

    CybelAngelEventCollector.main()
    assert send_events_mocker.called
    fetched_events = send_events_mocker.call_args[0][0]
    assert len(fetched_events) == 98

    assert set_last_run_mocker.called
    last_run = set_last_run_mocker.call_args[0][0]
    assert last_run[CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME] == fetched_events[-1]["_time"]
    assert last_run[CybelAngelEventCollector.LastRun.LATEST_FETCHED_REPORTS_IDS][0] == fetched_events[-1]["id"]


def test_fetch_events_with_last_run_no_events(mocker):
    """
    Given:
     - last run of fetched events IDs [1, 2]
     - last run time from previous fetch
     - no new events have been received from the api

    When:
     - running the fetch-events

    Then:
     - make sure no events are sent into xsiam
     - make sure last run is kept the same as previous fetch
    """
    import CybelAngelEventCollector

    send_events_mocker: MagicMock = mocker.patch.object(CybelAngelEventCollector, "send_events_to_xsiam")
    set_last_run_mocker: MagicMock = mocker.patch.object(demisto, "setLastRun", return_value={})
    last_run = {
        CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME: "2024-02-29T13:48:32",
        CybelAngelEventCollector.LastRun.LATEST_FETCHED_REPORTS_IDS: [1, 2],
    }
    mocker.patch.object(demisto, "getLastRun", return_value=last_run)
    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )
    mocker.patch.object(demisto, "command", return_value="fetch-events")

    http_mocker = HttpRequestsMocker(0)

    mocker.patch.object(CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.valid_http_request_side_effect)

    CybelAngelEventCollector.main()
    assert send_events_mocker.called
    fetched_events = send_events_mocker.call_args[0][0]
    assert len(fetched_events) == 0

    assert set_last_run_mocker.called
    actual_last_run = set_last_run_mocker.call_args[0][0]
    assert actual_last_run == last_run


def test_fetch_events_without_last_run_no_events(mocker):
    """
    Given:
     - no last run
     - no new events have been received from the api

    When:
     - running the fetch-events

    Then:
     - make sure no events are sent into xsiam
     - make sure last run is returned with the last run updated
    """
    import CybelAngelEventCollector

    send_events_mocker: MagicMock = mocker.patch.object(CybelAngelEventCollector, "send_events_to_xsiam")
    set_last_run_mocker: MagicMock = mocker.patch.object(demisto, "setLastRun", return_value={})

    mocker.patch.object(demisto, "getLastRun", return_value={})
    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )
    mocker.patch.object(demisto, "command", return_value="fetch-events")

    http_mocker = HttpRequestsMocker(0)

    mocker.patch.object(CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.valid_http_request_side_effect)

    CybelAngelEventCollector.main()
    assert send_events_mocker.called
    fetched_events = send_events_mocker.call_args[0][0]
    assert len(fetched_events) == 0

    assert set_last_run_mocker.called
    actual_last_run = set_last_run_mocker.call_args[0][0]
    assert actual_last_run[CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME]


def test_fetch_events_with_last_run_dedup_event(mocker):
    """
    Given:
     - last run with event that was already fetched
     - no new events have been received from the api

    When:
     - running the fetch-events

    Then:
     - make sure no events are sent into xsiam
     - make sure last run does not get updated
    """
    import CybelAngelEventCollector

    send_events_mocker: MagicMock = mocker.patch.object(CybelAngelEventCollector, "send_events_to_xsiam")
    set_last_run_mocker: MagicMock = mocker.patch.object(demisto, "setLastRun")

    mocker.patch.object(
        demisto,
        "getLastRun",
        return_value={
            CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME: "2021-02-01T00:00:00",
            CybelAngelEventCollector.LastRun.LATEST_FETCHED_REPORTS_IDS: 1,
        },
    )

    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )
    mocker.patch.object(demisto, "command", return_value="fetch-events")

    http_mocker = HttpRequestsMocker(0)

    mocker.patch.object(CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.valid_http_request_side_effect)

    CybelAngelEventCollector.main()
    assert send_events_mocker.called
    fetched_events = send_events_mocker.call_args[0][0]
    assert len(fetched_events) == 0

    assert set_last_run_mocker.called
    actual_last_run = set_last_run_mocker.call_args[0][0]
    assert actual_last_run == {
        CybelAngelEventCollector.LastRun.LATEST_REPORT_TIME: "2021-02-01T00:00:00",
        CybelAngelEventCollector.LastRun.LATEST_FETCHED_REPORTS_IDS: 1,
    }


def test_get_events_command_command(mocker):
    """
    Given:
     - start date

    When:
     - running the fetch-events

    Then:
     - make sure the command returns all the fetched events
    """
    import CybelAngelEventCollector

    mocker.patch.object(demisto, "getLastRun", return_value={})
    return_results_mocker = mocker.patch.object(CybelAngelEventCollector, "return_results")
    mocker.patch.object(
        demisto,
        "params",
        return_value={
            "url": TEST_URL,
            "credentials": {
                "identifier": "1234",
                "password": "1234",
            },
            "max_fetch": 100,
        },
    )
    mocker.patch.object(
        demisto,
        "args",
        return_value={
            "start_date": "2024-02-29T13:48:32",
        },
    )
    mocker.patch.object(demisto, "command", return_value="cybelangel-get-events")

    http_mocker = HttpRequestsMocker(100)

    mocker.patch.object(CybelAngelEventCollector.Client, "_http_request", side_effect=http_mocker.valid_http_request_side_effect)

    CybelAngelEventCollector.main()
    fetched_events = return_results_mocker.call_args[0][0]
    assert len(fetched_events.outputs) == 100


def mock_client():
    """
    Create a mock client for testing.
    """
    from CybelAngelEventCollector import Client

    return Client(
        TEST_URL,
        client_id="1234",
        client_secret="1234",
        verify=False,
        proxy=False,
    )


def test_cybelangel_report_list_command(mocker):
    """
    Given:
     - A start date and an end date.

    When:
     - Retrieving a list of reports within the specified date range.

    Then:
     - Ensure the command returns a valid list of reports.
     - Validate that the outputs are correctly formatted.
    """
    from CybelAngelEventCollector import cybelangel_report_list_command

    client = mock_client()
    mocker.patch.object(
        client,
        "_http_request",
        return_results=load_test_data("report_list"),
    )
    args = {"start_date": "2024-01-01", "end_date": "2024-02-01"}

    result = cybelangel_report_list_command(client, args)

    assert isinstance(result, CommandResults)
    assert result.outputs_prefix == "CybelAngel.Report"
    assert result.outputs is not None
    assert "Reports list" in result.readable_output


def test_cybelangel_report_get_command(mocker):
    """
    Given:
     - A specific report ID.

    When:
     - Retrieving the details of the report.

    Then:
     - Ensure the command returns the correct report details.
     - Validate that the readable output includes the report ID.
    """
    from CybelAngelEventCollector import cybelangel_report_get_command

    client = mock_client()
    mocker.patch.object(
        client,
        "_http_request",
        return_results=load_test_data("report_list").get("reports")[0],
    )
    args = {"report_id": "test"}

    result = cybelangel_report_get_command(client, args)

    assert isinstance(result, CommandResults)
    assert result.outputs_prefix == "CybelAngel.Report"
    assert result.outputs is not None
    assert "Report ID" in result.readable_output


def test_cybelangel_report_get_command_to_pdf(mocker):
    """
    Given:
     - A report ID and the 'pdf' flag set to true.

    When:
     - Requesting to export the report as a PDF.

    Then:
     - Ensure the command returns a valid file result in PDF format.
    """
    from CybelAngelEventCollector import cybelangel_report_get_command

    client = mock_client()
    mocker.patch.object(
        client,
        "_http_request",
        return_results=load_test_data("report_list").get("reports")[0],
    )
    # test get report to pdf
    args = {"report_id": "test", "pdf": "true"}
    mocker.patch(
        "CybelAngelEventCollector.fileResult",
        return_value={
            "Contents": "",
            "ContentsFormat": "text",
            "Type": 9,
            "File": "cybelangel_report_<report_id>.pdf",
            "FileID": "<report_id>",
        },
    )
    result = cybelangel_report_get_command(client, args)
    assert isinstance(result, dict)


def test_cybelangel_mirror_report_get_command(mocker):
    """
    Given:
     - A report ID with the 'csv' flag set to false.

    When:
     - Fetching mirror report details.

    Then:
     - Ensure the command returns a CommandResults object with the expected report data.
    """
    from CybelAngelEventCollector import cybelangel_mirror_report_get_command

    client = mock_client()
    mocker.patch.object(
        client,
        "_http_request",
        return_results=load_test_data("mirror-report"),
    )
    args = {"csv": "false", "report_id": "test"}

    result = cybelangel_mirror_report_get_command(client, args)

    assert isinstance(result, CommandResults)
    assert result.outputs_prefix == "CybelAngel.ReportMirror"
    assert result.outputs is not None
    assert "Mirror details for Report ID" in result.readable_output


def test_cybelangel_mirror_report_get_command_to_csv(mocker):
    """
    Given:
     - A report ID with the 'csv' flag set to true.

    When:
     - Requesting to export the mirror report as a CSV file.

    Then:
     - Ensure the command returns a valid file result in CSV format.
    """
    from CybelAngelEventCollector import cybelangel_mirror_report_get_command

    client = mock_client()
    mocker.patch.object(
        client,
        "_http_request",
        return_results=load_test_data("mirror-report"),
    )
    args = {"report_id": "test", "csv": "true"}
    mocker.patch(
        "CybelAngelEventCollector.fileResult",
        return_value={
            "Contents": "",
            "ContentsFormat": "text",
            "Type": 9,
            "File": "cybelangel_mirror_report_<report_id>.csv",
            "FileID": "<report_id>",
        },
    )
    result = cybelangel_mirror_report_get_command(client, args)
    assert isinstance(result, dict)


def test_cybelangel_report_comment_create_command(mocker):
    """
    Given:
     - A discussion ID, comment content, and additional metadata.

    When:
     - Creating a new comment for the report.

    Then:
     - Ensure the command successfully adds the comment and returns the expected output.
    """
    from CybelAngelEventCollector import cybelangel_report_comment_create_command, Client

    client = mock_client()
    report_id = "11223344"

    mocker.patch.object(
        Client,
        "get_report_comment",
        return_value=load_test_data("create_comment_result"),
    )

    args = {"discussion_id": f"{report_id}:tenant id", "content": "Test func", "parent_id": "55667788", "assigned": "true"}
    response = cybelangel_report_comment_create_command(client, args)

    assert f"Comment created successfully for report ID: {report_id}" in response.readable_output


def test_cybelangel_report_comment_create_command_invalid(mocker):
    """
    Given:
     - An invalid discussion ID that does not follow the 'report_id:tenant_id' format.

    When:
     - Attempting to create a comment with the invalid discussion ID.

    Then:
     - Ensure the command raises a ValueError with the correct error message.
    """
    from CybelAngelEventCollector import cybelangel_report_comment_create_command

    client = mock_client()
    report_id = "11223344"

    # Case: Invalid discussion_id format (no colon)
    args_invalid = {"discussion_id": report_id, "content": "Test func"}
    with pytest.raises(ValueError, match="Invalid discussion_id format. Expected format: 'report_id:tenant_id'."):
        cybelangel_report_comment_create_command(client, args_invalid)


def test_cybelangel_archive_report_by_id_get_command(mocker):
    """
    Given:
     - A report ID to retrieve the archived version of the report.

    When:
     - Requesting the archived report in ZIP format.

    Then:
     - Ensure the command returns a file result containing the ZIP archive.
     - Validate that the returned file name follows the expected format.
    """
    from CybelAngelEventCollector import cybelangel_archive_report_by_id_get_command

    client = mock_client()
    mocker.patch.object(
        client,
        "_http_request",
        return_results=load_test_data("mirror-report"),
    )
    args = {"report_id": "test"}
    mocker.patch(
        "CybelAngelEventCollector.fileResult",
        return_value={
            "Contents": "",
            "ContentsFormat": "text",
            "Type": 9,
            "File": "cybelangel_archive_report_<report_id>.zip",
            "FileID": "<report_id>",
        },
    )
    result = cybelangel_archive_report_by_id_get_command(client, args)
    assert isinstance(result, dict)


def test_cybelangel_report_comments_get_command(mocker):
    """
    Given:
     - A report ID for which comments need to be retrieved.
     - A response containing existing comments for the report.

    When:
     - Running the `cybelangel_report_comments_get_command`.

    Then:
     - Ensure the command successfully retrieves comments for the given report.
     - Validate that the `discussion_id` starts with the report ID.
     - Validate that the `discussion_id` ends with 'Tenant id'.
    """
    from CybelAngelEventCollector import cybelangel_report_comments_get_command, Client

    client = mock_client()
    # case No previous comments exist in this report
    mocker.patch.object(
        Client,
        "get_report_comment",
        return_value=load_test_data("get_comments_res"),
    )
    report_id = "11223344"
    args = {"report_id": report_id}
    response = cybelangel_report_comments_get_command(client, args)
    assert response.outputs.get("Comment")[0].get("discussion_id").startswith(report_id)  # type: ignore
    assert response.outputs.get("Comment")[0].get("discussion_id").endswith("Tenant id")  # type: ignore


def test_cybelangel_report_attachment_get_command(mocker):
    """
    Given:
     - report ID and attachment ID

    When:
     - running the cybelangel_report_attachment_get_command with the given arguments

    Then:
     - ensure the function returns a dictionary containing the expected file details
        and the text of the attachment starts with "sep=" for CSV file.
    """
    from CybelAngelEventCollector import cybelangel_report_attachment_get_command, Client

    client = mock_client()
    response = mocker.patch.object(
        Client,
        "get_report_attachment",
        return_value=type(
            "StringWrapper", (object,), {"text": "sep=,\nkeyword,email,password\nTest1,Test2,Test3\nTest1,Test2"}
        )(),
    )
    report_id = "11223344"
    attachment_id = "55667788"
    args = {"report_id": report_id}
    mocker.patch(
        "CybelAngelEventCollector.fileResult",
        return_value={
            "Contents": "",
            "ContentsFormat": "text",
            "Type": 9,
            "File": f"cybelangel_report_{report_id}_attachment_{attachment_id}.csv",
            "FileID": "<report_id>",
        },
    )
    result = cybelangel_report_attachment_get_command(client, args)
    assert isinstance(result, dict)
    assert response.text.startswith("sep=")
