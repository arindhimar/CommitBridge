from flask import request, jsonify, Blueprint
from models.XIntegrationModel import XIntegrationModel
import tweepy

x_integration_bp = Blueprint('x_integration_bp', __name__)
x_integration_model = XIntegrationModel()

# Routes for managing X integrations
@x_integration_bp.route('/x-integrations', methods=['GET'])
def get_all_integrations():
    """Fetch all X integrations from the database."""
    integrations = x_integration_model.fetch_all_integrations()
    return jsonify(integrations)

@x_integration_bp.route('/x-integrations/<int:integration_id>', methods=['GET'])
def get_integration(integration_id):
    """Fetch a specific X integration by its ID."""
    integration = x_integration_model.fetch_integration_by_id(integration_id)
    if not integration:
        return jsonify({'error': 'Integration not found'}), 404
    return jsonify(integration)

@x_integration_bp.route('/x-integrations', methods=['POST'])
def create_integration():
    """Create a new X integration with the provided credentials."""
    data = request.get_json() or request.form
    required_fields = ['bearer_token', 'api_key', 'api_secret', 'access_token', 'access_token_secret']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    x_integration_model.create_integration(
        data['bearer_token'], data['api_key'], data['api_secret'], data['access_token'], data['access_token_secret']
    )
    return jsonify({'message': 'Integration created successfully'}), 201

@x_integration_bp.route('/x-integrations/<int:integration_id>', methods=['PUT'])
def update_integration(integration_id):
    """Update an existing X integration."""
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
    """Delete an X integration."""
    if not x_integration_model.fetch_integration_by_id(integration_id):
        return jsonify({'error': 'Integration not found'}), 404

    x_integration_model.delete_integration(integration_id)
    return jsonify({'message': 'Integration deleted successfully'})

# Functions to interact with the X API
def initialize_x_client():
    """
    Initialize the X API client dynamically using credentials from the database.
    """
    credentials = x_integration_model.fetch_latest_integration()
    if not credentials:
        raise Exception("X API credentials not found")

    bearer_token, api_key, api_secret, access_token, access_token_secret = credentials

    # Return an authenticated Tweepy client
    return tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

@x_integration_bp.route('/post_update', methods=['POST'])
def post_update():
    """Endpoint to post an update (formerly a tweet) on X."""
    data = request.get_json()
    update_content = data.get('update')

    if not update_content:
        return jsonify({'error': 'Update content is required'}), 400

    try:
        client = initialize_x_client()
        response = client.create_tweet(text=update_content)
        return jsonify({
            'message': 'Update posted successfully',
            'update_id': response.data['id']
        }), 200
    except tweepy.TweepyException as e:
        return jsonify({'error': str(e)}), 500

@x_integration_bp.route('/post_latest_update', methods=['POST'])
def post_latest_update():
    """Endpoint to post the latest update content from the database."""
    update_content = x_integration_model.get_latest_update_content()

    if not update_content:
        return jsonify({'error': 'No update content found in the database'}), 404

    try:
        client = initialize_x_client()
        response = client.create_tweet(text=update_content)
        return jsonify({
            'message': 'Latest update posted successfully',
            'update_id': response.data['id']
        }), 200
    except tweepy.TweepyException as e:
        return jsonify({'error': str(e)}), 500
