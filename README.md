# GigDex API 🎸

API para o app **GigDex** – O Rastreador de Shows e Festivais. Estilo "Pokédex" para fãs de música colecionarem artistas vistos ao vivo.

## 🚀 Tecnologias
- **FastAPI** (Framework Web)
- **SQLAlchemy** (ORM)
- **Neon Serverless Postgres** (Banco de Dados)
- **MusicBrainz API** (Dados de Artistas)
- **Vercel** (Hospedagem)

## 🛠️ Configuração

1. Clone o repositório.
2. Crie um banco de dados no [Neon](https://neon.tech).
3. Configure a variável de ambiente `DATABASE_URL` no Vercel ou em um arquivo `.env`.
4. Instale as dependências: `pip install -r requirements.txt`.

## 🗄️ Populando o Banco (Seeding)
Para carregar os artistas iniciais usando a MusicBrainz API, execute:
```bash
python seed_db.py
```

## 📍 Endpoints Principais
- `GET /api/v1/artists`: Lista todos os artistas.
- `POST /api/v1/shows`: Realiza o check-in de um novo show.
- `GET /api/v1/shows`: Lista o histórico de shows do usuário.
- `GET /api/v1/stats/{user_id}`: Retorna estatísticas e nível do fã.

## 🎨 Estilo Visual Sugerido (Frontend)
- Modo escuro por padrão.
- Cores: Roxo (#8A2BE2), Ciano (#00FFFF), Magenta (#FF00FF).
- Design vibrante e imersivo inspirado em iluminação de palcos.
