from flask import Blueprint, request, jsonify
from models.vaccines import Vaccine,db
from datetime import datetime
from sqlalchemy import func


vaccines_bp = Blueprint('vaccines', __name__)

@vaccines_bp.route('/', methods=['GET'])
def get_vaccines():
    vaccines = Vaccine.query.all()
    return jsonify([{
        'id': v.id_vaccines,
        'name': v.name,
        'description': v.description,
        'manufacturer': v.manufacturer,
        'efficacy': v.efficacy,
        'side_effects': v.side_effects,
        'category': v.category,
        'quantity': v.quantity,

    } for v in vaccines]), 200

@vaccines_bp.route('/', methods=['POST'])
def add_vaccine():
    data = request.get_json()

    if not data:
        return jsonify({'Lỗi': 'Yêu cầu phải gửi dữ liệu JSON hợp lệ'}), 400

    # Lấy dữ liệu từ JSON
    id_vaccines = data.get('id')  
    name = data.get('name')
    description = data.get('description')
    manufacturer = data.get('manufacturer')
    efficacy = data.get('efficacy')
    side_effects = data.get('side_effects')
    category = data.get('category', 'Bắt buộc')  # Mặc định là 'Bắt buộc' nếu không có
    quantity = data.get('quantity', 1)

    # Kiểm tra các trường bắt buộc
    if id_vaccines is None:
        return jsonify({'Lỗi': 'ID vaccine là bắt buộc'}), 400
    if Vaccine.query.get(id_vaccines):
        return jsonify({'Lỗi': 'ID vaccine đã tồn tại'}), 400

    if not name:
        return jsonify({'Lỗi': 'Tên vaccine là bắt buộc'}), 400
    if quantity is None or not isinstance(quantity, int) or quantity < 0:
        return jsonify({'Lỗi': 'Số lượng vaccine phải là số nguyên không âm'}), 400

    try:
        vaccine = Vaccine(
            id_vaccines=id_vaccines,
            name=name,
            description=description,
            manufacturer=manufacturer,
            efficacy=float(efficacy) if efficacy is not None else None,
            side_effects=side_effects,
            category=category,
            quantity=quantity
        )

        db.session.add(vaccine)
        db.session.commit()

        return jsonify({'Thông báo': 'Thêm vaccine thành công'}), 201

    except ValueError:
        return jsonify({'Lỗi': 'Hiệu quả vaccine (efficacy) phải là số'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi thêm vaccine: {str(e)}'}), 500

@vaccines_bp.route('/<int:id_vaccines>', methods=['PUT'])
def update_vaccine(id_vaccines):
    data = request.get_json()

    if not data:
        return jsonify({'Lỗi': 'Yêu cầu phải gửi dữ liệu JSON hợp lệ'}), 400

    vaccine = Vaccine.query.get(id_vaccines)
    if not vaccine:
        return jsonify({'Lỗi': 'Vaccine không tồn tại'}), 404

    # Cập nhật nếu có, không thì giữ nguyên
    vaccine.name = data.get('name', vaccine.name)
    vaccine.description = data.get('description', vaccine.description)
    vaccine.manufacturer = data.get('manufacturer', vaccine.manufacturer)
    vaccine.category = data.get('category', vaccine.category)
    vaccine.quantity = data.get('quantity', vaccine.quantity)

    try:
        efficacy_value = data.get('efficacy', vaccine.efficacy)
        vaccine.efficacy = float(efficacy_value) if efficacy_value is not None else None
    except ValueError:
        return jsonify({'Lỗi': 'Hiệu quả vaccine (efficacy) phải là số'}), 400

    vaccine.side_effects = data.get('side_effects', vaccine.side_effects)

    try:
        db.session.commit()
        return jsonify({'Thông báo': 'Cập nhật vaccine thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi cập nhật vaccine: {str(e)}'}), 500

@vaccines_bp.route('/<int:id_vaccines>', methods=['DELETE'])    
def delete_vaccine(id_vaccines):
    vaccine = Vaccine.query.get(id_vaccines)
    if not vaccine:
        return jsonify({'Lỗi': 'Vaccine không tồn tại'}), 404

    try:
        db.session.delete(vaccine)
        db.session.commit()
        return jsonify({'Thông báo': 'Xóa vaccine thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi xóa vaccine: {str(e)}'}), 500
    
@vaccines_bp.route('/<int:id_vaccines>', methods=['GET'])
def get_vaccine_by_id(id_vaccines): 
    vaccine = Vaccine.query.get(id_vaccines)
    if not vaccine:
        return jsonify({'Lỗi': 'Vaccine không tồn tại'}), 404

    return jsonify({
        'id': vaccine.id_vaccines,
        'name': vaccine.name,
        'description': vaccine.description,
        'manufacturer': vaccine.manufacturer,
        'efficacy': vaccine.efficacy,
        'side_effects': vaccine.side_effects,
        'category': vaccine.category,
        'quantity': vaccine.quantity,
    }), 200

@vaccines_bp.route('/stats', methods=['GET'])
def vaccine_stats():
    try:
        total_vaccines = Vaccine.query.count()
        total_quantity = db.session.query(func.sum(Vaccine.quantity)).scalar() or 0

        # Thống kê theo category
        category_counts = db.session.query(
            Vaccine.category, func.count(Vaccine.id_vaccines)
        ).group_by(Vaccine.category).all()

        category_data = {cat: count for cat, count in category_counts}

        # Hiệu quả trung bình
        avg_efficacy = db.session.query(func.avg(Vaccine.efficacy)).scalar()
        avg_efficacy = round(avg_efficacy, 2) if avg_efficacy else None
 
        vaccine_details = db.session.query(
            Vaccine.name, Vaccine.quantity
        ).all()
        quantity_by_vaccine = [
            {"name": name, "quantity": quantity} for name, quantity in vaccine_details
        ]

        return jsonify({
            'Số loại vaccines': total_vaccines,
            'Tổng số lượng': total_quantity,
            'Số lượng theo vaccine': quantity_by_vaccine,
            'Số lượng theo phân loại': category_data,
            'Hiệu quả trung bình': avg_efficacy
        }), 200

    except Exception as e:
        return jsonify({'Lỗi': f'Lỗi khi thống kê: {str(e)}'}), 500
    
# @vaccines_bp.route('/search', methods=['GET'])
# def search_vaccines():  
#     query = request.args.get('query', '').strip()
#     if not query:
#         return jsonify({'Lỗi': 'Yêu cầu phải cung cấp từ khóa tìm kiếm'}), 400

#     vaccines = Vaccine.query.filter(
#         Vaccine.name.ilike(f'%{query}%') |
#         Vaccine.description.ilike(f'%{query}%') |   
#         Vaccine.manufacturer.ilike(f'%{query}%') |
#         Vaccine.side_effects.ilike(f'%{query}%') |
#         Vaccine.category.ilike(f'%{query}%')
#     ).all()
#     if not vaccines:
#         return jsonify({'Thông báo': 'Không tìm thấy vaccine nào phù hợp với từ khóa'}), 404