from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.database.connection import db
from app.models import Equipamento, Usuario
from app.models.RegistroSuporte import RegistroSuporte
from datetime import datetime
from sqlalchemy import or_, func

registro_suporte_bp = Blueprint('registro_suporte', __name__, url_prefix='/registro-suporte')

@registro_suporte_bp.route('/', methods=['GET', 'POST'])
def registrar_suporte():
    if request.method == 'GET':
        equipamentos = Equipamento.query.all()
        responsaveis = Usuario.query.all()

        equipamento_id = request.args.get('id_equipamento')
        equipamento_selecionado = Equipamento.query.get(equipamento_id)

        return render_template(
                'suporte/cadastro.html',
                equipamentos=equipamentos,
                responsaveis=responsaveis,
                equipamento_selecionado=equipamento_selecionado
        )
            
    try:
        if request.is_json:
            dados = request.get_json()
        else:
            dados = request.form.to_dict()

        dados['id_usuario'] = session['user_id']

        if 'data_suporte' in dados and dados['data_suporte']:
            dados['data_suporte'] = datetime.strptime(dados['data_suporte'], '%Y-%m-%d').date()

        registro = RegistroSuporte(**dados)
        db.session.add(registro)
        db.session.commit()

        if request.is_json:
            return jsonify(registro.to_dict()), 201
        else:
            flash('Registro de suporte cadastrado com sucesso!', 'success')
            return redirect(url_for('equipamento.consultar_equipamento', id=dados['id_equipamento']))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'erro': str(e)}), 400
        else:
            flash(f'Erro ao cadastrar registro: {str(e)}', 'danger')
            equipamentos = Equipamento.query.all()
            responsaveis = Usuario.query.all()
            equipamento_selecionado = Equipamento.query.get(equipamento_id)
                
            return render_template('suporte/cadastro.html', 
                     dados=dados,
                     equipamentos=equipamentos,
                     responsaveis=responsaveis,
                     equipamento_selecionado=equipamento_selecionado)
        
@registro_suporte_bp.route('/lista', methods=['GET'])
def listar_registros():
    try:
        equipamento = request.args.get('equipamento')
        tipo_suporte = request.args.get('tipo_suporte')
        responsavel = request.args.get('responsavel')
        data_suporte = request.args.get('data_suporte')

        pesquisa = request.args.get('pesquisa', '').strip()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page',  5, type=int)

        query = (
            RegistroSuporte.query
            .join(Equipamento, RegistroSuporte.id_equipamento == Equipamento.id)
            .outerjoin(Usuario, RegistroSuporte.id_usuario == Usuario.id)
        )


        if equipamento and equipamento != 'all':
            equipamento_id = int(equipamento)
            query = query.filter(Equipamento.id == equipamento_id)
        if tipo_suporte and tipo_suporte != 'all':
            query = query.filter(RegistroSuporte.tipo_suporte == tipo_suporte)
        if responsavel and responsavel != 'all':
            query = query.filter(RegistroSuporte.responsavel == responsavel)
        if data_suporte:
            try:
                data_suporte = datetime.strptime(data_suporte, '%Y-%m-%d').date()
                query = query.filter(func.date(RegistroSuporte.data_suporte) == data_suporte)
            except ValueError:
                pass

        if pesquisa:
            term = pesquisa.lower()
            query = query.filter(
                or_(
                    func.lower(Equipamento.patrimonio).contains(term),
                    func.lower(Equipamento.modelo).contains(term),
                    func.lower(Equipamento.marca).contains(term),
                    func.lower(Usuario.nome).contains(term),
                    func.lower(RegistroSuporte.descricao).contains(term)
                )
            )
        
        query = query.order_by(RegistroSuporte.data_suporte.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        registros = pagination.items
        
        if request.is_json:
            return jsonify({
                'total': pagination.total,
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'registros': [registro.to_dict() for registro in registros ]
            }), 200
        
        opcoes_filtros = {
            'tipo_suporte': [tipo[0] for tipo in db.session.query(RegistroSuporte.tipo_suporte).distinct().all()],
            'responsavel': [{'id': t[1], 'nome': t[0]} for t in db.session.query(Usuario.nome, Usuario.id).all()],
            'equipamentos': [{'id': e[0], 'descricao': f"{e[1]} - {e[2]} {e[3]}"} for e in db.session.query(Equipamento.id, Equipamento.patrimonio, Equipamento.marca, Equipamento.modelo).all()]
        }

        return render_template('suporte/lista.html',
            registros=registros,
            pagination=pagination,
            filtros={
                'equipamento': equipamento,
                'tipo_suporte': tipo_suporte,
                'responsavel': responsavel,
                'data_suporte': data_suporte,
                'pesquisa': pesquisa
            },
            opcoes_filtros=opcoes_filtros
            
        )
    
    except Exception as e:
        db.session.rollback()

        if request.is_json:
            return jsonify({'erro': str(e)}), 500
        flash(f'Erro ao listar registros: {str(e)}', 'danger')
        return render_template('suporte/lista.html',
            registros=[], pagination=None, filtros={}, opcoes_filtros={})