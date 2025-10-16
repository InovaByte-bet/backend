from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Union
from blackjack_logic import JogoBlackjack # Importa a lógica

app = FastAPI(
    title="Blackjack API 0.1.0", # Adicionado versão e título conforme OAS
    description="Backend de Jogo de Blackjack para Frontend"
)

# --- Configuração CORS ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "*" # Mantido para desenvolvimento, com ressalva
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulação de armazenamento de um jogo (Estado global)
jogo_atual: Union[JogoBlackjack, None] = None

def get_jogo() -> JogoBlackjack:
    """Função para gerenciar o estado do jogo atual, garantindo que exista uma instância."""
    global jogo_atual
    if jogo_atual is None:
        jogo_atual = JogoBlackjack()
        # Inicia o jogo automaticamente se for a primeira vez que é chamado
        # (O endpoint /iniciar é a forma correta de começar, mas isso garante um estado mínimo)
    return jogo_atual


# --- Endpoints da API ---
# A tipagem de retorno Dict[str, Any] está correta e mantida.

@app.get("/status", response_model=Dict[str, Any])
def get_status():
    """Retorna o estado do jogo atual."""
    jogo = get_jogo()
    return jogo.get_estado_jogo()

@app.post("/iniciar", response_model=Dict[str, Any])
def iniciar_jogo_endpoint():
    """Inicia um novo jogo e distribui as cartas iniciais."""
    global jogo_atual
    # Cria uma nova instância do jogo para reiniciar
    jogo_atual = JogoBlackjack() 
    # O método iniciar_jogo já retorna o estado completo
    return jogo_atual.iniciar_jogo()

@app.post("/pedir_carta", response_model=Dict[str, Any])
def pedir_carta_endpoint():
    """Ação do jogador: 'Hit' (pedir mais uma carta)."""
    jogo = get_jogo()
    return jogo.pedir_carta()

@app.post("/parar", response_model=Dict[str, Any])
def parar_endpoint():
    """Ação do jogador: 'Stand' (parar de pedir cartas). Inicia o turno do Dealer."""
    jogo = get_jogo()
    return jogo.parar()

# --- Execução do Servidor ---
if __name__ == "__main__":
    import uvicorn
    # O servidor rodará em http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)