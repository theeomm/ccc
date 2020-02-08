from flask import jsonify


def errorResponse(message, status=404):
    return jsonify({
        'error': {
            'message': message
        },
        'statusCode': status,
    }), status
