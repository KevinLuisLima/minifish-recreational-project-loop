import unittest
from typing import List, Tuple

# ======================================================================
# MOCK STRUCTURES & HELPERS (Simula a integração com C++ structs)
# Estes mocks replicam as estruturas definidas em api_c_layer.h e BoardState.h
# para permitir que o teste unitário Python seja autônomo, sem compilação C++.
# ======================================================================

class Position:
    def __init__(self, row: int, col: int):
        self.row = row  # 0-7
        self.col = col  # 0-7

class PieceType:
    EMPTY_SQUARE = -1
    WHITE_PAWN = 1
    WHITE_KNIGHT = 2
    WHITE_BISHOP = 3
    WHITE_ROOK = 4
    WHITE_QUEEN = 5
    WHITE_KING = 6
    BLACK_PAWN = -1
    BLACK_KNIGHT = -2
    BLACK_BISHOP = -3
    BLACK_ROOK = -4
    BLACK_QUEEN = -5
    BLACK_KING = -6

class MockBoardState:
    """Representa o estado do tabuleiro, contendo a lógica mínima necessária para testes."""
    def __init__(self):
        # Um array 8x8. Em um teste real, isso seria preenchido com 'initial position'.
        self.board = [[PieceType.EMPTY_SQUARE] * 8 for _ in range(8)]

class Move:
    """Representa um movimento no formato de string/estruturado."""
    def __init__(self, start_sq: str, end_sq: str):
        self.start_sq = start_sq
        self.end_sq = end_sq

# Mocks das funções de utilidade que existiriam em BoardState.cpp ou seriam exportadas da C-API
def get_piece(state: MockBoardState, pos: Position) -> int:
    """Retorna a peça na posição (row, col). Simula acesso direto ao array do estado."""
    if 0 <= pos.row < 8 and 0 <= pos.col < 8:
        return state.board[pos.row][pos.col]
    return PieceType.EMPTY_SQUARE

def get_owner(piece: int) -> int:
    """Retorna a cor (1=White, 2=Black)."""
    if piece >= PieceType.WHITE_PAWN and piece <= PieceType.WHITE_ROOK: return 1
    if piece >= PieceType.BLACK_PAWN and piece <= PieceType.BLACK_KING: return 2
    return 0

def get_enemy(piece: int) -> int:
    """Retorna o inimigo da peça."""
    if piece > 0: return -1 # White vs Black (Placeholder)
    if piece < 0: return 1  # Black vs White (Placeholder)
    return 0

# ======================================================================
# FUNÇÕES DE TESTE PARA BOARDSTATE
# Estes são os *stubs* das funções a serem testadas em BoardState.cpp
# ======================================================================

def is_pawn_move_valid(state: MockBoardState, start: Position, end: Position, piece: int) -> bool:
    """Stub para o teste de validação de peões."""
    if piece != PieceType.WHITE_PAWN: return False # Apenas testamos brancas por enquanto

    # Regra básica: movimento vertical ou diagonal (peão só avança na coluna).
    # 1. Deve avançar em reta (colunas iguais)
    if start.col != end.col: return False
    # 2. Apenas avance se for mais de um quadrado OU seja o primeiro movimento (simplificado para > 0)
    delta_row = abs(start.row - end.row)
    if delta_row == 0 or delta_row > 2: return False

    # Exemplo simples de validação de primeira jogada (avançar 2 casas e o meio livre)
    if start.row == 6 and end.row == 4 and state.board[start.row - 1][start.col] == PieceType.EMPTY_SQUARE:
        return True # Movimento de duas casas simples

    # Captura diagonal (simplificado): Linha e Coluna mudam de forma perpendicular ao avanço principal
    if start.row != end.row and abs(start.col - end.col) == 1:
         # Aqui seria a checagem se o alvo contém peça inimiga!
         return True

    return False # Falha por padrão


def is_knight_move_valid(state: MockBoardState, start: Position, end: Position, piece: int) -> bool:
    """Stub para o teste de validação de Cavalo."""
    if piece != PieceType.WHITE_KNIGHT: return False

    row_diff = abs(start.row - end.row)
    col_diff = abs(start.col - end.col)

    # Deve ser (2, 1) ou (1, 2) e o destino não deve ter amigo.
    if ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
        return True
    return False


def is_valid_move(state: MockBoardState, start: Position, end: Position) -> bool:
    """Dispatcher principal de validação."""
    piece = get_piece(state, start)
    if piece == PieceType.EMPTY_SQUARE: return False

    # 1. Verificação de posse/inimigo (sempre a primeira verificação).
    target_piece = get_piece(state, end)
    if target_piece != PieceType.EMPTY_SQUARE and get_enemy(piece) == get_owner(target_piece):
        return False

    # 2. Dispatcher de regras: Chama o validador específico.
    if piece == PieceType.WHITE_PAWN:
        return is_pawn_move_valid(state, start, end, piece)
    elif piece == PieceType.WHITE_KNIGHT:
        return is_knight_move_valid(state, start, end, piece)
    # Adicionar outros casos (Bishop, Rook, etc.)

    return False # Fallback seguro


# ======================================================================
# CLASSES DE TESTE UNITÁRIO
# ======================================================================

class TestChessEngineCore(unittest.TestCase):
    def setUp(self):
        """Configura o estado do tabuleiro ANTES de cada teste."""
        self.state = MockBoardState()

        # Configurar um estado inicial conhecido para testes: Exemplo (Pawn em E2, Knight em G1)
        self.state.board[6][4] = PieceType.WHITE_PAWN  # E2 (row 6 is the second row from white side)
        self.state.board[7][6] = PieceType.WHITE_KNIGHT # G1

    def test_01_valid_knight_move(self):
        """Testa um movimento de cavalo válido: N em g1 (7, 6) para e2 (6, 4)."""
        start = Position(row=7, col=6) # G1
        end = Position(row=6, col=4)   # E2
        piece = PieceType.WHITE_KNIGHT

        self.assertTrue(is_knight_move_valid(self.state, start, end, piece), "O movimento de cavalo deveria ser válido.")

    def test_02_invalid_knight_move(self):
        """Testa um movimento de cavalo inválido: Tentativa diagonal simples."""
        start = Position(row=7, col=6) # G1
        end = Position(row=5, col=4)   # E3 (distância 2, 2 - Inválido para Cavalo)
        piece = PieceType.WHITE_KNIGHT

        self.assertFalse(is_knight_move_valid(self.state, start, end, piece), "O movimento deveria ser inválido.")

    def test_03_basic_pawn_advancement(self):
        """Testa o avanço básico de um peão para duas casas (primeiro movimento)."""
        start = Position(row=6, col=4) # E2
        end = Position(row=4, col=4)   # E4
        piece = PieceType.WHITE_PAWN

        self.assertTrue(is_pawn_move_valid(self.state, start, end, piece), "O avanço de peão em 2 casas deveria ser válido.")

    def test_04_basic_pawn_capture(self):
        """Testa um movimento de captura diagonal (requer que o alvo esteja ocupado)."""
        # Simular alvo inimigo na posição de destino para forçar a checagem de captura.
        # Para este teste, simplesmente verificamos a geometria.
        start = Position(row=6, col=3) # D2
        end = Position(row=5, col=4)   # E3 (Captura diagonal)
        piece = PieceType.WHITE_PAWN

        self.assertTrue(is_pawn_move_valid(self.state, start, end, piece), "A captura de peão diagonal deveria ser válida.")


    def test_05_end_to_end_validation(self):
        """Testa o dispatcher principal is_valid_move com diferentes peças."""
        # 1. Teste Cavalo: Válido
        start = Position(row=7, col=6) # G1
        end = Position(row=5, col=5)   # E3
        self.assertTrue(is_valid_move(self.state, start, end), "A validação de cavalo no fluxo principal falhou.")

        # 2. Teste Peão: Válido (avanço duas casas simulado)
        start = Position(row=6, col=4) # E2
        end = Position(row=4, col=4)   # E4
        self.assertTrue(is_valid_move(self.state, start, end), "A validação de peão no fluxo principal falhou.")

        # 3. Teste Falha: Peça vazia na origem
        start = Position(row=0, col=0) # Posição não inicializada / vaga
        end = Position(row=1, col=2)
        self.assertFalse(is_valid_move(self.state, start, end), "Deve falhar se a origem estiver vazia.")


if __name__ == '__main__':
    unittest.main()