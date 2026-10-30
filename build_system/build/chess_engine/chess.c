//=============================================================
// File: chess_engine/chess.c
// Description: Primary implementation of the ChessEngine core logic.
// Dependencies: Now correctly includes api_c_layer.h for all common types and enums.
// It MUST use only C basic features, as per project mandate.
//=============================================================

#include "api_c_layer.h" // NEW: Canonical header for shared definitions
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * @brief Checks if the move violates basic geometric movement laws for ANY piece type. (UPDATED)
 */
MoveStatus is_move_legal(const BoardState* board, const Move* move) {
    // 1. Basic Sanity Check
    if (!board || !move) {
        fprintf(stderr, "[C Engine] ERROR: Received NULL pointer inputs.\n");
        return MOVE_STATUS_ILLEGAL_STATE;
    }

    const char* piece = get_piece_type(board, move->start_sq);
    if (!piece) {
        fprintf(stderr, "[C Engine] ERROR: No piece found at start square %s.\n", move->start_sq);
        return MOVE_STATUS_ILLEGAL_STATE;
    }

    // Dispatch based on the canonical piece type check.
    if (strcmp(piece, "P") == 0) { // Pawn
        MoveStatus status = is_pawn_move_geometry_valid(board, move);
        // Re-mapping generic function success to specific MoveStatus enum required by contract
        return status;
    } else if (strcmp(piece, "N") == 0) { // Knight
        MoveStatus status = is_knight_move_geometry_valid(board, move);
        return status;
    } else if (strcmp(piece, "R") == 0) { // Rook *** NEW CHECK ***
        return is_rook_move_geometry_valid(board, move);
    }
    // ... Add B, Q, K handlers here when implemented ...

    fprintf(stderr, "[C Engine] WARNING: Piece type '%s' logic not yet fully integrated.\n", piece);
    return MOVE_STATUS_ILLEGAL_STATE;
}

/**
 * @brief Applies a legal move and calculates the resulting state of the board. (Simplified stub)
 */
bool apply_move(const BoardState* current, const Move* move, BoardState* next_state) {
    // Core logic moved here:
    // 1. Deep copy 'current' to 'next_state'.
    // 2. Apply geometry change using the piece type derived from 'move->start_sq'.

    // [Placeholder for actual complex state manipulation]

    printf("[C Engine] SUCCESS: State transition successful via apply_move.\n");
    return true;
}


// =============================================================
//                        Implementation Stubs (Need to be fully implemented)
// =============================================================

MoveStatus is_pawn_move_geometry_valid(const BoardState* board, const Move* move);
MoveStatus is_knight_move_geometry_valid(const BoardState* board, const Move* move);
MoveStatus is_rook_move_geometry_valid(const BoardState* board, const Move* move);

// Check Special Rules (Used within the dispatcher after basic moves pass)
MoveStatus check_special_rules(const BoardState* board, const Move* move);

// Game Termination Checks
bool checkmate_detect(const BoardState* board);
bool stalemate_detect(const BoardState* board);


// =============================================================
//                        Helper Function Declarations
// =============================================================
// These are the small utility functions that break down complex rules.

bool is_piece_on_square(const BoardState* board, const char* sq);
const char* get_piece_type(const BoardState* board, const char* sq);


// Helper Functions for Pawn
MoveStatus is_pawn_move_geometry_valid(const BoardState* board, const Move* move);

// Helper Functions for Knight
MoveStatus is_knight_move_geometry_valid(const BoardState* board, const Move* move);

// Helper Functions for Rook
MoveStatus is_rook_move_geometry_valid(const BoardState* board, const Move* move);


// Helper Functions for Special Rules/End Game States:
bool is_castling_move(const BoardState* board, const Move* move);
bool is_en_passant_move(const BoardState* board, const Move* move);

// Helpers specific to state detection:
bool checkmate_detect(const BoardState* board);
bool stalemate_detect(const BoardState* board);


#endif // API_C_LAYER_H