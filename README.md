DeribitCurses


![image](https://raw.githubusercontent.com/nuggattiStar/DeribitCurses/master/img/Interface.png)



This is a keyboard driven interface for Deribit
It's still a bit rough around the edges and missing alot of functionality.
What's working at the moment is buying, selling and cancellation of all orders.

standard input is:
buy 					: a
sell					: s
move buySell away from index price 	: k
move buySell towards index price 	: j
cancel all orders 			: c

this can be can be changed in settings.py

Installation instructions

Depends on deribit_api and websockets

Can be installed with pipenv.

To start app 

Add api key and secret in settings_example.py and rename/copy with to settings.py

Run with DeribitCurses.py BTC-PERPETUAL

More instruments can be added in settings.py
