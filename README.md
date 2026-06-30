# jobz-scraper 🚀

Jobz.az iş portalının avtomatik scraping və məlumat toplayıcı platforması.

## 📋 Layihə Haqqında

Bu layihə jobz.az saytından iş əlanlarını avtomatik şəkildə toplayıb, xüsusi verilənlər bazasında saxlamaq məqsədilə hazırlanmışdır.

## 🛠️ Texniki Stack

- **Python 3.11+** - Backend dili
- **BeautifulSoup4** - HTML parsing
- **Selenium** - Dynamic content scraping
- **PostgreSQL** - Verilənlər bazası
- **FastAPI** - REST API
- **GitHub Actions** - Avtomatik scraping (Günlük)
- **Docker** - Containerization

## 📁 Layihə Strukturu

```
jobz-scraper/
├── scraper/
│   ├── __init__.py
│   ├── main.py              # Ana scraper logikası
│   ├── parser.py            # HTML parsing
│   ├── database.py          # DB əməliyyatları
│   └── utils.py             # Köməkçi funksiyalar
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI tətbiqi
│   ├── routes.py            # API endpoints
│   └── models.py            # Pydantic models
├── .github/
│   └── workflows/
│       └── scrape.yml       # GitHub Actions workflow
├── requirements.txt         # Python dependencies
├── config.py               # Tənzimləmələr
└── README.md
```

## 🚀 Başlamaq

1. Repository klonla
2. Python virtual environment yarat
3. Dependencies qur: `pip install -r requirements.txt`
4. `.env` faylını konfiqurasiya et
5. Scraperi çalış: `python -m scraper.main`
