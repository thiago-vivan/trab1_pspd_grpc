package main

import (
    "context"
    "log"
    "net"
    "strings"

    pb "project2_grpc/serverA/protos"
    "google.golang.org/grpc"
)

type server struct {
    pb.UnimplementedTextProcessorAServer
}

func (s *server) CountWords(ctx context.Context, req *pb.TextRequest) (*pb.TextResponse, error) {
    count := len(splitWords(req.Text))
    return &pb.TextResponse{Result: int32(count)}, nil
}

func splitWords(text string) []string {
    // Simples separação por espaço
    return strings.Fields(text)
}

func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    grpcServer := grpc.NewServer()
    pb.RegisterTextProcessorAServer(grpcServer, &server{})
    log.Println("Servidor Go (A) rodando na porta 50051")
    grpcServer.Serve(lis)
}
