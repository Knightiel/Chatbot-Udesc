================================================================
UDESC CHATBOT — Assistente para Estudantes Estrangeiros
Disciplina: Redes de Computadores — UDESC/CCT — 2026/1
================================================================

DESCRIÇÃO
---------
ChatBot baseado em regras (menus e árvore de decisão), bilíngue
(Português/Inglês), para auxiliar estudantes estrangeiros em
intercâmbio na UDESC.

Canais disponíveis (qualquer pessoa pode usar, de forma anônima
e sem cadastro):
  - Telegram  (via Bot API — polling)
  - WhatsApp  (via Twilio Sandbox — webhook)
  - Navegador (interface web local, para testes)

Protocolo de transporte: TCP (aplicação: HTTP/HTTPS)


================================================================
COMEÇO RÁPIDO (5 PASSOS)
================================================================

  1. pip install -r requirements.txt
  2. copy .env.example .env        (Linux/Mac: cp .env.example .env)
  3. Edite o .env e preencha TELEGRAM_TOKEN (e Twilio, se usar WhatsApp)
  4. python app.py
  5. Abra o Telegram, procure seu bot pelo nome e envie /start

Para o WhatsApp, siga também a seção "CONFIGURANDO O WHATSAPP".


PRÉ-REQUISITOS
--------------
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Bot Telegram criado via @BotFather (grátis, 2 minutos)
- Conta Twilio gratuita (somente para o canal WhatsApp)
- ngrok (somente para o canal WhatsApp — expõe o servidor local)


INSTALAÇÃO
----------

1. Instale as dependências:

   pip install -r requirements.txt

2. Configure o arquivo .env:

   Copie o arquivo de exemplo:
     Windows: copy .env.example .env
     Linux:   cp .env.example .env

   Edite o .env com suas credenciais:
     TELEGRAM_TOKEN         = Token do bot obtido via @BotFather
     TWILIO_ACCOUNT_SID     = SID da sua conta Twilio (WhatsApp)
     TWILIO_AUTH_TOKEN      = Token de autenticação Twilio
     TWILIO_WHATSAPP_NUMBER = Número do Sandbox (ex: whatsapp:+14155238886)

   Observação: o bot funciona só com o Telegram configurado.
   O canal WhatsApp é ativado quando as credenciais Twilio existem.


EXECUTANDO O SERVIDOR
---------------------

   python app.py

Ao iniciar, o log mostra:
  - O IP local do servidor e a porta (padrão 5000)
  - A thread do Telegram (polling) iniciada
  - Os endpoints: /  (web), /whatsapp (webhook), /health


================================================================
CONFIGURANDO O TELEGRAM (qualquer pessoa pode usar)
================================================================

1. Abra o Telegram e fale com @BotFather
2. Envie /newbot e siga as instruções (defina nome e @username)
3. Copie o token gerado para o .env (TELEGRAM_TOKEN)
4. Inicie o app:  python app.py
5. Pronto! QUALQUER pessoa pode usar o bot:
   - Buscar o @username do bot na busca do Telegram, OU
   - Abrir o link t.me/<username_do_bot>
   - Enviar /start (ou qualquer mensagem) para começar

Não é preciso cadastro, aprovação ou lista de contatos: o bot é
público e responde a qualquer usuário do Telegram imediatamente.


================================================================
CONFIGURANDO O WHATSAPP (Twilio Sandbox — qualquer pessoa pode usar)
================================================================

1. Crie uma conta gratuita em https://www.twilio.com e copie o
   Account SID e o Auth Token para o .env

2. Com o servidor rodando (python app.py), exponha a porta 5000
   com o ngrok em outro terminal:

   ngrok http 5000

   O ngrok exibirá uma URL pública, ex:
     https://abc123.ngrok-free.app

3. No painel Twilio, acesse:
   Messaging → Try it out → Send a WhatsApp message → Sandbox Settings

   Configure em "When a message comes in":
     URL:    https://abc123.ngrok-free.app/whatsapp
     Método: POST

4. COMO QUALQUER PESSOA ENTRA NO BOT:
   O Twilio Sandbox mostra um código de entrada (ex: "join xxx-yyy").
   Qualquer pessoa, de qualquer celular, basta:
   - Adicionar/abrir o número do Sandbox no WhatsApp:
       +1 415 523 8886
   - Enviar UMA vez a mensagem:  join <código-do-sandbox>
   - A partir daí, conversar normalmente com o bot ("oi", "menu"...)

   Dica para a apresentação: compartilhe um QR Code do link
   https://wa.me/14155238886?text=join%20<código-do-sandbox>
   para a turma entrar no bot em segundos.


INTERFACE WEB (opcional, para testes locais)
--------------------------------------------
Com o servidor rodando, abra no navegador:

   http://localhost:5000/

O chat funciona sem cadastro — a sessão usa um UUID aleatório
gerado no próprio navegador.


================================================================
COMO USAR O CHATBOT
================================================================

1. Envie qualquer mensagem ("oi", "hello", /start...)
2. O bot dá as boas-vindas e pede o idioma:
     1 = Português   |   2 = English
3. O menu principal é exibido (espelha a Tabela 1 do trabalho):

     1  Endereços dos Centros UDESC
        (escolha o centro → endereço, telefone, site e Google Maps)
     2  Sistemas que você vai utilizar (SIGA, Moodle, SIGAA)
        (escolha o sistema → requisitos de acesso + ID UDESC)
     3  Como obter o ID UDESC (passo a passo)
     4  Sistemas UDESC — para que serve cada um
        (SIGA: notas/faltas | Moodle: disciplinas/exercícios |
         Site UDESC: PPC/professores | SAS: agendamento de salas |
         Office 365: e-mail institucional | Biblioteca online)
     5  Informações sobre CPF
        (como obter online + validação presencial na Receita
         Federal, com endereço COM BASE NO CENTRO escolhido)
     6  Tutoria Acadêmica (site/telefone do centro escolhido)
     7  Serviço de Orientação ao Estudante — SOE
        (serviços, horário de atendimento, site)
     8  Residência Estudantil (disponibilidade por centro)
     9  FAQ (RU, transporte, Wi-Fi, impressão, bancos, chip, moradia)
    10  Contatos de Emergência (190/192/193 + hospitais)
     0  Encerrar conversa

4. Navegação a qualquer momento:
     "menu"   → volta ao menu principal
     "voltar" → volta ao passo anterior
     "sair"   → encerra a conversa

5. O bot também entende palavras-chave: digitar "cpf", "moodle",
   "tutoria", "wifi" etc. leva direto à opção correspondente.


================================================================
USO ANÔNIMO (privacidade)
================================================================

O chatbot foi projetado para ser usado por QUALQUER pessoa de
forma anônima:

- Nenhum cadastro, nome ou dado pessoal é solicitado.
- O número de telefone (WhatsApp) e o chat ID (Telegram) NUNCA
  são armazenados nem gravados em log. Cada identificador passa
  por um hash SHA-256 truncado e irreversível
  (ex: "anon-9ce4b00d041d") — ver utils/anonymizer.py.
- O hash é determinístico: a mesma pessoa mantém sua sessão
  (idioma e posição no menu), mas não é possível descobrir o
  telefone a partir do log.
- As sessões ficam apenas em memória e são descartadas ao
  encerrar a conversa ("sair") ou reiniciar o servidor.


================================================================
INFORMAÇÕES DE REDE (para a apresentação — item 2.9)
================================================================

Protocolo de TRANSPORTE: TCP (não usa UDP)
Protocolo de APLICAÇÃO:  HTTP/HTTPS

Canal WhatsApp (arquitetura cliente-servidor):
  celular → servidores WhatsApp/Twilio → ngrok (HTTPS/TCP 443)
          → Flask local (TCP porta 5000)
  - IP de ORIGEM:  IP do Twilio/ngrok (logado a cada requisição
                   como [REDE] origem=...)
  - Porta ORIGEM:  dinâmica/efêmera (atribuída pelo SO do cliente)
  - IP de DESTINO: IP local da máquina (exibido ao iniciar o app)
  - Porta DESTINO: 5000 (Flask) / 443 (no túnel ngrok)

Canal Telegram (polling):
  o servidor local abre conexões HTTPS de saída para
  api.telegram.org na porta 443 (TCP)
  - ORIGEM:  IP local, porta efêmera
  - DESTINO: api.telegram.org:443

Todas as requisições registram IP/porta/protocolo no arquivo
logs/chatbot.log (utils/network_info.py).

Para conferir portas/conexões durante a apresentação (Windows):
   netstat -ano | findstr 5000     → Flask ouvindo em TCP
   netstat -ano | findstr 443      → conexões Telegram/ngrok


VERIFICAÇÃO DE FUNCIONAMENTO
-----------------------------

  Health check do servidor:
    curl http://localhost:5000/health

  Simular mensagem WhatsApp (teste local sem Twilio):
    curl -X POST http://localhost:5000/whatsapp -d "From=whatsapp:+5547999999999&Body=oi"


ESTRUTURA DO PROJETO
--------------------

udesc-chatbot/
├── app.py                  # Ponto de entrada (Flask + thread Telegram)
├── .env                    # Variáveis de ambiente (NÃO versionar)
├── .env.example            # Exemplo de configuração
├── requirements.txt        # Dependências Python
├── config/
│   └── settings.py         # Carrega e expõe configurações do .env
├── controllers/
│   ├── whatsapp_controller.py  # Webhook do Twilio (anonimiza o telefone)
│   ├── telegram_controller.py  # Polling do Telegram (anonimiza o chat ID)
│   └── web_controller.py       # Chat via navegador
├── services/
│   ├── bot_service.py      # Lógica conversacional (máquina de estados)
│   ├── session_service.py  # Sessões em memória
│   └── keyword_service.py  # Atalhos por palavras-chave
├── models/
│   └── session.py          # Modelo de sessão do usuário
├── routes/
│   ├── whatsapp_routes.py  # Rotas /whatsapp e /health
│   └── web_routes.py       # Rotas / e /chat
├── templates/
│   └── index.html          # Página do chat web
├── data/
│   ├── messages_pt.json    # Conteúdo em Português
│   └── messages_en.json    # Conteúdo em Inglês
├── utils/
│   ├── logger.py           # Logger (console + arquivo)
│   ├── anonymizer.py       # Hash SHA-256 dos identificadores
│   └── network_info.py     # Registra IP/porta/protocolo
└── logs/
    └── chatbot.log         # Log (gerado automaticamente)


SOLUÇÃO DE PROBLEMAS
--------------------
- "TELEGRAM_TOKEN não definido": preencha o token no .env.
- Bot do Telegram não responde: confira o token e a conexão;
  o polling exige internet de saída (TCP 443).
- WhatsApp não responde: confirme que o ngrok está rodando, que a
  URL do webhook no painel Twilio termina com /whatsapp e que a
  pessoa enviou o "join <código>" do Sandbox.
- Porta 5000 ocupada: mude PORT no .env (e o comando do ngrok).

================================================================
