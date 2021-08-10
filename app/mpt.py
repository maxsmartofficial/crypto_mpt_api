from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

def load_data(crypto_list):
    results = {}
    for c in crypto_list:
        vs = 'usd'
        this_morning = datetime.datetime.now().replace(hour=0,
            minute=0,second=0,microsecond=0).timestamp()
        long_ago = this_morning - 3000*24*60*60
        price_data = cg.get_coin_market_chart_range_by_id(id=c, vs_currency=vs,
            from_timestamp = long_ago, to_timestamp = this_morning)['prices']
        results[c] = price_data
        
    return(results)
    
