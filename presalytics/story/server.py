import os
import logging
import time
import posixpath
import urllib.parse
import flask
import threading
import webbrowser
import requests
import presalytics.lib.util
import presalytics.lib.exceptions


logger = logging.getLogger(__name__)


app = flask.Flask(__name__)


@app.route('/story/<id>')
def story(id):
    template_name = str(id) + '.html'
    return flask.render_template(template_name)

@app.route('/img/<path:filename>/')
def static_img(filename=None):
    directory = os.path.join(app.static_folder, "img")
    return flask.send_from_directory(directory, filename)


@app.route('/js/<path:filename>/')
def static_js(filename=None):
    directory = os.path.join(app.static_folder, "js")
    return flask.send_from_directory(directory, filename)


@app.route('/css/<path:filename>/')
def static_css(filename=None):
    directory = os.path.join(app.static_folder, "css")
    return flask.send_from_directory(directory, filename)


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(app.static_folder, 'favicon.ico')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = flask.request.environ.get('werkzeug.server.shutdown')
    shutdown_func()
    return 'Server shutting down...'


class LocalServer(object):
    def __init__(self, 
                 host='127.0.0.1', 
                 debug=True, 
                 port=8082, 
                 root_path=None,
                 use_reloader=False,
                 **kwargs):
        self.host = host
        self.debug = debug
        self.port = port
        self.root_path = self.make_local_folders(files_path=root_path)
        self.static_dir = os.path.join(self.root_path, "static")
        self.use_reloader = use_reloader
        self.get_preloaders()

    def run(self):
        app.root_path = self.root_path
        app.static_folder = self.static_dir
        app.run(host=self.host, 
                debug=self.debug, 
                port=self.port, 
                use_reloader=self.use_reloader)
    
    def make_local_folders(self, files_path=None):
        if files_path is None:
            files_path = os.getcwd()
        if not os.path.exists(files_path):
            os.mkdir(files_path)
        root = os.path.join(files_path, "presalytics")
        if not os.path.exists(root):
            os.mkdir(root)
        templates_path = os.path.join(root, "templates")
        if not os.path.exists(templates_path):
            os.mkdir(templates_path)
        static_files_path = os.path.join(root, "static")
        if not os.path.exists(static_files_path):
            os.mkdir(static_files_path)
        css_path = os.path.join(static_files_path, "css")
        if not os.path.exists(css_path):
            os.mkdir(css_path)
        js_path = os.path.join(static_files_path, "js")
        if not os.path.exists(js_path):
            os.mkdir(js_path)
        theme_path = os.path.join(css_path, "theme")
        if not os.path.exists(theme_path):
            os.mkdir(theme_path)
        img_path = os.path.join(static_files_path, "img")
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        local_preloader_path = os.path.join(static_files_path, "preloaders")
        if not os.path.exists(local_preloader_path):
            os.mkdir(local_preloader_path)
        return root

    def get_preloaders(self):
        preloaders = [
            'bars.svg'
        ]
        host = presalytics.lib.util.get_site_host()
        local_preloader_path = os.path.join(self.static_dir, "preloaders")
        for img in preloaders:
            try:
                preloader_url = urllib.parse.urljoin(host, "/static/preloaders/" + img)
                response = requests.get(preloader_url)
                if response.status_code == 200:
                    filename = os.path.join(local_preloader_path, img)
                    open(filename, 'wb').write(response.content)
                else:
                    message = "Error downloading preloader " + img
                    raise presalytics.lib.exceptions.ApiError(message=message, status_code=response.status_code)
            except Exception as ex:
                message = "Could not download preloader {0} from {1}".format(img, host)
                logger.error(message)
                # logger.exception(ex) # non-critical error



    def get_static_files_dict(self):
        static_files_dict = {}
        root = self.root_path
        static = os.path.join(root, "static")
        for item in os.listdir(static):
            if os.path.isdir(item):
                key = os.path.basename(item)
                value = os.path.abspath(item)
                static_files_dict[key] = value
        static_files_dict['favicon.ico'] = os.path.join(static, "favicon.ico")
        return static_files_dict
                


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
