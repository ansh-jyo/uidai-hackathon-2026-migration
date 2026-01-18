# UIDAI Hackathon 2026 — Migration & Urbanization Tracker 🛰️

A dark + neon corporate dashboard built using UIDAI aggregated datasets to analyze **migration signals (proxy)** and **urbanization hotspots** across India.

---

## 🔥 Key Features
- 🇮🇳 India Overview choropleth map (state boundaries)
- 📊 State ranking: Top In-migration vs Out-migration (proxy)
- 🌆 Urbanization hotspots scatter plot (activity vs migration index)
- 🌡️ Heatmap: Migration Index (State × Month)
- 🚀 Top Movers: Month-on-Month change detection
- 🏙️ State Deep Dive (trend + top districts)
- 📍 District Drilldown (district trend + age activity)
- 👥 Age Insights (proxy): trend + adult share % + age share donut

---

## 🧠 Important Note (Proxy Disclaimer)
This dashboard uses **aggregated UIDAI activity data**.  
The **Migration Index is a proxy signal**, based on activity and growth patterns.  
It does **NOT track individuals** and does **NOT represent exact migration counts**.

---

## 📂 Project Structure
uidai-hackathon-2026-migration/
│
├── dashboard/
│   ├── app.py
│   ├── requirements.txt
│   ├── india_states.geojson
│
├── data/
│   ├── dashboard_state_month.csv
│   ├── dashboard_district_month.csv
│
├── notebook/
│   └── UIDAI_Migration_Urbanization_Analysis.ipynb
│
├── assets/
│   └── aadhaar_transparent.png
│
└── README.md

---

## ▶️ Run Locally

### 1) Clone the repo
```bash
git clone https://github.com/ansh-jyo/uidai-hackathon-2026-migration.git
cd uidai-hackathon-2026-migration


pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py

http://localhost:8501


