from flask import Flask, render_template
from server.modules import odl_api
app = Flask(__name__)


@app.route("/")
@app.route("/topo")
def topology():
    try:
        list_switch, list_host = odl_api.get_topo()
        return render_template('topology.html', list_switch=list_switch, list_host=list_host)
    except Exception as e:
        return render_template('topology.html', error=str(e), list_switch=[], list_host=[])

@app.route("/config")
def config():
    return render_template('config.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
