## Shipping a Data Product: From Raw Telegram Data to an Analytical API

[![MIT License](https://img.shields.io/github/license/bkget/telegram-health-analytics.svg)](https://github.com/bkget/telegram-health-analytics/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/bkget/telegram-health-analytics.svg)](https://github.com/bkget/telegram-health-analytics/stargazers)
[![Issues](https://img.shields.io/github/issues/bkget/telegram-health-analytics.svg)](https://github.com/bkget/telegram-health-analytics/issues)

<!-- <p align="right">
  <a href="https://your-dbt-docs-link.com" target="_blank"><strong>» Explore dbt Docs «</strong></a>
</p> -->

---

### Business Objective

This project delivers an end-to-end data product that ingests and analyzes public Telegram messages from Ethiopian medical business channels. It is built to answer key analytical questions, such as:

- What are the most frequently mentioned medical products?
- How do pricing and availability trends evolve over time?
- What are the posting patterns (daily/weekly)?
- Which channels share the most image-based product content?

---

### Project Architecture

```text
┌────────────┐     ┌────────────┐     ┌─────────────┐     ┌─────────────┐
│ Telegram   │ --> │ Data Lake  │ --> │ PostgreSQL  │ --> │ FastAPI     │
│ Scraper    │     │ (JSON)     │     │ + dbt       │     │ (Analytics) │
└────────────┘     └────────────┘     └─────────────┘     └─────────────┘
                            ↑
                            │
                ┌──────────────────────┐
                │       YOLOv8         |
                │  (Image Detection)   |
                └──────────────────────┘
```

---

### Tech Stack

| Tool         | Purpose                                |
|--------------|----------------------------------------|
| **Telethon** | Scraping Telegram messages             |
| **PostgreSQL** | Central data storage (Dockerized)   |
| **dbt**       | Data transformation/modeling          |
| **YOLOv8**    | Image object detection                 |
| **FastAPI**   | REST API for analytical access        |
| **Dagster**   | Pipeline orchestration & scheduling   |
| **Docker**    | Development and production containerization |

---

### Getting Started

#### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Telegram API credentials (`api_id`, `api_hash`)

#### Setup & Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/bkget/telegram-data-api.git
   cd telegram-data-api
   ```

2. **Create your `.env` file**
   ```env
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_USERNAME=your_username
   ```

3. **Run the containers**
   ```bash
   docker-compose up --build
   ```

4. **Access Tools**
   - Dagster UI: [http://localhost:3000](http://localhost:3000)
   - FastAPI Docs: [http://localhost:8000/docs](http://localhost:8000)

---

### Features

- Scrapes text & media from public Telegram channels
- Transforms raw JSON to analytics-ready data via dbt
- Applies YOLOv8 to detect pills, creams, and packaging
- Aggregates posting trends by channel and day
- Schedules jobs using Dagster with Docker integration
- Exposes insights via a FastAPI interface

---

### API Overview

Example endpoints once the pipeline is live:

```http
GET /top-products?date=2025-07-15
GET /channel-trends?channel_id=1353257880
GET /media-insights
```

You can try them directly from Swagger UI at:  
👉 `http://localhost:8000/docs`

---

### Data Modeling (dbt)

- **Source Layer**: Raw JSON messages (`raw_telegram_messages`)
- **Staging Layer**: Normalized fields (`stg_telegram_messages`)
- **Mart Layer**:
  - `fct_daily_message_summary`: aggregated by author and day
  - `dim_authors`: unique Telegram authors extracted from `from_id`

Build models with:

```bash
dbt run --project-dir telegram_dbt --profiles-dir /app/.dbt
```

Explore lineage and documentation using `dbt docs serve`.

---

### Folder Structure

```
.
├── telegram_scraper/
├── telegram_dbt/
│   ├── models/
│   └── snapshots/
├── yolo_detector/
├── api/
├── dags/
├── docker-compose.yml
└── README.md
```

---

### 👤 Author

**Biruk Getaneh**  
📧 [bkgetmom@gmail.com](mailto:bkgetmom@gmail.com)  
🔗 [https://github.com/bkget](https://github.com/bkget)

---

### 🙏 Acknowledgements

- [Telegram API](https://core.telegram.org/)
- [YOLOv8 by Ultralytics](https://github.com/ultralytics/ultralytics)
- [10 Academy](https://10academy.org)
- [dbt](https://www.getdbt.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Dagster](https://dagster.io)

---

<!-- Shields -->
[license-shield]: https://img.shields.io/github/license/bkget/telegram-data-api?style=for-the-badge
[license-url]: https://github.com/bkget/telegram-data-api/blob/main/LICENSE
[stars-shield]: https://img.shields.io/github/stars/bkget/telegram-data-api?style=for-the-badge
[stars-url]: https://github.com/bkget/telegram-data-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/bkget/telegram-data-api?style=for-the-badge
[issues-url]: https://github.com/bkget/telegram-data-api/issues
