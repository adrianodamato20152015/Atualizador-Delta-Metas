#!/bin/bash
# Script de inicialização do DeltaMetas 2026

echo "============================================================"
echo "🌊 DeltaMetas 2026 - Inicializador"
echo "Sistema de Gestão de Metas - APA Delta do Parnaíba"
echo "============================================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

echo "✓ Python $(python3 --version | cut -d' ' -f2) encontrado"

# Verificar dependências
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Ambiente virtual criado"
else
    source venv/bin/activate
    echo "✓ Ambiente virtual ativado"
fi

# Instalar/atualizar dependências
echo ""
echo "📦 Instalando/atualizando dependências..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependências instaladas"

echo ""
echo "============================================================"
echo "Escolha o modo de execução:"
echo "============================================================"
echo "1) Dashboard Web (Recomendado)"
echo "2) Linha de Comando"
echo "3) Executar Exemplos"
echo "============================================================"
read -p "Digite sua escolha (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Iniciando Dashboard Web..."
        echo "Acesse: http://localhost:5000"
        echo "Pressione Ctrl+C para parar o servidor"
        echo ""
        python3 app.py
        ;;
    2)
        echo ""
        echo "🖥️  Executando modo linha de comando..."
        echo ""
        python3 deltametas.py
        ;;
    3)
        echo ""
        echo "📚 Executando exemplos..."
        echo ""
        python3 exemplo_uso.py
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac
