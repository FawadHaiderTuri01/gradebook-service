import urllib.error
import urllib.request

url = "http://localhost:8000/students/S1/"

try:
    response = urllib.request.urlopen(url)
    print("Status:", response.status)
except urllib.error.HTTPError as error:
    print("Status:", error.code)
    raise SystemExit(1)