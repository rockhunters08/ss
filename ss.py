#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, environ
from datadog import initialize, api
import sys, getopt

PORT_NUMBER = 8080

def main(argv):

    # get datadog keys
    try:
        opts, args = getopt.getopt(argv,"hi:p:",["api=","app="])
    except getopt.GetoptError:
        print 'ss.py -i <api_key> -p <app_key>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--api"):
            api_key = arg
        elif opt in ("-p", "--app"):
            app_key = arg

    class ssHandler(BaseHTTPRequestHandler):

        def do_GET(self):

            try:
                # We only serve the root index.html
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
                    self.send_error(404,'File Not Found: %s' % self.path)
                    api.Metric.send(metric='simpleserver.page.views.failure', points=1)
                return

            # on any exception, catch the error and send an error event to datadog
            # THIS SHOULD NEVER HAPPEN, ALARMS WILL FLOW AND NEED TO DEBUG!!!!!
            except:
                print 'ERROR: this code should never be hit ... why are we here?'
                self.send_error(400,'Bad Request ... how did we get here?: %s' % self.path)
                api.Metric.send(metric='simpleserver.page.views.error', points=1)

    try:

        # some configs for talking to datadog
        initialize(api_key, app_key)

        # launch our webserver listening on port 8080
        server = HTTPServer(('', PORT_NUMBER), ssHandler)
        print 'Started httpserver on port ' , PORT_NUMBER
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()

if __name__ == "__main__":
    main(sys.argv[1:])
