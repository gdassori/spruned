from spruned import settings
from spruned.service.abstract import RPCAPIService
from spruned.third_party.http_client import HTTPClient
from spruned.tools import normalize_transaction


class ChainSoService(RPCAPIService):
    def __init__(self, coin):
        self._coin_url = {
            settings.Network.BITCOIN: 'BTC/'
        }[coin]
        self.client = HTTPClient(baseurl='https://chain.so/api/v2/')

    def getrawtransaction(self, txid, **_):
        data = self.client.get('get_tx/' + self._coin_url + txid)
        return data and {
            'rawtx': normalize_transaction(data['data']['tx_hex']),
            'blockhash': data['data']['blockhash'],
            'txid': txid,
            'source': 'chainso'
        }

    def getblock(self, blockhash):
        print('getblock from %s' % self.__class__)
        data = self.client.get('get_block/' + self._coin_url + blockhash)
        return data and {
            'source': 'chainso',
            'hash': data['blockhash'],
            'tx': data['txs']
        }

