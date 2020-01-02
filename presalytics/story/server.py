import os
import time
import flask
import threading
import webbrowser


app = flask.Flask(__name__)


@app.route('/story/<id>')
def story(id):
    template_name = str(id) + '.html'
    return flask.render_template(template_name)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = flask.request.environ.get('werkzeug.server.shutdown')
    shutdown_func()
    return 'Server shutting down...'


class LocalServer(object):
    def __init__(self, 
                 host='127.0.0.1', 
                 debug=True, 
                 port=8080, 
                 root_path=None,
                 use_reloader=False,
                 **kwargs):
        self.host = host
        self.debug = debug
        self.port = port
        self.root_path = root_path
        if self.root_path is None:
            self.root_path = os.getcwd()
        self.use_reloader = use_reloader

    def run(self):
        app.root_path = self.root_path
        app.run(host=self.host, debug=self.debug, port=self.port, use_reloader=self.use_reloader)


class Browser(threading.Thread):
    def __init__(self, address, delay_time=2, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)
        self.address = address
        self.delay_time = delay_time

    def run(self):
        time.sleep(self.delay_time)
        webbrowser.open_new_tab(self.address)


if __name__ == '__main__':
    app.run(debug=True)
