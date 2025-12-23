#!/usr/bin/env python3
"""
Script de exemplo para demonstrar uso da API do DeltaMetas
"""

from deltametas import GerenciadorMetas, Meta

def exemplo_basico():
    """Exemplo básico de uso do sistema"""
    print("=" * 60)
    print("Exemplo de Uso - DeltaMetas 2026")
    print("=" * 60)
    print()
    
    # Criar gerenciador
    gerenciador = GerenciadorMetas("metas_exemplo.json")
    
    # Adicionar uma nova meta
    print("1. Adicionando nova meta...")
    nova_meta = Meta(
        id="META-EXEMPLO-001",
        titulo="Capacitação da Equipe",
        descricao="Treinar toda equipe em novas metodologias de gestão",
        responsavel="Coordenação Geral",
        prazo="2026-06-30",
        valor_alvo=100.0,
        unidade="%",
        categoria="Desenvolvimento"
    )
    gerenciador.adicionar_meta(nova_meta)
    print("   ✓ Meta criada com sucesso!")
    print()
    
    # Atualizar progresso
    print("2. Atualizando progresso...")
    gerenciador.atualizar_meta(
        "META-EXEMPLO-001",
        25.0,
        "Primeira fase de capacitação concluída"
    )
    print("   ✓ Progresso atualizado para 25%")
    print()
    
    # Consultar meta
    print("3. Consultando meta...")
    meta = gerenciador.obter_meta("META-EXEMPLO-001")
    if meta:
        print(f"   Título: {meta.titulo}")
        print(f"   Progresso: {meta.calcular_progresso():.1f}%")
        print(f"   Status: {meta.status}")
    print()
    
    # Gerar relatório
    print("4. Gerando relatório...")
    relatorio = gerenciador.gerar_relatorio()
    print(f"   Total de metas: {relatorio['resumo']['total_metas']}")
    print(f"   Progresso médio: {relatorio['resumo']['progresso_medio']:.1f}%")
    print()
    
    # Exportar para Excel
    print("5. Exportando para Excel...")
    gerenciador.exportar_excel("exemplo_relatorio.xlsx")
    print("   ✓ Arquivo 'exemplo_relatorio.xlsx' criado!")
    print()
    
    print("=" * 60)
    print("Exemplo concluído com sucesso!")
    print("=" * 60)


def exemplo_multiplas_metas():
    """Exemplo com múltiplas metas e categorias"""
    print("\nExemplo: Criando múltiplas metas...")
    
    gerenciador = GerenciadorMetas("metas_multiplas.json")
    
    metas = [
        ("META-A1", "Análise de Impacto Ambiental", "Ambiental", 50.0),
        ("META-A2", "Recuperação de Áreas Degradadas", "Ambiental", 10.0),
        ("META-E1", "Workshop Comunitário", "Educação", 5.0),
        ("META-E2", "Material Educativo", "Educação", 1000.0),
    ]
    
    for meta_id, titulo, categoria, valor_alvo in metas:
        meta = Meta(
            id=meta_id,
            titulo=titulo,
            descricao=f"Descrição da {titulo}",
            responsavel=f"Equipe {categoria}",
            prazo="2026-12-31",
            valor_alvo=valor_alvo,
            categoria=categoria
        )
        gerenciador.adicionar_meta(meta)
    
    print(f"✓ {len(metas)} metas criadas!")
    
    # Listar por categoria
    print("\nMetas por categoria:")
    for categoria in ["Ambiental", "Educação"]:
        metas_cat = gerenciador.listar_metas(filtro_categoria=categoria)
        print(f"  {categoria}: {len(metas_cat)} metas")


if __name__ == "__main__":
    # Executar exemplos
    exemplo_basico()
    exemplo_multiplas_metas()
    
    print("\n" + "=" * 60)
    print("Todos os exemplos foram executados!")
    print("Verifique os arquivos gerados:")
    print("  - metas_exemplo.json")
    print("  - exemplo_relatorio.xlsx")
    print("  - metas_multiplas.json")
    print("=" * 60)
