from flask import request, jsonify, Blueprint
from models.LinkedInIntegrationModel import LinkedInIntegrationModel

linkedin_integration_bp = Blueprint('linkedin_integration_bp', __name__)
linkedin_integration_model = LinkedInIntegrationModel()

@linkedin_integration_bp.route('/linkedin-integrations', methods=['GET'])
def get_all_integrations():
    integrations = linkedin_integration_model.fetch_all_integrations()
    return jsonify(integrations)

@linkedin_integration_bp.route('/linkedin-integrations/<int:integration_id>', methods=['GET'])
def get_integration(integration_id):
    integration = linkedin_integration_model.fetch_integration_by_id(integration_id)
    if not integration:
        return jsonify({'error': 'Integration not found'}), 404
    return jsonify(integration)

@linkedin_integration_bp.route('/linkedin-integrations', methods=['POST'])
def create_integration():
    data = request.get_json() or request.form
    if not all(key in data for key in ('access_token', 'linkedin_id_urn')):
        return jsonify({'error': 'Missing required fields'}), 400
    linkedin_integration_model.create_integration(data['access_token'], data['linkedin_id_urn'])
    return jsonify({'message': 'Integration created successfully'}), 201

@linkedin_integration_bp.route('/linkedin-integrations/<int:integration_id>', methods=['PUT'])
def update_integration(integration_id):
    data = request.get_json() or request.form
    if not linkedin_integration_model.fetch_integration_by_id(integration_id):
        return jsonify({'error': 'Integration not found'}), 404
    linkedin_integration_model.update_integration(
        integration_id, data.get('access_token'), data.get('linkedin_id_urn')
    )
    return jsonify({'message': 'Integration updated successfully'})

@linkedin_integration_bp.route('/linkedin-integrations/<int:integration_id>', methods=['DELETE'])
def delete_integration(integration_id):
    if not linkedin_integration_model.fetch_integration_by_id(integration_id):
        return jsonify({'error': 'Integration not found'}), 404
    linkedin_integration_model.delete_integration(integration_id)
    return jsonify({'message': 'Integration deleted successfully'})

@linkedin_integration_bp.route('/linkedin/post', methods=['POST'])
def create_linkedin_post():
    credentials = linkedin_model.get_linkedin_credentials()
    if not credentials:
        return jsonify({'error': 'LinkedIn credentials not found'}), 404

    access_token, linkedin_id = credentials

    blog_post = linkedin_model.get_latest_blog_post()
    if not blog_post:
        return jsonify({'error': 'No blog post available for sharing'}), 404

    blog_url, blog_description = blog_post

    api_url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
    }
    post_body = {
        'author': f'urn:li:person:{linkedin_id}',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {'text': 'Check out our latest blog post!'},
                'shareMediaCategory': 'ARTICLE',
                'media': [
                    {
                        'status': 'READY',
                        'description': {'text': blog_description},
                        'originalUrl': blog_url,
                    },
                ],
            },
        },
        'visibility': {'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'},
    }

    response = requests.post(api_url, headers=headers, json=post_body)

    if response.status_code == 201:
        return jsonify({'message': 'Post successfully created'}), 201
    else:
        return jsonify({'error': 'Failed to create LinkedIn post', 'details': response.json()}), response.status_code