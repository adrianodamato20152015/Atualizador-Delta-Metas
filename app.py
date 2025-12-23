#!/usr/bin/env python3
"""
Dashboard Web DeltaMetas 2026
Interface web moderna para visualização e gestão de metas
"""

from flask import Flask, render_template, request, jsonify, send_file
from deltametas import GerenciadorMetas, Meta, inicializar_metas_exemplo
import os
from datetime import datetime

app = Flask(__name__)
gerenciador = GerenciadorMetas()

# Inicializar com exemplos se necessário
if len(gerenciador.metas) == 0:
    inicializar_metas_exemplo(gerenciador)


@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('dashboard.html')


@app.route('/api/metas')
def api_listar_metas():
    """API: Lista todas as metas"""
    categoria = request.args.get('categoria')
    responsavel = request.args.get('responsavel')
    
    metas = gerenciador.listar_metas(categoria, responsavel)
    return jsonify([m.to_dict() for m in metas])


@app.route('/api/meta/<meta_id>')
def api_obter_meta(meta_id):
    """API: Obtém detalhes de uma meta específica"""
    meta = gerenciador.obter_meta(meta_id)
    if meta:
        return jsonify(meta.to_dict())
    return jsonify({"error": "Meta não encontrada"}), 404


@app.route('/api/meta', methods=['POST'])
def api_adicionar_meta():
    """API: Adiciona uma nova meta"""
    dados = request.json
    
    meta = Meta(
        dados['id'],
        dados['titulo'],
        dados['descricao'],
        dados['responsavel'],
        dados['prazo'],
        float(dados['valor_alvo']),
        dados.get('unidade', '%'),
        dados.get('categoria', 'Geral')
    )
    
    gerenciador.adicionar_meta(meta)
    return jsonify({"success": True, "meta": meta.to_dict()})


@app.route('/api/meta/<meta_id>/atualizar', methods=['POST'])
def api_atualizar_meta(meta_id):
    """API: Atualiza o progresso de uma meta"""
    dados = request.json
    novo_valor = float(dados['valor'])
    observacao = dados.get('observacao', '')
    
    sucesso = gerenciador.atualizar_meta(meta_id, novo_valor, observacao)
    
    if sucesso:
        meta = gerenciador.obter_meta(meta_id)
        return jsonify({"success": True, "meta": meta.to_dict()})
    return jsonify({"error": "Meta não encontrada"}), 404


@app.route('/api/relatorio')
def api_relatorio():
    """API: Retorna relatório consolidado"""
    relatorio = gerenciador.gerar_relatorio()
    return jsonify(relatorio)


@app.route('/api/exportar-excel')
def api_exportar_excel():
    """API: Exporta relatório em Excel"""
    arquivo = "relatorio_metas_2026.xlsx"
    gerenciador.exportar_excel(arquivo)
    return send_file(arquivo, as_attachment=True)


@app.route('/api/categorias')
def api_categorias():
    """API: Lista todas as categorias únicas"""
    categorias = list(set(m.categoria for m in gerenciador.metas))
    return jsonify(sorted(categorias))


@app.route('/api/responsaveis')
def api_responsaveis():
    """API: Lista todos os responsáveis únicos"""
    responsaveis = list(set(m.responsavel for m in gerenciador.metas))
    return jsonify(sorted(responsaveis))


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Iniciando Dashboard DeltaMetas 2026")
    print("=" * 60)
    print(f"📊 Metas carregadas: {len(gerenciador.metas)}")
    print("🌐 Acesse: http://localhost:5000")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
