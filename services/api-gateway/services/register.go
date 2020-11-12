package services

import "google.golang.org/grpc"

func Register(server *grpc.Server) {
	registerPlansService(server)
}
