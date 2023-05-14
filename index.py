from flask import Flask, render_template_string
import requests
import threading
import time

app = Flask(__name__)

html = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Website Status</title>
  </head>
  <body>
    <h1>Website Status</h1>
    <p>Status code: {{ status_code }}</p>
    <p>Response time: {{ response_time }} seconds</p>
  </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html, status_code=app.config.get('status_code', 'N/A'), response_time=app.config.get('response_time', 'N/A'))

def send_requests():
    while True:
        try:
            response = requests.get('https://x59rl7-5000.csb.app/')
            status_code = response.status_code
            response_time = response.elapsed.total_seconds()
            print(status_code, response_time)
        except requests.exceptions.RequestException:
            status_code = 'Error'
            response_time = 'N/A'
        app.config['status_code'] = status_code
        app.config['response_time'] = response_time
        time.sleep(5)

if __name__ == '__main__':
    thread = threading.Thread(target=send_requests)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
