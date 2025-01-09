from flask import request, jsonify, Blueprint
from models.UserModel import UserModel

user_bp = Blueprint('user_bp', __name__)
user_model = UserModel()

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = user_model.fetch_all_users()
    return jsonify(users)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.fetch_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or request.form
    if not all(key in data for key in ('name', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    user_model.create_user(data['name'], data['email'], data['password'], data.get('timezone', 'UTC'))
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json() or request.form
    if not user_model.fetch_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    user_model.update_user(user_id, data.get('name'), data.get('email'), data.get('password'), data.get('timezone'))
    return jsonify({'message': 'User updated successfully'})

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not user_model.fetch_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    user_model.delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'})
