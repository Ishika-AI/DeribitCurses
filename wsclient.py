import asyncio
import websockets
import json
from settings import auth, sub

# import rejson
# from rejson import Client, Path
import wsdata



async def single(msg):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        
        await websocket.send(json.dumps(auth))
        
        i = await websocket.recv()
        # print(i)
        m = json.loads(i)
        a = m['result']['access_token']
        o = json.loads(msg)
        o['params']["access_token"] = a
        await websocket.send(json.dumps(o))

        resp = await websocket.recv()
            
        m = json.loads(resp)
        
        if 'id' in m and type(m['id']) != int:
            reqid = m['id']
            # if('sub' in reqid):
                # print(m)
            if('acc' in reqid):
                wsdata.Data.account = m
                # print(wsdata.Data.account)
                # r.rj.jsonset('obj', Path('.acc'),  m)
                # print(m)
            if('op' in reqid):
                wsdata.Data.orders = m
                # print(wsdata.Data.orders)

                # r.rj.jsonset('obj', Path('.orders'),  m)
                # print(m)
            if('po' in reqid):
                wsdata.Data.positions = m



async def wsSub(msg):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        
        await websocket.send(json.dumps(auth))
        
        i = await websocket.recv()
        # print(i)
        m = json.loads(i)
        a = m['result']['access_token']
        o = json.loads(msg)
        o['params']["access_token"] = a
        await websocket.send(json.dumps(o))

        async for message in websocket:
            
            m = json.loads(message)
            if 'method' in m:
                lala = m['params']['channel']
                if('ticker' in lala):
                    if __name__ != '__main__':
                        wsdata.Data.ticker = m['params']['data']
                    # print(wsdata.Data.ticker)
                    # r.rj.jsonset('obj', Path('.ticker'), m['params'])
                if('trades' in lala):
                    for tr in m['params']['data']:
                        if __name__ == '__main__':
                            print('{amount: <6} {price: <5} {direction: <5} {tick_direction}'.format(**tr)) 
                        else:
                            wsdata.Data.trades.append(tr)
                        # print(wsdata.Data.trades)
                        # r.rj.jsonarrappend('obj', Path('.trades'), tr)
                # else:
                #     print(m)
            

                    
if __name__ == "__main__":

    subadub = json.dumps(sub('BTC-PERPETUAL'))
    asyncio.run(wsSub(subadub))

