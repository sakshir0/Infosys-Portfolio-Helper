# Infosys-Portfolio-Helper

## Inspiration ##
This is a proof-of-concept application built for Infosys. We wanted to create a digital platform that provided algorithm-driven, automated financial planning services.  

## What It Does ##
It is an application designed to help clients create and manage a stock portfolio using momentum as a metric. It creates a stock portfolio for clients with stocks containing the highest momentum scores that will automatically rebalance itself every six months. It limits turnover within the portfolio to reduce costs. It also allows clients to search for a stock ticker and see its price history and our calculated momentum score for that particular stock. 

## How It Works ##
We calculate a momentum score for each stock in the Russell 3000 index using a risk-adjusted momentum investing strategy created by a research paper by Research Affiliates. We calculate the return minus the risk-free rate and divide by the volatility. We find the z-scores of these momentum values, winsorize the data, and then give a stock a score based on this z-score. 

When rebalancing the portfolio, we use a fixed security buffer algorithm of fifty percent to limit turnover. We will first pick fifty percent of the portfolio using the top ranked stocks by momentum score. We will then pick any stock that was previously in our portfolio and is still in the top 150% of ranked stocks until we have the desired amount. We also make sure that no stock has too high a weight within the portfolio and will adjust the portfolio if this is the case. 

## Built With ##
- [Django](https://www.djangoproject.com/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [SQLite](https://www.sqlite.org/index.html)
