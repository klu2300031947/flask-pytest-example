from flask import Flask, jsonify, request

app = Flask(__name__)

def configure_routes(app):
    @app.route('/', methods=['GET'])
    def base_route():
        return "Hello, World!", 200

    @app.route('/post/test', methods=['POST'])
    def post_route():
        headers = request.headers
        data = request.get_json()

        # Authorization check
        if 'authorization-sha256' not in headers:
            return jsonify({'message': 'Unauthorized'}), 401

        # Bad request check
        if not data or 'request_id' not in data or 'payload' not in data:
            return jsonify({'message': 'Bad Request'}), 400

        # Successful response
        return jsonify({
            'message': 'Success',
            'data': data['payload']
        }), 200

    @app.route('/delete/test/<request_id>', methods=['DELETE'])
    def delete_route(request_id):
        # Simulate checking if the request_id exists
        if request_id == '123':
            return jsonify({'message': f'Resource with id {request_id} deleted successfully'}), 200
        else:
            return jsonify({'message': 'Resource not found'}), 404


if __name__ == '__main__':
    configure_routes(app)
    app.run(debug=True)
