# Deploy Checklist — RAG Q&A на HF Spaces

> Когда освободишься — пройди эти шаги, ~10 минут.

## Backend-провайдер для LLM

Generator провайдер-агностичный. Достаточно ОДНОГО из ключей:
- **OpenRouter** (сейчас используется в eval) — `openai/gpt-oss-120b:free`, лимит 200/день
- **Groq** (рекомендую для prod demo) — Llama 3.3 70B, 14,400/день, самый быстрый
- **HF Inference Providers** — free tier ~$0.10/мес (мало)

Для публичного Space лучше Groq (если не упрёшься в лимит). HF_TOKEN всё равно нужен для самого Space (push/deploy), просто не как LLM-провайдер.

## 1. HuggingFace аккаунт

- https://huggingface.co/join
- Email + username (будет часть URL).

## 2. Получить HF_TOKEN

- https://huggingface.co/settings/tokens → **Create new token** → тип **Write** (нужен для push в Space)
- Имя: `rag-qa-deploy`
- Скопировать `hf_...`.

## 3. Создать Space

- https://huggingface.co/new-space
- Name: `rag-qa`
- SDK: **Streamlit**
- Hardware: **CPU basic (free)**
- Visibility: **Public**
- Create.

## 4. Добавить секреты

Settings → **Variables and secrets** → New secret. Добавить ОДИН (или несколько — первый подходящий будет выбран):

- `GROQ_API_KEY` — если используешь Groq (перегенерь ключ на console.groq.com — старый был битый)
- `OPENROUTER_API_KEY` — если OpenRouter (тот что уже есть в локальном .env)

## 5. Push код

Из папки `ai-portfolio/rag-qa/`:

```bash
git init
git remote add space https://huggingface.co/spaces/<username>/rag-qa
git add .
git commit -m "Initial deploy"
git push space main
```

Если просит auth — логин `<username>`, пароль — HF_TOKEN из шага 2.

## 6. Ждать билд

- Вкладка **App** → логи билда.
- Первый билд: 3-5 минут (torch, sentence-transformers).
- После: публичный URL `<username>-rag-qa.hf.space`.
- Cold start: ~30 секунд.

## 7. После успешного деплоя

Скинь URL — добавлю:
1. В `README.md` Project 1 (раздел Demo).
2. В `ai-portfolio/README.md` (когда появится).
3. В LinkedIn пост (когда будем писать).

## Если сломалось

- **Build fail на pip install** — скинь логи, посмотрим версии.
- **App падает с "No LLM provider configured"** — проверь что секрет в **Secrets**, не в Variables.
- **"Index not built"** — `chroma_db/` не закоммитился. Проверь `.gitignore` — у нас он намеренно исключён из Space push (индекс строится при запуске).

## Стоимость

Всё бесплатно. Если Groq упрётся в 14.4k/день — заведём OR как fallback (код уже умеет).

## Безопасность

После деплоя **ротируй все ключи** из этой локальной `.env` — они в истории чата.
