package main

import (
	"log"
	"net"

	RpcServices "coteach/services"

	"google.golang.org/grpc"
)

func main() {
	network := "tcp"
	port := ":8080"
	listen, err := net.Listen(network, port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Println("Server listening on port", port)

	gRPCServer := grpc.NewServer()
	RpcServices.Register(gRPCServer)
	if err := gRPCServer.Serve(listen); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
