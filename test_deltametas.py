#!/usr/bin/env python3
"""
Testes do Sistema DeltaMetas 2026
Valida funcionalidades principais do sistema
"""

import unittest
import json
import os
from deltametas import Meta, GerenciadorMetas, inicializar_metas_exemplo
from app import app


class TestMeta(unittest.TestCase):
    """Testes da classe Meta"""
    
    def test_criar_meta(self):
        """Testa criação de uma meta"""
        meta = Meta(
            "TEST-001",
            "Teste Meta",
            "Descrição teste",
            "Equipe Teste",
            "2026-12-31",
            100.0
        )
        self.assertEqual(meta.id, "TEST-001")
        self.assertEqual(meta.titulo, "Teste Meta")
        self.assertEqual(meta.valor_alvo, 100.0)
        self.assertEqual(meta.valor_atual, 0.0)
    
    def test_atualizar_progresso(self):
        """Testa atualização de progresso"""
        meta = Meta("TEST-002", "Test", "Desc", "Resp", "2026-12-31", 100.0)
        meta.atualizar_progresso(50.0, "Metade completa")
        
        self.assertEqual(meta.valor_atual, 50.0)
        self.assertEqual(len(meta.historico), 1)
        self.assertEqual(meta.historico[0]["valor"], 50.0)
    
    def test_calcular_progresso(self):
        """Testa cálculo de progresso percentual"""
        meta = Meta("TEST-003", "Test", "Desc", "Resp", "2026-12-31", 200.0)
        meta.valor_atual = 50.0
        
        self.assertEqual(meta.calcular_progresso(), 25.0)
    
    def test_status_automatico(self):
        """Testa atualização automática de status"""
        meta = Meta("TEST-004", "Test", "Desc", "Resp", "2026-12-31", 100.0)
        
        # Status: Atrasada
        meta.atualizar_progresso(10.0)
        self.assertEqual(meta.status, "Atrasada")
        
        # Status: Iniciada
        meta.atualizar_progresso(30.0)
        self.assertEqual(meta.status, "Iniciada")
        
        # Status: Em Andamento
        meta.atualizar_progresso(60.0)
        self.assertEqual(meta.status, "Em Andamento")
        
        # Status: Em Progresso Avançado
        meta.atualizar_progresso(80.0)
        self.assertEqual(meta.status, "Em Progresso Avançado")
        
        # Status: Concluída
        meta.atualizar_progresso(100.0)
        self.assertEqual(meta.status, "Concluída")
    
    def test_conversao_dict(self):
        """Testa conversão de/para dicionário"""
        meta = Meta("TEST-005", "Test", "Desc", "Resp", "2026-12-31", 100.0)
        meta_dict = meta.to_dict()
        
        self.assertIn("id", meta_dict)
        self.assertIn("titulo", meta_dict)
        self.assertIn("progresso", meta_dict)
        
        meta_restaurada = Meta.from_dict(meta_dict)
        self.assertEqual(meta_restaurada.id, meta.id)
        self.assertEqual(meta_restaurada.titulo, meta.titulo)


class TestGerenciadorMetas(unittest.TestCase):
    """Testes da classe GerenciadorMetas"""
    
    def setUp(self):
        """Prepara ambiente de teste"""
        self.arquivo_teste = "test_metas.json"
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)
        self.gerenciador = GerenciadorMetas(self.arquivo_teste)
    
    def tearDown(self):
        """Limpa após teste"""
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)
    
    def test_adicionar_meta(self):
        """Testa adição de meta"""
        meta = Meta("TEST-006", "Test", "Desc", "Resp", "2026-12-31", 100.0)
        self.gerenciador.adicionar_meta(meta)
        
        self.assertEqual(len(self.gerenciador.metas), 1)
        self.assertTrue(os.path.exists(self.arquivo_teste))
    
    def test_obter_meta(self):
        """Testa busca de meta por ID"""
        meta = Meta("TEST-007", "Test", "Desc", "Resp", "2026-12-31", 100.0)
        self.gerenciador.adicionar_meta(meta)
        
        meta_encontrada = self.gerenciador.obter_meta("TEST-007")
        self.assertIsNotNone(meta_encontrada)
        self.assertEqual(meta_encontrada.id, "TEST-007")
        
        meta_inexistente = self.gerenciador.obter_meta("INEXISTENTE")
        self.assertIsNone(meta_inexistente)
    
    def test_atualizar_meta(self):
        """Testa atualização de meta"""
        meta = Meta("TEST-008", "Test", "Desc", "Resp", "2026-12-31", 100.0)
        self.gerenciador.adicionar_meta(meta)
        
        sucesso = self.gerenciador.atualizar_meta("TEST-008", 75.0, "Observação")
        self.assertTrue(sucesso)
        
        meta_atualizada = self.gerenciador.obter_meta("TEST-008")
        self.assertEqual(meta_atualizada.valor_atual, 75.0)
    
    def test_listar_metas_filtros(self):
        """Testa listagem com filtros"""
        meta1 = Meta("TEST-009", "Test1", "Desc", "Resp1", "2026-12-31", 100.0, categoria="Cat1")
        meta2 = Meta("TEST-010", "Test2", "Desc", "Resp2", "2026-12-31", 100.0, categoria="Cat2")
        meta3 = Meta("TEST-011", "Test3", "Desc", "Resp1", "2026-12-31", 100.0, categoria="Cat1")
        
        self.gerenciador.adicionar_meta(meta1)
        self.gerenciador.adicionar_meta(meta2)
        self.gerenciador.adicionar_meta(meta3)
        
        # Filtro por categoria
        metas_cat1 = self.gerenciador.listar_metas(filtro_categoria="Cat1")
        self.assertEqual(len(metas_cat1), 2)
        
        # Filtro por responsável
        metas_resp1 = self.gerenciador.listar_metas(filtro_responsavel="Resp1")
        self.assertEqual(len(metas_resp1), 2)
    
    def test_gerar_relatorio(self):
        """Testa geração de relatório"""
        meta1 = Meta("TEST-012", "Test1", "Desc", "Resp", "2026-12-31", 100.0)
        meta1.atualizar_progresso(50.0)
        meta2 = Meta("TEST-013", "Test2", "Desc", "Resp", "2026-12-31", 100.0)
        meta2.atualizar_progresso(100.0)
        
        self.gerenciador.adicionar_meta(meta1)
        self.gerenciador.adicionar_meta(meta2)
        
        relatorio = self.gerenciador.gerar_relatorio()
        
        self.assertIn("resumo", relatorio)
        self.assertEqual(relatorio["resumo"]["total_metas"], 2)
        self.assertEqual(relatorio["resumo"]["metas_concluidas"], 1)
        self.assertEqual(relatorio["resumo"]["progresso_medio"], 75.0)
    
    def test_persistencia(self):
        """Testa persistência em arquivo JSON"""
        meta = Meta("TEST-014", "Test", "Desc", "Resp", "2026-12-31", 100.0)
        self.gerenciador.adicionar_meta(meta)
        
        # Carregar em novo gerenciador
        gerenciador2 = GerenciadorMetas(self.arquivo_teste)
        self.assertEqual(len(gerenciador2.metas), 1)
        
        meta_carregada = gerenciador2.obter_meta("TEST-014")
        self.assertIsNotNone(meta_carregada)
        self.assertEqual(meta_carregada.titulo, "Test")


class TestWebApp(unittest.TestCase):
    """Testes da aplicação web"""
    
    def setUp(self):
        """Configura app para testes"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_dashboard_page(self):
        """Testa carregamento da página do dashboard"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DeltaMetas 2026', response.data)
    
    def test_api_metas(self):
        """Testa API de listagem de metas"""
        response = self.client.get('/api/metas')
        self.assertEqual(response.status_code, 200)
        
        dados = json.loads(response.data)
        self.assertIsInstance(dados, list)
        self.assertGreater(len(dados), 0)
    
    def test_api_relatorio(self):
        """Testa API de relatório"""
        response = self.client.get('/api/relatorio')
        self.assertEqual(response.status_code, 200)
        
        dados = json.loads(response.data)
        self.assertIn('resumo', dados)
        self.assertIn('total_metas', dados['resumo'])
    
    def test_api_categorias(self):
        """Testa API de categorias"""
        response = self.client.get('/api/categorias')
        self.assertEqual(response.status_code, 200)
        
        categorias = json.loads(response.data)
        self.assertIsInstance(categorias, list)
    
    def test_api_responsaveis(self):
        """Testa API de responsáveis"""
        response = self.client.get('/api/responsaveis')
        self.assertEqual(response.status_code, 200)
        
        responsaveis = json.loads(response.data)
        self.assertIsInstance(responsaveis, list)
    
    def test_api_filtros(self):
        """Testa API com filtros"""
        # Com filtro de categoria
        response = self.client.get('/api/metas?categoria=Ambiental')
        self.assertEqual(response.status_code, 200)
        
        dados = json.loads(response.data)
        self.assertIsInstance(dados, list)


def executar_testes():
    """Executa todos os testes"""
    print("=" * 70)
    print("DeltaMetas 2026 - Suite de Testes")
    print("=" * 70)
    print()
    
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestMeta))
    suite.addTests(loader.loadTestsFromTestCase(TestGerenciadorMetas))
    suite.addTests(loader.loadTestsFromTestCase(TestWebApp))
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Resumo
    print()
    print("=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"Testes executados: {resultado.testsRun}")
    print(f"Sucessos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")
    print("=" * 70)
    
    return resultado.wasSuccessful()


if __name__ == '__main__':
    sucesso = executar_testes()
    exit(0 if sucesso else 1)
