"""
EPA AQS Daily PM2.5 Analysis — Worcester County, MA
Dataset: EPA Air Quality System (AQS) daily summary
Source: https://aqs.epa.gov/aqsweb/airdata/download_files.html
  -> daily_88101_2024.zip  (PM2.5 FRM/FEM, all US monitors, 2024)

Usage:
    Download daily_88101_2024.zip, unzip, place CSV in same folder.
    python epa_aqs_worcester.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CSV = "daily_88101_2024.csv"

# --- load & filter ---
df = pd.read_csv(CSV, parse_dates=["Date Local"])
df.columns = df.columns.str.strip()
wor = df[df["County Name"].str.lower() == "worcester"].copy()
wor = wor.rename(columns={
    "Date Local": "date",
    "Arithmetic Mean": "pm25",
    "Site Num": "site"
})

# --- basic clean ---
wor = wor[wor["pm25"] >= 0].dropna(subset=["pm25", "date"])
wor["month"] = wor["date"].dt.month

# --- stats summary ---
print(wor.groupby("site")["pm25"].describe().round(2))
print(f"\nDays above EPA 24h NAAQS (35 µg/m³): {(wor['pm25'] > 35).sum()}")

# --- seasonal trend ---
monthly = wor.groupby("month")["pm25"].mean()

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

axes[0].bar(monthly.index, monthly.values, color="#3a7ebf")
axes[0].axhline(12, color="red", linestyle="--", linewidth=0.9, label="Annual NAAQS 12 µg/m³")
axes[0].set(xlabel="Month", ylabel="Mean PM2.5 (µg/m³)",
            title="Worcester County — Monthly Mean PM2.5 (2024)", xticks=range(1, 13))
axes[0].legend(fontsize=8)

# --- daily time series per site ---
for site_id, grp in wor.groupby("site"):
    axes[1].plot(grp["date"], grp["pm25"], linewidth=0.7, alpha=0.8, label=f"Site {site_id}")
axes[1].axhline(35, color="red", linestyle="--", linewidth=0.9, label="24h NAAQS 35 µg/m³")
axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b"))
axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
axes[1].set(xlabel="Date", ylabel="PM2.5 (µg/m³)", title="Daily PM2.5 by Monitor Site (2024)")
axes[1].legend(fontsize=7)

plt.tight_layout()
plt.savefig("worcester_pm25_epa_2024.png", dpi=150)
plt.show()
print("Saved: worcester_pm25_epa_2024.png")
