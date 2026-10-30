# -*- coding: utf-8 -*-
"""
Módulo de Interoperabilidade Python <-> C++.

ESTE MÓDULO É O PONTO DE ENCONTRO (THE BRIDGE) entre o poder computacional e a
estrutura lógica do motor de xadrez C++ e o ambiente de alto nível de gerenciamento de estado em Python.

IMPORTANTE: Este script assume que os arquivos chess_engine/BoardState.cpp,
chess_engine/ChessAPIWrapper.cpp e cabeçalhos foram compilados na biblioteca compartilhada
'libchess_core.so' (ou '.dll' no Windows).

Funções de teste devem ser adaptadas ao caminho exato da sua compilação!
"""
import ctypes
import os

# --- Configuração do Bindling C/C++ ---
try:
    # Adapte esta linha conforme seu sistema operacional e a extensão de biblioteca (.so, .dll)
    LIB_PATH = "./libchess_core.so"
    chess_lib = ctypes.CDLL(LIB_PATH)
    print("[✅] Biblioteca C++ core carregada com sucesso.")
except OSError as e:
    print("========================================================")
    print(f"[❌] ERRO CRÍTICO DE COMPILAÇÃO (OS Error): {e}")
    print("🚨 PARE! Você deve compilar o código C++/C para uma biblioteca compartilhada")
    print(f"   ex: g++ chess_engine/*.cpp -o libchess_core.so -shared")
    print("========================================================")
    # Em caso de falha, precisamos mockar as funções para continuar os testes conceituais (se for o caso).
    # Neste ponto, é melhor parar e pedir a compilação correta.
    chess_lib = None

def run_poc_test():
    """
    Executa um Proof-of-Concept: Inicializa o tabuleiro em C++, usa Python para testar
    a validade do movimento e transição de turno, e exibe os resultados.
    """
    if chess_lib is None:
        print("\n[!] Não é possível rodar o PoC sem a biblioteca core compilada.")
        return

    # --- Preparação de Estruturas C em Python ---
    # 1. Definir tipos de dados C++ que Python precisa conhecer (Estrutura BoardState)
    class Position(ctypes.Structure):
        _fields_ = [("row", ctypes.c_int), ("col", ctypes.c_int)]

    class BoardState(ctypes.Structure):
        _fields_ = [] # A complexidade de arrays dinâmicos em ctypes é alta; simplificamos a simulação
        # Em um cenário real, você teria que mapear o array [8][8] manualmente.
        pass

    # Para este PoC, vamos confiar nas chamadas diretas da API wrapper e ignorar a complexidade do ctpyes Array em Python

    print("\n--- Iniciando Teste de Prova de Conceito (PoC) ---")

    # 1. Criar um estado do tabuleiro na memória C++
    board_state = BoardState() # Instância simulada
    chess_lib.api_initialize_board(ctypes.pointer(board_state))
    print("✅ Estado inicial do tabuleiro foi carregado (Turno: Brancas).")

    # 2. Simular um movimento conhecido para testar a transição de turno e validade.
    start = Position(row=6, col=0) # Peão em A7 (Brancas)
    end = Position(row=5, col=1)   # Destino vazio (simulação de avanço 1 casa)

    print(f"Tentando movimento: {start.col}:{start.row} -> {end.col}:{end.row}")

    is_valid = chess_lib.api_is_valid_move(&board_state, start, end)
    if is_valid:
        print("  [VALIDAÇÃO] Movimento considerado legal pelo motor C++.")

        # Executa o movimento e atualiza o estado
        success = chess_lib.api_make_move(&board_state, start, end)

        if success:
            print(f"✅ Sucesso! Estado atualizado. Próximo turno esperado (Pretas).")
        else:
            print("❌ FALHA ao aplicar o movimento.")
    else:
        print("⚠️ Atenção: O PoC não conseguiu validar um movimento específico. A lógica de 'is_valid_move' deve ser preenchida no motor C++.")

if __name__ == "__main__":
    run_poc_test()
