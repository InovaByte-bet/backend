import random
from typing import List, Tuple, Dict, Any, Union

# Definições de Tipo
Carta = Tuple[str, str] # Ex: ('A', 'Ouros')
Mao = List[Carta]

# Valores das cartas
VALORES: Dict[str, int] = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
NAIPES: List[str] = ['Copas', 'Ouros', 'Espadas', 'Paus']
CARTAS: List[str] = list(VALORES.keys())

class Baralho:
    def __init__(self, num_decks: int = 6):
        """Inicializa e embaralha o baralho (múltiplos decks)."""
        deck_base = [(c, n) for c in CARTAS for n in NAIPES]
        self.cartas: List[Carta] = deck_base * num_decks
        random.shuffle(self.cartas)

    def tirar_carta(self) -> Carta:
        """Remove e retorna a próxima carta do baralho."""
        if not self.cartas:
            # Em um jogo de cassino, um novo sapato seria introduzido
            raise Exception("Baralho vazio, é necessário reiniciar o jogo.")
        return self.cartas.pop()

class JogoBlackjack:
    def __init__(self):
        self.baralho = Baralho()
        self.mao_jogador: Mao = []
        self.mao_dealer: Mao = []
        self.status: str = "Novo Jogo" # Inicializa com um status claro

    # --- Métodos Auxiliares ---
    
    def _calcular_valor(self, mao: Mao) -> int:
        """Calcula o valor da mão, tratando os Ases (11 ou 1)."""
        valor = sum(VALORES[c[0]] for c in mao)
        num_ases = sum(1 for c in mao if c[0] == 'A')

        # Converte Ás de 11 para 1 se estourar 21
        while valor > 21 and num_ases > 0:
            valor -= 10
            num_ases -= 1
        return valor
    
    def _fim_de_jogo(self) -> bool:
        """Verifica se o status atual indica o fim do jogo."""
        return self.status not in ["Aguardando Jogada", "Novo Jogo"]

    # --- Lógica do Jogo ---

    def iniciar_jogo(self) -> Dict[str, Any]:
        """Distribui as cartas iniciais e verifica Blackjacks."""
        self.mao_jogador = [self.baralho.tirar_carta(), self.baralho.tirar_carta()]
        self.mao_dealer = [self.baralho.tirar_carta(), self.baralho.tirar_carta()]

        valor_jogador = self._calcular_valor(self.mao_jogador)
        valor_dealer = self._calcular_valor(self.mao_dealer)
        
        if valor_jogador == 21:
            if valor_dealer == 21:
                self.status = "Empate (Push) com Blackjack"
            else:
                self.status = "Blackjack! Jogador Vence"
        elif valor_dealer == 21:
            self.status = "Dealer Vence com Blackjack"
        else:
            self.status = "Aguardando Jogada"

        # Se o jogo terminou com Blackjack, revela_dealer é True
        return self.get_estado_jogo(revelar_dealer=self._fim_de_jogo())

    def pedir_carta(self) -> Dict[str, Any]:
        """Ação 'Hit' do jogador."""
        if self.status != "Aguardando Jogada":
            return self.get_estado_jogo()

        self.mao_jogador.append(self.baralho.tirar_carta())
        valor_jogador = self._calcular_valor(self.mao_jogador)

        if valor_jogador > 21:
            self.status = "Estourou (Bust)! Dealer Vence"
            revelar_dealer = True
        elif valor_jogador == 21:
            # Automaticamente Stand, vai para o Dealer
            self.status = "21. Vez do Dealer."
            return self._turno_dealer()
        else:
            revelar_dealer = False
        
        return self.get_estado_jogo(revelar_dealer=revelar_dealer)

    def parar(self) -> Dict[str, Any]:
        """Ação 'Stand' do jogador. Inicia o turno do Dealer."""
        if self.status != "Aguardando Jogada":
            return self.get_estado_jogo()

        self.status = "Jogador Parou. Vez do Dealer."
        return self._turno_dealer()

    def _turno_dealer(self) -> Dict[str, Any]:
        """Lógica de jogo do Dealer (chamada após o 'Stand' ou 21 do jogador)."""
        
        # Pega o valor do jogador ANTES de jogar
        valor_jogador = self._calcular_valor(self.mao_jogador)

        # Se o jogador já estourou, o Dealer não precisa jogar.
        if valor_jogador > 21:
             # O status já deve ter sido definido em pedir_carta
            return self.get_estado_jogo(revelar_dealer=True)

        # Dealer pede carta até 17 ou mais
        while self._calcular_valor(self.mao_dealer) < 17:
            self.mao_dealer.append(self.baralho.tirar_carta())

        # Determina o vencedor
        valor_dealer = self._calcular_valor(self.mao_dealer)

        if valor_dealer > 21:
            self.status = "Dealer Estourou (Bust)! Jogador Vence"
        elif valor_jogador > valor_dealer:
            self.status = "Jogador Vence"
        elif valor_dealer > valor_jogador:
            self.status = "Dealer Vence"
        else:
            self.status = "Empate (Push)"
        
        return self.get_estado_jogo(revelar_dealer=True)


    def get_estado_jogo(self, revelar_dealer: bool = False) -> Dict[str, Any]:
        """
        Retorna o estado atual do jogo para o frontend. 
        Gerencia o mascaramento da segunda carta do dealer.
        """
        
        # 1. Determina se deve revelar (fim de jogo ou instrução explícita)
        deve_revelar = revelar_dealer or self._fim_de_jogo()
        
        # 2. Configura a mão e o valor do dealer para exibição
        if deve_revelar or len(self.mao_dealer) < 2:
            dealer_mao_exibida = self.mao_dealer
            valor_dealer_exibido = self._calcular_valor(self.mao_dealer)
        else:
            # Mascara a segunda carta (e as demais se houver)
            # A carta mascarada é representada como um tuple especial
            carta_mascarada: Carta = ("???", "???") 
            dealer_mao_exibida = [self.mao_dealer[0], carta_mascarada]
            
            # O valor exibido é apenas o da primeira carta
            valor_dealer_exibido = self._calcular_valor([self.mao_dealer[0]])

        # 3. Formata as cartas para o formato string exigido pelo frontend
        def formatar_carta(carta: Carta) -> str:
            if carta[0] == "???" and carta[1] == "???":
                return "??? de ???"
            return f"{carta[0]} de {carta[1]}"

        # 4. Retorna o Dicionário de Estado
        return {
            "mao_jogador": [formatar_carta(c) for c in self.mao_jogador],
            "valor_jogador": self._calcular_valor(self.mao_jogador),
            "mao_dealer": [formatar_carta(c) for c in dealer_mao_exibida],
            "valor_dealer": valor_dealer_exibido,
            "status": self.status,
            "fim_jogo": self._fim_de_jogo()
        }