Projeto de API de Jogos de Cassino: Blackjack & Aviator
Integrantes do Grupo:

Augusto Oliveira / RM: 562080

Felipe Cabral / RM: 561720

Gabriel Tonelli / RM: 564705

Sofia Bueris / RM: 565818

Vinicius Adrian / RM: 564962

Introdução
Este projeto consiste no desenvolvimento do backend para dois populares jogos de cassino, Blackjack e Aviator, utilizando Python e o framework FastAPI. A arquitetura foi projetada para ser modular e eficiente, separando a lógica de cada jogo de sua respectiva interface de API. O objetivo é fornecer uma base sólida e funcional para ser consumida por um frontend.

Descrição Geral
O repositório contém duas aplicações FastAPI independentes, cada uma servindo um jogo específico:

Blackjack API: Uma implementação do clássico jogo de cartas "21", onde o jogador compete contra o dealer (a mesa).

Aviator (Crash Game) API: Uma implementação do popular jogo de "crash", onde os jogadores apostam em um multiplicador crescente e devem retirar seus ganhos antes que ele pare subitamente.

Como Executar o Projeto
Pré-requisitos: Para executar qualquer um dos jogos, você precisará ter o Python 3.7+ instalado em sua máquina. Em seguida, instale as dependências necessárias executando o seguinte comando no seu terminal: pip install fastapi "uvicorn[standard]"

Executando o Servidor de Blackjack: Navegue até o diretório onde os arquivos main.py e blackjack_logic.py estão localizados e execute o comando: uvicorn main:app --reload O servidor da API de Blackjack estará disponível em http://127.0.0.1:8000.

Executando o Servidor de Aviator: Navegue até o diretório onde os arquivos main_aviator.py e aviator_logic.py estão localizados e execute o comando: uvicorn main_aviator:app --reload O servidor da API de Aviator também estará disponível em http://127.0.0.1:8000.

Nota Importante: Como ambos os servidores estão configurados para rodar na mesma porta (8000), eles não podem ser executados simultaneamente. Certifique-se de parar um servidor antes de iniciar o outro.

Jogo 1: Detalhes do Blackjack
A API do Blackjack simula uma partida com 6 baralhos. A lógica do jogo está concentrada no arquivo blackjack_logic.py, na classe JogoBlackjack. Esta classe gerencia a criação e o embaralhamento das cartas, a distribuição das mãos, o cálculo dos valores (tratando o Ás como 1 ou 11) e o gerenciamento dos status da partida (Aguardando Jogada, Jogador Vence, Dealer Vence, etc.). O dealer segue a regra padrão de parar ao atingir 17 pontos ou mais.

A API, definida em main.py, oferece endpoints claros para a interação. Com um POST para /iniciar, uma nova partida é criada. A ação de pedir uma carta (Hit) é feita com um POST para /pedir_carta. Quando o jogador decide parar (Stand), ele envia um POST para /parar, o que aciona o turno do dealer para determinar o vencedor. A qualquer momento, o estado completo do jogo pode ser consultado com um GET para /status.

Jogo 2: Detalhes do Aviator
O Aviator é uma simulação de "crash game", onde um multiplicador de aposta aumenta progressivamente e pode parar a qualquer momento. A lógica, contida em aviator_logic.py, é gerenciada pela classe JogoAviator. Ela é responsável por gerar um ponto de "crash" aleatório para cada rodada, controlar os status do jogo ("Aguardando Apostas", "Em Voo") e simular o aumento do multiplicador com base no tempo.

A API correspondente, em main_aviator.py, permite que o jogador registre sua aposta para a próxima rodada via POST em /aposta. Após as apostas, um POST para /iniciar_voo dá início à subida do multiplicador. Para garantir os ganhos, o jogador deve enviar um POST para /sacar (Cash Out) antes do "crash". O ganho é calculado com base no multiplicador no exato momento da retirada. O estado atual da rodada, incluindo o multiplicador, pode ser verificado com um GET em /status.
