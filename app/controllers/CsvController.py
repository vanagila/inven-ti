from flask import Blueprint, request, jsonify, Response
from app.models.Equipamento import Equipamento
from app.models.RegistroSuporte import RegistroSuporte
import io
import csv
from datetime import datetime
from sqlalchemy import func, or_
from app.decorators import login_required

csv_bp = Blueprint('csv_export', __name__, url_prefix='/exportar')

@csv_bp.route('/equipamentos/csv')
@login_required
def exportar_equipamento_csv():
    try:
        equipamentos = Equipamento.query.order_by(Equipamento.data_cadastro.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)
        
        writer.writerow([
            'ID', 'Patrimônio', 'Tipo', 'Marca', 'Modelo', 
            'Número Série', 'Data Aquisição', 'Localização', 
            'Status', 'Observações', 'Data Cadastro', 
            'Data Última Alteração', 'ID Usuário Cadastro',
            'ID Usuário Última Alteração'
        ])
        
        for equipamento in equipamentos:
            writer.writerow([
                equipamento.id,
                equipamento.patrimonio or '',
                equipamento.tipo or '',
                equipamento.marca or '',
                equipamento.modelo or '',
                equipamento.numero_serie or '',
                equipamento.data_aquisicao.strftime('%d/%m/%Y') if equipamento.data_aquisicao else '',
                equipamento.localizacao or '',
                equipamento.status or '',
                equipamento.observacoes or '',
                equipamento.data_cadastro.strftime('%d/%m/%Y %H:%M') if equipamento.data_cadastro else '',
                equipamento.data_ultima_alteracao.strftime('%d/%m/%Y %H:%M') if equipamento.data_ultima_alteracao else '',
                equipamento.id_usuario_cadastro or '',
                equipamento.id_usuario_ultima_alteracao or ''
            ])
        
        output.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"relatorio_completo_equipamentos_{timestamp}.csv"
        
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
        
    except Exception as e:
        return jsonify({'error': f'Erro ao exportar relatório: {str(e)}'}), 500

@csv_bp.route('/registro-suporte/csv')
@login_required
def exportar_suporte_csv():
    try:
        equipamento = request.args.get('equipamento')
        tipo_suporte = request.args.get('tipo_suporte')
        responsavel = request.args.get('responsavel')
        data_suporte = request.args.get('data_suporte')

        pesquisa = request.args.get('pesquisa', '').strip()

        query = (
            RegistroSuporte.query
            .join(Equipamento, RegistroSuporte.id_equipamento == Equipamento.id)

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
                    func.lower(RegistroSuporte.responsavel).contains(term),
                    func.lower(RegistroSuporte.descricao).contains(term)
                )
            )
        
        registros = query.order_by(RegistroSuporte.data_suporte.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)

        writer.writerow([
            'ID', 'ID Equipamento', 'ID Usuário', 'Descrição', 'Data Suporte', 'Tipo Suporte', 'Responsável', 'Custo'
        ])

        for registro in registros:
            writer.writerow([
                registro.id,
                registro.id_equipamento or '',
                registro.id_usuario or '',
                registro.descricao or '',
                registro.data_suporte.strftime('%d/%m/%Y') if registro.data_suporte else '',
                registro.tipo_suporte or '',
                registro.responsavel or '',
                registro.custo or '0.00'
            ])

        output.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"registro_suporte_{timestamp}.csv"

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
        
    except Exception as e:
        return jsonify({'error': f'Erro ao exportar equipamentos: {str(e)}'}), 500