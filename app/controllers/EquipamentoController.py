from time import strptime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.database.connection import db
from app.models.Equipamento import Equipamento
from datetime import datetime

equipamento_bp = Blueprint('equipamento', __name__, url_prefix='/equipamentos')

@equipamento_bp.route('/', methods=['GET', 'POST'])
def cadastrar_equipamento():
    if request.method == 'GET':
        return render_template('equipamentos/cadastro.html')

    try:
        if request.is_json:
            dados = request.get_json()
        else:
            dados = request.form.to_dict()

        user_id = session.get('user_id')
        if not user_id:
            flash('É necessário estar logado para cadastrar equipamentos.', 'danger')
            return redirect(url_for('auth.login'))

        dados['id_usuario_cadastro'] = user_id

        if 'data_aquisicao' in dados and dados['data_aquisicao']:
            dados['data_aquisicao'] = datetime.strptime(dados['data_aquisicao'], '%Y-%m-%d').date()

        if Equipamento.query.filter_by(patrimonio=dados.get('patrimonio')).first():
            flash('Este número de patrimônio já está cadastrado.', 'danger')
            return render_template('equipamentos/cadastro.html', dados=dados)

        if Equipamento.query.filter_by(numero_serie=dados.get('numero_serie')).first():
            flash('Este número de série já está cadastrado.', 'danger')
            return render_template('equipamentos/cadastro.html', dados=dados)

        equipamento = Equipamento(**dados)
        db.session.add(equipamento)
        db.session.commit()

        if request.is_json:
            return jsonify(equipamento.to_dict()), 201
        else:
            flash('Equipamento cadastrado com sucesso!', 'success')
            return redirect(url_for('equipamento.cadastrar_equipamento'))

    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'erro': str(e)}), 400
        else:
            flash(f'Erro ao cadastrar equipamento: {str(e)}', 'danger')
            return render_template('equipamentos/cadastro.html', dados=request.form)