from app import app
from flask import request, jsonify
from .mpt import find_optimal_allocation

ROUTE = '/mpt_api/v1.0/'

@app.route(ROUTE, methods=["GET"])
def mpt():
    """tolerance is a number representing the percentage risk"""
    tolerance = request.args.get('tolerance')
    if tolerance is None:
        return(404)
    try:
        tolerance = float(tolerance)
    except:
        return(404)
    results = find_optimal_allocation(tolerance)
    return(jsonify(results))