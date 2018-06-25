import simplejson as json
from sys import argv
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from requests import put


HOST = 'localhost'
PORT = 5000

# Put your elasticsearch config here
ELASTIC_URL = ''
ELASTIC_PORT = None


class BulkHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # get message from POST
        self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode('UTF-8')
        self.send_response(200)
        self.end_headers()

        # read JSON data and transform conflicting fields
        bulk = []
        for line in self.data_string.splitlines():
            if line != '':
                data = json.loads(line)

                if data.get('timestamp'):
                    timestamp = datetime.strptime(data['timestamp'], "%d/%m/%YT%H:%M:%S")
                    data['timestamp'] = timestamp.strftime('%Y-%m-%dT%H:%M:%S')

                if data.get('message'):
                    data['message'] = float(data['message'])

                if data.get('index'):
                    if data['index'].get('_type'):
                        data['index']['_type'] = '_doc'

                bulk.append(json.dumps(data))

        elastic_data = '\n'.join(bulk)+'\n'

        headers = {'Content-type': 'application/x-ndjson'}
        try:
            response = put(ELASTIC_URL +':'+ str(ELASTIC_PORT) + '/_bulk',
                    data=elastic_data.encode('utf-8'), headers=headers)
            print(response.text)
        except ConnectionError as con_err:
            print("Something went wrong", con_err)

        return


def run(host=HOST, port=PORT, server_class=HTTPServer, handler_class=BulkHandler):
    httpd = server_class((host, port), handler_class)
    try:
        print("Starting httpd at", host, port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    if len(argv) > 2:
        run(host=argv[1], port=int(argv[2]))
    else:
        run()
