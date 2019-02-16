#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, environ
from datadog import initialize, api

PORT_NUMBER = 8080
API_KEY = environ.get('DATADOG_API_KEY')
APP_KEY = environ.get('DATADOG_APP_KEY')

class ssHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            # we only serve the root index.html
            if self.path=="/":
                self.path="/index.html"
                mimetype='text/html'
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                api.Metric.send(metric='simpleserver.page.views.success', points=1)
            else:
                # if this is not for the root document, send a fail event with a 404
                send_error(404,'File Not Found: %s' % self.path)
                api.Metric.send(metric='simpleserver.page.views.failure', points=1)
            return

        # on any exception, catch the error and send an error event to datadog
        except:
            self.send_error(404,'File Not Found: %s' % self.path)
            api.Metric.send(metric='simpleserver.page.views.error', points=1)

try:

    # some configs for talking to datadog
    initialize(api_key=API_KEY, app_key=APP_KEY)

    # launch our webserver listening on port 8080
    server = HTTPServer(('', PORT_NUMBER), ssHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
