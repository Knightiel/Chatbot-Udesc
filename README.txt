UDESC CHATBOT - Assistente para novos estudantes
Disciplina: Redes de Computadores - UDESC/CCT - 2026/1

DESCRIÇÃO
---------
ChatBot baseado em regras (menus e árvore de decisão), bilíngue
(Português/Inglês), para guiar e auxiliar novos estudantes na UDESC.

Canais disponíveis:
  - Telegram  (via Bot API)
  - WhatsApp  (via Twilio Sandbox integrado com ngrok)


PRÉ-REQUISITOS
--------------
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Bot Telegram criado via @BotFather
- Conta Twilio gratuita (somente para o canal WhatsApp)
- ngrok (somente para o canal WhatsApp - expõe o servidor local)


PASSO A PASSO
-------------

1. Com o Python instalado, crie uma pasta e inicie um ambiente virtual (venv):

   python -m venv venv

2. Inicie o ambiente com o comando:

   .\venv\Scripts\activate (Windows)
   source venv/bin/activate (Linux)

3. Instale as dependências:

   pip install -r requirements.txt

4. Crie um arquivo .env com os dados do token do Telegrem:

    TELEGRAM_TOKEN = Token do bot obtido via @BotFather

5. Execute o comando no terminal

   python app.py


----------------------------------------------------------------
CONFIGURANDO O TELEGRAM
----------------------------------------------------------------

1. Abra o Telegram e inicie uma conversa com o @BotFather
2. Envie /newbot e siga as instruções (defina nome e @username)
3. Copie o token gerado para o .env (TELEGRAM_TOKEN)


----------------------------------------------------------------
CONFIGURANDO O WHATSAPP (Twilio Sandbox)
----------------------------------------------------------------

1. Crie uma conta gratuita em https://www.twilio.com

2. Com o servidor rodando (python app.py), exponha a porta 5000
   com o ngrok em outro terminal:

   ngrok http 5000

   O ngrok exibirá uma URL pública, ex:
     https://abc123.ngrok-free.app

3. No painel Twilio, acesse:
   Messaging -> Try it out -> Send a WhatsApp message -> Sandbox Settings

   Configure em "When a message comes in":
     URL:    https://abc123.ngrok-free.app/whatsapp
     Método: POST

   (Opcionalmente) Configure "Status callback URL":
     URL:    https://abc123.ngrok-free.app/status
     Método: POST

4. COMO ACESSAR:
   O Twilio Sandbox mostra um código de entrada (ex: "join xxx-yyy").
   - Abra / adicione o número do Sandbox no Whatsapp:
       +1 415 523 8886
   - Envie uma vez a mensagem:  join <código-do-sandbox>
   - A partir daí, o bot já estará iniciado e pronto para uso


----------------------------------------------------------------
COMO USAR O CHATBOT
----------------------------------------------------------------

1. Envie qualquer mensagem ("oi", "hello", /start...)
2. O bot dá as boas-vindas e pede o idioma:
     1 = Português   |   2 = English
3. O menu principal é exibido:

     1  Endereços dos Centros UDESC
        (escolha o centro -> endereço, telefone, site e Google Maps)
     2  Sistemas que você vai utilizar (SIGA, Moodle, SIGAA)
        (escolha o sistema -> requisitos de acesso + ID UDESC)
     3  Como obter o ID UDESC (passo a passo)
     4  Sistemas UDESC - para que serve cada um
        (SIGA: notas/faltas | Moodle: disciplinas/exercícios |
         Site UDESC: PPC/professores | SAS: agendamento de salas |
         Office 365: e-mail institucional | Biblioteca online)
     5  Informações sobre CPF
        (como obter online + validação presencial na Receita
         Federal, com endereço COM BASE NO CENTRO escolhido)
     6  Tutoria Acadêmica (site/telefone do centro escolhido)
     7  Serviço de Orientação ao Estudante - SOE
        (serviços, horário de atendimento, site)
     8  Residência Estudantil (disponibilidade por centro)
     9  FAQ (RU, transporte, Wi-Fi, impressão, bancos, chip, moradia)
    10  Contatos de Emergência (190/192/193 + hospitais)
     0  Encerrar conversa

4. Navegação a qualquer momento:
     "menu"   -> volta ao menu principal
     "voltar" -> volta ao passo anterior
     "sair"   -> encerra a conversa


VERIFICAÇÃO DE FUNCIONAMENTO
-----------------------------

  Checar o status do servidor:
    curl http://localhost:5000/health

  Simular mensagem WhatsApp (teste local sem Twilio):
    curl -X POST http://localhost:5000/whatsapp -d "From=whatsapp:+5547999999999&Body=oi"
