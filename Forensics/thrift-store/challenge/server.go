package main

import (
	"fmt"

	"github.com/ImaginaryCTF/ImaginaryCTF-2025-Challenges/forensics/thrift-store/challenge/gen-go/store"
	"github.com/apache/thrift/lib/go/thrift"
)

func runServer(transportFactory thrift.TTransportFactory, protocolFactory thrift.TProtocolFactory, addr string) error {

	transport, err := thrift.NewTServerSocket(addr)

	if err != nil {
		return err
	}

	basketStore := &InMemoryBasketStore{data: make(map[string][]*store.BasketItem)}
	handler := NewStoreHandler(basketStore)
	processor := store.NewStoreProcessor(handler)
	server := thrift.NewTSimpleServer4(processor, transport, transportFactory, protocolFactory)

	fmt.Println("Starting the simple server... on ", addr)
	return server.Serve()
}
