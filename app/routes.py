from app import app
from flask import request, jsonify

ROUTE = '/mpt_api/v1.0/'

@app.route(ROUTE, methods=["GET"])
def mpt():
    """risk is a number representing the percentage risk"""
    print(request.args.get('risk'))
    risk = request.args.get('risk')
    if risk is None:
        return(404)
    if risk < 30:
        return('bitcoin')
    elif risk < 70:
        return('dogecoin')
    else:
        return('maxcoins')