# Crypto MPT API #
This is a pretty basic implementation of a [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory "MPT WikiPedia") algorithm which optimises a portfolio of cryptocurrencies.

The cryptocurrencies used are defined in `app/mpt.py`. The data is from [CoinGecko](https://www.coingecko.com/en/api/documentation "CoinGecko API Documentation").

To install this:
```
git clone https://github.com/maxsmartofficial/crypto_mpt_api.git
cd crypto_mpt_api
```
Install the requirements in a virtual environment:
```
python3 -m venv venv
pip install -r requirements.txt
```
Run some tests:
```
pytest
```
Set the `FLASK_APP` environment variable:
```
export FLASK_APP=main.py
```
Then run the API using the development server:
```
flask run
```
Now that's running, you can access the API like this:
```
curl http://127.0.0.1:5000/mpt_api/v1.0/?tolerance=1
```
And here are the results:
```Javascript
{
	optimal_log_return	0.006469921903312092, // expected daily log-return
	optimal_log_risk	0.07172936725376261, // expected daily log-risk
	optimal_return	"0.649%", // expected daily return (better formatting)
	optimal_risk	"7.44%", // expected daily risk
	tolerance	"Highly Aggressive", // Description of the risk profile
	allocation: [
		{
			"allocation":0.5048772909201732, // Proportion of the portfolio to be allocated
			"coin":"matic-network", // CoinGecko id of the cryptocurrency
			"log_mean":"0.006446367106269741",
			"log_std":"0.08794704677552131",
			"mean":"0.647%",
			"std":"9.19%"
		}, 
		...
	]
}
```