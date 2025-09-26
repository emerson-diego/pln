# Implementação da Metodologia do Relatório - Gerador de Corpus Xenofobia

## 📋 Resumo das Mudanças Implementadas

O gerador `gerador_corpus_xenofobia.py` foi completamente reformulado para seguir rigorosamente as orientações metodológicas do relatório acadêmico, implementando um **esquema de anotação multicamadas** e foco específico no **contexto brasileiro de xenofobia**.

## 🎯 Principais Alterações

### 1. **Esquema de Anotação Multicamadas**

Implementado conforme **Tabela 3** do relatório:

#### **Camada 1: Classificação Primária**
- `XENOPHOBIC_HATE`: Texto que ataca grupos com base na origem
- `OFFENSIVE_GENERAL`: Texto ofensivo mas não xenofóbico
- `NEUTRAL_BENIGN`: Texto neutro ou benigno

#### **Camada 2: Identidade do Alvo**
- `TARGET_NORDESTINO`: Nordestinos (xenofobia interna)
- `TARGET_VENEZUELANO`: Venezuelanos
- `TARGET_HAITIANO`: Haitianos
- `TARGET_GENERIC_FOREIGNER`: Estrangeiros em geral
- `TARGET_OTHER`: Outros alvos específicos

#### **Camada 3: Estratégia do Discurso de Ódio**
- `STRATEGY_INCITEMENT`: Apela à violência ou ação hostil
- `STRATEGY_DEHUMANIZATION`: Nega humanidade do grupo
- `STRATEGY_SLUR`: Usa termos depreciativos
- `STRATEGY_STEREOTYPING`: Atribui características negativas
- `STRATEGY_EXCLUSION`: Defende segregação ou negação de direitos

#### **Camada 4: Nível de Explicitude**
- `EXPLICIT`: Intenção odiosa direta e inequívoca
- `IMPLICIT_CODED`: Intenção mascarada por linguagem codificada

### 2. **Alvos Específicos do Brasil**

Baseado na **Seção 1.3** do relatório:

#### **Xenofobia Interna (Nordestinofobia)**
- Gentílicos: nordestino, paraíba, baiano, cearense, pernambucano
- Slurs: paraíba, baiano, cabeça chata
- Esteriótipos: preguiçoso, vive de auxílio, bolsa família, não sabe votar
- Contextos: eleições, política, programas sociais

#### **Hostilidade contra Venezuelanos**
- Gentílicos: venezuelano, veneco
- Esteriótipos: invasor, criminoso, doença, sobrecarrega saúde
- Contextos: fronteira, Roraima, crise migratória, criminalidade

#### **Preconceito contra Haitianos**
- Gentílicos: haitiano
- Esteriótipos: rouba emprego, não fala português, cultura estranha
- Contextos: terremoto, migração, trabalho, cultura

### 3. **Metodologia de Role-Playing**

Implementada conforme **Tabela 2** do relatório:

#### **Personas para Geração**
1. **Usuário Preconceituoso**: Agressivo e direto, usa slurs
2. **Cidadão Preocupado**: Aparentemente razoável, mas com viés
3. **Morador Frustrado**: Ambíguo, permite negação plausível

### 4. **Contextos Específicos do Brasil**

Atualizados para refletir realidades brasileiras:
- Tweet sobre eleições e nordestinos
- Comentário sobre crise migratória venezuelana
- Post sobre imigrantes haitianos
- Tweet sobre programas sociais e região Nordeste
- Comentário sobre fronteira e imigração

## 🔧 Estrutura dos Dados Gerados

### Exemplo de Texto com Xenofobia:
```json
{
  "id": "corpus_00001",
  "texto": "Esses paraíbas só vêm pra cá viver de auxílio, não trabalham nem nada",
  "classificacao_primaria": "XENOPHOBIC_HATE",
  "alvo": "TARGET_NORDESTINO",
  "estrategia": "STRATEGY_STEREOTYPING",
  "explicitude": "EXPLICIT",
  "contexto": "tweet sobre eleições e nordestinos no Twitter",
  "palavras_chave": ["paraíbas", "auxílio", "não trabalham"],
  "sintetico": true,
  "tipo": "discurso_odio_xenofobia",
  "data_geracao": "2025-01-12T14:30:22",
  "versao": "2.0_metodologia_relatorio"
}
```

### Exemplo de Texto Neutro:
```json
{
  "id": "corpus_00002",
  "texto": "A imigração traz diversidade cultural e contribui para o desenvolvimento",
  "classificacao_primaria": "NEUTRAL_BENIGN",
  "alvo": "NENHUM",
  "estrategia": "NENHUMA",
  "explicitude": "NENHUMA",
  "contexto": "post no Twitter sobre diversidade cultural no Brasil",
  "palavras_chave": ["imigração", "diversidade", "desenvolvimento"],
  "sintetico": true,
  "tipo": "texto_neutro",
  "data_geracao": "2025-01-12T14:30:22",
  "versao": "2.0_metodologia_relatorio"
}
```

## 📊 Vantagens da Nova Implementação

### 1. **Metodologia Científica Rigorosa**
- Esquema multicamadas permite análise granular
- Alinhado com pesquisa de ponta na área
- Facilita cálculo de concordância interanotadores

### 2. **Especificidade do Contexto Brasileiro**
- Foca nos principais alvos de xenofobia no Brasil
- Usa termos e esteriótipos comuns no país
- Considera xenofobia interna (nordestinofobia)

### 3. **Geração Realista**
- Role-playing com personas específicas
- Contextos autênticos do Brasil
- Estratégias discursivas variadas

### 4. **Validação Robusta**
- Validação por camada
- Critérios específicos para cada tipo
- Detecção de inconsistências

## 🚀 Como Usar

### Geração Básica:
```bash
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 5
```

### Geração Apenas Xenofobia:
```bash
python pipeline/scripts/geracao_sintetica/gerador_corpus_xenofobia.py 5 --apenas-xenofobia
```

## 📈 Resultados Esperados

Para um corpus de 100 textos:
- **50 textos com xenofobia** (50%)
- **50 textos neutros** (50%)
- **Distribuição por alvo**: ~25 textos por alvo principal
- **Distribuição por estratégia**: Variada conforme persona
- **Distribuição por explicitude**: ~50% explícito, 50% implícito

## 🔬 Contribuições Acadêmicas

1. **Corpus Especializado**: Primeiro corpus focado em xenofobia brasileira
2. **Metodologia Multicamadas**: Implementação prática do esquema proposto
3. **Role-Playing Avançado**: Geração realista com personas específicas
4. **Validação Rigorosa**: Critérios de qualidade acadêmicos

## 📚 Referências

- Relatório metodológico completo
- Tabela 3: Esquema de Anotação Multicamadas
- Tabela 2: Modelos de Engenharia de Prompt
- Seção 1.3: Panorama Brasileiro da Xenofobia

---

**Data de Implementação**: Janeiro 2025  
**Versão**: 2.0_metodologia_relatorio  
**Baseado em**: Relatório metodológico acadêmico
