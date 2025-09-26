# -*- coding: utf-8 -*-

"""
Avaliador de Concordância entre Anotadores
Trabalho de Mestrado em Processamento de Linguagem Natural

Calcula métricas de concordância entre anotadores para validar a qualidade
das anotações de xenofobia.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class AvaliadorConcordancia:
    """Avaliador de concordância entre anotadores."""
    
    def __init__(self, arquivo_anotacoes: str):
        self.arquivo_anotacoes = arquivo_anotacoes
        self.anotacoes = self._carregar_anotacoes()
        self.dados_concordancia = self._preparar_dados_concordancia()
    
    def _carregar_anotacoes(self) -> List[Dict[str, Any]]:
        """Carrega anotações do arquivo JSONL."""
        anotacoes = []
        if Path(self.arquivo_anotacoes).exists():
            with open(self.arquivo_anotacoes, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        anotacoes.append(json.loads(line))
        return anotacoes
    
    def _preparar_dados_concordancia(self) -> Dict[str, List[Dict[str, Any]]]:
        """Agrupa anotações por texto para análise de concordância."""
        grupos = defaultdict(list)
        for anotacao in self.anotacoes:
            id_texto = anotacao.get('id_texto')
            if id_texto:
                grupos[id_texto].append(anotacao)
        
        # Filtra apenas textos com múltiplas anotações
        return {k: v for k, v in grupos.items() if len(v) > 1}
    
    def calcular_kappa_cohen(self) -> Dict[str, float]:
        """Calcula coeficiente Kappa de Cohen para diferentes aspectos."""
        resultados = {}
        
        if not self.dados_concordancia:
            return {"erro": "Nenhum texto com múltiplas anotações encontrado"}
        
        # Prepara dados para cálculo
        textos_ids = list(self.dados_concordancia.keys())
        
        # Kappa para categoria principal
        categorias_anotador1 = []
        categorias_anotador2 = []
        
        for texto_id in textos_ids:
            anotacoes = self.dados_concordancia[texto_id]
            if len(anotacoes) >= 2:
                categorias_anotador1.append(anotacoes[0].get('categoria_principal', ''))
                categorias_anotador2.append(anotacoes[1].get('categoria_principal', ''))
        
        if categorias_anotador1 and categorias_anotador2:
            kappa_categoria = cohen_kappa_score(categorias_anotador1, categorias_anotador2)
            resultados['categoria_principal'] = kappa_categoria
        
        # Kappa para subcategoria (apenas textos classificados como XENOFOBIA)
        subcategorias_anotador1 = []
        subcategorias_anotador2 = []
        
        for texto_id in textos_ids:
            anotacoes = self.dados_concordancia[texto_id]
            if len(anotacoes) >= 2:
                cat1 = anotacoes[0].get('categoria_principal')
                cat2 = anotacoes[1].get('categoria_principal')
                if cat1 == 'XENOFOBIA' and cat2 == 'XENOFOBIA':
                    subcategorias_anotador1.append(anotacoes[0].get('subcategoria', ''))
                    subcategorias_anotador2.append(anotacoes[1].get('subcategoria', ''))
        
        if subcategorias_anotador1 and subcategorias_anotador2:
            kappa_subcategoria = cohen_kappa_score(subcategorias_anotador1, subcategorias_anotador2)
            resultados['subcategoria'] = kappa_subcategoria
        
        # Kappa para intensidade (apenas textos classificados como XENOFOBIA)
        intensidades_anotador1 = []
        intensidades_anotador2 = []
        
        for texto_id in textos_ids:
            anotacoes = self.dados_concordancia[texto_id]
            if len(anotacoes) >= 2:
                cat1 = anotacoes[0].get('categoria_principal')
                cat2 = anotacoes[1].get('categoria_principal')
                if cat1 == 'XENOFOBIA' and cat2 == 'XENOFOBIA':
                    intensidades_anotador1.append(anotacoes[0].get('intensidade', ''))
                    intensidades_anotador2.append(anotacoes[1].get('intensidade', ''))
        
        if intensidades_anotador1 and intensidades_anotador2:
            kappa_intensidade = cohen_kappa_score(intensidades_anotador1, intensidades_anotador2)
            resultados['intensidade'] = kappa_intensidade
        
        return resultados
    
    def calcular_concordancia_porcentual(self) -> Dict[str, float]:
        """Calcula concordância percentual para diferentes aspectos."""
        resultados = {}
        
        if not self.dados_concordancia:
            return {"erro": "Nenhum texto com múltiplas anotações encontrado"}
        
        total_textos = len(self.dados_concordancia)
        
        # Concordância para categoria principal
        concordantes_categoria = 0
        for anotacoes in self.dados_concordancia.values():
            if len(anotacoes) >= 2:
                cat1 = anotacoes[0].get('categoria_principal')
                cat2 = anotacoes[1].get('categoria_principal')
                if cat1 == cat2:
                    concordantes_categoria += 1
        
        resultados['categoria_principal'] = (concordantes_categoria / total_textos * 100) if total_textos > 0 else 0
        
        # Concordância para subcategoria (apenas XENOFOBIA)
        textos_xenofobia = 0
        concordantes_subcategoria = 0
        
        for anotacoes in self.dados_concordancia.values():
            if len(anotacoes) >= 2:
                cat1 = anotacoes[0].get('categoria_principal')
                cat2 = anotacoes[1].get('categoria_principal')
                if cat1 == 'XENOFOBIA' and cat2 == 'XENOFOBIA':
                    textos_xenofobia += 1
                    subcat1 = anotacoes[0].get('subcategoria')
                    subcat2 = anotacoes[1].get('subcategoria')
                    if subcat1 == subcat2:
                        concordantes_subcategoria += 1
        
        resultados['subcategoria'] = (concordantes_subcategoria / textos_xenofobia * 100) if textos_xenofobia > 0 else 0
        
        # Concordância para intensidade (apenas XENOFOBIA)
        concordantes_intensidade = 0
        
        for anotacoes in self.dados_concordancia.values():
            if len(anotacoes) >= 2:
                cat1 = anotacoes[0].get('categoria_principal')
                cat2 = anotacoes[1].get('categoria_principal')
                if cat1 == 'XENOFOBIA' and cat2 == 'XENOFOBIA':
                    int1 = anotacoes[0].get('intensidade')
                    int2 = anotacoes[1].get('intensidade')
                    if int1 == int2:
                        concordantes_intensidade += 1
        
        resultados['intensidade'] = (concordantes_intensidade / textos_xenofobia * 100) if textos_xenofobia > 0 else 0
        
        return resultados
    
    def analisar_discordancias(self) -> List[Dict[str, Any]]:
        """Identifica e analisa casos de discordância entre anotadores."""
        discordancias = []
        
        for texto_id, anotacoes in self.dados_concordancia.items():
            if len(anotacoes) >= 2:
                anotacao1 = anotacoes[0]
                anotacao2 = anotacoes[1]
                
                # Verifica discordâncias
                discordancia = {
                    'id_texto': texto_id,
                    'texto': anotacao1.get('texto_original', ''),
                    'anotador1': anotacao1.get('anotador', ''),
                    'anotador2': anotacao2.get('anotador', ''),
                    'discordancias': []
                }
                
                # Categoria principal
                if anotacao1.get('categoria_principal') != anotacao2.get('categoria_principal'):
                    discordancia['discordancias'].append({
                        'aspecto': 'categoria_principal',
                        'anotador1': anotacao1.get('categoria_principal'),
                        'anotador2': anotacao2.get('categoria_principal')
                    })
                
                # Subcategoria
                if anotacao1.get('subcategoria') != anotacao2.get('subcategoria'):
                    discordancia['discordancias'].append({
                        'aspecto': 'subcategoria',
                        'anotador1': anotacao1.get('subcategoria'),
                        'anotador2': anotacao2.get('subcategoria')
                    })
                
                # Intensidade
                if anotacao1.get('intensidade') != anotacao2.get('intensidade'):
                    discordancia['discordancias'].append({
                        'aspecto': 'intensidade',
                        'anotador1': anotacao1.get('intensidade'),
                        'anotador2': anotacao2.get('intensidade')
                    })
                
                if discordancia['discordancias']:
                    discordancias.append(discordancia)
        
        return discordancias
    
    def gerar_relatorio(self) -> str:
        """Gera relatório completo de concordância."""
        kappa = self.calcular_kappa_cohen()
        concordancia_pct = self.calcular_concordancia_porcentual()
        discordancias = self.analisar_discordancias()
        
        relatorio = f"""
# Relatório de Concordância entre Anotadores
## Detecção de Discurso de Ódio - XENOFOBIA

### Resumo Geral
- **Total de anotações**: {len(self.anotacoes)}
- **Textos com múltiplas anotações**: {len(self.dados_concordancia)}
- **Casos de discordância**: {len(discordancias)}

### Métricas de Concordância

#### Coeficiente Kappa de Cohen
- **Categoria Principal**: {kappa.get('categoria_principal', 'N/A'):.3f}
- **Subcategoria**: {kappa.get('subcategoria', 'N/A'):.3f}
- **Intensidade**: {kappa.get('intensidade', 'N/A'):.3f}

#### Concordância Percentual
- **Categoria Principal**: {concordancia_pct.get('categoria_principal', 0):.1f}%
- **Subcategoria**: {concordancia_pct.get('subcategoria', 0):.1f}%
- **Intensidade**: {concordancia_pct.get('intensidade', 0):.1f}%

### Interpretação dos Resultados

#### Kappa de Cohen
- **< 0.20**: Concordância pobre
- **0.21-0.40**: Concordância razoável
- **0.41-0.60**: Concordância moderada
- **0.61-0.80**: Concordância substancial
- **> 0.80**: Concordância quase perfeita

#### Meta de Qualidade
- **Kappa ≥ 0.70**: Concordância substancial
- **Concordância percentual ≥ 80%**: Boa concordância

### Casos de Discordância
"""
        
        if discordancias:
            relatorio += f"\nEncontrados {len(discordancias)} casos de discordância:\n\n"
            for i, disc in enumerate(discordancias[:5], 1):  # Mostra apenas os primeiros 5
                relatorio += f"#### Caso {i}\n"
                relatorio += f"**Texto**: {disc['texto'][:100]}...\n"
                relatorio += f"**Anotadores**: {disc['anotador1']} vs {disc['anotador2']}\n"
                relatorio += f"**Discordâncias**:\n"
                for d in disc['discordancias']:
                    relatorio += f"- {d['aspecto']}: {d['anotador1']} vs {d['anotador2']}\n"
                relatorio += "\n"
        else:
            relatorio += "\nNenhum caso de discordância encontrado.\n"
        
        relatorio += f"""
### Recomendações

1. **Treinamento adicional**: Se Kappa < 0.70, revisar diretrizes
2. **Discussão de casos difíceis**: Analisar discordancias identificadas
3. **Revisão de diretrizes**: Clarificar critérios ambíguos
4. **Validação cruzada**: Implementar anotação por terceiro anotador

### Próximos Passos

1. Revisar casos de discordância com a equipe
2. Atualizar diretrizes de anotação se necessário
3. Realizar nova rodada de anotações
4. Recalcular métricas de concordância
"""
        
        return relatorio
    
    def salvar_relatorio(self, arquivo_saida: str = "relatorio_concordancia.md"):
        """Salva o relatório em arquivo."""
        relatorio = self.gerar_relatorio()
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        print(f"Relatório salvo em: {arquivo_saida}")

def main():
    """Função principal para executar avaliação de concordância."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Avaliador de Concordância entre Anotadores")
    parser.add_argument("--arquivo", "-a", default="anotacoes_xenofobia.jsonl", 
                       help="Arquivo de anotações")
    parser.add_argument("--saida", "-s", default="relatorio_concordancia.md",
                       help="Arquivo de saída do relatório")
    
    args = parser.parse_args()
    
    # Executa avaliação
    avaliador = AvaliadorConcordancia(args.arquivo)
    
    print("🔍 Analisando concordância entre anotadores...")
    print(f"📁 Arquivo: {args.arquivo}")
    
    # Gera e salva relatório
    avaliador.salvar_relatorio(args.saida)
    
    # Exibe resumo no console
    kappa = avaliador.calcular_kappa_cohen()
    concordancia = avaliador.calcular_concordancia_porcentual()
    
    print("\n📊 Resumo dos Resultados:")
    print(f"Kappa - Categoria: {kappa.get('categoria_principal', 'N/A'):.3f}")
    print(f"Kappa - Subcategoria: {kappa.get('subcategoria', 'N/A'):.3f}")
    print(f"Concordância - Categoria: {concordancia.get('categoria_principal', 0):.1f}%")
    print(f"Concordância - Subcategoria: {concordancia.get('subcategoria', 0):.1f}%")
    
    print(f"\n✅ Relatório completo salvo em: {args.saida}")

if __name__ == "__main__":
    main()
