import re
from settings import login, httpcnnct
from deribit_api import RestClient


client = RestClient(login['Key'], login['Secret'], httpcnnct)

def postCheck(cmd, str):
    if(cmd[:1] == str):
        return True
    else:
        return False




def order(cmd, ordprice, activeInst):
    if(cmd == 'ms' or cmd == 'ps'):
        post = postCheck(cmd, 'm')
        order = client.sell(instrument=activeInst,quantity=10 ,price=float(ordprice) ,postOnly=post)
    if(cmd == 'pb' or cmd == 'mb'):
        post =  postCheck(cmd, 'm')   
        order = client.buy(instrument=activeInst,quantity=10 ,price=float(ordprice) ,postOnly=post)




def inputcheck(inputstr, activeInst, client):
	
         
        cmd = ''.join(re.findall("^(mb|pb|ps|pb|ms|mb|s)", inputstr))
        ordprice = ''.join(re.findall("[0-9\.]", inputstr))
        order(cmd, ordprice, activeInst)
