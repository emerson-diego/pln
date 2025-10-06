# Geração de Dados Sintéticos - XENOFOBIA

Trabalho de Mestrado em Processamento de Linguagem Natural

## 📋 Sobre o Projeto

Trata-se de um projeto para geração de dados sintéticos usando o Gemini, focado na criação de corpus de textos com discurso de ódio xenofóbico em português brasileiro, simulando tweets do Twitter.

## 🎯 Objetivos

- Gerar dados sintéticos usando API Gemini
- Criar corpus balanceado (50% com xenofobia, 50% sem xenofobia)
- Simular tweets do Twitter (máximo 280 caracteres)
- Desenvolver sistema de classificação simplificado
- Automatizar geração de textos realistas em português brasileiro

## 🏗️ Estrutura do Projeto

```
pipeline/
├── scripts/
│   └── geracao_sintetica/
│       └── gerador_corpus_xenofobia.py    # Gerador de corpus
└── data/
    └── corpus_xenofobia.jsonl             # Corpus gerado
```

## 🚀 Como Usar

### 1. Configuração do Ambiente

```bash
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração da API

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY_1="sua_chave_gemini_aqui"
GEMINI_API_KEY_2="outra_chave_gemini_aqui"
```

### 3. Geração do Corpus

```bash
# Gerar corpus balanceado (padrão)
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 5


# Gerar com arquivo específico
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 10 --arquivo "meu_corpus.jsonl"
```

## 🏷️ Sistema de Classificação

### Categorias Principais
- **ODIO_XENOFOBICO**: Texto contém discurso de ódio xenofóbico
- **OFENSIVO_GERAL**: Texto ofensivo mas não xenofóbico
- **NEUTRO**: Texto neutro ou positivo

### Alvos Específicos
- **Nordestinos**: Paraíba, baiano, cearense, etc.
- **Venezuelanos**: Venezuelano, veneco
- **Haitianos**: Haitiano
- **Estrangeiros**: Gringo, estrangeiro, imigrante

### Estratégias de Ódio
- **INCITAMENTO**: "dar um jeito", "mandar embora", "expulsar"
- **DESUMANIZACAO**: "praga", "invasão", "doença", "vírus"
- **INJURIA**: "paraíba", "baiano", "veneco", "gringo"
- **ESTEREOTIPIZACAO**: "todo", "sempre", "são todos iguais"
- **EXCLUSAO**: "não deveria ter acesso", "não merece"

## 📊 Estrutura do Corpus

```json
{
  "id": "corpus_00001",
  "texto": "texto do tweet...",
  "classificacao": "ODIO_XENOFOBICO|OFENSIVO_GERAL|NEUTRO",
  "contexto": "contexto do tweet",
  "palavras_chave": ["palavra1", "palavra2"],
  "data_geracao": "2025-01-XX",
  "versao": "2.0"
}
```

## 🔧 Parâmetros do Gerador

- `lotes`: Número de lotes a gerar (obrigatório)
- `--arquivo`: Nome do arquivo de saída (padrão: corpus_xenofobia.jsonl)
- `--tamanho-lote`: Tamanho de cada lote (padrão: 10)

## 📈 Exemplo de Uso

```bash
# Gerar 5 lotes (50 textos) balanceados
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 5


# Gerar com lote maior
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 3 --tamanho-lote 20
```

## 📚 Características Técnicas

- **API**: Google Gemini 2.5 Flash para geração de textos
- **Linguagem**: Português brasileiro coloquial
- **Formato**: Tweets (máximo 280 caracteres)
- **Personas**: 3 tipos de usuários (preconceituoso, preocupado, frustrado)
- **Contextos**: 10 contextos diferentes (redes sociais, notícias, etc.)
- **Validação**: Automática de qualidade e formato
- **Processamento**: Assíncrono com múltiplas chaves API


## 📄 Licença

Este projeto é destinado exclusivamente para fins acadêmicos e de pesquisa.

---

**Data de Criação**: Outubro 2025  
**Versão**: 2.0  
**Curso**: Mestrado em Processamento de Linguagem Natural