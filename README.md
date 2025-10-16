Projeto de API de Jogos de Cassino
Este projeto consiste no desenvolvimento do backend para dois populares jogos de cassino, Blackjack e Aviator, utilizando Python e FastAPI. A arquitetura foi projetada para ser modular, separando a lógica de cada jogo de sua respectiva interface de API.

Integrantes do Grupo:

Augusto Oliveira / RM:562080

Felipe Cabral / rm: 561720

Gabriel Tonelli / rm:564705

Sofia Bueris / rm: 565818

Vinicius Adrian / rm: 564962

📜 Descrição Geral
O repositório contém duas aplicações FastAPI independentes:

Blackjack API: Uma implementação do clássico jogo de cartas "21", onde o jogador compete contra o dealer.

Aviator (Crash Game) API: Uma implementação do popular jogo de "crash", onde os jogadores apostam em um multiplicador crescente e devem sacar seus ganhos antes que ele "crashe".

Ambas as APIs foram construídas para fornecer uma interface clara e funcional para um frontend, gerenciando o estado do jogo e as ações do usuário.

🚀 Como Executar o Projeto
Para executar qualquer um dos jogos, você precisará ter Python 3.7+ instalado.

1. Pré-requisitos
Instale as dependências necessárias. Ambas as aplicações utilizam as mesmas bibliotecas.

Bash

pip install fastapi "uvicorn[standard]"
2. Executando o Servidor de Blackjack
Navegue até o diretório onde os arquivos main.py e blackjack_logic.py estão localizados e execute o seguinte comando no terminal:

Bash

uvicorn main:app --reload
O servidor da API de Blackjack estará disponível em http://127.0.0.1:8000.

3. Executando o Servidor de Aviator
Navegue até o diretório onde os arquivos main_aviator.py e aviator_logic.py estão localizados e execute o seguinte comando:

Bash

uvicorn main_aviator:app --reload
O servidor da API de Aviator também estará disponível em http://127.0.0.1:8000.

Nota: Como ambos os servidores estão configurados para rodar na mesma porta (8000), eles não podem ser executados simultaneamente. Certifique-se de parar um antes de iniciar o outro.

🃏 Jogo 1: Blackjack
A API de Blackjack simula um jogo com 6 baralhos. O jogador pode iniciar uma partida, pedir cartas (Hit) ou parar (Stand). O dealer segue a regra padrão de parar em 17 ou mais.

Lógica do Jogo (blackjack_logic.py)
Baralho: Gerencia a criação e o embaralhamento de múltiplos baralhos.

JogoBlackjack: Classe principal que encapsula toda a lógica do jogo:

Distribuição de cartas.

Cálculo dos valores das mãos, com tratamento especial para o Ás (pode valer 1 ou 11).

Gerenciamento de status do jogo (Aguardando Jogada, Jogador Vence, Dealer Vence, Estourou, etc.).

Implementação das ações pedir_carta (Hit) e parar (Stand).

Lógica para o turno do dealer.

A API de Blackjack, definida no arquivo main.py, oferece endpoints claros para interagir com o jogo. Utilizando o método POST no endpoint /iniciar, um jogador pode começar 

uma nova partida, o que distribui as cartas e retorna o estado inicial. A ação de pedir uma nova carta (Hit) é realizada através de uma requisição POST para /pedir_carta, 

que atualiza o estado do jogo. Quando o jogador decide encerrar sua jogada (Stand), ele envia uma requisição POST para /parar, o que aciona a lógica do dealer para 

determinar o vencedor. A qualquer momento, o estado completo da partida, incluindo mãos, valores e status, pode ser consultado com uma chamada GET ao endpoint /status.

O segundo jogo é o Aviator, uma simulação de "crash game" onde um multiplicador aumenta progressivamente e o jogador precisa sacar seus ganhos antes que ele pare 

aleatoriamente. A lógica, contida em aviator_logic.py, é gerenciada pela classe JogoAviator, que gera um ponto de "crash" aleatório para cada rodada, controla os status do 

jogo como "Aguardando Apostas" e "Em Voo", e simula o aumento do multiplicador com base no tempo. A API correspondente, em main_aviator.py, permite que o jogador registre 

uma aposta para a próxima rodada através de uma requisição POST para /aposta, enviando o valor no corpo da requisição. Após a aposta, o voo é iniciado com um POST para 

/iniciar_voo. Para realizar o "Cash Out", o jogador envia uma requisição POST para /sacar, e o ganho é calculado com base no multiplicador atual. O estado da rodada, 

incluindo o multiplicador e o status, pode ser verificado a qualquer momento através de uma chamada GET para /status.
