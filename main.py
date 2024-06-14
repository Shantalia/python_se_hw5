import sys
import json
import aiohttp
import asyncio
import platform
from datetime import timedelta, datetime


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

async def main(days):
    #curr_day = datetime.now() - timedelta(days=int(days))
    curr_response = {}
    curr_EUR = {}
    for day in range(1,int(days)+1):
        curr_day = (datetime.now() - timedelta(days=int(day))).strftime("%d.%m.%Y")
        try:
            response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={curr_day}')
            print(f'{response}\n')
            print(response['exchangeRate'])
            for key, value in response['exchangeRate']:
                curr_EUR[key] = value
            print(curr_EUR)
            curr_response[curr_day] = response
            continue
        except HttpError as err:
            print(err)
    return curr_response
    


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(sys.argv)
    # if int(sys.argv[1]) >= 10:
    #     raise HttpError("You only can request currency maximum for the last 10 days")
    # else:
    #     r = asyncio.run(main(sys.argv[1]))
    #     print(r)

    r = asyncio.run(main(2))
    #print(r)