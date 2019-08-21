from flask import Flask, request, render_template, jsonify
import presalytics.client.auth


app = Flask(__name__)

@app.route('/auth', methods=['GET'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')

@app.route('/auth/code', methods=['POST'])
def code():    
    if request.method == 'POST':
        data = request.json
        presalytics.client.auth.put_data_in_queue(data)
        resp = jsonify(success=True)
        return resp

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    shutdown_func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug = True)
        
