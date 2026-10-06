# Task 2 - Breaking the Gradebook Service

## (a) GET /students/NOPE

Command:
curl.exe -i localhost:8000/students/NOPE

Result:
HTTP/1.0 200 OK
{"error": "not found"}

The service returned HTTP 200 instead of an appropriate error status.

## (b) POST /students with body 5

Command:
curl.exe -i -X POST localhost:8000/students -H "Content-Type: application/json" -d "5"

Result:
curl: (52) Empty reply from server

Server error:
TypeError: argument of type 'int' is not iterable
gradebook.py line 89

## (c) Create S1 and A1, then POST a mark with score "abc"

Student S1 was created successfully.

Assessment A1 was created successfully.

Command:
curl.exe -i -X POST http://localhost:8000/marks -H "Content-Type: application/json" -d '{"student":"S1","assessment":"A1","score":"abc"}'

Result:
{"ok":"true"}

The invalid score "abc" was accepted.

Command:
curl.exe -i http://localhost:8000/students/S1

Result:
curl: (52) Empty reply from server

Server error:
ValueError: could not convert string to float: 'abc'
gradebook.py line 39

## (d) Delete gradebook.json, restart, create S1, create assessment with total 0, add mark, then GET /report

gradebook.json was deleted before restarting so the test started with an empty gradebook and did not use data left from previous tests.

S1 was created successfully.

An assessment A1 with total 0 was created successfully.

A mark with score 5 was accepted.

Command:
curl.exe -i http://localhost:8000/report

Result:
HTTP/1.0 200 OK
[{"id": "S1", "name": "Ayesha", "pct": "0"}]

The service returned a report even though the assessment total was 0.

## (e) Delete gradebook.json, restart, then POST a mark for a non-existing assessment

gradebook.json was deleted again before restarting.

Command:
curl.exe -i -X POST http://localhost:8000/marks -H "Content-Type: application/json" -d '{"student":"S1","assessment":"NOPE","score":50}'

Result:
HTTP/1.0 200 OK
{"error": "no such student"}

There was no error in the server terminal.

The service checked the student before checking whether the assessment existed.

## Why gradebook.json had to be deleted

gradebook.json stores the current gradebook data. It was deleted so each test started with a clean and empty state. This prevented students, assessments, and marks from earlier tests from affecting the results.

## Ruff check

Command:
ruff check .

Result:
Found 10 errors.

## Bare except statements

gradebook.py line 19 - load()
gradebook.py line 28 - save()
gradebook.py line 84 - do_POST()