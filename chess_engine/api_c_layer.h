//=============================================================
// File: chess_engine/api_c_layer.h
// Description: Defines the Function Interface Specification (FIS)
//              for all functions crossing the C <-> Python boundary.
// Contract: Python must use these types and function signatures exactly.
//=============================================================

#ifndef API_C_LAYER_H
#define API_C_LAYER_H

#include <stdbool.h>
#include <stdint.h>

// Type definition for a move (e.g., standard UCI format or structured board change).
typedef struct {
    char start_sq[3]; // e.g., "a1"
    char end_sq[3];   // e.g., "a8"
    bool is_promotion; // true if pawn promotion occurred
} Move;

// Type definition for a standardized chess board state (simplified Bitboard representation).
// In a real system, this would be much more complex.
typedef struct {
    uint64_t white_pieces[6];  // Pieces positions for White
    uint64_t black_pieces[6];  // Pieces positions for Black
    Move last_move;           // Record of the move that led to this state
    bool is_checkmate;
    bool is_stalemate;
} BoardState;

/**
 * @brief Validates if a given move from a starting position is legal according to FIDE rules.
 *
 * @param board The current, assumed-valid board state.
 * @param move The move to validate.
 * @return true if the move does not violate any rule (e.g., king exposed).
 * @return false otherwise.
 */
// Status codes for move validation in the C core engine
typedef enum {
    MOVE_STATUS_SUCCESS = 0,     // Move is perfectly legal and validated.
    MOVE_STATUS_ILLEGAL_STATE,   // The board state itself is invalid (e.g., corrupted data).
    MOVE_STATUS_RULE_VIOLATION,  // The move violates FIDE rules (e.g., moving backward illegally).
    MOVE_STATUS_UNKNOWN_ERROR,   // An unexpected internal engine error occurred.
} MoveStatus;

/**
 * @brief Validates if a given move from a starting position is legal according to FIDE rules.
 *
 * @param board The current, assumed-valid board state.
 * @param move The move to validate.
 * @return MoveStatus detailing why the validation succeeded or failed.
 */
MoveStatus is_move_legal(const BoardState* board, const Move* move);

/**
 * @brief Applies a legal move and calculates the resulting state of the board.
 *
 * This function modifies an output board state struct based on valid inputs.
 *
 * @param current The state before the move.
 * @param move The validated move to apply.
 * @param next_state A pointer to a BoardState structure where the result will be stored.
 * @return true if the transition was successful and the new state is valid.
 * @return false on failure (e.g., internal memory error).
 */
bool apply_move(const BoardState* current, const Move* move, BoardState* next_state);

#endif // API_C_LAYER_H