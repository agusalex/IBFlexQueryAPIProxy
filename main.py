import os

from flask import Flask
from flask import jsonify, request
from ibflex import client, parser, FlexQueryResponse, Trade
from datetime import datetime


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


@app.route('/api/v1/ghostfolio-trades', methods=['GET'])
# For ghostfolio
def get_trades():
    ibkrtoken = request.headers['IBKR-TOKEN']
    ibkrquery = request.headers['IBKR-QUERY']
    response = client.download(ibkrtoken, ibkrquery)
    query: FlexQueryResponse = parser.parse(response)
    activities = []
    date_format = "%Y-%m-%d"
    for trade in query.FlexStatements[0].Trades:
        if trade.openCloseIndicator.CLOSE:
            date = datetime.strptime(str(trade.tradeDate), date_format)
            iso_format = date.isoformat()
            symbol = trade.symbol
            if ".USD-PAXOS" in trade.symbol:
                symbol = trade.symbol.replace(".USD-PAXOS", "") + "USD"

            activities.append({
                "currency": trade.currency,
                "dataSource": "YAHOO",
                "date": iso_format,
                "fee": float(0),
                "quantity": float(trade.quantity),
                "symbol": symbol,
                "type": trade.buySell,
                "unitPrice": float(trade.tradePrice)
            })
    activities = sorted(activities, key=lambda x: x["date"])
    return jsonify({"activities": activities})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
