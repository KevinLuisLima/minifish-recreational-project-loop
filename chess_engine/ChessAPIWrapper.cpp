#include "BoardState.h"
#include <cstdio>

// ========================================
// API Wrapper Functions (Exportáveis para Python)
// Estas funções servem como a interface C-style para o motor de xadrez.
// Elas encapsulam e chamam as funções reais dentro da biblioteca.
// ========================================

/**
 * @brief Inicializa um novo estado do tabuleiro.
 * Deve ser chamada no início de cada simulação ou jogo testado.
 * @param state Um ponteiro para a estrutura BoardState que será inicializada.
 */
void api_initialize_board(BoardState* state) {
    // Chama a função interna, mantendo a lógica pura do motor.
    initialize_board(state);
}

/**
 * @brief Verifica se um movimento é legal.
 * Retorna 1 (true) ou 0 (false).
 */
int api_is_valid_move(const BoardState* state, Position start, Position end) {
    return is_valid_move(state, start, end);
}

/**
 * @brief Tenta aplicar um movimento e atualiza o estado do tabuleiro.
 * Retorna 1 (true) se o movimento foi aplicado com sucesso, 0 caso contrário.
 */
int api_make_move(BoardState* currentState, Position start, Position end) {
    return make_move(currentState, start, end);
}

// O compilador C++ deve exportar estas funções para serem encontradas pelo linker/ctypes do Python.
// Na prática real de build, usaríamos extern "C" ou CMake para garantir isso.
