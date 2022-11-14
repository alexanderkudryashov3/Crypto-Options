import asyncio
import websockets
import json
import pandas as pd
import datetime as dt
from datetime import datetime




class Parser:
    def __init__(self, index = 'btc_usd'):

        self.index = index

        self.index_msg = \
            json.dumps({"jsonrpc": "2.0",
                        "method": "public/get_index_price",
                        "id": 42,
                        "params": {
                            "index_name": index}
                        })

        self.options_msg = \
            json.dumps({"jsonrpc": "2.0",
                        "method": "public/subscribe",
                        "id": 42,
                        "params": {
                            "channels": ["markprice.options." + index]}
                        })

    async def call_api_index(self):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(self.index_msg)
            response = await websocket.recv()
            return pd.DataFrame(json.loads(response))['result']['index_price']

    def get_index_price(self):
        loop2 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop2)
        res = loop2.run_until_complete(self.call_api_index())
        return res

    def json_to_dataframe(self, json_resp):
        res_df = pd.DataFrame()
        index_price = self.get_index_price()
        res = json.loads(json_resp)
        df = pd.DataFrame(res['params']['data'])
        instrument = [string.split('-') for string in df['instrument_name']]
        res_df['currency'] = [x[0] for x in instrument]
        res_df['type'] = ['call' if x[3] == 'C' else 'put' for x in instrument]
        res_df['days until expiration'] = [int((datetime.strptime(x[1], '%d%b%y') - datetime.today()).days) for x in
                                           instrument]
        res_df['strike'] = [int(x[2]) for x in instrument]
        res_df['mark_price'] = df['mark_price']
        res_df['iv'] = df['iv']
        res_df['underlying_price'] = [index_price for i in range(len(df))]

        return res_df

    async def call_api_options(self, min_delta):
        df_master = pd.DataFrame()
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(self.options_msg)
            now = dt.datetime.now()
            finish_condition = dt.datetime.now() + dt.timedelta(minutes=min_delta)
            while (finish_condition - dt.datetime.now()).total_seconds() > 10:

                response = await websocket.recv()

                if 'params' not in json.loads(response):
                    continue

                temp_df = self.json_to_dataframe(response)

                df_master = df_master.append(temp_df)

            return df_master

    def get_live_data(self, min_delta=1):
        import nest_asyncio
        nest_asyncio.apply()

        loop = asyncio.get_event_loop()
        df = loop.run_until_complete(self.call_api_options(min_delta))

        return df


    def preprocess(self, df):
        data = pd.DataFrame()
        data['currency'] = [string.split('-')[0] for string in df['symbol']]
        data['type'] = df['type']
        data['days until expiration'] = [(datetime.fromtimestamp(
            df['expiration'].iloc[i] / 1e+6) - datetime.fromtimestamp(df['timestamp'].iloc[i] / 1e+6)).days for i in
                                         range(len(df))]
        data['strike'] = df['strike_price']
        data['mark_price'] = df['mark_price']
        data['mark_iv'] = df['mark_iv']
        data['underlying_price'] = df['underlying_price']

        return data


    def get_historical_data(self, year='2022', month='11'):
        import nest_asyncio
        nest_asyncio.apply()
        from tardis_dev import datasets

        datasets.download(
            exchange="deribit",
            data_types=["options_chain"],
            from_date=year+"-"+"-"+month+"-01",
            to_date=year+"-"+"-"+month+"-02",
            symbols=["OPTIONS"]
        )

        df = pd.read_csv('datasets/deribit_options_chain_'+year+"-"+"-"+month+"-01"+'_OPTIONS.csv')

        return self.preprocess(df)




