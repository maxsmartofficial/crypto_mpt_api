from app import app, cache
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
    
    results = cache.get(str(tolerance))
    if results is None:
        print('Calculating:', tolerance)
        results = find_optimal_allocation(tolerance)
        cache.set(str(tolerance), results)
    else:
        print('Fetched from cache:', tolerance)
    return(jsonify(results))