
# from deribit_api import RestClient
# from rejson import Client, Path
import json
##################Settings##################


inputs = dict(
        buy = 'b',
        sell = 's',
        closerToMarket = 'j',
        furtherFromMarket = 'k',
        cancelAll = 'c',
        moreCorntracts = 'l',
        lessCorntracts = 'h',
        vimMode = 'o'
        # osv.....

)



def msg(msg ,param, transid): 
    output = {
    "jsonrpc" : "2.0",
    "id" : transid,
    "method" : f"private/{msg}",
    "params" : param
    }
    return output


def buySell(market, amount, price ,side): 
    order = {
      "jsonrpc" : "2.0",
      "id" : 5275,
      "method" : f"private/{side}",
      "params" : {
        "instrument_name" : "BTC-PERPETUAL",
        "amount" : amount,
        "type" : market,
        "price": price,
        "label" : "market0000234"
      }
    }
    return json.dumps(order)




auth = {
  
        "jsonrpc" : "2.0",
        "id" : 9929,
        "method" : "public/auth",
        "params" : {
            "grant_type" : "client_credentials",
            "client_id" : "A7fcDnN2rqkb",
            "client_secret" : "RVAIJ6Y3CQ6ZWONAB5X52OMXQWUALFTZ"}
    }

def sub(activeInst, *token):
    output = {
        "jsonrpc" : "2.0",
        "id" : "sub949",
        "method" : "private/subscribe",
        "params" : { "channels" : [f"ticker.{activeInst}.100ms",f"trades.{activeInst}.raw"], 
        "access_token": token}    
    }
    return output 

