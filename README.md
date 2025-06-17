# FlexoAI Sacose

Agent AI de ofertare sacose personalizate, cu backend FastAPI și frontend compatibil WordPress.

## Deploy pe Render

1. Crează un nou serviciu pe Render din acest repo.
2. Setează build command: `pip install -r requirements.txt`
3. Setează start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## API

**POST /oferta**

```json
{
  "dimensiune": "24X11X32",
  "material": "albă",
  "maner": "plat",
  "imprimare": "mică",
  "cantitate": 5000
}
```

## Frontend

Se inserează în WordPress prin iframe sau ca fișier HTML direct.
