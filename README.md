# Worcester Air Quality Analysis

Python scripts for downloading, cleaning, and analyzing outdoor PM2.5, temperature, and humidity data from EPA regulatory monitors and PurpleAir low-cost sensors in Worcester County, Massachusetts.

Built in the context of the City of Worcester Division of Public Health [Healthy Air, Healthy Communities](https://www.worcesterma.gov/public-health) initiative — a pilot deploying 25 PurpleAir sensors across environmental justice neighborhoods (Jan 2026 – Jan 2027).

---

## Repo Structure

```
worcester-air-quality/
│
├── epa_aqs_worcester.py          # EPA AQS regulatory monitor analysis
├── purpleair_analysis.py         # PurpleAir multi-sensor analysis
│
├── data/
│   └── purpleair_data/           # Drop PurpleAir CSV exports here
│       └── .gitkeep
│
├── outputs/                      # Generated figures saved here
│   └── .gitkeep
│
├── docs/
│   ├── README_epa_aqs.md         # Dataset guide for EPA AQS script
│   └── README_purpleair.md       # Dataset guide for PurpleAir script
│
├── requirements.txt
├── .gitignore
└── README.md                     # This file
```

---

## Scripts

### 1. `epa_aqs_worcester.py` — EPA Regulatory Monitors

Analyzes daily PM2.5 from EPA AQS monitors in Worcester County.  
→ See [`docs/README_epa_aqs.md`](docs/README_epa_aqs.md) for full dataset and usage guide.

**Outputs:**
- Console: per-site descriptive stats, count of NAAQS exceedance days
- Figure: monthly mean bar chart + daily time series per monitor

### 2. `purpleair_analysis.py` — PurpleAir Sensor Network

Ingests exports from multiple PurpleAir sensors, flags anomalies, and generates a weekly brief table.  
→ See [`docs/README_purpleair.md`](docs/README_purpleair.md) for full dataset and usage guide.

**Outputs:**
- Console: weekly PM2.5 pivot table, anomaly day log
- Figure: daily PM2.5 per sensor + temperature/humidity reference panel

---

## Datasets

| Dataset | Source | Variables | Access |
|---|---|---|---|
| EPA AQS Daily Summary | [aqs.epa.gov](https://aqs.epa.gov/aqsweb/airdata/download_files.html) | PM2.5 (µg/m³) | Free download |
| PurpleAir Sensor Export | [map.purpleair.com](https://map.purpleair.com) | PM2.5, Temp, RH | Free via map UI |

Neither dataset requires an API key for the methods used here.

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/worcester-air-quality.git
cd worcester-air-quality
pip install -r requirements.txt
```

---

## Requirements

```
pandas
matplotlib
numpy
```

Full list in `requirements.txt`.

---

## Context

Worcester adults and youth have asthma rates above the Massachusetts state average. Hyper-local air quality data — especially in historically undermonitored environmental justice neighborhoods — is critical for evidence-based public health messaging and policy. These scripts provide a reproducible, open workflow for weekly data review, anomaly detection, and trend reporting.

---

## Author

**Samuel Chibuoyim Uche**  
PhD Candidate, Computer Science — Worcester Polytechnic Institute  
scuche@wpi.edu | [LinkedIn](https://www.linkedin.com/in/samuelchibuoyimuche/)
