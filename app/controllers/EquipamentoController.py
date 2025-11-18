from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.database.connection import db
from app.models.Equipamento import Equipamento
from app.models.RegistroSuporte import RegistroSuporte
from datetime import datetime
from app.models.enums import StatusEquipamento
from app.models.enums import TipoSuporte
from sqlalchemy import func, or_
from app.decorators import admin_required, login_required

equipamento_bp = Blueprint('equipamento', __name__, url_prefix='/equipamentos')

@equipamento_bp.route('/', methods=['GET', 'POST'])
@admin_required
def cadastrar_equipamento():
    if request.method == 'GET':
        return render_template('equipamentos/cadastro.html', status_options=StatusEquipamento.todos())

    try:
        if request.is_json:
            dados = request.get_json()
        else:
            dados = request.form.to_dict()
            dados['status'] = dados.get('status') or StatusEquipamento.EM_USO

        user_id = session.get('user_id')
        if not user_id:
            flash('É necessário estar logado para cadastrar equipamentos.', 'danger')
            return redirect(url_for('auth.login'))

        dados['id_usuario_cadastro'] = user_id

        if 'data_aquisicao' in dados and dados['data_aquisicao']:
            dados['data_aquisicao'] = datetime.strptime(dados['data_aquisicao'], '%Y-%m-%d').date()

        if Equipamento.query.filter_by(patrimonio=dados.get('patrimonio')).first():
            flash('Este número de patrimônio já está cadastrado.', 'danger')
            return redirect(url_for('equipamento.listar_equipamentos'))

        if Equipamento.query.filter_by(numero_serie=dados.get('numero_serie')).first():
            flash('Este número de série já está cadastrado.', 'danger')
            return redirect(url_for('equipamento.listar_equipamentos'))

        equipamento = Equipamento(**dados)
        db.session.add(equipamento)
        db.session.commit()

        if request.is_json:
            return jsonify(equipamento.to_dict()), 201
        else:
            flash('Equipamento cadastrado com sucesso!', 'success')
            return redirect(url_for('equipamento.listar_equipamentos'))

    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'erro': str(e)}), 400
        else:
            flash(f'Erro ao cadastrar equipamento', 'danger')
            return redirect(url_for('equipamento.cadastrar_equipamento'))
        
@equipamento_bp.route('/lista', methods=['GET'])
@login_required
def listar_equipamentos():
    try:
        tipo = request.args.get('tipo')
        status = request.args.get('status')
        localizacao = request.args.get('localizacao')
        marca = request.args.get('marca')

        pesquisa = request.args.get('pesquisa', '').strip()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page',  5, type=int)

        query = Equipamento.query

        if tipo and tipo != 'all':
            query = query.filter(Equipamento.tipo.contains(tipo))
        if status and status != 'all':
            query = query.filter(Equipamento.status == status)
        if localizacao and localizacao != 'all':
            query = query.filter(Equipamento.localizacao.contains(localizacao))
        if marca and marca != 'all':
            query = query.filter(Equipamento.marca.contains(marca))

        if pesquisa:
            term = pesquisa.lower()
            query = query.filter(
                or_(
                    func.lower(Equipamento.patrimonio).contains(term),
                    func.lower(Equipamento.modelo).contains(term),
                    func.lower(Equipamento.numero_serie).contains(term),
                    func.lower(Equipamento.marca).contains(term)
                )
            )

        query = query.order_by(Equipamento.data_cadastro.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        equipamentos = pagination.items

        if request.is_json:
            return jsonify({
                'total': pagination.total,
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'equipamentos': [eq.to_dict() for eq in equipamentos]
            }), 200
        
        opcoes_filtros = {
            'localizacao': [local[0] for local in db.session.query(Equipamento.localizacao).distinct().all()],
            'tipo': [tip[0] for tip in db.session.query(Equipamento.tipo).distinct().all()]
        }
        
        return render_template('equipamentos/lista.html',
            equipamentos=equipamentos,
            pagination=pagination,
            filtros={
                'tipo': tipo,
                'status': status,
                'tipo': localizacao,
                'marca': marca,
                'pesquisa': pesquisa
            },
            opcoes_filtros=opcoes_filtros
        )

    except Exception as e:
        db.session.rollback()

        if request.is_json:
            return jsonify({'erro': str(e)}), 500
        flash(f'Erro ao listar equipamentos: {str(e)}', 'danger')

        class DummyPagination:
            def __init__(self):
                self.page = 1
                self.per_page = 5
                self.total = 0
                self.items = []
                self.has_prev = False
                self.has_next = False
                self.prev_num = None
                self.next_num = None
                
            def iter_pages(self):
                return []

        return render_template('equipamentos/lista.html', equipamentos=[], pagination=DummyPagination, filtros={}, opcoes_filtros={})

@equipamento_bp.route('/<int:id>', methods=['GET'])
@login_required
def consultar_equipamento(id):
    try:
        equipamento = Equipamento.query.get_or_404(id)

        if request.is_json:
            return jsonify(equipamento.to_dict())
        else:
            registros = (
                RegistroSuporte.query
                .filter(RegistroSuporte.id_equipamento == id)
                .order_by(RegistroSuporte.data_suporte.desc())
                .all()
            )

            return render_template('equipamentos/detalhes.html', equipamento=equipamento, registros=registros, tipos_suporte=TipoSuporte.todos(), equipamento_selecionado=equipamento)
        
    except Exception as e:
        if request.is_json:
            return jsonify({'erro': str(e)}), 404
        else:
            flash('Equipamento não encontrado.', 'danger')
            return redirect(url_for('equipamento.listar_equipamentos'))
        
@equipamento_bp.route('/<int:id>/atualizar', methods=['PUT', 'POST'])
@admin_required
def atualizar_equipamento(id):
    try:
        equipamento = Equipamento.query.get_or_404(id)

        user_id = session.get('user_id')
        if not user_id:
            if request.is_json:
                return jsonify({'erro': 'Usuário não autenticado'}), 401
            else:
                flash('É necessário estar logado.', 'danger')
                return redirect(url_for('auth.login'))

        if request.is_json:
            dados = request.get_json()
        else:
            dados = request.form.to_dict()

        campos_permitidos = ['localizacao', 'status', 'tipo', 'marca', 'modelo', 'observacoes']
        campos_atualizados = []

        for campo in campos_permitidos:
            if campo in dados and dados[campo] is not None:
                setattr(equipamento, campo, dados[campo])
                campos_atualizados.append(campo)

        equipamento.atualizar_alteracao(user_id)
        db.session.commit()

        if request.is_json:
            return jsonify({
                'mensagem': 'Equipamento atualizado com sucesso!',
                'campos_atualizados': campos_atualizados,
                'equipamento': equipamento.to_dict()
            })
        else:
            flash('Equipamento atualizado com sucesso!', 'success')
            return redirect(url_for('equipamento.consultar_equipamento', id=id))
    
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'erro': str(e)}), 400
        else:
            flash('Erro ao atualizar equipamento.' 'danger')
            return redirect(url_for('equipamento.consultar_equipamento', id=id))
        
@equipamento_bp.route('/<int:id>/desativar', methods=['POST', 'DELETE'])
@admin_required
def desativar_equipamento(id):
    try:
        equipamento = Equipamento.query.get_or_404(id)

        user_id = session.get('user_id')
        if not user_id:
            if request.is_json:
                return jsonify({'erro': 'Usuário não autenticado'}), 401
            else:
                flash('É necessário estar logado.', 'danger')
                return redirect(url_for('auth.login'))
        
        if equipamento.status == 'Desativado':
            if request.is_json:
                return jsonify({'erro': 'Equipamento já está desativado'}), 400
            else:
                flash('Equipamento já está desativado.' 'warning')
            return redirect(url_for('equipamento.consultar_equipamento', id=id))
        
        equipamento.status = 'Desativado'
        equipamento.atualizar_alteracao(user_id)
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'mensagem': 'Equipamento desativado com sucesso!',
                'equipamento': equipamento.to_dict()
            })
        else:
            flash('Equipamento desativado com sucesso!', 'success')
            return redirect(url_for('equipamento.listar_equipamentos'))
    
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'erro': str(e)}), 400
        else:
            flash(f'Erro ao desativar equipamento: {str(e)}', 'danger')
            return redirect(url_for('equipamento.consultar_equipamento', id=id))
        
@equipamento_bp.route('/exportar-csv')
@login_required
def exportar_csv():
    try:
        args = request.args.to_dict()

        export_url = url_for('csv_export.exportar_equipamento_csv', **args)
        return redirect(export_url)
        
    except Exception as e:
        flash(f'Erro ao exportar CSV: {str(e)}', 'danger')
        return redirect(url_for('equipamento.listar_equipamentos'))