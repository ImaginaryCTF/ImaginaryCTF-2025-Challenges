package main

import (
	"crypto/tls"

	"github.com/apache/thrift/lib/go/thrift"
)

func main() {
	cfg := &thrift.TConfiguration{
		TLSConfig: &tls.Config{
			InsecureSkipVerify: true,
		},
	}

	if err := runServer(
		thrift.NewTFramedTransportFactoryConf(thrift.NewTBufferedTransportFactory(8192), cfg),
		thrift.NewTBinaryProtocolFactoryConf(nil), "0.0.0.0:9090"); err != nil {
		panic(err)
	}
}
