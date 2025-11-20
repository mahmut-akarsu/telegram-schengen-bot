Elbette, işte metnin Markdown formatına çevrilmiş hali:

# 📄 Schengen Telegram Bot – API Dokümantasyonu

## 1. Proje Tanımı

Bu proje, farklı Telegram kanallarına (ülkelere göre) duyuru gönderebilen bir sistemdir.

**Backend:** FastAPI  
**Telegram Bot:** `python-telegram-bot` (v21+)

**Özellikler:**

*   Ülke bazlı dinamik endpoint’ler (Italya, Fransa, vb.)
*   Her endpoint’e `POST` isteği ile mesaj gönderme
*   Kanal `chat_id`’si `.env` dosyasından okunur
*   Bot mesaj gönderme yetkisine sahip olmalı

## 2. Kurulum

### 2.1 Gerekli paketler

Python 3.11+ ile uyumlu.

```bash
pip install fastapi uvicorn python-telegram-bot python-dotenv requests
```

### 2.2 .env Dosyası

Proje kök dizininde `.env` dosyası oluşturun:

```ini
BOT_TOKEN=<bot_tokeniniz>
ITALYA_CHAT_ID=<italya_kanal_id>
FRANSA_CHAT_ID=<fransa_kanal_id>
```

*   **`BOT_TOKEN`** → BotFather’dan alınan token
*   **`*_CHAT_ID`** → Kanalın `chat_id`’si (bot admin olarak kanalda olmalı)

## 3. Dosya Yapısı Önerisi

```
schengen_bot_telegram/
├── bot_main.py       ← Telegram bot polling
├── api_main.py       ← FastAPI endpoint’leri
├── .env
├── requirements.txt
```

## 4. Çalıştırma Adımları

### 4.1 Bot’u Başlat

```bash
python bot_main.py
```

Bot, Telegram API ile sürekli polling yapacak. `/start` komutu ile “Çoklu duyuru botu aktif.” mesajını gönderebilir.

### 4.2 API’yi Başlat

```bash
uvicorn api_main:app --reload
```

API, farklı ülke endpoint’lerini dinler ve `POST` isteklerini Telegram kanallarına iletir.

## 5. API Endpointleri

### 5.1 Mesaj Gönderme

`POST /{country}/announce`

#### Parametreler

| Parametre | Açıklama                          | Örnek          |
| :-------- | :-------------------------------- | :------------- |
| `country` | Kanal adı (`CHANNELS` sözlüğünde) | `italya`, `fransa` |

#### Body (JSON)

```json
{
  "text": "Merhaba"
}
```

#### Response

```json
{
  "status": "sent",
  "channel": "italya",
  "chat_id": -1001234567890,
  "text": "Merhaba"
}
```

### 5.2 Kanal Listesi

`GET /channels`

#### Response

```json
{
  "italya": -1001234567890,
  "fransa": -1009876543210
}
```

## 6. Kullanım Örnekleri

### 6.1 Curl ile POST isteği

```bash
curl -X POST http://127.0.0.1:8000/italya/announce \
-H "Content-Type: application/json" \
-d "{\"text\": \"Merhaba İtalya!\"}"
```

### 6.2 Python ile istek

```python
import requests

url = "http://127.0.0.1:8000/italya/announce"
data = {"text": "Merhaba İtalya!"}

response = requests.post(url, json=data)
print(response.json())
```

## 7. Önemli Notlar

*   **Bot Yetkileri:**
    *   Bot, mesaj göndereceği kanalda admin olmalı.
*   **Kanal Chat ID’si:**
    *   Kanal `chat_id`’si `getUpdates` veya test mesajları ile öğrenilebilir.
*   **Python Versiyon:**
    *   Python 3.11+ ve `python-telegram-bot` v21+ önerilir.
*   **FastAPI & Bot Entegrasyonu:**
    *   Bot ve API ayrı process’lerde çalıştırılmalıdır (tek event loop çakışmasını önlemek için).