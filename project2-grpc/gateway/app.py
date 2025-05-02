from flask import Flask, request, jsonify
import grpc
import textprocessor_pb2
import textprocessor_pb2_grpc

app = Flask(__name__)

# Endereço dos microserviços (ajuste conforme sua rede/infra)
A_ADDRESS = 'localhost:50051'  # Go server
B_ADDRESS = 'localhost:50052'  # Ruby server

@app.route('/count-words', methods=['POST'])
def count_words():
    data = request.get_json()
    text = data.get('text', '')
    with grpc.insecure_channel(A_ADDRESS) as channel:
        stub = textprocessor_pb2_grpc.TextProcessorAStub(channel)
        response = stub.CountWords(textprocessor_pb2.TextRequest(text=text))
    return jsonify({'result': response.result})

@app.route('/count-characters', methods=['POST'])
def count_characters():
    data = request.get_json()
    text = data.get('text', '')
    with grpc.insecure_channel(B_ADDRESS) as channel:
        stub = textprocessor_pb2_grpc.TextProcessorBStub(channel)
        response = stub.CountCharacters(textprocessor_pb2.TextRequest(text=text))
    return jsonify({'result': response.result})

@app.route('/')
def index():
    return '''
    <h1>API Gateway (P)</h1>
    <form action="/count-words" method="post" enctype="application/json">
        <input name="text" placeholder="Digite o texto">
        <button type="submit">Contar Palavras</button>
    </form>
    <form action="/count-characters" method="post" enctype="application/json">
        <input name="text" placeholder="Digite o texto">
        <button type="submit">Contar Caracteres</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
