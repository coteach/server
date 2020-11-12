package services

import (
	"context"
	. "coteach/services/plans"
	"log"

	"google.golang.org/grpc"
)

type PlansService struct {
	UnimplementedPlansRpcServer
}

func registerPlansService(server *grpc.Server) {
	RegisterPlansRpcServer(server, &PlansService{})
}

func (s *PlansService) View(ctx context.Context, in *ViewRequest) (*Empty, error) {
	log.Printf("Received: %v", in.Id)
	return &Empty{}, nil
}
