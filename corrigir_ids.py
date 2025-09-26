#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir IDs sequenciais no arquivo JSONL.
"""

import json
import re

def corrigir_ids_jsonl(arquivo_entrada, arquivo_saida):
    """Corrige IDs para ficarem sequenciais."""
    textos = []
    
    # Lê o arquivo
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.strip():
                try:
                    data = json.loads(linha)
                    textos.append(data)
                except json.JSONDecodeError:
                    print(f"Erro ao processar linha: {linha[:100]}...")
                    continue
    
    print(f"📊 Total de textos encontrados: {len(textos)}")
    
    # Corrige IDs sequenciais
    for i, texto in enumerate(textos, 1):
        texto['id'] = f"corpus_{i:05d}"
    
    # Salva o arquivo corrigido
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for texto in textos:
            f.write(json.dumps(texto, ensure_ascii=False) + '\n')
    
    print(f"✅ IDs corrigidos e salvos em: {arquivo_saida}")
    print(f"📈 IDs agora vão de corpus_00001 até corpus_{len(textos):05d}")

if __name__ == "__main__":
    corrigir_ids_jsonl("corpus_xenofobia_sintetico.jsonl", "corpus_xenofobia_sintetico_corrigido.jsonl")
