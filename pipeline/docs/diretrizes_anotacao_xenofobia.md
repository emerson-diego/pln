# Diretrizes de Anotação para Detecção de Discurso de Ódio - XENOFOBIA

## 1. Definição do Problema

**Objetivo**: Classificar textos em português brasileiro quanto à presença de discurso de ódio xenofóbico.

**Definição de Xenofobia**: Aversão, preconceito ou discriminação contra pessoas estrangeiras, imigrantes ou de nacionalidades diferentes, baseada em características como origem nacional, etnia, cultura ou status migratório.

## 2. Categorias de Classificação (Tagset)

### 2.1 Categoria Principal
- **XENOFOBIA**: Texto contém discurso de ódio xenofóbico
- **NAO_XENOFOBIA**: Texto não contém discurso de ódio xenofóbico

### 2.2 Subcategorias de Xenofobia
- **NACIONALIDADE**: Discriminação baseada em país de origem
- **IMIGRANTE**: Discriminação baseada em status migratório
- **DISCRIMINACAO_ECONOMICA**: Discriminação baseada em aspectos econômicos
- **DISCRIMINACAO_CULTURAL**: Discriminação baseada em diferenças culturais
- **GENERALIZACAO_NEGATIVA**: Generalizações negativas sobre grupos

### 2.3 Níveis de Intensidade
- **SUTIL**: Linguagem indireta, implícita ou sutil
- **MODERADO**: Linguagem direta mas sem palavrões explícitos
- **EXPLICITO**: Linguagem agressiva, ofensiva ou com palavrões

## 3. Critérios de Anotação

### 3.1 Textos que DEVEM ser classificados como XENOFOBIA

#### 3.1.1 Discriminação por Nacionalidade
- ✅ "Esses gringos só vêm pra cá se aproveitar"
- ✅ "Português é tudo igual, só quer saber de dinheiro"
- ✅ "Japonês não se mistura com brasileiro"

#### 3.1.2 Discriminação contra Imigrantes
- ✅ "Imigrante ilegal não deveria ter direito a nada"
- ✅ "Refugiado vem pra cá viver de auxílio"
- ✅ "Eles invadem nosso país e querem mudar tudo"

#### 3.1.3 Discriminação Econômica
- ✅ "Estrangeiro rouba emprego do brasileiro"
- ✅ "Venezuelano só vem pra cá gastar nosso dinheiro"
- ✅ "Boliviano trabalha por menos e estraga o mercado"

#### 3.1.4 Discriminação Cultural
- ✅ "Não falam português direito, não deveriam estar aqui"
- ✅ "Vêm pra cá com cultura estranha e querem mudar tudo"
- ✅ "Não respeitam nossos costumes, são diferentes demais"

#### 3.1.5 Generalizações Negativas
- ✅ "Todos os estrangeiros são iguais, só causam problema"
- ✅ "Eles nunca se adaptam, sempre fazem a mesma coisa"
- ✅ "São todos problemáticos, não mudam nunca"

### 3.2 Textos que NÃO devem ser classificados como XENOFOBIA

#### 3.2.1 Críticas Legítimas a Políticas
- ❌ "O governo deveria controlar melhor a imigração"
- ❌ "Precisamos de políticas migratórias mais claras"
- ❌ "A imigração descontrolada pode causar problemas"
- ❌ "Falta estrutura para receber tantos imigrantes"

#### 3.2.2 Discussões Neutras e Positivas
- ❌ "Muitos imigrantes vêm para o Brasil em busca de oportunidades"
- ❌ "A diversidade cultural enriquece nossa sociedade"
- ❌ "Imigrantes contribuem para a economia local"
- ❌ "A integração cultural é importante para o desenvolvimento"

#### 3.2.3 Opiniões Políticas Respeitosas
- ❌ "Sou contra a política de portas abertas"
- ❌ "Acredito que devemos priorizar brasileiros no mercado de trabalho"
- ❌ "O país não tem estrutura para receber tantos imigrantes"
- ❌ "Precisamos de um debate mais maduro sobre imigração"

#### 3.2.4 Debates Construtivos
- ❌ "Como podemos melhorar a integração dos imigrantes?"
- ❌ "Quais políticas funcionam melhor em outros países?"
- ❌ "Como equilibrar controle migratório e acolhimento?"
- ❌ "A imigração traz benefícios e desafios para o país"

#### 3.2.5 Comentários Informativos
- ❌ "A imigração venezuelana aumentou nos últimos anos"
- ❌ "Muitos refugiados buscam asilo no Brasil"
- ❌ "A comunidade japonesa no Brasil é numerosa"
- ❌ "Imigrantes trabalham em diversos setores da economia"

## 4. Instruções Específicas para Anotadores

### 4.1 Processo de Anotação
1. **Leia o texto completo** antes de classificar
2. **Identifique o contexto** e a intenção do autor
3. **Procure por indicadores** de xenofobia listados acima
4. **Classifique a categoria principal** (XENOFOBIA/NAO_XENOFOBIA)
5. **Se XENOFOBIA**, classifique subcategoria e intensidade
6. **Justifique sua decisão** em caso de dúvida

### 4.2 Casos Limítrofes
- **Dúvida entre SUTIL e MODERADO**: Classifique como MODERADO
- **Dúvida entre MODERADO e EXPLICITO**: Classifique como EXPLICITO
- **Dúvida sobre categoria**: Use a mais específica possível
- **Dúvida geral**: Discuta com outros anotadores

### 4.3 Exemplos de Classificação

#### Exemplo 1:
**Texto**: "Esses venezuelanos só vêm pra cá viver de auxílio do governo"
- **Categoria**: XENOFOBIA
- **Subcategoria**: DISCRIMINACAO_ECONOMICA
- **Intensidade**: MODERADO

#### Exemplo 2:
**Texto**: "Precisamos de políticas migratórias mais eficientes"
- **Categoria**: NAO_XENOFOBIA
- **Justificativa**: Crítica legítima a políticas, não discriminação

#### Exemplo 3:
**Texto**: "Gringo filho da puta, volta pro seu país!"
- **Categoria**: XENOFOBIA
- **Subcategoria**: NACIONALIDADE
- **Intensidade**: EXPLICITO

## 5. Controle de Qualidade

### 5.1 Validação Cruzada
- Cada texto deve ser anotado por pelo menos 2 anotadores
- Em caso de discordância, um terceiro anotador decide
- Documente todas as discordâncias para análise

### 5.2 Métricas de Concordância
- **Coeficiente Kappa de Cohen**: Meta ≥ 0.7
- **Concordância por categoria**: Meta ≥ 80%
- **Revisão de casos discordantes**: 100%

### 5.3 Treinamento dos Anotadores
- Sessão inicial de 2 horas com exemplos
- Teste prático com 20 textos de exemplo
- Reuniões semanais para alinhamento
- Documentação de casos difíceis

## 6. Ferramentas de Apoio

### 6.1 Lista de Palavras-Chave
- **Nacionalidades**: gringo, português, japonês, chinês, coreano, etc.
- **Status migratório**: imigrante, refugiado, ilegal, clandestino
- **Termos discriminatórios**: invasor, forasteiro, estrangeiro
- **Expressões xenofóbicas**: "volta pro seu país", "não é daqui"

### 6.2 Contextos de Alto Risco
- Comentários em notícias sobre imigração
- Discussões sobre economia e emprego
- Debates sobre política migratória
- Redes sociais e fóruns online

## 7. Considerações Éticas

### 7.1 Princípios
- Respeito à dignidade humana
- Não reprodução de discursos de ódio
- Foco na detecção, não na promoção
- Uso responsável dos dados

### 7.2 Cuidados
- Não compartilhar textos ofensivos fora do contexto de pesquisa
- Anonimizar dados pessoais
- Manter confidencialidade das anotações
- Relatar casos extremos às autoridades competentes

## 8. Exemplos de Anotação Completa

### Exemplo A:
```json
{
  "id": "xenofobia_00001",
  "texto": "Esses bolivianos invadem nossa cidade e roubam nossos empregos",
  "categoria_principal": "XENOFOBIA",
  "subcategoria": "DISCRIMINACAO_ECONOMICA",
  "intensidade": "MODERADO",
  "contexto": "comentário em rede social",
  "palavras_chave": ["bolivianos", "invadem", "roubam", "empregos"],
  "justificativa": "Generalização negativa sobre bolivianos associada a roubo de empregos"
}
```

### Exemplo B:
```json
{
  "id": "nao_xenofobia_00001",
  "texto": "A imigração é um fenômeno complexo que requer políticas públicas adequadas",
  "categoria_principal": "NAO_XENOFOBIA",
  "subcategoria": null,
  "intensidade": null,
  "contexto": "artigo de opinião",
  "palavras_chave": ["imigração", "políticas", "públicas"],
  "justificativa": "Discussão neutra sobre políticas migratórias, sem discriminação"
}
```

---

**Data de criação**: Janeiro 2025  
**Versão**: 1.0  
**Responsável**: Equipe de Mestrado em PLN
