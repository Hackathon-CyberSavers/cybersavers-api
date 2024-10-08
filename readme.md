# CyberSavers etapa 1 - Banco de Dados e APIs
## Descrição

CyberSavers é um MVP desenvolvido para ajudar pequenos e médios agricultores a otimizar suas atividades por meio de uma plataforma digital. Utilizando tecnologia de inteligência artificial, o projeto fornece informações em tempo real sobre práticas agrícolas, condições do solo e tendências de mercado. O projeto também inclui um marketplace para conectar produtores a compradores locais, eliminando intermediários e maximizando os lucros dos agricultores.
Funcionalidades

1. Recomendações Personalizadas: Análises com base em inteligência artificial para otimizar a produção agrícola.
2. Marketplace Integrado: Conexão direta com compradores locais, facilitando a venda de produtos.
3. Análises em Tempo Real: Dados atualizados sobre cultivo e condições do solo.
4. Interface Intuitiva: Design acessível para usuários com pouca familiaridade tecnológica.

## Tecnologias Utilizadas

    Python
    Flask
    MongoDB
    copilot

## Estrutura do Projeto
```bash
CyberSavers/
├── app/
│   ├── __init__.py                 # Inicialização da aplicação
│   ├── assistant.py                # Assistente para processamento de dados agrícolas
│   ├── commodity_price.py          # Módulo de preços de commodities
│   ├── config.py                   # Configurações globais do projeto
│   ├── routes.py                   # Definição das rotas e APIs da aplicação
│   └── models/                     # Modelos de dados para o banco de dados
│       └── __init__.py             # Inicialização do módulo de modelos
├── .env-example                    # Exemplo de variáveis de ambiente
├── .gitignore                      # Arquivo para exclusão de arquivos no Git
├── gmail_cybersavers.txt           # Detalhes para a configuração do Gmail no projeto
├── readme                          # Arquivo README (atual)
├── requirements.txt                # Lista de dependências do projeto
└── run.py                          # Arquivo principal para execução do aplicativo

```

## Como rodar a aplicação

### Para instalar as depências deve rodar o comando:
    "Clone o repositório: `git clone https://github.com/Hackathon-CyberSavers/.github`",
    "Crie um ambiente virtual: `python -m venv venv`",
    "Ative o ambiente virtual: `source venv/bin/activate` (Linux/MacOS) ou `venv\\Scripts\\activate` (Windows)",
    "Instale as dependências: `pip install -r requirements.txt`",
    "Renomeie o arquivo `.env-example` para `.env` e configure as variáveis de ambiente.",
    "Execute a aplicação: `python run.py`",
