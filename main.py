import logging
import platform

import aiohttp
import asyncio
import aiofiles
import datetime
import sys
import json

def parse_dict(data,date):
    kurs_dict={date:{}}
    for kurs in data['exchangeRate']:
        if kurs['currency'] in ('USD','EUR'):
            kurs_dict[date][kurs['currency']]={'sale':kurs['saleRate'],'purchase':kurs['purchaseRate']}
    return kurs_dict

async def request(num):
        date=datetime.datetime.today()-datetime.timedelta(days=num)
        formated_date = date.strftime("%d.%m.%Y")
        url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={formated_date}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        r = await response.json()
                        return parse_dict(r,formated_date)
            except aiohttp.ClientConnectionError as e:
                logging.error(f'Connection error {url}: {e}')

async def main(num,list):
    for i in range(num):
        res = await request(i)
        list.append(res)
if __name__=="__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    days=int(sys.argv[1])
    result=[]
    if days>10:
        print("Can't do more than 10")
    else:
        r=asyncio.run(main(days,result))
        print(result)