# Export Spotify Liked Songs

Script em **Python** para exportar todas as músicas curtidas da sua conta Spotify (Saved Tracks) em um arquivo **CSV**.

## 🚀 Funcionalidades
- Exporta todas as músicas curtidas da sua conta Spotify.
- Gera um CSV com as seguintes colunas:
- `added_at` (quando foi curtida)
- `track_name`
- `artists`
- `album`
- `album_release_date`
- `duration_ms`
- `popularity`
- `explicit`
- `track_url`
- `isrc`


## 🛠 Pré-requisitos
- Python 3.9 ou superior
- Conta Spotify
- Criar um app no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- https://developer.spotify.com/dashboard
- https://developer.spotify.com/documentation/web-api/concepts/api-calls

## 📥 Instalação

Clone este repositório ou copie o script para sua máquina.

Crie e ative um ambiente virtual:
# bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

Instale as dependências:

# bash
pip install spotipy python-dotenv

## 🔑 Configuração

1. Crie um app no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Adicione o **Redirect URI**:

   http://127.0.0.1:8080/callback

3. Copie o **Client ID**.
4. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

# SPOTIFY_CLIENT_ID=seu_client_id_aqui
# SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui  (opcional, deixe em branco para PKCE)
# SPOTIFY_REDIRECT_URI=http://127.0.0.1:8080/callback
# OUTPUT_CSV=spotify_liked_songs.csv

## ▶️ Como usar

Execute o script:

bash
python export_spotify_liked_songs.py

O navegador abrirá para você autorizar o app.
Após a autorização, o script gera o arquivo definido em `OUTPUT_CSV`.
# 📂 Saída

Um arquivo CSV com todas as músicas curtidas.
Exemplo de conteúdo:

| added\_at         | track\_name | artists     | album   | album\_release\_date | duration\_ms | popularity | explicit | track\_url | isrc       |
| ----------------- | ----------- | ----------- | ------- | -------------------- | ------------ | ---------- | -------- | ---------- | ---------- |
| 2025-08-22T10:00Z | Song A      | Artist X, Y | Album A | 2023-05-01           | 210000       | 75         | False    | https\://… | USABC12345 |

## ⚠️ Observações

# O Redirect URI precisa ser **exatamente** o mesmo no Dashboard e no `.env`.
# Caso troque de máquina, pode ser necessário apagar o arquivo `.cache-liked-songs` para refazer a autenticação.
