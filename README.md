# 🌊 DeltaMetas 2026 - Sistema de Gestão de Metas

Sistema moderno de acompanhamento e gestão de metas da APA Delta do Parnaíba.

## 🎯 Visão Geral

O **DeltaMetas 2026** é uma plataforma completa para monitoramento e gestão de metas, desenvolvida para proporcionar à equipe uma nova forma de gestão com:

- ✅ Dashboard interativo e visual
- 📊 Relatórios consolidados e exportação para Excel
- 🎯 Acompanhamento de progresso em tempo real
- 👥 Gestão por responsável e categoria
- 📈 Histórico de atualizações
- 🔄 Sistema de status automático baseado no progresso

## 🚀 Funcionalidades Principais

### 1. Dashboard Web Interativo
- Interface moderna e responsiva
- Visualização de estatísticas em tempo real
- Filtros por categoria e responsável
- Atualização de progresso inline
- Exportação de relatórios

### 2. Sistema de Gestão de Metas
- Criação e gerenciamento de metas
- Categorização e atribuição de responsáveis
- Acompanhamento de valores alvo e valores atuais
- Histórico completo de atualizações

### 3. Relatórios e Analytics
- Resumo executivo automático
- Agrupamento por categoria e responsável
- Cálculo de progresso médio e taxa de conclusão
- Exportação para Excel com múltiplas abas

### 4. Status Automático
O sistema atualiza automaticamente o status das metas baseado no progresso:
- **Concluída**: ≥ 100% do valor alvo
- **Em Progresso Avançado**: 75-99% do valor alvo
- **Em Andamento**: 50-74% do valor alvo
- **Iniciada**: 25-49% do valor alvo
- **Atrasada**: < 25% do valor alvo

## 📦 Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone o repositório:
```bash
git clone https://github.com/adrianodamato20152015/Atualizador-Delta-Metas.git
cd Atualizador-Delta-Metas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

### Modo 1: Dashboard Web (Recomendado)

1. Inicie o servidor web:
```bash
python app.py
```

2. Acesse no navegador:
```
http://localhost:5000
```

3. Use o dashboard para:
   - Visualizar todas as metas
   - Filtrar por categoria ou responsável
   - Atualizar progresso das metas
   - Exportar relatórios em Excel

### Modo 2: Linha de Comando

Execute o sistema via terminal:
```bash
python deltametas.py
```

Isso irá:
- Carregar ou criar metas de exemplo
- Exibir resumo executivo
- Gerar relatório Excel
- Criar arquivo JSON com os dados

## 📁 Estrutura de Arquivos

```
Atualizador-Delta-Metas/
├── README.md                    # Documentação
├── requirements.txt             # Dependências Python
├── deltametas.py               # Motor principal do sistema
├── app.py                      # Servidor web Flask
├── templates/
│   └── dashboard.html          # Interface web
├── metas_2026.json            # Dados das metas (gerado)
└── relatorio_metas_2026.xlsx  # Relatório Excel (gerado)
```

## 📊 Exemplos de Uso

### Adicionar Nova Meta (via Python)

```python
from deltametas import GerenciadorMetas, Meta

gerenciador = GerenciadorMetas()

nova_meta = Meta(
    id="META-006",
    titulo="Nova Iniciativa",
    descricao="Descrição da iniciativa",
    responsavel="Nome do Responsável",
    prazo="2026-12-31",
    valor_alvo=100.0,
    unidade="%",
    categoria="Categoria"
)

gerenciador.adicionar_meta(nova_meta)
```

### Atualizar Progresso

```python
gerenciador.atualizar_meta(
    meta_id="META-001",
    novo_valor=75.0,
    observacao="Progresso significativo no último trimestre"
)
```

### Gerar Relatório

```python
relatorio = gerenciador.gerar_relatorio()
gerenciador.exportar_excel("relatorio_custom.xlsx")
```

## 🎨 Metas de Exemplo

O sistema vem com 5 metas pré-configuradas para demonstração:

1. **Preservação da Biodiversidade** - Aumentar área de preservação
2. **Educação Ambiental** - Programas educacionais nas comunidades
3. **Monitoramento de Água** - Implementar pontos de monitoramento
4. **Reflorestamento** - Plantio de mudas nativas
5. **Engajamento Comunitário** - Envolvimento das comunidades locais

## 🔧 API Endpoints

O servidor web disponibiliza os seguintes endpoints:

- `GET /` - Dashboard principal
- `GET /api/metas` - Lista todas as metas
- `GET /api/meta/<id>` - Detalhes de uma meta específica
- `POST /api/meta` - Adiciona nova meta
- `POST /api/meta/<id>/atualizar` - Atualiza progresso
- `GET /api/relatorio` - Relatório consolidado
- `GET /api/exportar-excel` - Download do relatório Excel
- `GET /api/categorias` - Lista categorias
- `GET /api/responsaveis` - Lista responsáveis

## 💡 Benefícios da Nova Gestão 2026

1. **Visibilidade Total**: Dashboard visual com todas as informações importantes
2. **Transparência**: Toda equipe pode acompanhar o progresso em tempo real
3. **Eficiência**: Atualizações rápidas e relatórios automáticos
4. **Colaboração**: Sistema centralizado para toda a equipe
5. **Análise**: Dados consolidados para melhor tomada de decisão
6. **Acessibilidade**: Interface web acessível de qualquer dispositivo

## 🌟 Diferenciais do Sistema

- **Interface Moderna**: Design responsivo e intuitivo
- **Zero Configuração**: Funciona imediatamente após instalação
- **Dados Persistentes**: Armazenamento em JSON para simplicidade
- **Exportação Excel**: Relatórios profissionais em múltiplas abas
- **Status Automático**: Sistema inteligente de classificação
- **Histórico Completo**: Rastreamento de todas as atualizações

## 📝 Licença

Este projeto é mantido pela equipe da APA Delta do Parnaíba.

## 🤝 Contribuição

Para contribuir com melhorias:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou sugestões sobre o sistema DeltaMetas 2026, entre em contato com a equipe de gestão da APA Delta do Parnaíba.

---

**DeltaMetas 2026** - Transformando a gestão de metas em 2026! 🌊🎯
