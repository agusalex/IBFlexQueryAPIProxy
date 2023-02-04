from flask import Flask
from flask import jsonify, request
from ibflex import client, parser


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@app.route('/api/v1/flex-query', methods=['GET'])
def get_accountStatement():
    ibkrtoken = request.headers['IBKR-TOKEN']
    ibkrquery = request.headers['IBKR-QUERY']
    response = client.download(ibkrtoken, ibkrquery)
    return jsonify(parser.parse(response).__dict__)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
