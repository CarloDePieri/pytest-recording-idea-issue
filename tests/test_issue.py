import requests
import vcr


@vcr.use_cassette('cassettes/test_issue/test_with_pytest_recording.yaml')
def test_with_pytest_recording():
    # 2 on this endpoint always return 200
    succ_resp = requests.get("https://reqres.in/api/users/2")
    assert succ_resp.status_code == 200
    # 23 on this endpoint always return 404
    fail_resp = requests.get("https://reqres.in/api/users/23")
    # This will raise an exception
    fail_resp.raise_for_status()
    # Won't get here
    assert fail_resp.status_code == 200
