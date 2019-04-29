from time import sleep
from deribit_api import RestClient
import asyncio
import json
import websockets, ws
import threading
import curses
import sys
from settings import *
from wsdata import *
import wsdata

if login['Testnet']:
    httpcnnct = "https://test.deribit.com"
    wscnt = 'wss://test.deribit.com/ws/api/v1/'
else:
    httpcnnct = "https://test.deribit.com"
    wscnt = 'wss://test.deribit.com/ws/api/v1/'



activeInst = sys.argv[1]
if(activeInst not in login['instrument']):
    sys.stderr.write(f'Err accepted instruments : {instrument}\n' )
    sys.exit(1)

def ikkenull(x, i):
    if(x is not None and x <= i ):
        x = i
    return x

def uInput(key, k, var, value):
    if(key == ord(k)):
        var += value
        return var 
    else:
        return var

def d(event, inst):
    return {
            "id": 5634, 
            "action": "/api/v1/private/subscribe" ,  
            "arguments": {"event": event,
                          "instrument": [inst]}
    }

client = RestClient(login['Key'],login['Secret'], httpcnnct)


def run():

    
    wsdata.orders = client.getopenorders(activeInst)
    
    t = threading.Thread(target=asyncio.run, args=(ws.connect(wscnt, client, d(["order_book", "user_order", "trade"], activeInst)), ))

    t.daemon = True
    t.start()
        
    def main(stdscr, running):
        
        stdscr.clear()
        curses.curs_set(0)
        begin_x = 0; begin_y = 0
        height = 8; width = 40
        curses.noecho()
        i = 0
        curses.start_color()
        curses.use_default_colors()
        stdscr.nodelay(1)
        ticksaway = 0
        quantity = 1
        oldScreenSize = None
        pos = client.positions()
        oldTrades = []
        y = 0
        tpos = 0
        trcounter = []
        account = client.account()
        


        for i in range(0, curses.COLORS):

            curses.init_pair(i + 1, i, -1)

        while(running):
            
            if(i >= 1000):
                pos = None
                pos = client.positions()
                account = client.account()
                i = 0
            i += 1
            screensize = stdscr.getmaxyx()
            if(oldScreenSize != screensize):  
                stdscr.erase()
            key = stdscr.getch()
            poswinWidth= screensize[1] - screensize[1] // 4
            tradewinWidth = screensize[1] - screensize[1] // 4 - 40
            priswin = stdscr.derwin(height, width, begin_y, begin_x)
            ordwin = stdscr.derwin(screensize[0], screensize[1] // 4, 0, screensize[1]- screensize[1] // 4)
            tradewin = stdscr.derwin(screensize[0] - 10, tradewinWidth, 0, 40)
            posWin = stdscr.derwin(10,  poswinWidth, screensize[0] - 10, 0)
        
            posWin.box()
            priswin.box()
            hh = 1
            y = 0
            wsAlive = t.isAlive()           
           

            #set orderice and contracts
            ticksaway = uInput(key, inputs['closerToMarket'], ticksaway, -1)
            ticksaway = uInput(key, inputs['furtherFromMarket'], ticksaway, 1)
            quantity = uInput(key, inputs['lessCorntracts'], quantity, -1)  
            quantity = uInput(key, inputs['moreCorntracts'], quantity, 1)  

            if(key == ord(inputs['cancelAll'])):
               client.cancelall('all') 
               ordwin.erase()
            
           
            if(ticksaway == 0):
                post = False
            else:
                post = True
            ticksaway = ikkenull(ticksaway, 0)
            quantity = ikkenull(quantity, 1)



            if(key == ord(inputs['buy'])):
                buy = client.buy(instrument=activeInst,quantity=quantity,price=priceinfo['bestBid'] - ticksaway ,postOnly=post)
            if(key == ord(inputs['sell'])):
                buy = client.sell(instrument=activeInst,quantity=quantity,price=priceinfo['bestAsk'] + ticksaway ,postOnly=post)
        
            try:
                ordwin.erase()
                ordwin.box()
                ordwin.addstr(1, 2, 'orders')
                for it in wsdata.orders:
                    hh += 1
                    ordwin.addstr(0 + hh, 2,str(hh) + ' {direction} : {amount} : {price}'.format(**it))
            except:
                ordwin.erase()
                ordwin.box()
                ordwin.addstr(2, 10, 'Nih!')

            try:
                priswin.addstr(1 , 1, activeInst)
                priswin.addstr(6 ,1 ,str(wsAlive))
                priswin.addstr(2 ,1 ,str(priceinfo['bestAsk']), curses.color_pair(2))
                priswin.addstr(4 ,1,str(priceinfo['bestBid']), curses.color_pair(3))
                


            except:
                print('nih!')
            
            
            posWin.addstr(1, 2, 'positions')
            try:
                # for a in account:
                # if(account['currency'] == activeInst[:3]):
                posWin.addstr(1 , poswinWidth // 2 ,"eq: {equity} af: {availableFunds}".format(**account))

            except:
                posWin.addstr(1, poswinWidth // 2, 'Ohnononono')


            try:
                for po in pos:
                    y += 1 
                    posWin.addstr(2 + y, 2, "{instrument} : {direction} : {size} : ".format(**po))
                    if(po['profitLoss'] > 0):
                        posWin.addstr(2 + y, 30, "{profitLoss}".format(**po), curses.color_pair(3)) 
                    else:
                        posWin.addstr(2 + y, 30, "{profitLoss}".format(**po), curses.color_pair(2))
            except:
                posWin.addstr(2, 2, 'No open positions')
            
            try:
                tradewin.erase()
                tradewin.box()
                for trade in trades:
                     
                    if(trade['tradeId'] not in trcounter):
                        trcounter.append(trade['tradeId'])
                        oldTrades.insert(0, trade)
                    while len(oldTrades) >= screensize[0] - 12:
                        oldTrades.pop()
                        oldTrades.pop()

                for tr in oldTrades:
                    tradewin.addstr(1 + tpos , 2, "{tradeId}:{amount} : {price} : {direction}".format(**tr))
                    tpos += 1
                tpos = 0
                    
            except:
                tradewin.erase()
                tradewin.box()
                tradewin.addstr(2, 2, 'Nono Trada')


            priswin.addstr(3 ,1 ,str(ticksaway) + ' : ' + str(quantity) + ' contracts')
            oldScreenSize = stdscr.getmaxyx()
            sleep(0.01)
            stdscr.refresh()
            if key == 120 :
                running = False

    running = True
    stdscr = curses.initscr()
    curses.wrapper(main(stdscr, running))
    
                    
    
run()

