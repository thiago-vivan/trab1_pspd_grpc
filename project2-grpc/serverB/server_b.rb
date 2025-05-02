require 'grpc'
require_relative 'textprocessor_services_pb'

class TextProcessorB < Textprocessor::TextProcessorB::Service
  def count_characters(request, _unused_call)
    Textprocessor::TextResponse.new(result: request.text.length)
  end
end

server = GRPC::RpcServer.new
server.add_http2_port('0.0.0.0:50052', :this_port_is_insecure)
server.handle(TextProcessorB.new)
puts "Servidor Ruby (B) rodando na porta 50052"
server.run_till_terminated

