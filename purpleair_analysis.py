"""
PurpleAir Multi-Sensor PM2.5 Analysis — Worcester-area sensors
Dataset: PurpleAir CSV exports (Primary Real Time data)
Source: https://www.purpleair.com/map  → click sensor → graph hamburger → Download

Each sensor exports a CSV with columns:
    created_at, PM1.0_CF1_ug/m3, PM2.5_CF1_ug/m3, PM10.0_CF1_ug/m3,
    UptimeMinutes, RSSI_dbm, Temperature_F, Humidity_%, PM2.5_ATM_ug/m3

Place all sensor CSVs in ./purpleair_data/ then run:
    python purpleair_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import numpy as np

DATA_DIR = Path("purpleair_data")
NAAQS_24H = 35   # µg/m³

def load_sensor(fp):
    df = pd.read_csv(fp, parse_dates=["created_at"])
    df = df.rename(columns={
        "created_at": "ts",
        "PM2.5_CF1_ug/m3": "pm25",
        "Temperature_F": "temp_f",
        "Humidity_%": "rh"
    })[["ts", "pm25", "temp_f", "rh"]]
    df = df[df["pm25"] >= 0].dropna()
    df["sensor"] = fp.stem[:30]
    return df

# --- load all sensors ---
frames = [load_sensor(f) for f in sorted(DATA_DIR.glob("*Primary*.csv"))]
df = pd.concat(frames, ignore_index=True)
df = df.set_index("ts").sort_index()

# --- daily aggregation (matches WDPH weekly brief workflow) ---
daily = df.groupby(["sensor", pd.Grouper(freq="D")])["pm25"].mean().reset_index()
daily.columns = ["sensor", "date", "pm25_daily"]

# --- anomaly flag: >2 SD above sensor mean ---
stats = daily.groupby("sensor")["pm25_daily"].agg(["mean", "std"]).reset_index()
daily = daily.merge(stats, on="sensor")
daily["anomaly"] = daily["pm25_daily"] > daily["mean"] + 2 * daily["std"]

# --- weekly brief table ---
weekly = daily.groupby([pd.Grouper(key="date", freq="W"), "sensor"])["pm25_daily"].mean().reset_index()
weekly.columns = ["week_end", "sensor", "pm25_weekly"]
print("=== Weekly PM2.5 Brief ===")
print(weekly.pivot(index="week_end", columns="sensor", values="pm25_weekly").round(1).to_string())
print(f"\nAnomaly days flagged: {daily['anomaly'].sum()}")
print(daily[daily["anomaly"]][["sensor", "date", "pm25_daily"]].to_string(index=False))

# --- plot ---
fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

for sensor, grp in daily.groupby("sensor"):
    axes[0].plot(grp["date"], grp["pm25_daily"], linewidth=0.8, alpha=0.75, label=sensor)
    anom = grp[grp["anomaly"]]
    axes[0].scatter(anom["date"], anom["pm25_daily"], s=20, zorder=5)

axes[0].axhline(NAAQS_24H, color="red", linestyle="--", linewidth=0.9, label=f"24h NAAQS {NAAQS_24H}")
axes[0].set(ylabel="Daily Mean PM2.5 (µg/m³)", title="PurpleAir Sensors — Daily PM2.5 with Anomalies")
axes[0].legend(fontsize=7, ncol=3)

# temp + RH for one sensor (first) to show environmental context
s0 = df[df["sensor"] == df["sensor"].iloc[0]]
daily_env = s0.resample("D")[["temp_f", "rh"]].mean()
axes[1].plot(daily_env.index, daily_env["temp_f"], color="darkorange", linewidth=0.8, label="Temp (°F)")
ax2 = axes[1].twinx()
ax2.plot(daily_env.index, daily_env["rh"], color="steelblue", linewidth=0.8, label="RH (%)")
axes[1].set(ylabel="Temperature (°F)", title="Temp & Humidity — Reference Sensor")
ax2.set_ylabel("Relative Humidity (%)")
axes[1].legend(loc="upper left", fontsize=7)
ax2.legend(loc="upper right", fontsize=7)

axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
axes[1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=30, ha="right")

plt.tight_layout()
plt.savefig("purpleair_worcester_analysis.png", dpi=150)
plt.show()
print("Saved: purpleair_worcester_analysis.png")
