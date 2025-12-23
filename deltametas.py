#!/usr/bin/env python3
"""
DeltaMetas 2026 - Sistema de Acompanhamento de Metas
Monitoramento moderno de metas da APA Delta do Parnaíba
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd


class Meta:
    """Representa uma meta individual"""
    
    def __init__(self, id: str, titulo: str, descricao: str, 
                 responsavel: str, prazo: str, valor_alvo: float,
                 unidade: str = "%", categoria: str = "Geral"):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.responsavel = responsavel
        self.prazo = prazo
        self.valor_alvo = valor_alvo
        self.valor_atual = 0.0
        self.unidade = unidade
        self.categoria = categoria
        self.historico = []
        self.data_criacao = datetime.now().isoformat()
        self.status = "Em Andamento"
        
    def atualizar_progresso(self, novo_valor: float, observacao: str = ""):
        """Atualiza o progresso da meta"""
        self.valor_atual = novo_valor
        self.historico.append({
            "data": datetime.now().isoformat(),
            "valor": novo_valor,
            "observacao": observacao
        })
        
        # Atualizar status baseado no progresso
        progresso_percentual = (self.valor_atual / self.valor_alvo) * 100
        if progresso_percentual >= 100:
            self.status = "Concluída"
        elif progresso_percentual >= 75:
            self.status = "Em Progresso Avançado"
        elif progresso_percentual >= 50:
            self.status = "Em Andamento"
        elif progresso_percentual >= 25:
            self.status = "Iniciada"
        else:
            self.status = "Atrasada"
    
    def calcular_progresso(self) -> float:
        """Calcula o percentual de progresso"""
        if self.valor_alvo == 0:
            return 0.0
        return (self.valor_atual / self.valor_alvo) * 100
    
    def to_dict(self) -> dict:
        """Converte a meta para dicionário"""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "responsavel": self.responsavel,
            "prazo": self.prazo,
            "valor_alvo": self.valor_alvo,
            "valor_atual": self.valor_atual,
            "unidade": self.unidade,
            "categoria": self.categoria,
            "progresso": self.calcular_progresso(),
            "status": self.status,
            "historico": self.historico,
            "data_criacao": self.data_criacao
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Meta':
        """Cria uma meta a partir de um dicionário"""
        meta = Meta(
            data["id"], data["titulo"], data["descricao"],
            data["responsavel"], data["prazo"], data["valor_alvo"],
            data.get("unidade", "%"), data.get("categoria", "Geral")
        )
        meta.valor_atual = data.get("valor_atual", 0.0)
        meta.historico = data.get("historico", [])
        meta.data_criacao = data.get("data_criacao", datetime.now().isoformat())
        meta.status = data.get("status", "Em Andamento")
        return meta


class GerenciadorMetas:
    """Gerenciador central de metas do DeltaMetas 2026"""
    
    def __init__(self, arquivo_dados: str = "metas_2026.json"):
        self.arquivo_dados = arquivo_dados
        self.metas: List[Meta] = []
        self.carregar_metas()
    
    def carregar_metas(self):
        """Carrega metas do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.metas = [Meta.from_dict(m) for m in dados]
    
    def salvar_metas(self):
        """Salva metas no arquivo JSON"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            dados = [m.to_dict() for m in self.metas]
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    def adicionar_meta(self, meta: Meta):
        """Adiciona uma nova meta"""
        self.metas.append(meta)
        self.salvar_metas()
    
    def obter_meta(self, meta_id: str) -> Optional[Meta]:
        """Obtém uma meta pelo ID"""
        for meta in self.metas:
            if meta.id == meta_id:
                return meta
        return None
    
    def atualizar_meta(self, meta_id: str, novo_valor: float, observacao: str = ""):
        """Atualiza o progresso de uma meta"""
        meta = self.obter_meta(meta_id)
        if meta:
            meta.atualizar_progresso(novo_valor, observacao)
            self.salvar_metas()
            return True
        return False
    
    def listar_metas(self, filtro_categoria: Optional[str] = None, 
                     filtro_responsavel: Optional[str] = None) -> List[Meta]:
        """Lista metas com filtros opcionais"""
        metas_filtradas = self.metas
        
        if filtro_categoria:
            metas_filtradas = [m for m in metas_filtradas if m.categoria == filtro_categoria]
        
        if filtro_responsavel:
            metas_filtradas = [m for m in metas_filtradas if m.responsavel == filtro_responsavel]
        
        return metas_filtradas
    
    def gerar_relatorio(self) -> Dict:
        """Gera relatório consolidado das metas"""
        total_metas = len(self.metas)
        metas_concluidas = len([m for m in self.metas if m.status == "Concluída"])
        metas_em_andamento = len([m for m in self.metas if m.status in ["Em Andamento", "Em Progresso Avançado", "Iniciada"]])
        metas_atrasadas = len([m for m in self.metas if m.status == "Atrasada"])
        
        progresso_medio = sum(m.calcular_progresso() for m in self.metas) / total_metas if total_metas > 0 else 0
        
        # Agrupar por categoria
        categorias = {}
        for meta in self.metas:
            if meta.categoria not in categorias:
                categorias[meta.categoria] = []
            categorias[meta.categoria].append(meta.to_dict())
        
        # Agrupar por responsável
        responsaveis = {}
        for meta in self.metas:
            if meta.responsavel not in responsaveis:
                responsaveis[meta.responsavel] = []
            responsaveis[meta.responsavel].append(meta.to_dict())
        
        return {
            "data_relatorio": datetime.now().isoformat(),
            "resumo": {
                "total_metas": total_metas,
                "metas_concluidas": metas_concluidas,
                "metas_em_andamento": metas_em_andamento,
                "metas_atrasadas": metas_atrasadas,
                "progresso_medio": round(progresso_medio, 2),
                "taxa_conclusao": round((metas_concluidas / total_metas * 100) if total_metas > 0 else 0, 2)
            },
            "por_categoria": categorias,
            "por_responsavel": responsaveis,
            "todas_metas": [m.to_dict() for m in self.metas]
        }
    
    def exportar_excel(self, arquivo_saida: str = "relatorio_metas_2026.xlsx"):
        """Exporta relatório para Excel"""
        relatorio = self.gerar_relatorio()
        
        # Criar DataFrame com todas as metas
        dados_metas = []
        for meta in self.metas:
            dados_metas.append({
                "ID": meta.id,
                "Título": meta.titulo,
                "Descrição": meta.descricao,
                "Responsável": meta.responsavel,
                "Categoria": meta.categoria,
                "Prazo": meta.prazo,
                "Valor Alvo": meta.valor_alvo,
                "Valor Atual": meta.valor_atual,
                "Unidade": meta.unidade,
                "Progresso (%)": round(meta.calcular_progresso(), 2),
                "Status": meta.status,
                "Data Criação": meta.data_criacao
            })
        
        df_metas = pd.DataFrame(dados_metas)
        
        # Criar DataFrame do resumo
        resumo = relatorio["resumo"]
        df_resumo = pd.DataFrame([resumo])
        
        # Salvar em Excel com múltiplas abas
        with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
            df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
            df_metas.to_excel(writer, sheet_name='Todas as Metas', index=False)
            
            # Criar aba por categoria
            for categoria, metas in relatorio["por_categoria"].items():
                df_cat = pd.DataFrame(metas)
                if not df_cat.empty:
                    df_cat.to_excel(writer, sheet_name=f'Cat_{categoria[:20]}', index=False)
        
        print(f"Relatório exportado para: {arquivo_saida}")


def inicializar_metas_exemplo(gerenciador: GerenciadorMetas):
    """Inicializa o sistema com metas de exemplo para 2026"""
    metas_exemplo = [
        Meta(
            "META-001", 
            "Preservação da Biodiversidade",
            "Aumentar área de preservação de espécies nativas",
            "Equipe Ambiental",
            "2026-12-31",
            100.0,
            "%",
            "Ambiental"
        ),
        Meta(
            "META-002",
            "Educação Ambiental",
            "Realizar programas educacionais nas comunidades locais",
            "Equipe Educação",
            "2026-06-30",
            50.0,
            "eventos",
            "Educação"
        ),
        Meta(
            "META-003",
            "Monitoramento de Água",
            "Implementar pontos de monitoramento de qualidade da água",
            "Equipe Técnica",
            "2026-09-30",
            25.0,
            "pontos",
            "Monitoramento"
        ),
        Meta(
            "META-004",
            "Reflorestamento",
            "Plantar mudas nativas na região do Delta",
            "Equipe Ambiental",
            "2026-12-31",
            10000.0,
            "mudas",
            "Ambiental"
        ),
        Meta(
            "META-005",
            "Engajamento Comunitário",
            "Envolver comunidades locais em ações de preservação",
            "Equipe Social",
            "2026-08-31",
            200.0,
            "pessoas",
            "Social"
        )
    ]
    
    for meta in metas_exemplo:
        gerenciador.adicionar_meta(meta)
    
    # Adicionar progresso inicial em algumas metas
    gerenciador.atualizar_meta("META-001", 35.0, "Progresso inicial - áreas mapeadas")
    gerenciador.atualizar_meta("META-002", 15.0, "15 eventos realizados")
    gerenciador.atualizar_meta("META-003", 8.0, "8 pontos instalados")
    gerenciador.atualizar_meta("META-004", 3500.0, "3500 mudas plantadas no 1º trimestre")
    gerenciador.atualizar_meta("META-005", 85.0, "85 pessoas engajadas")


if __name__ == "__main__":
    print("=" * 60)
    print("DeltaMetas 2026 - Sistema de Acompanhamento de Metas")
    print("APA Delta do Parnaíba")
    print("=" * 60)
    print()
    
    gerenciador = GerenciadorMetas()
    
    # Se não houver metas, inicializar com exemplos
    if len(gerenciador.metas) == 0:
        print("Inicializando sistema com metas de exemplo para 2026...")
        inicializar_metas_exemplo(gerenciador)
        print(f"✓ {len(gerenciador.metas)} metas criadas com sucesso!")
        print()
    
    # Gerar e exibir relatório
    relatorio = gerenciador.gerar_relatorio()
    resumo = relatorio["resumo"]
    
    print("\n📊 RESUMO EXECUTIVO")
    print("-" * 60)
    print(f"Total de Metas: {resumo['total_metas']}")
    print(f"Metas Concluídas: {resumo['metas_concluidas']}")
    print(f"Metas em Andamento: {resumo['metas_em_andamento']}")
    print(f"Metas Atrasadas: {resumo['metas_atrasadas']}")
    print(f"Progresso Médio: {resumo['progresso_medio']:.2f}%")
    print(f"Taxa de Conclusão: {resumo['taxa_conclusao']:.2f}%")
    print()
    
    print("\n📋 METAS POR CATEGORIA")
    print("-" * 60)
    for categoria, metas in relatorio["por_categoria"].items():
        print(f"\n{categoria}: {len(metas)} metas")
        for meta in metas:
            print(f"  • {meta['titulo']}: {meta['progresso']:.1f}% - {meta['status']}")
    
    print("\n\n👥 METAS POR RESPONSÁVEL")
    print("-" * 60)
    for responsavel, metas in relatorio["por_responsavel"].items():
        progresso_medio = sum(m['progresso'] for m in metas) / len(metas)
        print(f"\n{responsavel}: {len(metas)} metas (Progresso médio: {progresso_medio:.1f}%)")
        for meta in metas:
            print(f"  • {meta['titulo']}: {meta['progresso']:.1f}%")
    
    # Exportar para Excel
    print("\n\n📁 Exportando relatório...")
    gerenciador.exportar_excel()
    
    print("\n✓ Sistema DeltaMetas 2026 executado com sucesso!")
    print("  Arquivo de dados: metas_2026.json")
    print("  Relatório Excel: relatorio_metas_2026.xlsx")
