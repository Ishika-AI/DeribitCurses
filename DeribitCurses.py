#!/usr/bin/env python

from time import sleep
from deribit_api import RestClient
import asyncio
# import ws
import threading
import curses
from curses.textpad import Textbox
from sys import argv
from settings import login, inputs, buySell, sub, auth, msg, accountSum
from wsdata import *
import wsdata
# from viInput import inputcheck
import requests
import json
import redis
from rejson import Client, Path
import wsclient


activeInst = argv[1]
if(activeInst not in login['instrument']):
    sys.stderr.write(f'Err accepted instruments : {login["instrument"]}\n')
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

def sendWs(msg):
    b = threading.Thread(target=asyncio.run, args=[wsclient.hello(msg)])
    b.start()
    b.join

def run():
    


    try:
        subadub = sub(activeInst)
        sendWs(subadub)
        
        
    except requests.exceptions.ReadTimeout: 
        print('wsLogin Failed')
        pass


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
        # pos = client.positions()
        oldTrades = []
        y = 0
        tpos = 0
        trcounter = []
        trid = 10
        # account = client.account()
        rj = Client(host='localhost', port=6379, decode_responses=True)

        def timedinput(stdscr):

            inputwin = stdscr.derwin(height, width, 10, begin_x)

            tbox = Textbox(inputwin)
            
            tbox.edit()
            k = tbox.gather()
            wsdata.inputstr = k.rstrip()
            inputwin.erase()
            

            inputcheck(wsdata.inputstr, activeInst, client) 

            return


        for i in range(0, curses.COLORS):

            curses.init_pair(i + 1, i, -1)

        while(running):
            
            if(i >= 1000):
                pos = None
                sendWs(msg('get_open_orders_by_instrument', {"instrument_name" : activeInst}, f"op-{trid}"))
                trid += 1
                sendWs(msg('get_position', {"instrument_name" : activeInst}, f"po-{trid}"))
                trid += 1
                sendWs(msg("get_account_summary", {"currency":"BTC"}, f"acc-{trid}"))
                trid += 1


                i = 0
            i += 1
            screensize = stdscr.getmaxyx()
            if(oldScreenSize != screensize):  
                stdscr.erase()
            key = stdscr.getch()
            poswinWidth = screensize[1] - screensize[1] // 4
            tradewinWidth = screensize[1] - screensize[1] // 4 - 40
            priswin = stdscr.derwin(height, width, begin_y, begin_x)
            
            ordwin = stdscr.derwin(screensize[0], screensize[1] // 4, 0, screensize[1] - screensize[1] // 4)
            tradewin = stdscr.derwin(screensize[0] - 10, tradewinWidth, 0, 40)
            posWin = stdscr.derwin(10,  poswinWidth, screensize[0] - 10, 0)
            posWin.box()
            
            hh = 1
            y = 0
            # wsAlive = t.isAlive()           

            #set ordeprice and contracts
            ticksaway = uInput(key, inputs['closerToMarket'], ticksaway, -1)
            ticksaway = uInput(key, inputs['furtherFromMarket'], ticksaway, 1)
            quantity = uInput(key, inputs['lessCorntracts'], quantity, -1)  
            quantity = uInput(key, inputs['moreCorntracts'], quantity, 1)  

            # if(key == ord(inputs['vimMode'])):
            #     t2 = threading.Thread(target=timedinput, args=[stdscr])
            #     t2.start()


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
                bb = rj.jsonget('obj', Path('.ticker[-1]["data"]["best_bid_price"]'))
                sendWs(buySell('market', bb - ticksaway, 'buy'))               
            if(key == ord(inputs['sell'])):
                ba = rj.jsonget('obj', Path('.ticker[+1]["data"]["best_ask_price"]'))
                sendWs(buySell('market', ba - ticksaway, 'sell'))               
                
            try:
                ordwin.erase()
                ordwin.box()
                ordwin.addstr(1, 2, 'orders')
                ords = rj.jsonget('obj', Path('.orders'))

                for it in ords['result']:
                    hh += 1
                    ordwin.addstr(0 + hh, 2,str(' {direction} : {amount} : {price}'.format(**it)))
            except:
                ordwin.erase()
                ordwin.box()
                ordwin.addstr(2, 10, str(threading.active_count()))

            try:
                priswin.erase()
                priswin.box()
                # priswin.addstr(1 , 1, activeInst)
                # priswin.addstr(1 , 20, str(threading.active_count()))
                # priswin.addstr(6 ,10 , str(wsdata.inputstr))
                priswin.addstr(4 ,1,str(rj.jsonget('obj', Path('.ticker[-1]["data"]["last_price"]'))), curses.color_pair(3))



            except:
                priswin.addstr(1 , 20, 'Nih')
            
            
            posWin.addstr(1, 2, 'positions')
            try:
                acc = rj.jsonget('obj', Path('.acc'))
                posWin.addstr(1 , poswinWidth // 2 ,"eq: {equity} af: {available_funds}".format(**acc['result']))

            except:
                posWin.addstr(1, poswinWidth // 2, 'Ohnononono')


            try:
                pos = rj.jsonget('obj', Path('.pos')) 
                # for po in pos:
                y += 1 
                # posWin.addstr(2 + y, 2, "{instrument} : {direction} : {size} : ".format(**po))
                if(pos['result']['total_profit_loss'] > 0):
                    posWin.addstr(2 + y, 10, "{size}".format(**pos['result']))
                    posWin.addstr(2 + y, 30, "{total_profit_loss}".format(**pos['result']), curses.color_pair(3)) 
                else:
                    posWin.addstr(2 + y, 30, "{total_profit_loss}".format(**pos['result']), curses.color_pair(2))
            except:
                posWin.addstr(2, 2, 'No open positions')
            
            try:

                tradewin.erase()
                tradewin.box()
                tr = rj.jsonget('obj', Path('.trades'))
                for trade in tr[::-1]:
                    tradewin.addstr(1 + tpos , 2, "{trade_id}:{amount} : {price} : {direction} {tick_direction}".format(**trade))
                    tpos += 1
                    if(tpos > screensize[0] -13):
                        break
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

