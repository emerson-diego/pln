# Detecção de Discurso de Ódio - XENOFOBIA

Trabalho de Mestrado em Processamento de Linguagem Natural

## 📋 Sobre o Projeto

Este projeto visa desenvolver um sistema para detecção automática de discurso de ódio xenofóbico em textos em português brasileiro. O trabalho está estruturado em diferentes etapas, desde a geração de corpus sintético até a anotação manual e avaliação de concordância entre anotadores.

## 🎯 Objetivos

- Gerar corpus sintético de textos contendo discurso de ódio xenofóbico
- Criar dataset balanceado (50% com xenofobia, 50% sem xenofobia)
- Simular tweets do Twitter (máximo 280 caracteres)
- Desenvolver diretrizes claras para anotação manual
- Criar ferramentas para anotação e avaliação de concordância
- Estabelecer métricas de qualidade para o dataset

## 🏗️ Estrutura do Projeto

```
pipeline/
├── scripts/
│   ├── geracao_sintetica/
│   │   └── gerador_corpus_xenofobia.py    # Gerador de corpus sintético
│   └── ferramentas/
│       ├── ferramenta_anotacao.py         # Interface de anotação
│       └── avaliador_concordancia.py      # Avaliação de concordância
├── docs/
│   └── diretrizes_anotacao_xenofobia.md   # Diretrizes de anotação
└── data/
    ├── corpus_xenofobia_sintetico.jsonl   # Corpus gerado
    └── anotacoes_xenofobia.jsonl          # Anotações manuais
```

## 🚀 Como Usar

### 1. Configuração do Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração da API

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY_1="sua_chave_gemini_aqui"
GEMINI_API_KEY_2="outra_chave_gemini_aqui"
GEMINI_API_KEY="chave_principal_gemini"
```

### 3. Geração do Corpus Sintético

```bash
# Gerar corpus balanceado (50/50) no formato Twitter - PADRÃO
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 5

# Gerar apenas textos com xenofobia no formato Twitter
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 5 --apenas-xenofobia

# Gerar com parâmetros customizados
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 10 --arquivo "meu_corpus.jsonl" --tamanho-lote 15

# Gerar corpus balanceado com arquivo específico
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 8 --arquivo "corpus_balanceado.jsonl" --balanceado
```

### 4. Anotação Manual

```bash
# Executar ferramenta de anotação
streamlit run pipeline/scripts/ferramentas/ferramenta_anotacao.py
```

### 5. Avaliação de Concordância

```bash
# Avaliar concordância entre anotadores
python pipeline/scripts/ferramentas/avaliador_concordancia.py --arquivo anotacoes_xenofobia.jsonl
```

## 📊 Categorias de Xenofobia

O projeto foca em 5 categorias principais de xenofobia:

1. **NACIONALIDADE**: Discriminação baseada em país de origem
2. **IMIGRANTE**: Discriminação baseada em status migratório
3. **DISCRIMINACAO_ECONOMICA**: Discriminação baseada em aspectos econômicos
4. **DISCRIMINACAO_CULTURAL**: Discriminação baseada em diferenças culturais
5. **GENERALIZACAO_NEGATIVA**: Generalizações negativas sobre grupos

## 🏷️ Sistema de Anotação

### Categorias Principais
- **XENOFOBIA**: Texto contém discurso de ódio xenofóbico
- **NAO_XENOFOBIA**: Texto não contém discurso de ódio xenofóbico

### Níveis de Intensidade
- **SUTIL**: Linguagem indireta e implícita
- **MODERADO**: Linguagem direta mas sem palavrões
- **EXPLICITO**: Linguagem agressiva e ofensiva

## 📈 Métricas de Qualidade

### Concordância entre Anotadores
- **Coeficiente Kappa de Cohen**: Meta ≥ 0.7
- **Concordância Percentual**: Meta ≥ 80%

### Interpretação do Kappa
- **< 0.20**: Concordância pobre
- **0.21-0.40**: Concordância razoável
- **0.41-0.60**: Concordância moderada
- **0.61-0.80**: Concordância substancial
- **> 0.80**: Concordância quase perfeita

## 🔧 Ferramentas Disponíveis

### 1. Gerador de Corpus Sintético
- Gera textos realistas com discurso de ódio xenofóbico
- Usa diferentes contextos (redes sociais, fóruns, etc.)
- Varia níveis de intensidade
- Validação automática de qualidade

### 2. Ferramenta de Anotação
- Interface web intuitiva
- Classificação por categoria e intensidade
- Justificativas para cada anotação
- Estatísticas em tempo real

### 3. Avaliador de Concordância
- Calcula métricas de concordância
- Identifica casos de discordância
- Gera relatórios detalhados
- Recomendações de melhoria

## 📚 Diretrizes de Anotação

Consulte o arquivo `pipeline/docs/diretrizes_anotacao_xenofobia.md` para:
- Definições detalhadas de cada categoria
- Exemplos de classificação
- Critérios de anotação
- Casos limítrofes
- Considerações éticas

## 🤝 Contribuição

Este é um projeto acadêmico. Para contribuições:

1. Leia as diretrizes de anotação
2. Siga os padrões de qualidade estabelecidos
3. Documente suas alterações
4. Teste as ferramentas antes de submeter

## 📄 Licença

Este projeto é destinado exclusivamente para fins acadêmicos e de pesquisa.

## 👥 Equipe

- **Líderes do Grupo**: Coordenação e relatórios
- **Construtores do Corpus**: Geração e coleta de dados
- **Anotadores**: Classificação manual dos textos
- **Avaliadores**: Análise de concordância e qualidade

## 📞 Contato

Para dúvidas sobre o projeto, consulte a documentação ou entre em contato com a equipe de mestrado.

---

**Data de Criação**: Janeiro 2025  
**Versão**: 1.0  
**Instituição**: [Nome da Instituição]  
**Curso**: Mestrado em Processamento de Linguagem Natural
