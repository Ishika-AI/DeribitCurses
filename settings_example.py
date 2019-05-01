##################Settings unt setup #################
from deribit_api import RestClient


login = dict(
	Testnet = True,	##only change if you are feeling brave
	Key = "",
	Secret = "",
        instrument = ["BTC-PERPETUAL", "BTC-28JUN19", "ETH-PERPETUAL"]

)

inputs = dict(
        buy = 'b',
        sell = 's',
        closerToMarket = 'j',
        furtherFromMarket = 'k',
        cancelAll = 'c',
        moreCorntracts = 'l',
        lessCorntracts = 'h'
        # osv.....
)


if login['Testnet']:
    httpcnnct = "https://test.deribit.com"
    wscnt = 'wss://test.deribit.com/ws/api/v1/'
else:
    httpcnnct = "https://test.deribit.com"
    wscnt = 'wss://test.deribit.com/ws/api/v1/'


client = RestClient(login['Key'], login['Secret'], httpcnnct)

