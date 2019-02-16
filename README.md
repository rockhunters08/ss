<!-- TITLE/ -->
<h1>Simple Server</h1>
<!-- /TITLE -->

Description
------------
Simple Server runs a basic python HTTP server for a root HTML file using Python's BaseHTTPServer.

Installation
------------
To install from pip:

    pip install datadog
    
Core server being used here

    https://docs.python.org/2/library/basehttpserver.html

## Using
Command line usage:
NOTE: Make sure you set these environment variables correctly or else you will not receive any metrics when the server runs.
``` bash
export DATADOG_API_KEY=XXXXXXXX
export DATADOG_APP_KEY=YYYYYYYY
python ./ss.py
```
Then on any browser go to:

http://localhost:8080

## Testing
This is pre-production code, execute test.bash in order to test and do NOT go live until no monitors are triggered!
``` bash
./test.bash
```
Then review the dashboard here and make sure there are no error events:

https://app.datadoghq.com/dashboard/ehd-5e5-muy/simpleserver-status-dashboard
