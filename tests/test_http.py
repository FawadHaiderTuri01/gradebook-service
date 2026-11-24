import threading
from http.server import HTTPServer
from urllib.request import urlopen

import pytest

import gradebook


@pytest.fixture
def http_server(loaded):
    server = HTTPServer(("127.0.0.1", 0), gradebook.Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield f"http://127.0.0.1:{server.server_port}"

    server.shutdown()
    thread.join()
    server.server_close()


@pytest.mark.parametrize(
    "path",
    [
        "/students/S1",
        "/students/S1/",
        "/students/S1?format=json",
    ],
)
def test_get_student_urls_return_200(http_server, path):
    with urlopen(f"{http_server}{path}") as response:
        assert response.status == 200

def test_body_that_is_not_utf8_is_a_bad_request(http_server):
    import urllib.error
    from urllib.request import Request, urlopen

    request = Request(
        f"{http_server}/students",
        data=b"\x80\x81\x82",
        method="POST",
    )

    with pytest.raises(urllib.error.HTTPError) as error:
        urlopen(request)

    assert error.value.code == 400