from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
import uvicorn
import time

# IMPORTAÇÃO CORRETA:
# Importa a lógica do novo jogo. O arquivo 'aviator_logic.py' DEVE conter a classe JogoAviator.
from aviator_logic import JogoAviator 

app = FastAPI(
    title="Aviator API (Crash Game) 1.0.0", 
    description="Backend de Jogo Aviator (Crash Game) para Frontend"
)

# --- Configuração CORS ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulação de armazenamento de um jogo (Estado global)
rodada_atual: Optional[JogoAviator] = None

def get_rodada_atual() -> JogoAviator:
    """Garante que sempre haja uma instância de jogo atual."""
    global rodada_atual
    
    # Se a rodada atual terminou (após Crash ou Saque), e o tempo de pausa (TEMPO_APOSTA)
    # na lógica do jogo já passou, a lógica já terá resetado o status para "Aguardando Apostas".
    
    if rodada_atual is None:
        rodada_atual = JogoAviator()
        
    return rodada_atual


# --- Endpoints da API ---

@app.get("/status", response_model=Dict[str, Any])
def get_status_rodada():
    """Retorna o estado da rodada atual (multiplicador, status, etc.)."""
    rodada = get_rodada_atual()
    return rodada.get_estado_jogo()

@app.post("/aposta", response_model=Dict[str, Any])
def fazer_aposta_endpoint(aposta: Dict[str, float]):
    """Define a aposta para a próxima rodada."""
    valor = aposta.get("valor")
    if valor is None or valor <= 0:
        raise HTTPException(status_code=400, detail="Valor de aposta inválido.")
    
    rodada = get_rodada_atual()
    if rodada.status not in ["Aguardando Apostas", "Aguardando Início da Rodada"]:
        raise HTTPException(status_code=409, detail=f"Não é permitido apostar agora. Status atual: {rodada.status}")

    return rodada.fazer_aposta(valor)

@app.post("/iniciar_voo", response_model=Dict[str, Any])
def iniciar_rodada_endpoint():
    """Endpoint para iniciar o voo após o tempo de aposta (simulado)."""
    rodada = get_rodada_atual()
    
    if rodada.status != "Aguardando Início da Rodada":
        raise HTTPException(status_code=409, detail=f"O voo só pode ser iniciado após a aposta ser feita. Status: {rodada.status}")
        
    return rodada.iniciar_rodada()


@app.post("/sacar", response_model=Dict[str, Any])
def sacar_endpoint():
    """Ação do jogador: 'Cash Out' (sacar a aposta)."""
    rodada = get_rodada_atual()
    
    if rodada.status != "Em Voo":
        # Se o crash ocorreu logo após o último status/polling,
        # o status pode não ser "Em Voo" mais. Atualiza o estado para verificar.
        rodada.get_estado_jogo() 
        if rodada.aposta_saque is not None:
             raise HTTPException(status_code=409, detail=f"Saque já realizado ou aposta perdida. Status: {rodada.status}")
        
    if rodada.status != "Em Voo":
        raise HTTPException(status_code=409, detail=f"Não é possível sacar agora. Status atual: {rodada.status}")
        
    return rodada.sacar()

# --- Execução do Servidor ---
if __name__ == "__main__":
    # Garante que 'aviator_logic.py' está no mesmo diretório
    uvicorn.run(app, host="127.0.0.1", port=8000)