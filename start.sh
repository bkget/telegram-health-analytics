#!/bin/sh
echo "▶️ Starting scraping..."
python scripts/scraper.py

echo "▶️ Loading JSON files to Postgres..."
python scripts/load_json_to_postgres.py
