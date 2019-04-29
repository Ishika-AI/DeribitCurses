import websockets
import json
import asyncio
from settings import login 
import wsdata
from wsdata import trades, priceinfo

# async def ping():
#     async with websockets.connect(url) as websocket:
#         data = {
#             "id": 5634, 
#             "action": "/api/v1/public/ping"}
#         # data['sig'] = client.generate_signature(data['action'], data['arguments'])

#         await websocket.send(json.dumps(data))

#         resp = await websocket.recv()
        
#         print(f'{resp}')
#         await asyncio.sleep(3)


async def connct(url, client, data):

    # settings.orders = client.getopenorders()
    print(client.account())
    async with websockets.connect(url) as websocket:
        data = data        
        data['sig'] = client.generate_signature(data['action'], data['arguments'])


        await websocket.send(json.dumps(data))
        
        greeting = await websocket.recv()
        # print(f"{greeting}")
        

        async for message in websocket:
                
            await printer(message)
            print(str(orders))   




async def connect(url, client, data):

    # orders = client.getopenorders()

    async with websockets.connect(url) as websocket:
        data = data        
        data['sig'] = client.generate_signature(data['action'], data['arguments'])


        await websocket.send(json.dumps(data))
        
        greeting = await websocket.recv()
        # print(f"{greeting}")
        

        async for message in websocket:
                
            await printer(message)
            # print(str(orders))   
     
async def printer(message):
    
    try:
        mge = json.loads(message)
        msg = mge.get('notifications')[0].get('message')
        if(msg == 'order_book_event'):
             
            priceinfo['bestBid'] = mge.get('notifications')[0].get('result').get('bids')[0].get('price')
            priceinfo['bestAsk'] = mge.get('notifications')[0].get('result').get('asks')[0].get('price')
            # print(str(BestBid))
        if (msg == 'user_orders_event'):
            ordmsg = mge.get('notifications')[0].get('result')
            
            for item in ordmsg:
                if(item['state'] == 'open'):
                    wsdata.orders.append(item)
                if(item['state'] == 'cancelled'):
                    for o in wsdata.orders:
                        # print('deleting')
                        if(item['orderId'] == o['orderId']):
                            wsdata.orders.remove(o)
        if (msg == 'trade_event'):
            
            for trade in mge.get('notifications')[0].get('result'):
                trades.append(trade)
            
            
            if len(lTrades) > 30:
                for i in reversed(range(0, len(lTrades) -10)):
                    trades.pop(i)
                    
        # await print(str(mge))
        # await asyncio.sleep(1)
    except:
       print ('') 
        






if __name__ == "__main__":
    import asyncio
    from deribit_api import RestClient
    import websockets
    import json
    with open("creds.json") as data_file:
        creds = json.load(data_file)
    url = 'wss://test.deribit.com/ws/api/v1/'
   
    instrument = "BTC-PERPETUAL"
    client = RestClient(creds['Key'], creds['Secret'], 'https://test.deribit.com')
    d = {
            "id": 5634, 
            "action": "/api/v1/private/subscribe",  
            "arguments": {"event": ["user_order", "order_book", "trade"],
                          "instrument": [instrument]}
        }
    # orders = client.getopenorders()
    asyncio.run(connct(url, client, d))
