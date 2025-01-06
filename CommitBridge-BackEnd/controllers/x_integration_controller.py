from flask import request, jsonify, Blueprint
from models.x_integration import XIntegrationModel

x_integration_bp = Blueprint('x_integration_bp', __name__)
x_integration_model = XIntegrationModel()

@x_integration_bp.route('/x-integrations', methods=['GET'])
def get_all_integrations():
    integrations = x_integration_model.fetch_all_integrations()
    return jsonify(integrations)

@x_integration_bp.route('/x-integrations/<int:integration_id>', methods=['GET'])
def get_integration(integration_id):
    integration = x_integration_model.fetch_integration_by_id(integration_id)
    if not integration:
        return jsonify({'error': 'Integration not found'}), 404
    return jsonify(integration)

@x_integration_bp.route('/x-integrations', methods=['POST'])
def create_integration():
    data = request.get_json() or request.form
    if not all(key in data for key in ('bearer_token', 'api_key', 'api_secret', 'access_token', 'access_token_secret')):
        return jsonify({'error': 'Missing required fields'}), 400
    x_integration_model.create_integration(
        data['bearer_token'], data['api_key'], data['api_secret'], data['access_token'], data['access_token_secret']
    )
    return jsonify({'message': 'Integration created successfully'}), 201

@x_integration_bp.route('/x-integrations/<int:integration_id>', methods=['PUT'])
def update_integration(integration_id):
    data = request.get_json() or request.form
    if not x_integration_model.fetch_integration_by_id(integration_id):
        return jsonify({'error': 'Integration not found'}), 404
    x_integration_model.update_integration(
        integration_id,
        data.get('bearer_token'), data.get('api_key'), data.get('api_secret'),
        data.get('access_token'), data.get('access_token_secret')
    )
    return jsonify({'message': 'Integration updated successfully'})

@x_integration_bp.route('/x-integrations/<int:integration_id>', methods=['DELETE'])
def delete_integration(integration_id):
    if not x_integration_model.fetch_integration_by_id(integration_id):
        return jsonify({'error': 'Integration not found'}), 404
    x_integration_model.delete_integration(integration_id)
    return jsonify({'message': 'Integration deleted successfully'})
