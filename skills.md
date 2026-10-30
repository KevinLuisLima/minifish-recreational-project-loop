# ♟️ Chess Engine Development Status (Project Reference)

**Data:** 2026-10-30
**Projeto:** Código do motor de xadrez (chess_engine).
**Objetivo desta documentação:** Detalhar a arquitetura e o fluxo de execução definidos nesta sessão, servindo como um guia de referência para os próximos estágios de desenvolvimento.

## 🎯 Objetivo Geral da Implementação
Construir um motor de xadrez moderno que separe claramente as responsabilidades: A IA é responsável por *decidir* qual movimento fazer, o Motor Core (C++) é responsável por *validar* a legalidade e calcular o *novo estado*, e a Pythonização orquestra este ciclo.

## 🧱 Arquitetura de Componentes
O projeto se divide em três camadas principais:

1.  **Camada de Orquestração (Python):**
    *   `main.py`: O ponto de entrada principal (`run_engine`). Ele gerencia o loop do jogo, chamando os agentes e orquestrando a passagem do estado através da C-API.
    *   `agent_interface.py`: Define `AgentInterface`, o template method que todos os agentes de IA devem implementar. É onde a lógica de carregamento de pesos (via **HuggingFace API**) será integrada.

2.  **Motor Core Game State (C/C++):**
    *   `BoardState.h`/`.cpp`: Contém as estruturas e funções essenciais para o estado do jogo (`BoardState`, `Position`, `Move`).
        *   Funções de validação modularizadas: `is_pawn_move_valid()`, `is_knight_move_valid()` etc., que desacoplam a lógica das regras específicas.
    *   `api_c_layer.h`: O **Contrato Funcional** obrigatório, definindo as assinaturas de funções (`MoveStatus is_move_legal(...)`) que devem ser expostas para Python através do binding C/C++.

3.  **Camada Teste:**
    *   `test_boardstate.py`: Contém testes unitários para validar a matemática e as regras básicas de movimento em isolamento, garantindo a integridade da lógica antes da integração completa com o fluxo principal.

## 🔄 Fluxo de Execução (The Run Mode)

O motor opera em um ciclo transacional rigoroso:

1.  **Initialize:** O `main.py` inicializa os agentes e o `current_state`.
2.  **Agent Decision (`agent.get_move`):** O agente usa seu modelo preditivo para sugerir uma jogada (`Move`).
3.  **Validation (C-API Call):** A função `run_c_is_move_legal(state, move)` recebe a jogada e verifica *todas* as regras do xadrez contra o estado atual (`BoardState`), retornando um `MoveStatus` (Sucesso ou Erro de Regra).
4.  **Transition (C-API Call):** Se válido, `run_c_apply_move(state, move, next_state)` é chamada. Esta função copia e calcula o *novo estado* do tabuleiro (`next_state`) sem modificar o estado anterior até que ela retorne sucesso.
5.  **Update:** O `current_state` recebe o `next_state`, e o turno é alternado, reiniciando o loop para o próximo agente/turno.

## 🚀 Próximos Passos Recomendados (Ação)

O motor está **arquiteturalmente robusto**. A próxima fase deve focar em preencher a lógica de regras:

1.  **Prioridade Alta:** Concluir a implementação de *todos* os métodos de validação e cálculo de movimentos (`is_..._valid`) dentro de `BoardState.cpp`, transformando os stubs atuais em código funcional do xadrez.
2.  **Alternativa/Teste:** Se a lógica C++ estiver estável, podemos avançar para o módulo Python, concentrando-nos na integração real da **HuggingFace API** no `agent_interface.py` e ajustando os *mocks* de estado em `main.py`.

A documentação será atualizada conforme cada componente principal (ex: 'En Passant Implementation') for concluído com testes unitários aprovados.