import datetime
import pandas
import numpy
from scipy.optimize import minimize

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

COINS = [
    'bitcoin',
    'ethereum',
    'tether',
    'binancecoin',
    'cardano',
    'ripple',
    'dogecoin',
    'vechain',
    'matic-network',
    'ethereum-classic',
    'litecoin',
    'theta-token',
    'bitcoin-cash',
    'bitcoin-cash-sv',
    'stellar',
    'terra-luna',
    'okb',
    'chainlink',
    'tron',
    'ftx-token',
    'monero',
    'neo',
    'cosmos',
    'maker',
    'tezos'
]

def load_data(crypto_list):
    """
    Download data from CoinGecko API
    The data is in the form {coin: [[timestamp, value], ...], ...}
    """
    results = {}
    for c in crypto_list:
        vs = 'usd'
        this_morning = datetime.datetime.now().replace(hour=0,
            minute=0,second=0,microsecond=0).timestamp()
        long_ago = this_morning - 730*24*60*60
        price_data = cg.get_coin_market_chart_range_by_id(id=c, vs_currency=vs,
            from_timestamp = long_ago, to_timestamp = this_morning)['prices']
        results[c] = price_data
        
    return(results)
    
def transform_to_timestamp(data):
    """
    Transform data in the form {coin: [[timestamp, value], ...], ...}
    to {timestamp: {'coin1': coin1_value, ...}, ...}
    """
    timestamp_data = {}
    for c in data:
        for v in data[c]:
            timestamp, value = v
            if timestamp in timestamp_data:
                timestamp_data[timestamp][c] = value
            else:
                timestamp_data[timestamp] = {c: value}
    return(timestamp_data)
    
def transform_to_dataframe(data):
    """
    data is a dictionary: {timestamp: {'coin1': coin1_value, ...}, ...}
    """
    new_data = {}
    for d in data:
        date = datetime.datetime.fromtimestamp(d/1000).date()
        new_data[date] = data[d]
    df = pandas.DataFrame.from_dict(new_data, orient='index')
    return(df)
    
def clean_dataframe(df):
    """
    Remove null values
    """
    df = df.fillna(method="pad")
    df = df.dropna(axis=0)
    return(df)
    
def calculate_returns(df):
    """
    Return a dataframe of the daily log-returns for each coin
    """
    returns = pandas.DataFrame()
    for i in range(len(df) - 1):
        dfi = df.iloc[i]
        dfi_next = df.iloc[i + 1]
        date = df.index[i]
        a = numpy.log(dfi_next/dfi)
        a['Date']=date
        d = pandas.DataFrame(a).T
        returns = returns.append(d)
	
    returns = returns.set_index('Date')
    returns = returns.astype(float)
    
    return(returns)

    
def portfolio_risk(weights, cov):
    """
    weights is a numpy array of portfolio weights
    cov is the covariance matrix for the portfolio
    """
    return(numpy.dot(numpy.dot(weights, cov), weights.T))


def portfolio_return(weights, returns):
    """
    weights is a numpy array of portfolio weights
    returns is a numpy array of expected returns
    """
    return(numpy.dot(returns, weights))


def value(weights, tolerance, cov, returns):
    """
    returns the value of a given portfolio
    tolerance is the risk tolerance
    """
    r = portfolio_risk(weights, cov)
    p = tolerance * portfolio_return(weights, returns)
    return(r - p)

def optimise_portfolio(tolerance, cov, returns):
    """
    Calculate the optimal portfolio
    """
    # Initial point is an equal weighted array
    x = numpy.ones(len(returns))
    x0 = x/sum(x)
    # As it's a weighting - must sum to 1 and be in (0, 1)^len(w)
    f = value
    res = minimize(lambda w: f(w, tolerance, cov, returns), x0 = x0,
        constraints = [{"type": "eq", "fun": lambda w: numpy.sum(w) - 1}], 
        bounds = [(0, 1) for i in range(len(returns))])
    # Return optimised value
    return(res.x)


def find_optimal_allocation(risk_tolerance):
    # Load data from CoinGecko API
    data = load_data(COINS)
    # Index data by timestamp
    t = transform_to_timestamp(data)
    # Convert the indices to date format and use a pandas DataFrame
    df = transform_to_dataframe(t)
    # Remove null values
    df = clean_dataframe(df)
    # Calculate a DataFrame of daily log-returns
    df = calculate_returns(df)
    # Calculate the expected return for each coin, and the covariance matrix
    expected_returns = df.mean()
    covariance_matrix = df.cov()
    # Calculate the optimal portfolio
    optimal_allocation = optimise_portfolio(risk_tolerance, covariance_matrix, expected_returns)
    results = []
    for i in range(len(COINS)):
        c = COINS[i]
        result = {'coin': c, 'allocation': optimal_allocation[i]}
        result['log_mean'] = str(expected_returns[c])
        result['mean'] = str(round((numpy.exp(expected_returns[c]) - 1) * 100, 3)) + '%'
        result['log_std'] = str(df.std()[c])
        result['std'] = str(round((numpy.exp(df.std()[c]) - 1) * 100, 2)) + '%'
        results.append(result)
    results.sort(key = lambda r: -r['allocation'])
    
    return_dict = {"allocation": results}
    
    # Return values for the optimal portfolio
    return_dict['optimal_log_return'] = portfolio_return(optimal_allocation, expected_returns)
    return_dict['optimal_log_risk'] = portfolio_risk(optimal_allocation, covariance_matrix)
    return_dict['optimal_return'] = str(round((numpy.exp(optimal_log_return) - 1) * 100, 3)) + '%'
    return_dict['optimal_risk'] = str(round((numpy.exp(optimal_log_risk) - 1) * 100, 2)) + '%'
    return(return_dict)
    
