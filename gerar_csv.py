#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar CSV com ID e texto do corpus.
"""

import json
import csv

def gerar_csv_corpus(arquivo_jsonl, arquivo_csv):
    """Gera CSV com ID e texto do corpus."""
    textos = []
    
    # Lê o arquivo JSONL
    with open(arquivo_jsonl, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.strip():
                try:
                    data = json.loads(linha)
                    textos.append({
                        'id': data.get('id', ''),
                        'texto': data.get('texto', '')
                    })
                except json.JSONDecodeError:
                    print(f"Erro ao processar linha: {linha[:100]}...")
                    continue
    
    print(f"📊 Total de textos processados: {len(textos)}")
    
    # Gera CSV
    with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'texto'])  # Cabeçalho
        
        for texto in textos:
            writer.writerow([texto['id'], texto['texto']])
    
    print(f"✅ CSV gerado: {arquivo_csv}")
    print(f"📈 {len(textos)} linhas de dados + 1 cabeçalho")

if __name__ == "__main__":
    gerar_csv_corpus("corpus_xenofobia_sintetico_corrigido.jsonl", "corpus_xenofobia_sintetico.csv")
