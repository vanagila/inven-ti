from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.database.connection import db
from app.models import Equipamento
from app.models.Usuario import Usuario
import re
from app.models.enums import StatusEquipamento

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        try:
            if request.is_json:
                dados = request.get_json()
                nome = (dados.get('nome') or '').strip()
                email = (dados.get('email') or '').strip().lower()
                senha = dados.get('senha') or ''
                departamento = (dados.get('departamento') or '').strip()
                cargo = (dados.get('cargo') or '').strip()
                is_admin = dados.get('is_admin', False)
            else:
                nome = (request.form.get('nome') or '').strip()
                email = (request.form.get('email') or '').strip().lower()
                senha = request.form.get('senha') or ''
                departamento = (request.form.get('departamento') or '').strip()
                cargo = (request.form.get('cargo') or '').strip()
                is_admin = True if request.form.get('is_admin') == 'on' else False

            if not nome or not email or not senha:
                flash('Nome, email e senha são obrigatórios.', 'danger')
                return render_template('auth/cadastrar.html', dados=request.form)

            # validacao email
            email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
            if not email_re.match(email):
                flash('Email inválido.', 'danger')
                return render_template('auth/cadastrar.html', dados=request.form)

            # 6 caracteres, pelo menos um digito e uma letra
            if len(senha) < 6 or not re.search(r"[0-9]", senha) or not re.search(r"[A-Za-z]", senha):
                flash('Senha fraca. Use pelo menos 6 caracteres, com letras e números.', 'danger')
                return render_template('auth/cadastrar.html', dados=request.form)

            if Usuario.query.filter_by(email=email).first():
                flash('Este email já está cadastrado', 'danger')
                return render_template('auth/cadastrar.html', dados=request.form)

            dados = {
                'nome': nome,
                'email': email,
                'senha': senha,
                'departamento': departamento,
                'cargo': cargo,
                'is_admin': is_admin
            }

            usuario = Usuario(**dados)
            db.session.add(usuario)
            db.session.commit()

            if request.is_json:
                return jsonify({
                    'mensagem': 'Usuário cadastrato com sucesso',
                    'usuario': usuario.to_dict()
                }), 201
            else:
                flash('Usuário cadastrado com sucesso. Faça login.', 'success')
                return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'danger')
    
    return render_template('auth/cadastrar.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            dados = request.get_json()
            email = dados.get('email')
            senha = dados.get('senha')
        else:
            email = request.form.get('email')
            senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email, ativo=True).first()

        if usuario and usuario.check_senha(senha):
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome
            session['user_email'] = usuario.email
            session['is_admin'] = usuario.is_admin

            if request.is_json:
                return jsonify({
                    'mensagem': f'Bem-vindo(a), {usuario.nome}',
                    'usuario': usuario.to_dict()
                })
            else:
                # flash(f'Bem vindo(a), {usuario.nome}!', 'success')
                return redirect(url_for('auth.painel'))
        else:
            mensagem = 'Email ou senha incorretos.'
            if request.is_json:
                return jsonify({'erro': mensagem}), 401
            else:
                flash(mensagem, 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('user_nome', None)
        session.pop('user_email', None)
        session.pop('is_admin', None)

        session.clear()

        flash('Você saiu da sua conta com sucesso.', 'info')
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/painel', methods=['GET'])
def painel():
    try:
        total_equipamentos = Equipamento.query.count()
        equipamentos_em_uso = Equipamento.query.filter_by(status=StatusEquipamento.EM_USO).count()
        equipamentos_desativados = Equipamento.query.filter_by(status=StatusEquipamento.DESATIVADO).count()
        equipamentos_em_manutencao = Equipamento.query.filter_by(status=StatusEquipamento.EM_MANUTENCAO).count()
        equipamentos_recentes = Equipamento.query.order_by(Equipamento.data_cadastro.desc()).limit(5).all()

        if request.is_json:
            return jsonify({
                'total_equipamentos': total_equipamentos,
                'equipamentos_desativados': equipamentos_desativados,
                'equipamentos_em_uso': equipamentos_em_uso,
                'equipamentos_em_manutencao': equipamentos_em_manutencao,
                'equipamentos_recentes': equipamentos_recentes
            }), 200
        
        return render_template('auth/painel.html', total_equipamentos=total_equipamentos, equipamentos_desativados=equipamentos_desativados, equipamentos_em_manutencao=equipamentos_em_manutencao, equipamentos_em_uso=equipamentos_em_uso,
        equipamentos_recentes=equipamentos_recentes)
    
    except Exception as e:
        if request.is_json:
            return jsonify({'erro': str(e)}), 500
        else:
            flash(f'Erro ao carregar painel: {str(e)}', 'danger')
            return render_template('auth/painel.html',
                total_equipamentos=0,
                equipamentos_em_uso=0,
                equipamentos_em_manutencao=0,
                equipamentos_desativados=0,
                equipamentos_recentes=[]
            )