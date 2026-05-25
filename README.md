# 🌱 Smart City Sustainability Dashboard

A Streamlit dashboard for urban sustainability analytics across 5 Indian cities.

## Features
- Sustainability Score (gauge)
- KPI cards: AQI, Traffic, Energy, Recycling
- Interactive charts: AQI trend, Traffic congestion, Energy usage, Waste split
- City & month filters
- Raw data viewer + CSV export

## Dataset
`data/smart_city_sustainability.csv`
- 1,825 records · 5 cities · Full year 2023
- Columns: Date, City, AQI, AQI_Category, Traffic_Congestion_Pct, Traffic_Category,
  Energy_Consumption_MWh, Waste_Recycled_Pct, Waste_Landfill_Pct,
  Waste_Composted_Pct, Sustainability_Score

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to https://streamlit.io/cloud
3. Click **New app** → select your repo → set **Main file**: `app.py`
4. Click **Deploy**

## Project Structure

```
smartcity/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── smart_city_sustainability.csv
```
