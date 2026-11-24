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