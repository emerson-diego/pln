# -*- coding: utf-8 -*-

"""
Ferramenta de Anotação Manual para Detecção de Discurso de Ódio - XENOFOBIA
Trabalho de Mestrado em Processamento de Linguagem Natural

Interface web simples para anotação manual de textos.
Permite classificação de textos quanto à presença de xenofobia.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Anotação de Xenofobia",
    page_icon="🚫",
    layout="wide"
)

@dataclass
class ConfigAnotacao:
    """Configurações da ferramenta de anotação."""
    CATEGORIAS = ["XENOFOBIA", "NAO_XENOFOBIA"]
    SUBCATEGORIAS = {
        "XENOFOBIA": [
            "NACIONALIDADE", "IMIGRANTE", "DISCRIMINACAO_ECONOMICA",
            "DISCRIMINACAO_CULTURAL", "GENERALIZACAO_NEGATIVA"
        ],
        "NAO_XENOFOBIA": []
    }
    INTENSIDADES = ["SUTIL", "MODERADO", "EXPLICITO"]
    ARQUIVO_ANOTACOES = "anotacoes_xenofobia.jsonl"

class FerramentaAnotacao:
    """Ferramenta principal de anotação."""
    
    def __init__(self):
        self.config = ConfigAnotacao()
        self.textos_para_anotar = []
        self.anotacoes = []
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega textos para anotação e anotações existentes."""
        # Carrega textos do corpus sintético
        corpus_path = Path("../../geracao_sintetica/corpus_xenofobia_sintetico.jsonl")
        if corpus_path.exists():
            with open(corpus_path, 'r', encoding='utf-8') as f:
                self.textos_para_anotar = [json.loads(line) for line in f if line.strip()]
        
        # Carrega anotações existentes
        anotacoes_path = Path(self.config.ARQUIVO_ANOTACOES)
        if anotacoes_path.exists():
            with open(anotacoes_path, 'r', encoding='utf-8') as f:
                self.anotacoes = [json.loads(line) for line in f if line.strip()]
    
    def salvar_anotacao(self, anotacao: Dict[str, Any]):
        """Salva uma anotação no arquivo."""
        with open(self.config.ARQUIVO_ANOTACOES, 'a', encoding='utf-8') as f:
            f.write(json.dumps(anotacao, ensure_ascii=False) + '\n')
        self.anotacoes.append(anotacao)
    
    def obter_proximo_texto(self) -> Optional[Dict[str, Any]]:
        """Obtém o próximo texto para anotação."""
        # Filtra textos já anotados
        ids_anotados = {anotacao.get('id_texto') for anotacao in self.anotacoes}
        textos_nao_anotados = [
            texto for texto in self.textos_para_anotar 
            if texto.get('id') not in ids_anotados
        ]
        
        if not textos_nao_anotados:
            return None
        
        return random.choice(textos_nao_anotados)
    
    def calcular_estatisticas(self) -> Dict[str, Any]:
        """Calcula estatísticas das anotações."""
        if not self.anotacoes:
            return {"total": 0}
        
        total = len(self.anotacoes)
        xenofobia = sum(1 for a in self.anotacoes if a.get('categoria_principal') == 'XENOFOBIA')
        nao_xenofobia = total - xenofobia
        
        # Contagem por subcategoria
        subcategorias = {}
        for anotacao in self.anotacoes:
            subcat = anotacao.get('subcategoria')
            if subcat:
                subcategorias[subcat] = subcategorias.get(subcat, 0) + 1
        
        # Contagem por intensidade
        intensidades = {}
        for anotacao in self.anotacoes:
            intensidade = anotacao.get('intensidade')
            if intensidade:
                intensidades[intensidade] = intensidades.get(intensidade, 0) + 1
        
        return {
            "total": total,
            "xenofobia": xenofobia,
            "nao_xenofobia": nao_xenofobia,
            "percentual_xenofobia": (xenofobia / total * 100) if total > 0 else 0,
            "subcategorias": subcategorias,
            "intensidades": intensidades
        }

def main():
    """Interface principal da ferramenta."""
    st.title("🚫 Ferramenta de Anotação - Xenofobia")
    st.markdown("**Trabalho de Mestrado em Processamento de Linguagem Natural**")
    
    # Inicializa ferramenta
    if 'ferramenta' not in st.session_state:
        st.session_state.ferramenta = FerramentaAnotacao()
    
    ferramenta = st.session_state.ferramenta
    
    # Sidebar com estatísticas
    with st.sidebar:
        st.header("📊 Estatísticas")
        stats = ferramenta.calcular_estatisticas()
        
        if stats["total"] > 0:
            st.metric("Total Anotado", stats["total"])
            st.metric("Xenofobia", f"{stats['xenofobia']} ({stats['percentual_xenofobia']:.1f}%)")
            st.metric("Não Xenofobia", stats["nao_xenofobia"])
            
            if stats["subcategorias"]:
                st.subheader("Subcategorias")
                for subcat, count in stats["subcategorias"].items():
                    st.write(f"• {subcat}: {count}")
            
            if stats["intensidades"]:
                st.subheader("Intensidades")
                for intensidade, count in stats["intensidades"].items():
                    st.write(f"• {intensidade}: {count}")
        else:
            st.info("Nenhuma anotação ainda")
    
    # Área principal de anotação
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Anotação de Texto")
        
        # Obtém próximo texto
        texto_atual = ferramenta.obter_proximo_texto()
        
        if not texto_atual:
            st.success("🎉 Todos os textos foram anotados!")
            st.info("Adicione mais textos ao corpus para continuar anotando.")
            return
        
        # Exibe texto para anotação
        st.subheader("Texto para Anotação")
        st.write(f"**ID:** {texto_atual.get('id', 'N/A')}")
        st.write(f"**Contexto:** {texto_atual.get('contexto', 'N/A')}")
        
        # Texto principal em destaque
        st.markdown(f"### \"{texto_atual.get('texto', '')}\"")
        
        # Formulário de anotação
        with st.form("form_anotacao"):
            st.subheader("Classificação")
            
            # Categoria principal
            categoria = st.radio(
                "Categoria Principal:",
                ferramenta.config.CATEGORIAS,
                help="Classifique se o texto contém discurso de ódio xenofóbico"
            )
            
            # Subcategoria (se xenofobia)
            subcategoria = None
            if categoria == "XENOFOBIA":
                subcategoria = st.selectbox(
                    "Subcategoria:",
                    ferramenta.config.SUBCATEGORIAS["XENOFOBIA"],
                    help="Especifique o tipo de xenofobia"
                )
            
            # Intensidade (se xenofobia)
            intensidade = None
            if categoria == "XENOFOBIA":
                intensidade = st.selectbox(
                    "Intensidade:",
                    ferramenta.config.INTENSIDADES,
                    help="Nível de intensidade do discurso de ódio"
                )
            
            # Palavras-chave
            palavras_chave = st.text_input(
                "Palavras-chave (separadas por vírgula):",
                value=", ".join(texto_atual.get('palavras_chave', [])),
                help="Palavras que indicam xenofobia no texto"
            )
            
            # Justificativa
            justificativa = st.text_area(
                "Justificativa:",
                placeholder="Explique brevemente sua classificação...",
                help="Justifique sua decisão de classificação"
            )
            
            # Botões
            col_salvar, col_pular = st.columns(2)
            
            with col_salvar:
                if st.form_submit_button("💾 Salvar Anotação", type="primary"):
                    # Cria anotação
                    anotacao = {
                        "id_texto": texto_atual.get('id'),
                        "texto_original": texto_atual.get('texto'),
                        "categoria_principal": categoria,
                        "subcategoria": subcategoria,
                        "intensidade": intensidade,
                        "palavras_chave": [p.strip() for p in palavras_chave.split(',') if p.strip()],
                        "justificativa": justificativa,
                        "anotador": "anotador_1",  # Em produção, pegar do login
                        "data_anotacao": st.session_state.get('data_atual', '2025-01-12')
                    }
                    
                    # Salva anotação
                    ferramenta.salvar_anotacao(anotacao)
                    st.success("✅ Anotação salva com sucesso!")
                    st.rerun()
            
            with col_pular:
                if st.form_submit_button("⏭️ Pular Texto"):
                    st.info("Texto pulado. Próximo texto será carregado.")
                    st.rerun()
    
    with col2:
        st.header("📋 Instruções")
        st.markdown("""
        ### Como Anotar:
        
        1. **Leia o texto completo**
        2. **Identifique indicadores de xenofobia**:
           - Discriminação por nacionalidade
           - Aversão a imigrantes
           - Generalizações negativas
           - Linguagem ofensiva
        
        3. **Classifique**:
           - **XENOFOBIA**: Contém discurso de ódio
           - **NAO_XENOFOBIA**: Não contém discurso de ódio
        
        4. **Se XENOFOBIA**, especifique:
           - **Subcategoria**: Tipo de xenofobia
           - **Intensidade**: Nível de ofensividade
        
        5. **Justifique** sua decisão
        """)
        
        st.header("🔍 Exemplos")
        
        with st.expander("Exemplo de XENOFOBIA"):
            st.write("**Texto:** 'Esses gringos só vêm pra cá se aproveitar'")
            st.write("**Classificação:** XENOFOBIA - NACIONALIDADE - MODERADO")
        
        with st.expander("Exemplo de NÃO XENOFOBIA"):
            st.write("**Texto:** 'Precisamos de políticas migratórias melhores'")
            st.write("**Classificação:** NAO_XENOFOBIA")
        
        st.header("📁 Arquivos")
        st.write(f"**Corpus:** {len(ferramenta.textos_para_anotar)} textos")
        st.write(f"**Anotados:** {len(ferramenta.anotacoes)} textos")
        
        if st.button("📥 Baixar Anotações"):
            if ferramenta.anotacoes:
                # Cria arquivo para download
                json_str = json.dumps(ferramenta.anotacoes, ensure_ascii=False, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name="anotacoes_xenofobia.json",
                    mime="application/json"
                )
            else:
                st.warning("Nenhuma anotação para baixar")

if __name__ == "__main__":
    main()
