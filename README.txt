================================================================
UDESC CHATBOT — Assistente para Estudantes Estrangeiros
Disciplina: Redes de Computadores — UDESC/CCT — 2026/1
================================================================

DESCRIÇÃO
---------
ChatBot bilíngue (Português/Inglês) para auxiliar estudantes
estrangeiros em intercâmbio na UDESC.

Canais disponíveis:
  - WhatsApp (via Twilio Sandbox)
  - Telegram (via Bot API — polling)

Protocolo de transporte: TCP/IP (HTTPS porta 443)


PRÉ-REQUISITOS
--------------
- Python 3.10 ou superior
- Pip (gerenciador de pacotes Python)
- Conta Twilio (gratuita) para WhatsApp
- Bot Telegram criado via @BotFather
- ngrok (para expor o servidor local ao Twilio)


INSTALAÇÃO
----------

1. Instale as dependências:

   pip install -r requirements.txt


2. Configure o arquivo .env:

   Copie o arquivo de exemplo:
     Windows: copy .env.example .env
     Linux:   cp .env.example .env

   Edite o .env com suas credenciais:
     TWILIO_ACCOUNT_SID  = SID da sua conta Twilio
     TWILIO_AUTH_TOKEN   = Token de autenticação Twilio
     TWILIO_WHATSAPP_NUMBER = Número Twilio Sandbox (ex: whatsapp:+14155238886)
     TELEGRAM_TOKEN      = Token do bot obtido via @BotFather


EXECUTANDO O SERVIDOR
---------------------

   python app.py

O servidor Flask iniciará na porta 5000 (configurável em PORT=).


CONFIGURANDO O WEBHOOK DO WHATSAPP (Twilio)
-------------------------------------------

1. Baixe e execute o ngrok:

   ngrok http 5000

   O ngrok exibirá uma URL pública, ex:
     https://abc123.ngrok-free.app

2. Acesse o painel Twilio:
   https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

3. Na seção "Sandbox Settings", configure o webhook:
   Webhook URL: https://abc123.ngrok-free.app/whatsapp
   Método: POST

4. No WhatsApp, envie a mensagem de ativação do Sandbox:
   Para: +1 415 523 8886
   Mensagem: join <seu-código-sandbox>


CONFIGURANDO O BOT DO TELEGRAM
-------------------------------

1. Abra o Telegram e fale com @BotFather

2. Envie /newbot e siga as instruções para criar o bot

3. Copie o token gerado para o .env (TELEGRAM_TOKEN)

4. O bot usa polling — não precisa de webhook ou ngrok

5. Inicie o app (python app.py) e procure seu bot pelo nome no Telegram

6. Envie /start para iniciar a conversa


ESTRUTURA DO PROJETO
--------------------

udesc-chatbot/
├── app.py                  # Ponto de entrada (Flask + Telegram thread)
├── .env                    # Variáveis de ambiente (NÃO versionar)
├── .env.example            # Exemplo de configuração
├── requirements.txt        # Dependências Python
├── config/
│   └── settings.py         # Carrega e expõe configurações do .env
├── controllers/
│   ├── whatsapp_controller.py   # Processa webhook do Twilio
│   └── telegram_controller.py  # Gerencia polling do Telegram
├── services/
│   ├── bot_service.py      # Lógica conversacional (máquina de estados)
│   ├── session_service.py  # Gerencia sessões em memória
│   └── keyword_service.py  # Busca por palavras-chave
├── models/
│   └── session.py          # Modelo de sessão do usuário
├── routes/
│   └── whatsapp_routes.py  # Rotas Flask (/whatsapp, /health)
├── data/
│   ├── messages_pt.json    # Conteúdo em Português
│   └── messages_en.json    # Conteúdo em Inglês
├── utils/
│   ├── logger.py           # Logger com arquivo + console
│   └── network_info.py     # Captura IP/porta/protocolo (RT03)
└── logs/
    └── chatbot.log         # Arquivo de log (gerado automaticamente)


INFORMAÇÕES DE REDE (RT03)
--------------------------

Protocolo de transporte: TCP
Protocolo de aplicação:  HTTPS (sobre TLS/TCP)

  Origem (cliente WhatsApp):
    IP: endereço IP do usuário (logado em cada requisição)
    Porta de origem: dinâmica (atribuída pelo SO do cliente)

  Destino (servidor Flask):
    IP: IP local da máquina (exibido ao iniciar o app)
    Porta de destino: 5000 (Flask local) / 443 (Twilio → ngrok)

  Canal Telegram:
    O bot faz polling HTTPS para api.telegram.org:443
    Protocolo: TCP/IP

Todas as informações de IP e porta são registradas no arquivo de log.


VERIFICAÇÃO DE FUNCIONAMENTO
-----------------------------

  Health check do servidor:
    curl http://localhost:5000/health

  Simular mensagem WhatsApp (teste local):
    curl -X POST http://localhost:5000/whatsapp \
         -d "From=whatsapp:+5547999999999&Body=oi"


MENUS DISPONÍVEIS
-----------------

  Idioma: Português / English (bilíngue — RF02)

  Menu Principal:
    1. Endereços dos Centros UDESC (7 centros com Maps)
    2. Sistemas Acadêmicos (SIGA, SIGAA, Moodle, SAS, Office 365, Biblioteca, Site)
    3. Como obter o ID UDESC
    4. Informações sobre CPF (com endereços da Receita Federal por cidade)
    5. Tutoria Acadêmica (por centro)
    6. Serviço de Orientação ao Estudante (SOE)
    7. Residência Estudantil (por centro)
    8. FAQ (RU, Transporte, Wi-Fi, Impressão, Bancos, Chip, Moradia)
    9. Contatos de Emergência (190, 192, 193 + hospitais por cidade)

  Navegação:
    "menu"   → volta ao menu principal
    "voltar" → volta ao menu anterior
    "sair"   → encerra a conversa

================================================================
