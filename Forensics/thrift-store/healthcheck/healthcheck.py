#!/usr/bin/env python3

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from store import Store


def make_client():
    """Helper to create a connected thrift client."""
    transport = TSocket.TSocket("localhost", 9090)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Store.Client(protocol)
    transport.open()
    return client, transport


def test_store():
    client, transport = make_client()
    ret = 1
    try:
        basket = client.createBasket()
        client.addToBasket(basket.basketId, "flag")
        response = client.pay(basket.basketId, 9999)
        print(response.flag)
        ret = (0 if response.flag != None else 1)
    except Exception as e:
        print(e)
        exit(ret)
    finally:
        transport.close()
        exit(ret)


if __name__ == "__main__":
    test_store()
