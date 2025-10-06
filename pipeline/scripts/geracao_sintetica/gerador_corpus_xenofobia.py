# -*- coding: utf-8 -*-

"""
Gerador de Corpus para Detecção de Discurso de Ódio - XENOFOBIA
Trabalho de Mestrado em Processamento de Linguagem Natural

Versão: 2.0
Data: Outubro 2025

Objetivo: Gerar corpus focado em discursos de ódio xenofóbicos
para treinamento de modelos de classificação de texto.

"""

import os
import json
import random
import argparse
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

import google.generativeai as genai
import aiofiles
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

# --- Configuração ---
@dataclass
class Config:
    """Configurações centralizadas do gerador."""
    # API
    MODELO_GEMINI: str = 'gemini-2.5-flash'
    MAX_TENTATIVAS: int = 3
    ESPERA_RETRY: int = 2
    
    # Corpus
    TAMANHO_LOTE: int = 10
    ARQUIVO_SAIDA: str = 'corpus_xenofobia.jsonl'
    
    # Validação (Twitter: máximo 280 caracteres)
    TAMANHO_MIN_PALAVRAS: int = 3
    TAMANHO_MAX_CARACTERES: int = 280
    
    @staticmethod
    def carregar_chaves_api() -> List[str]:
        """Carrega chaves da API Gemini."""
        try:
            # Caminho correto: 3 níveis acima (geracao_sintetica -> scripts -> pipeline -> raiz)
            project_root = Path(__file__).resolve().parent.parent.parent
            env_path = project_root / '.env'
            print(f"Procurando .env em: {env_path}")
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
                print(f"Arquivo .env carregado de: {env_path}")
            else:
                print(f"Arquivo .env não encontrado em: {env_path}")
                # Tenta carregar da raiz atual como fallback
                load_dotenv()
        except Exception as e:
            print(f"Erro ao carregar .env: {e}")
            # Tenta carregar da raiz atual como fallback
            load_dotenv()
        
        keys = []
        for i in range(1, 9): 
            key = os.getenv(f"GEMINI_API_KEY_{i}") or os.getenv("GEMINI_API_KEY")
            if key:
                keys.append(key)
        
        if not keys:
            raise ValueError("Nenhuma chave da API Gemini encontrada!")
        
        return keys

# --- Alvos Específicos de Xenofobia no Brasil ---
ALVOS_XENOFOBIA = {
    "ALVO_NORDESTINO": {
        "gentilicos": ["nordestino", "paraíba", "baiano", "cearense", "pernambucano", "maranhense"],
        "insultos": ["paraíba", "baiano", "nordestino", "cabeça chata"],
        "estereotipos": ["preguiçoso", "vive de auxílio", "bolsa família", "não sabe votar", "atrasado"],
        "contextos": ["eleições", "política", "programas sociais", "votação", "desenvolvimento"]
    },
    "ALVO_VENEZUELANO": {
        "gentilicos": ["venezuelano", "veneco"],
        "insultos": ["veneco", "venezuelano"],
        "estereotipos": ["invasor", "criminoso", "doença", "sobrecarrega saúde", "rouba emprego"],
        "contextos": ["fronteira", "Roraima", "crise migratória", "criminalidade", "saúde pública"]
    },
    "ALVO_HAITIANO": {
        "gentilicos": ["haitiano", "haitiano"],
        "insultos": ["haitiano"],
        "estereotipos": ["rouba emprego", "não fala português", "cultura estranha", "não se adapta"],
        "contextos": ["terremoto", "migração", "trabalho", "cultura", "integração"]
    },
    "ALVO_ESTRANGEIRO": {
        "gentilicos": ["gringo", "estrangeiro", "imigrante", "refugiado", "forasteiro"],
        "insultos": ["gringo", "estrangeiro", "imigrante"],
        "estereotipos": ["invasor", "não é daqui", "vem pra cá se aproveitar", "ameaça identidade"],
        "contextos": ["nacionalidade", "identidade", "segurança", "economia", "cultura"]
    }
}

# --- Estratégias de Discurso de Ódio ---
ESTRATEGIAS_ODIO = {
    "INCITAMENTO": [
        "dar um jeito", "mandar embora", "expulsar", "deportar", "acabar com",
        "alguém precisa fazer algo", "tem que resolver isso"
    ],
    "DESUMANIZACAO": [
        "praga", "invasão", "infestação", "doença", "câncer", "vírus",
        "animais", "bichos", "coisa", "lixo"
    ],
    "INJURIA": [
        "paraíba", "baiano", "veneco", "gringo", "cabeça chata",
        "nordestino", "haitiano"
    ],
    "ESTEREOTIPIZACAO": [
        "todo", "todos", "sempre", "nunca", "são todos iguais",
        "característica do grupo", "típico de"
    ],
    "EXCLUSAO": [
        "não deveria ter acesso", "não merece", "não tem direito",
        "deveria ser proibido", "não pode ficar aqui"
    ]
}


# --- Contextos Específicos do Brasil ---
CONTEXTOS_GERACAO = [
    "tweet reagindo a notícia sobre imigração",
    "post no Twitter sobre venezuelanos na cidade",
    "comentário sobre nordestinos vindo pro sul",
    "tweet sobre haitianos no bairro",
    "post reagindo a vídeo de imigrante",
    "comentário sobre estrangeiros no trabalho",
    "tweet sobre notícia de criminalidade",
    "post sobre fila do SUS com imigrantes",
    "comentário sobre vaga de emprego",
    "tweet sobre eleição e imigração"
]

# --- Personas ---
PERSONAS_GERACAO = {
    "usuario_preconceituoso": {
        "descricao": "usuário do Twitter que posta conteúdo xenófobo de forma direta e agressiva",
        "linguagem": "informal, com gírias, abreviações e emojis. Usa 'cara', 'mano', 'galera', 'tá', 'né'",
        "caracteristicas": ["usa hashtags", "escreve em caps", "usa emojis de raiva", "linguagem coloquial"],
        "estrategias": ["INJURIA", "INCITAMENTO"]
    },
    "cidadao_preocupado": {
        "descricao": "usuário que parece preocupado com questões sociais, mas tem viés xenófobo",
        "linguagem": "mais formal, mas com expressões do dia a dia. Usa 'realmente', 'sinceramente', 'na verdade'",
        "caracteristicas": ["usa reticências", "faz perguntas retóricas", "cita notícias", "linguagem aparentemente educada"],
        "estrategias": ["ESTEREOTIPIZACAO", "EXCLUSAO"]
    },
    "morador_frustrado": {
        "descricao": "pessoa que vive em área com muitos imigrantes e expressa frustração de forma sutil",
        "linguagem": "coloquial e regional. Usa 'aqui', 'onde eu moro', 'na minha cidade', 'todo mundo sabe'",
        "caracteristicas": ["fala de experiência pessoal", "usa linguagem ambígua", "permite negação plausível"],
        "estrategias": ["DESUMANIZACAO"]
    }
}

class GeradorCorpusXenofobia:
    """Gerador principal do corpus de xenofobia."""
    
    def __init__(self, api_keys: List[str]):
        self.api_keys = api_keys
        self.current_key = 0
        self.contador_id = 0
    
    def _proxima_chave(self) -> str:
        """Rotaciona entre as chaves da API."""
        chave = self.api_keys[self.current_key]
        self.current_key = (self.current_key + 1) % len(self.api_keys)
        return chave
    
    def _criar_prompt(self, quantidade: int, incluir_nao_xenofobia: bool = True) -> str:
        """Cria prompt"""
        contexto = random.choice(CONTEXTOS_GERACAO)
        persona = random.choice(list(PERSONAS_GERACAO.keys()))
        persona_info = PERSONAS_GERACAO[persona]
        
        # Seleciona alvo específico baseado no contexto brasileiro
        alvo_escolhido = random.choice(list(ALVOS_XENOFOBIA.keys()))
        alvo_info = ALVOS_XENOFOBIA[alvo_escolhido]
        
        # Seleciona estratégias baseadas na persona
        estrategias_persona = persona_info["estrategias"]
        estrategia_escolhida = random.choice(estrategias_persona)
        
        # Define proporção de textos com e sem xenofobia (50/50)
        if incluir_nao_xenofobia:
            qtd_xenofobia = quantidade // 2  # 50% com xenofobia
            qtd_nao_xenofobia = quantidade - qtd_xenofobia  # 50% sem xenofobia
            # Dentro dos não-xenofobia, dividir entre NEUTRAL_BENIGN e OFFENSIVE_GENERAL
            qtd_neutral = qtd_nao_xenofobia // 2  # 25% neutros
            qtd_offensive = qtd_nao_xenofobia - qtd_neutral  # 25% ofensivos gerais
            
            return f"""
Você é um especialista em análise de discurso de ódio xenofóbico no Brasil. Sua tarefa é criar {quantidade} exemplos de TWEETS em português brasileiro, sendo {qtd_xenofobia} com discurso de ódio xenofóbico e {qtd_nao_xenofobia} sem xenofobia.

CONTEXTO: Os textos devem simular {contexto}.

INSTRUÇÕES PARA TWEETS COM XENOFOBIA ({qtd_xenofobia} textos):
- PERSONA: Assuma a persona de um {persona_info['descricao']}
- ALVO PRINCIPAL: Foque em {alvo_escolhido} ({', '.join(alvo_info['gentilicos'][:3])})
- ESTRATÉGIA: Use {estrategia_escolhida} - {', '.join(ESTRATEGIAS_ODIO.get(estrategia_escolhida, [])[:3])}
- LINGUAGEM: {persona_info['linguagem']}
- CARACTERÍSTICAS: {', '.join(persona_info['caracteristicas'])}
- EXEMPLOS DE PALAVRAS-CHAVE: {', '.join(alvo_info['insultos'][:2])}, {', '.join(alvo_info['estereotipos'][:2])}

INSTRUÇÕES PARA TWEETS SEM XENOFOBIA ({qtd_nao_xenofobia} textos):
- NEUTRO ({qtd_neutral} textos): Discussões neutras sobre imigração, diversidade cultural, políticas migratórias
- OFENSIVO_GERAL ({qtd_offensive} textos): Críticas legítimas a políticas (não a pessoas), opiniões políticas respeitosas sobre imigração
- Comentários positivos sobre diversidade cultural
- Debates construtivos sobre economia e imigração
- IMPORTANTE: Gere EXATAMENTE {qtd_offensive} tweets OFENSIVO_GERAL (críticas a políticas, não a pessoas)

IMPORTANTE: Para TODOS os tweets, use linguagem informal e coloquial, como se fosse uma pessoa real postando no Twitter.

ESTILO DE TWEET AUTÊNTICO (OBRIGATÓRIO):
1. LINGUAGEM SUPER INFORMAL: "cara", "mano", "galera", "tá", "né", "realmente", "tipo", "assim", "tipo assim"
2. ABREVIAÇÕES OBRIGATÓRIAS: "pq", "vc", "tb", "mt", "hj", "q", "n", "ñ", "tbm", "pra", "pro", "nao", "ta"
3. EMOJIS FREQUENTES: 😤😡🤬💀🔥 (xenofobia) ou 🤔💭📊😅 (neutros)
4. HASHTAGS: #Brasil #Imigracao #Seguranca #Economia #Realidade
5. PONTUAÇÃO INFORMAL: "...", "??", "!!", "??", "!!"
6. EXPRESSÕES BRASILEIRAS: "nossa", "cara", "galera", "tipo assim", "realmente", "sinceramente"
7. ESTRUTURA FRAGMENTADA: Frases curtas, quebras de linha, pontos de exclamação
8. MÁXIMO 280 caracteres
9. ESCREVA COMO UMA PESSOA REAL NO TWITTER - NÃO COMO UM ACADÊMICO

PROIBIDO (NÃO FAÇA):
- Linguagem formal: "Assistindo ao vídeo e pensando na complexidade..."
- Termos acadêmicos: "políticas públicas bem pensadas e integradoras"
- Frases longas e complexas
- Linguagem de relatório ou artigo científico
- Tom neutro demais ou "correto" demais

OBRIGATÓRIO (FAÇA):
- Linguagem coloquial: "Cara, vi um vídeo e fiquei pensando..."
- Abreviações: "pq", "vc", "tb", "mt", "hj", "q", "n", "ñ"
- Emojis: 😤😡🤬💀🔥 (xenofobia) ou 🤔💭📊😅 (neutros)
- Hashtags: #Brasil #Imigracao #Seguranca #Economia
- Expressões brasileiras: "nossa", "cara", "galera", "tipo assim"

EXEMPLOS DE TWEETS REAIS:
XENOFÓBICOS: 
- "Cara, não aguento mais esses venecos aqui na cidade... sempre causando confusão 😤 #BrasilPrimeiro"
- "Galera, vcs viram q mais um nordestino foi preso? N é atoa q a situação tá assim... 🤦‍♂️"
- "Mano, aqui onde eu moro tá cheio de gringo... ninguém aguenta mais 😡"
- "Pq o governo n faz nada com esses invasores? A galera tá revoltada... 💀 #SegurancaPublica"

NEUTROS:
- "Realmente, a imigração é um tema complexo. Precisamos de políticas melhores 🤔 #ImigracaoBrasil"
- "A diversidade cultural enriquece nosso país, mas precisamos de planejamento 💭"
- "Nossa, q interessante ver como diferentes culturas se misturam aqui no Brasil 🌍 #Diversidade"
- "Cara, a imigração pode ser uma oportunidade se bem planejada 💡 #Desenvolvimento"

FORMATO DE SAÍDA (JSON puro, sem markdown):
CRÍTICO: Gere APENAS JSON válido. Use aspas duplas, escape aspas internas com \", termine todas as strings.

[
  {{
    "texto": "texto completo aqui",
    "classificacao": "ODIO_XENOFOBICO|OFENSIVO_GERAL|NEUTRO",
    "contexto": "{contexto}",
    "palavras_chave": ["palavra1", "palavra2", "palavra3"]
  }}
]

REGRAS OBRIGATÓRIAS:
1. Use APENAS aspas duplas para strings
2. Escape aspas internas: \"texto com aspas\"
3. Termine TODAS as strings corretamente
4. Use vírgulas entre propriedades
5. Feche todas as chaves e colchetes
6. NÃO use quebras de linha dentro de strings
7. NÃO use caracteres especiais que quebrem JSON

EXEMPLO CORRETO:
[
  {{
    "texto": "Cara, não aguento mais esses venecos... sempre causando confusão 😤 #BrasilPrimeiro",
    "classificacao": "ODIO_XENOFOBICO",
    "contexto": "tweet reagindo a notícia sobre imigração",
    "palavras_chave": ["venecos", "confusão", "BrasilPrimeiro"]
  }}
]

EXEMPLOS ESPECÍFICOS DE COMO ESCREVER:

❌ NÃO FAÇA (muito formal):
"Assistindo ao vídeo e pensando na complexidade da imigração. É um desafio global q exige políticas públicas bem pensadas e integradoras."

✅ FAÇA (autêntico do Twitter):
"Cara, vi um vídeo de imigrante e fiquei pensando... pq o governo n faz nada com esses invasores? A galera tá revoltada! 😡 #BrasilPrimeiro"

❌ NÃO FAÇA (muito formal):
"Que legal ver a diversidade cultural q a imigração traz! É uma troca de experiências q enriquece mt o nosso país."

✅ FAÇA (autêntico do Twitter):
"Nossa, q interessante ver como diferentes culturas se misturam aqui no Brasil 🌍 #Diversidade"

REGRAS FINAIS:
1. SEMPRE comece com "Cara", "Mano", "Galera", "Nossa", "Realmente"
2. Use MUITAS abreviações: "pq", "vc", "tb", "mt", "hj", "q", "n", "ñ"
3. Use emojis em TODOS os tweets
4. Use hashtags em TODOS os tweets
5. Seja MUITO informal e coloquial
6. NÃO use linguagem acadêmica ou formal
7. TWEETS CURTOS: Muitos tweets reais têm 50-150 caracteres, não 280!
8. VARIEDADE DE TAMANHOS: Misture tweets curtos (50-100 chars) e médios (100-200 chars)
9. GERE OFENSIVO_GERAL: Críticas a políticas, não a pessoas

EXEMPLOS DE TWEETS CURTOS:
- "Cara, n aguento mais esses venecos! 😤 #BrasilPrimeiro" (60 chars)
- "Nossa, q interessante! 🌍 #Diversidade" (45 chars)
- "Mano, a imigração é complexa... 🤔 #ImigracaoBrasil" (55 chars)

EXEMPLOS DE OFENSIVO_GERAL (críticas a políticas, não a pessoas):
- "Cara, as políticas de imigração estão uma bagunça! 😤 #PoliticasPublicas" (70 chars)
- "Mano, o governo n sabe o q faz com imigrantes... 🤦‍♂️ #GestaoPublica" (65 chars)
- "Galera, essas leis de imigração são ridículas! 😡 #ReformaJa" (60 chars)

Gere os {quantidade} exemplos agora:
"""
        else:
            # Prompt apenas para xenofobia
            return f"""
Você é um especialista em análise de discurso de ódio xenofóbico no Brasil. Sua tarefa é criar {quantidade} exemplos de textos que contenham discurso de ódio xenofóbico em português brasileiro.

CONTEXTO: Os textos devem simular {contexto}.

INSTRUÇÕES PARA GERAÇÃO:
- PERSONA: Assuma a persona de um {persona_info['descricao']}
- ALVO PRINCIPAL: Foque em {alvo_escolhido} ({', '.join(alvo_info['gentilicos'][:3])})
- ESTRATÉGIA: Use {estrategia_escolhida} - {', '.join(ESTRATEGIAS_ODIO.get(estrategia_escolhida, [])[:3])}
- LINGUAGEM: {persona_info['linguagem']}
- EXEMPLOS DE PALAVRAS-CHAVE: {', '.join(alvo_info['insultos'][:2])}, {', '.join(alvo_info['estereotipos'][:2])}

INSTRUÇÕES IMPORTANTES:
1. Gere textos realistas que uma pessoa poderia escrever no Twitter
2. Use linguagem natural do português brasileiro
3. Respeite o limite de 280 caracteres do Twitter
4. Use linguagem informal típica de redes sociais
5. Foque em xenofobia específica do contexto brasileiro
6. Use termos e estereótipos comuns no Brasil

FORMATO DE SAÍDA (JSON puro, sem markdown):
[
  {{
    "texto": "texto completo aqui",
    "classificacao": "ODIO_XENOFOBICO|OFENSIVO_GERAL|NEUTRO",
    "contexto": "{contexto}",
    "palavras_chave": ["palavra1", "palavra2", "palavra3"]
  }}
]

EXEMPLOS ESPECÍFICOS DE COMO ESCREVER:

❌ NÃO FAÇA (muito formal):
"Assistindo ao vídeo e pensando na complexidade da imigração. É um desafio global q exige políticas públicas bem pensadas e integradoras."

✅ FAÇA (autêntico do Twitter):
"Cara, vi um vídeo de imigrante e fiquei pensando... pq o governo n faz nada com esses invasores? A galera tá revoltada! 😡 #BrasilPrimeiro"

❌ NÃO FAÇA (muito formal):
"Que legal ver a diversidade cultural q a imigração traz! É uma troca de experiências q enriquece mt o nosso país."

✅ FAÇA (autêntico do Twitter):
"Nossa, q interessante ver como diferentes culturas se misturam aqui no Brasil 🌍 #Diversidade"

REGRAS FINAIS:
1. SEMPRE comece com "Cara", "Mano", "Galera", "Nossa", "Realmente"
2. Use MUITAS abreviações: "pq", "vc", "tb", "mt", "hj", "q", "n", "ñ"
3. Use emojis em TODOS os tweets
4. Use hashtags em TODOS os tweets
5. Seja MUITO informal e coloquial
6. NÃO use linguagem acadêmica ou formal
7. TWEETS CURTOS: Muitos tweets reais têm 50-150 caracteres, não 280!
8. VARIEDADE DE TAMANHOS: Misture tweets curtos (50-100 chars) e médios (100-200 chars)
9. GERE OFENSIVO_GERAL: Críticas a políticas, não a pessoas

EXEMPLOS DE TWEETS CURTOS:
- "Cara, n aguento mais esses venecos! 😤 #BrasilPrimeiro" (60 chars)
- "Nossa, q interessante! 🌍 #Diversidade" (45 chars)
- "Mano, a imigração é complexa... 🤔 #ImigracaoBrasil" (55 chars)

EXEMPLOS DE OFENSIVO_GERAL (críticas a políticas, não a pessoas):
- "Cara, as políticas de imigração estão uma bagunça! 😤 #PoliticasPublicas" (70 chars)
- "Mano, o governo n sabe o q faz com imigrantes... 🤦‍♂️ #GestaoPublica" (65 chars)
- "Galera, essas leis de imigração são ridículas! 😡 #ReformaJa" (60 chars)

Gere os {quantidade} exemplos agora:
"""
    
    async def _gerar_lote(self, prompt: str, lote_num: int) -> Optional[List[Dict[str, Any]]]:
        """Gera um lote de textos usando a API Gemini."""
        for tentativa in range(Config.MAX_TENTATIVAS):
            try:
                api_key = self._proxima_chave()
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    Config.MODELO_GEMINI,
                    generation_config={
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "max_output_tokens": 4096
                    }
                )
                
                response = await model.generate_content_async(prompt)
                texto_resposta = response.text.strip()
                
                # Limpa formatação markdown se presente
                if texto_resposta.startswith("```json"):
                    texto_resposta = texto_resposta[7:-3].strip()
                elif texto_resposta.startswith("```"):
                    texto_resposta = texto_resposta.strip("```")
                
                # Tenta corrigir JSON malformado
                try:
                    dados = json.loads(texto_resposta)
                except json.JSONDecodeError as e:
                    print(f"Erro JSON (tentativa {tentativa + 1}): {str(e)[:100]}")
                    # Tenta extrair JSON válido da resposta
                    import re
                    json_match = re.search(r'\[.*\]', texto_resposta, re.DOTALL)
                    if json_match:
                        try:
                            dados = json.loads(json_match.group())
                        except:
                            raise e
                    else:
                        raise e
                if not isinstance(dados, list):
                    raise ValueError("Resposta não é uma lista")
                
                print(f"Lote {lote_num}: {len(dados)} textos")
                return dados
                
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_SERVICE_BLOCKED" in error_msg or "403" in error_msg:
                    print(f"Lote {lote_num} (tentativa {tentativa + 1}): Chave bloqueada - {error_msg[:50]}...")
                    # Para chaves bloqueadas, não tenta novamente
                    return None
                else:
                    print(f"Lote {lote_num} (tentativa {tentativa + 1}): Erro - {error_msg[:100]}")
                
                if tentativa < Config.MAX_TENTATIVAS - 1:
                    await asyncio.sleep(Config.ESPERA_RETRY * (2 ** tentativa))
                else:
                    print(f"Lote {lote_num}: Falha após {Config.MAX_TENTATIVAS} tentativas")
                    return None
    
    def _processar_texto(self, texto_bruto: Dict[str, Any]) -> Dict[str, Any]:
        """Processa e adiciona metadados ao texto usando esquema simplificado."""
        self.contador_id += 1
        
        # Esquema simplificado de classificação
        classificacao = texto_bruto.get("classificacao", "NEUTRO")
        
        return {
            "id": f"corpus_{self.contador_id:05d}",
            "texto": texto_bruto.get("texto", ""),
            "contexto": texto_bruto.get("contexto", "desconhecido"),
            "palavras_chave": texto_bruto.get("palavras_chave", []),
            "sintetico": True,
            "data_geracao": datetime.now().isoformat(),
            "versao": "2.0",
            # Classificação
            "classificacao": classificacao,
        }
    
    def _validar_texto(self, texto_processado: Dict[str, Any]) -> List[str]:
        """Valida se o texto atende aos critérios mínimos do esquema simplificado."""
        problemas = []
        texto = texto_processado.get("texto", "")
        palavras = texto.split()
        caracteres = len(texto)
        
        # Validações básicas
        if len(palavras) < Config.TAMANHO_MIN_PALAVRAS:
            problemas.append(f"Texto muito curto: {len(palavras)} palavras")
        
        if caracteres > Config.TAMANHO_MAX_CARACTERES:
            problemas.append(f"Texto muito longo: {caracteres} caracteres (máximo 280)")
        
        if not texto.strip():
            problemas.append("Texto vazio")
        
        # Validação do esquema simplificado
        classificacao = texto_processado.get("classificacao")
        classificacoes_validas = ["ODIO_XENOFOBICO", "OFENSIVO_GERAL", "NEUTRO"]
        if classificacao not in classificacoes_validas:
            problemas.append(f"Classificação inválida: {classificacao}")
        
        return problemas
    
    async def _salvar_lote(self, lote: List[Dict[str, Any]], arquivo: Path):
        """Salva um lote de textos no arquivo JSONL."""
        if not lote:
            return
        
        linhas = [json.dumps(item, ensure_ascii=False) + '\n' for item in lote]
        async with aiofiles.open(arquivo, 'a', encoding='utf-8') as f:
            await f.writelines(linhas)
    
    async def gerar_corpus(self, num_lotes: int, arquivo_saida: str, incluir_nao_xenofobia: bool = True):
        """Gera o corpus completo de forma assíncrona."""
        print(f"🚀 Iniciando processamento...")
        print(f"📊 Parâmetros: {num_lotes} lotes de {Config.TAMANHO_LOTE} textos")
        print(f"💾 Arquivo de saída: {arquivo_saida}")
        
        arquivo_path = Path(arquivo_saida)
        arquivo_path.parent.mkdir(parents=True, exist_ok=True)
        
        total_gerados = 0
        total_rejeitados = 0
        total_xenofobia = 0
        total_nao_xenofobia = 0
        
        # Gera lotes de forma assíncrona
        semaforo = asyncio.Semaphore(3)  # Máximo 3 chamadas simultâneas
        
        async def processar_lote(lote_num: int):
            async with semaforo:
                prompt = self._criar_prompt(Config.TAMANHO_LOTE, incluir_nao_xenofobia)
                textos_brutos = await self._gerar_lote(prompt, lote_num)
                
                if not textos_brutos:
                    return 0, 0, 0, 0
                
                # Processa e valida cada texto
                textos_validos = []
                textos_rejeitados = []
                xenofobia_count = 0
                nao_xenofobia_count = 0
                
                for texto_bruto in textos_brutos:
                    texto_processado = self._processar_texto(texto_bruto)
                    problemas = self._validar_texto(texto_processado)
                    
                    if problemas:
                        texto_processado["problemas_validacao"] = problemas
                        textos_rejeitados.append(texto_processado)
                    else:
                        textos_validos.append(texto_processado)
                        if texto_processado.get("classificacao") == "NEUTRO":
                            nao_xenofobia_count += 1
                        elif texto_processado.get("classificacao") == "ODIO_XENOFOBICO":
                            xenofobia_count += 1
                
                # Salva textos válidos
                await self._salvar_lote(textos_validos, arquivo_path)
                
                return len(textos_validos), len(textos_rejeitados), xenofobia_count, nao_xenofobia_count
        
        # Executa todos os lotes
        tasks = [processar_lote(i) for i in range(1, num_lotes + 1)]
        
        for future in tqdm(asyncio.as_completed(tasks), total=num_lotes, desc="Gerando corpus"):
            validos, rejeitados, xenofobia, nao_xenofobia = await future
            total_gerados += validos
            total_rejeitados += rejeitados
            total_xenofobia += xenofobia
            total_nao_xenofobia += nao_xenofobia
        
        print(f"\n✅ Processo concluído!")
        print(f"📈 Total de textos: {total_gerados}")
        print(f"🚫 Textos com xenofobia (ODIO_XENOFOBICO): {total_xenofobia}")
        print(f"✅ Textos neutros (NEUTRO): {total_nao_xenofobia}")
        print(f"❌ Total de textos rejeitados: {total_rejeitados}")
        print(f"💾 Corpus salvo em: {arquivo_path.absolute()}")
        
        if incluir_nao_xenofobia and total_gerados > 0:
            proporcao_xenofobia = (total_xenofobia / total_gerados) * 100
            print(f"📊 Proporção de xenofobia: {proporcao_xenofobia:.1f}%")
        
        print(f"🐦 Formato: Tweets (máximo 280 caracteres)")
        print(f"📋 Esquema: Classificação única")
        print(f"🇧🇷 Foco: Xenofobia no contexto brasileiro")

async def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description="Gerador de Corpus para Xenofobia")
    parser.add_argument("lotes", type=int, help="Número de lotes a gerar")
    parser.add_argument("--arquivo", "-o", default=Config.ARQUIVO_SAIDA, help="Arquivo de saída")
    parser.add_argument("--tamanho-lote", "-s", type=int, default=Config.TAMANHO_LOTE, help="Tamanho de cada lote")
    parser.add_argument("--apenas-xenofobia", action="store_true", help="Gerar apenas textos com xenofobia (sem textos neutros)")
    parser.add_argument("--balanceado", action="store_true", default=True, help="Gerar corpus balanceado (com e sem xenofobia)")
    
    args = parser.parse_args()
    
    # Atualiza configuração se necessário
    Config.TAMANHO_LOTE = args.tamanho_lote
    
    # Define se deve incluir textos sem xenofobia
    incluir_nao_xenofobia = not args.apenas_xenofobia
    
    try:
        # Carrega chaves da API
        api_keys = Config.carregar_chaves_api()
        print(f"🔑 Carregadas {len(api_keys)} chaves da API")
        
        # Cria gerador e executa
        gerador = GeradorCorpusXenofobia(api_keys)
        await gerador.gerar_corpus(args.lotes, args.arquivo, incluir_nao_xenofobia)
        
    except KeyboardInterrupt:
        print("\n⏹️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    asyncio.run(main())
