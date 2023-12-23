
class WebSocketDefine:
    # Uri = "wss://dstream.binance.com/ws"
    # testnet
    Uri = "wss://dstream.binancefuture.com/ws"
    Uri = "wss://dstream.binance.com/ws" #damian
    # testnet new spec
    # Uri = "wss://sdstream.binancefuture.com/ws"

class RestApiDefine:
    Url = "https://dapi.binance.com"
    # testnet
    #Url = "https://testnet.binancefuture.com"


#https://binance-docs.github.io/apidocs/delivery/en/#change-log
#testnet
#Most of the endpoints can be also used in the testnet platform.
#The REST baseurl for testnet is "https://testnet.binancefuture.com"
#The Websocket baseurl for testnet is "wss://dstream.binancefuture.com"

class DamianTestnetWebSocketDefine:
    # testnet
    Uri = "wss://dstream.binance.com/ws" #damian
    # testnet new spec
    # Uri = "wss://sdstream.binancefuture.com/ws"

class DamianTestnetRestApiDefine:
    Url = "https://testnet.binancefuture.com"

