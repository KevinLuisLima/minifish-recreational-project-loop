#ifndef BOARDSTATE_H
#define BOARDSTATE_H

#include <iostream>

// --- Definições de Peças e Constantes ---

// Tipo base para representar uma peça em um quadrado
typedef int PieceType;

/**
 * @brief Estrutura para coordenadas (row/col).
 */
typedef struct {
    int row; // Linha: 0 a 7
    int col; // Coluna: 0 a 7
} Position;

// Constantes de Peças (Números mágicos devem ser tratados com cuidado!)
#define EMPTY_SQUARE -1

// Brancas
#define WHITE_PAWN 1
#define WHITE_KNIGHT 2
#define WHITE_BISHOP 3
#define WHITE_ROOK 4
#define WHITE_QUEEN 5
#define WHITE_KING 6 // Adicionado o Rei, essencial para vitória

// Pretas (Usamos valores diferentes para distinguir)
#define BLACK_PAWN -1
#define BLACK_KNIGHT -2
#define BLACK_BISHOP -3
#define BLACK_ROOK -4
#define BLACK_QUEEN -5
#define BLACK_KING -6

// Valores heurísticos de material (para scoring)
#define VALUE_PAWN 1.0
#define VALUE_KNIGHT 2.0
#define VALUE_BISHOP 3.0
#define VALUE_ROOK 5.0
#define VALUE_QUEEN 9.0
#define VALUE_KING 100.0 // O rei tem valor quase infinito para não ser sacrificado

/**
 * @brief Calcula todos os movimentos legais possíveis para uma peça específica em uma dada posição.
 * @param state O estado atual do tabuleiro.
 * @param start A posição de origem.
 * @param piece_type O tipo de peça a mover.
 * @return Um array/lista de todas as posições de destino válidas. (Simplificado para este header).
 */
Position* calculate_legal_destinations(const BoardState* state, Position start, PieceType piece_type);