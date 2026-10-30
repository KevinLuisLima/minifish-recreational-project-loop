#ifndef API_C_LAYER_H
#define API_C_LAYER_H

#include <stdbool.h>
#include <stdio.h> // For standard C logging

// --- ENUMERATIONS (Single Source of Truth) ---

/**
 * @brief Enumerates all possible outcomes of a move attempt according to FIDE rules validation.
 */
typedef enum {
    MOVE_STATUS_SUCCESS = 0,          // Move is perfectly legal.
    MOVE_STATUS_ILLEGAL_STATE,       // System error (NULL pointers, corrupted memory).
    MOVE_STATUS_RULE_VIOLATION,      // Geometry or target constraint fail (e.g., Pawn jump).
    MOVE_STATUS_CHECK_FAILURE,       // The move leaves the King in check from a different angle/perspective.
    MOVE_STATUS_NO_MOVES_FOR_TURN     // No moves are legal (Stalemate or Checkmate state reached).
} MoveStatus;

/**
 * @brief Holds detailed information about a move candidate.
 */
typedef struct {
    char start_sq[3]; // e.g., "a1"
    char end_sq[3];   // e.g., "b2"
    bool is_capture;
    int promotion_type; // 1=Queen, 2=Rook, etc.
} Move;


/**
 * @brief Represents the immutable state of the chess game board at a specific moment in time.
 */
typedef struct {
    char pieces[65][3]; // Array of 8x8 squares (e.g., "bP" for Black Pawn)
    char last_move[10];
    int turn_count;
    char player_color[7]; // "WHITE" or "BLACK"
    bool is_checkmate;
    bool is_stalemate;

    // State tracking needed for complex rules:
    bool can_castle_king_side[2];
    bool can_castle_queen_side[2];
    char last_pawn_double_advance[10]; // Tracks the location of a recent pawn double-move.

} BoardState;

// === Function Prototypes (Must match headers/definitions) ===

MoveStatus is_move_legal(const BoardState* board, const Move* move);
bool apply_move(const BoardState* current, const Move* move, BoardState* next_state);


#endif // API_C_LAYER_H