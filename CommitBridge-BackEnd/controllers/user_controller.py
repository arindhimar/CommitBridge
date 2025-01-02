from flask import Blueprint, request, jsonify
from models.user import User
from .auth_controller import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user:
        return jsonify({'error': 'Authentication required'}), 401
    
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    if not current_user:
        return jsonify({'error': 'Authentication required'}), 401
    
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if not current_user or current_user.id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    try:
        current_user.update(**data)
        return jsonify({
            'message': 'User updated successfully',
            'user': current_user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if not current_user or current_user.id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        current_user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

