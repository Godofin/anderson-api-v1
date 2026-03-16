# Anderson API v1 (Go Backend)

Esta é a API de backend desenvolvida em Go para o sistema SaaS de gestão de excursões.

## Tecnologias Utilizadas
- **Linguagem:** Go (Golang) 1.22+
- **Framework Web:** Gorilla Mux
- **ORM:** GORM
- **Banco de Dados:** PostgreSQL
- **Autenticação:** JWT (JSON Web Token)

## Estrutura do Projeto
- `cmd/api`: Ponto de entrada da aplicação.
- `internal/handlers`: Controladores das rotas da API.
- `internal/models`: Definições das entidades do banco de dados.
- `internal/repository`: Lógica de negócio e acesso a dados.
- `internal/config`: Configurações de banco de dados e ambiente.

## Funcionalidades Principais
- **Multi-tenancy:** Isolamento de dados por loja (tenant_id).
- **Controle de Planos:** Limites de excursões e funcionários baseados no plano (Basic, Pro, Ultimate).
- **Gestão de Excursões:** Criação, listagem e exportação de passageiros.
- **Reservas e Financeiro:** Controle de vagas, pagamentos parciais e status automático.
- **Check-in:** Registro de embarque/desembarque com timestamp.

## Como Rodar
1. Configure as variáveis de ambiente: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`.
2. Execute: `go run cmd/api/main.go`
