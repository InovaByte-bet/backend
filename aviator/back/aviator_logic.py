import random
import time
from typing import Dict, Any, Union, Optional

class JogoAviator:
    # --- Constantes do Jogo ---
    # Multiplicador mínimo para o "crash" ser considerado uma rodada válida (ex: 1.01x)
    CRASH_MINIMO = 1.01 
    # Tempo de duração simulado do intervalo de aposta (em segundos)
    TEMPO_APOSTA = 5 
    # Fator de incremento do multiplicador (para simular a curva de subida)
    FATOR_INCREMENTO = 0.05 

    def __init__(self):
        self.status: str = "Aguardando Apostas" # Status inicial: Aguardando Apostas | Em Voo | Fim de Rodada
        self.multiplicador_atual: float = 1.00
        self.aposta_valor: Optional[float] = None
        self.aposta_saque: Optional[float] = None # Multiplicador em que o jogador fez Cash Out
        self.multiplicador_crash: Optional[float] = None # Multiplicador final da rodada (crash)
        self.timestamp_inicio: Optional[float] = None # Para simular a passagem do tempo
        
        # O "crash point" aleatório da rodada, simulando o algoritmo Provably Fair
        self._proximo_crash_point: float = self._gerar_crash_point()

    def _gerar_crash_point(self) -> float:
        """
        Gera o ponto de 'crash' aleatório.
        Simulação simplificada: Um número aleatório com viés para multiplicadores baixos.
        """
        # Garante que seja pelo menos o CRASH_MINIMO (1.01x)
        # Usa a função exponencial inversa para viés (mais chance de ser baixo)
        r = random.random()
        crash_point = max(self.CRASH_MINIMO, round(1 / (1 - r) * 0.01, 2))
        return crash_point

    def iniciar_rodada(self) -> Dict[str, Any]:
        """Inicia o voo do avião após o tempo de aposta."""
        if self.status not in ["Aguardando Apostas", "Aguardando Início da Rodada"]:
            # Se já estiver em voo, apenas retorna o estado atual
            return self.get_estado_jogo()

        if self.aposta_valor is None:
            self.status = "Erro: Aposta não definida"
            return self.get_estado_jogo()

        self.status = "Em Voo"
        self.multiplicador_atual = 1.00
        self.aposta_saque = None
        self.multiplicador_crash = None
        self.timestamp_inicio = time.time()
        
        return self.get_estado_jogo()

    def fazer_aposta(self, valor: float) -> Dict[str, Any]:
        """Define o valor da aposta para a próxima rodada."""
        if self.status != "Aguardando Apostas":
            # Permite re-apostar enquanto aguarda o início, mas apenas se a aposta_valor for None
            if self.aposta_valor is not None:
                self.status = "Erro: Aposta já realizada ou fora do tempo."
                return self.get_estado_jogo()

        if valor <= 0:
            self.status = "Erro: Valor de aposta inválido"
        else:
            self.aposta_valor = valor
            self.status = "Aguardando Início da Rodada"
        
        return self.get_estado_jogo()

    def sacar(self) -> Dict[str, Any]:
        """Ação 'Cash Out' do jogador."""
        if self.status != "Em Voo":
            self.status = "Erro: Saque não permitido no momento"
            return self.get_estado_jogo()
        
        # Ponto de saque é o multiplicador atual
        self.aposta_saque = self.multiplicador_atual
        
        # Calcula o ganho
        ganho = self.aposta_valor * self.aposta_saque if self.aposta_valor is not None else 0.0
        
        self.status = f"Saque Realizado! Ganho: R${ganho:.2f}"
        self.multiplicador_crash = self._proximo_crash_point # Revela o ponto de crash
        
        # Prepara a próxima rodada
        self._resetar_para_nova_rodada()
        
        return self.get_estado_jogo()

    def _atualizar_multiplicador(self) -> float:
        """
        Atualiza o multiplicador e verifica se houve crash.
        Isto simula a progressão contínua do jogo.
        """
        if self.status == "Em Voo":
            # Simula a passagem do tempo e o aumento do multiplicador
            tempo_decorrido = time.time() - (self.timestamp_inicio or time.time())
            
            # Multiplicador aumenta com o tempo (curva exponencial simulada)
            novo_multiplicador = 1.00 + (tempo_decorrido ** 2) * self.FATOR_INCREMENTO
            self.multiplicador_atual = round(novo_multiplicador, 2)
            
            # Checa o Crash
            if self.multiplicador_atual >= self._proximo_crash_point:
                self.multiplicador_crash = self._proximo_crash_point
                self.multiplicador_atual = self.multiplicador_crash # Trava no ponto de crash
                
                if self.aposta_saque is None:
                    # Jogador perdeu a aposta
                    self.status = f"CRASH em {self.multiplicador_crash:.2f}x. Aposta Perdida."
                else:
                    # Se já sacou, apenas informa o crash point
                    self.status = f"Saque já realizado. CRASH em {self.multiplicador_crash:.2f}x."

                # O jogo terminou
                self._resetar_para_nova_rodada()

        return self.multiplicador_atual

    def _resetar_para_nova_rodada(self):
        """Prepara o estado do jogo para a próxima rodada."""
        # Define o status para aguardar a próxima rodada
        self._proximo_crash_point = self._gerar_crash_point()
        
        # Simula o tempo de pausa (5 segundos de aposta)
        time.sleep(self.TEMPO_APOSTA)
        self.aposta_valor = None # Limpa a aposta anterior
        self.status = "Aguardando Apostas"


    def get_estado_jogo(self) -> Dict[str, Any]:
        """Retorna o estado atual do jogo para o frontend."""
        
        # Se estiver em voo, atualiza o multiplicador antes de retornar
        if self.status == "Em Voo":
            self._atualizar_multiplicador() 
        
        # Recalcula o ganho para exibição
        ganho = 0.0
        if self.aposta_saque is not None and self.aposta_valor is not None:
             ganho = self.aposta_valor * self.aposta_saque
        
        return {
            "status": self.status,
            "multiplicador_atual": self.multiplicador_atual,
            "aposta_valor": self.aposta_valor,
            "aposta_saque_multiplicador": self.aposta_saque,
            "ganho_rodada": round(ganho, 2),
            "multiplicador_crash_final": self.multiplicador_crash,
            "proxima_acao_necessaria": "Fazer Aposta" if self.status == "Aguardando Apostas" else "Sacar" if self.status == "Em Voo" else "Aguardar",
        }