#include "BoardState.h"
#include <iostream>
#include <cmath> // Para funções matemáticas como abs()

// Função auxiliar para obter o tipo de peça em uma posição dada (Positional Safety Check)
PieceType get_piece(const BoardState* state, Position pos) {
    if (pos.row < 0 || pos.row > 7 || pos.col < 0 || pos.col > 7) {
        // O console de logs não deve receber mensagens complexas, apenas valores de erro.
        return EMPTY_SQUARE; // Fora do tabuleiro
    }
    return state->board[pos.row][pos.col];
}

// ========================================
// Implementação das Funções Core do Motor C++
// ========================================

/**
 * @brief Inicializa o estado do tabuleiro para a posição inicial padrão (RFC).
 */
void initialize_board(BoardState* state) {
    // 1. Resetar todo o tabuleiro:
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 8; ++j) {
            state->board[i][j] = EMPTY_SQUARE;
        }
    }

    // 2. Configuração das peças Brancas (Linha 7, índice 7):
    // Peões na linha 6 (índice 6)
    for(int j = 0; j < 8; ++j) {
        state->board[6][j] = WHITE_PAWN;
    }
    // Linha 7: R, N, B, Q, K, B, N, R (Adaptado para incluir um Rei)
    state->board[7][0] = WHITE_ROOK;
    state->board[7][1] = WHITE_KNIGHT;
    state->board[7][2] = WHITE_BISHOP;
    state->board[7][3] = WHITE_QUEEN;
    state->board[7][4] = WHITE_KING; // Adicionado Rei em D1
    state->board[7][5] = WHITE_BISHOP;
    state->board[7][6] = WHITE_KNIGHT;
    state->board[7][7] = WHITE_ROOK;

    // 3. Configuração das peças Pretas (Linha 0, índice 0):
    // Peões na linha 1 (índice 1)
    for(int j = 0; j < 8; ++j) {
        state->board[1][j] = BLACK_PAWN;
    }
    // Linha 0: R, N, B, Q, K, B, N, R (Espelhamento)
    state->board[0][0] = BLACK_ROOK;
    state->board[0][1] = BLACK_KNIGHT;
    state->board[0][2] = BLACK_BISHOP;
    state->board[0][3] = BLACK_QUEEN;
    state->board[0][4] = BLACK_KING; // Adicionado Rei em D8
    state->board[0][5] = BLACK_BISHOP;
    state->board[0][6] = BLACK_KNIGHT;
    state->board[0][7] = BLACK_ROOK;

    // Definir o turno inicial
    state->turn = 1; // Brancas começam (Turno 1)
}


/**
 * @brief Verifica se um movimento é legal e seguro no estado atual.
 */
int is_valid_move(const BoardState* state, Position start, Position end) {
    // VALIDATION CHECK: 1. Origem/Destino devem ser dentro do tabuleiro (já assumido pela API de chamada).
    PieceType piece = get_piece(state, start);
    if (piece == EMPTY_SQUARE) return 0; // Origem vazia

    // VALIDATION CHECK: 2. Não pode mover para cima de um amigo
    PieceType target_piece = state->board[end.row][end.col];
    if (target_piece != EMPTY_SQUARE && get_enemy(piece) == get_owner(target_piece)) {
        return 0; // Tentando capturar seu próprio peão/peça.
    }

    // A lógica completa depende de funções complexas como calcular movimentos legais para cada peça:
    switch (piece) {
        case WHITE_PAWN:
            // Implementação da regra de peões é extremamente longa e requer a verificação do passado do movimento.
            return 1; // Placeholder, deveria ser verificada pela lógica completa
        case WHITE_KNIGHT:
            // Lógica de cavalo (L shape)
            return 1; // Placeholder
        default:
             // Para todas as outras peças e movimentos padrões (Roque, etc.)
            return 1; // Assume-se válido para fins do plano. A lógica real será construída em módulos específicos.
    }

    return 0;
}


/**
 * @brief Aplica o movimento de forma segura e atualiza o estado do jogo.
 */
int make_move(BoardState* currentState, Position start, Position end) {
    // Esta função é transacional: verifica, executa e só muda o turno se tudo der certo.

    if (!is_valid_move(currentState, start, end)) {
        return 0; // Movimento ilegal (Regra de negócio falhou).
    }

    // 1. Executar a cópia do estado antes da mudança para segurança (se fosse em C++, seria um const).
    // Em C, precisamos garantir que o cliente use uma *cópia* se quiser reverter.

    PieceType piece = get_piece(currentState, start);

    // 2. Aplicar a movimentação no estado atualizado
    currentState->board[end.row][end.col] = piece;
    currentState->board[start.row][start.col] = EMPTY_SQUARE;

    // 3. Alternar o turno (Game State Transition)
    if (currentState->turn == 1) {
        currentState->turn = 2; // Turno passa para Pretas
    } else {
        currentState->turn = 1; // Turno passa para Brancas
    }

    return 1;
}

// --- Funções Auxiliares de Utilitário (Necessárias para a lógica do jogo) ---

/**
 * @brief Determina se duas peças são inimigas.
 */
int get_enemy(PieceType piece) {
    if (piece >= WHITE_PAWN && piece <= WHITE_ROOK) return -1; // Brancas vs Pretas
    if (piece >= BLACK_PAWN && piece <= BLACK_KING) return 1;  // Pretas vs Brancas
    return 0; // Indefinido ou peças não classificadas.
}

/**
 * @brief Determina a cor da peça (Retorna 1 para Branca, 2 para Preta).
 */
int get_owner(PieceType piece) {
    if (piece >= WHITE_PAWN && piece <= WHITE_ROOK) return 1;
    if (piece >= BLACK_PAWN && piece <= BLACK_KING) return 2;
    return 0;
}

#endif // BOARDSTATE_H