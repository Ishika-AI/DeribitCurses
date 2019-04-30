#	DeribitCurses


![image](https://raw.githubusercontent.com/nuggattiStar/DeribitCurses/master/img/Interface.png)



###	A keyboard driven interface for Deribit.

It's still a bit rough around the edges and missing alot of functionality.
What's working at the moment is buying, selling and cancellation of all orders.

####	Standard input. 
* b : buy 
* s : sell
* k : move buySell away from index price 
* j : move buySell towards index price 
* c : cancel all orders 

Keys can be changed in settings.py

#### Installation instructions

NB! only works in linux as far as i know...

Depends on deribit_api, websockets and curses

Can be installed with pipenv.

#### Start app 

Add api key and secret in settings_example.py and rename/copy with to settings.py

Defaults to Testnet at test.deribit.com,

Run with DeribitCurses.py BTC-PERPETUAL

More instruments can be added in settings.py


#### TODO
  *  Fix websocket connection
  *  ordercancellation per order
  *  stops
  *  bulk orders maaybe
  *  set TIF on orders
