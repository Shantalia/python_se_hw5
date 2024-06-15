import sys
import json
import aiohttp
import asyncio
import platform
from datetime import timedelta, datetime
from timing import async_timed


class HttpError(Exception):
    pass

async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f'Connection error: {url}', str(err))

@async_timed()
async def main(days):
    curr_response = []
    curr_EUR = {}
    curr_USD = {}
    for day in range(1,int(days)+1):
        curr_day = (datetime.now() - timedelta(days=int(day))).strftime("%d.%m.%Y")
        try:
            response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={curr_day}')
            for item in response['exchangeRate']:
                if (item['baseCurrency'] == 'UAH') & (item['currency'] == 'EUR'):
                    curr_EUR['sale'] = item['saleRateNB']
                    curr_EUR['purchase'] = item['purchaseRateNB']
                elif (item['baseCurrency'] == 'UAH') & (item['currency'] == 'USD'):
                    curr_USD['sale'] = item['saleRateNB']
                    curr_USD['purchase'] = item['purchaseRateNB']
            curr_response.append({curr_day : {'EUR' : curr_EUR, 'USD' : curr_USD}})
        except HttpError as err:
            print(err)
    return curr_response
    


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if int(sys.argv[1]) >= 10:
        raise HttpError("You only can request currency maximum for the last 10 days")
    else:
        r = asyncio.run(main(sys.argv[1]))
        print(json.dumps(r, indent=2, sort_keys=True))