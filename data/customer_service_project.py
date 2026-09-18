import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# CUSTOMER SERVICE DATA QUALITY & ANALYSIS PROJECT
# ============================================================
# Workflow:
# Clean data
#     ↓
# Dirty data generation
#     ↓
# Data quality audit
#     ↓
# Cleaning
#     ↓
# Validation
#     ↓
# Analysis
#     ↓
# Visualisation
#     ↓
# Automated findings
# ============================================================


# ============================================================
# 1. SETUP
# ============================================================

random.seed(42)
np.random.seed(42)

DATA_FOLDER = "data"
VISUAL_FOLDER = "visuals"
REPORT_FOLDER = "reports"

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(VISUAL_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

SOURCE_FILE = "customer_service_clean.csv"

CLEAN_FILE = os.path.join(
    DATA_FOLDER,
    "customer_service_clean.csv"
)

DIRTY_FILE = os.path.join(
    DATA_FOLDER,
    "customer_service_dirty.csv"
)

VALIDATED_FILE = os.path.join(
    DATA_FOLDER,
    "customer_service_validated.csv"
)

FINDINGS_FILE = os.path.join(
    REPORT_FOLDER,
    "customer_service_findings.txt"
)


# ============================================================
# 2. LOAD CLEAN DATA
# ============================================================

print("=" * 70)
print("CUSTOMER SERVICE DATA QUALITY & ANALYSIS PROJECT")
print("=" * 70)

print("\n[1/8] Loading clean dataset...")

clean_df = pd.read_csv(SOURCE_FILE)

print(f"Rows loaded: {len(clean_df)}")
print(f"Columns loaded: {len(clean_df.columns)}")

clean_df.to_csv(
    CLEAN_FILE,
    index=False
)


# ============================================================
# 3. CREATE DIRTY DATA
# ============================================================

print("\n[2/8] Creating dirty dataset...")

df = clean_df.copy()


# ------------------------------------------------------------
# Product inconsistencies
# ------------------------------------------------------------

product_changes = {
    5: "suv",
    18: "SUV ",
    42: "sedan",
    73: "Truck ",
    109: "sUv",
    155: "SEDAN",
    52: "Suv",
    119: "sEDAN",
    189: "TRUCK"
}

for index, value in product_changes.items():
    if index < len(df):
        df.loc[index, "Product"] = value


# ------------------------------------------------------------
# Issue Type inconsistencies
# ------------------------------------------------------------

issue_changes = {
    12: "technical",
    31: " Technical",
    58: "BILLING",
    94: "delivery",
    137: " Delivery ",
    201: "TECHNICAL"
}

for index, value in issue_changes.items():
    if index < len(df):
        df.loc[index, "Issue_Type"] = value


# ------------------------------------------------------------
# Channel inconsistencies
# ------------------------------------------------------------

channel_changes = {
    8: "phone",
    27: " Phone ",
    49: "EMAIL",
    81: "email",
    124: "whatsapp",
    174: "WhatsApp ",
    236: "PHONE",
    67: "WhatApp",
    128: "Watsapp",
    198: "Whats App"
}

for index, value in channel_changes.items():
    if index < len(df):
        df.loc[index, "Channel"] = value


# ------------------------------------------------------------
# Repeat contact inconsistencies
# ------------------------------------------------------------

repeat_changes = {
    15: "YES",
    37: "yes",
    69: "NO",
    105: "no",
    149: " Yes ",
    188: " No "
}

for index, value in repeat_changes.items():
    if index < len(df):
        df.loc[index, "Repeat_Contact"] = value


# ------------------------------------------------------------
# Missing values
# ------------------------------------------------------------

missing_values = [
    (22, "Resolution_Time"),
    (47, "Satisfaction_Score"),
    (76, "Channel"),
    (101, "Issue_Type"),
    (129, "Product"),
    (163, "Resolution_Time"),
    (214, "Satisfaction_Score"),
    (258, "Channel")
]

for index, column in missing_values:
    if index < len(df):
        df.loc[index, column] = np.nan


# ------------------------------------------------------------
# Invalid satisfaction scores
# ------------------------------------------------------------

invalid_scores = {
    34: 6,
    88: 0,
    142: 7,
    197: -1,
    241: 10
}

for index, value in invalid_scores.items():
    if index < len(df):
        df.loc[index, "Satisfaction_Score"] = value


# ------------------------------------------------------------
# Invalid resolution times
# ------------------------------------------------------------

invalid_resolution = {
    55: 0,
    117: -15,
    181: 999,
    225: 1500
}

for index, value in invalid_resolution.items():
    if index < len(df):
        df.loc[index, "Resolution_Time"] = value


# ------------------------------------------------------------
# Date inconsistencies
# ------------------------------------------------------------

date_changes = {
    29: "03/02/2026",
    63: "2026/02/09",
    96: "10-03-2026",
    145: "2026.04.11",
    203: "05/05/2026"
}

for index, value in date_changes.items():
    if index < len(df):
        df.loc[index, "Date"] = value


# ------------------------------------------------------------
# Customer ID whitespace
# ------------------------------------------------------------

id_changes = {
    39: " C038",
    72: "C073 ",
    116: " C117 ",
    154: "C155 ",
    219: " C220"
}

for index, value in id_changes.items():
    if index < len(df):
        df.loc[index, "Customer_ID"] = value


# ------------------------------------------------------------
# Customer ID formatting problems
# ------------------------------------------------------------

bad_ids = {
    91: "c091",
    133: "C-133",
    177: "091",
    247: "CUSTOMER248"
}

for index, value in bad_ids.items():
    if index < len(df):
        df.loc[index, "Customer_ID"] = value


# ------------------------------------------------------------
# Exact duplicate records
# ------------------------------------------------------------

duplicate_indexes = [10, 35, 80, 150, 220]

duplicates = df.iloc[
    duplicate_indexes
].copy()

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)


# ------------------------------------------------------------
# Conflicting Customer IDs
# ------------------------------------------------------------

if len(df) >= 303:

    df.loc[300, "Customer_ID"] = "C050"
    df.loc[301, "Customer_ID"] = "C120"
    df.loc[302, "Customer_ID"] = "C200"

    df.loc[300, "Resolution_Time"] = 95
    df.loc[301, "Resolution_Time"] = 120
    df.loc[302, "Resolution_Time"] = 80

    df.loc[300, "Satisfaction_Score"] = 2
    df.loc[301, "Satisfaction_Score"] = 1
    df.loc[302, "Satisfaction_Score"] = 2

    df.loc[300, "Repeat_Contact"] = "Yes"
    df.loc[301, "Repeat_Contact"] = "Yes"
    df.loc[302, "Repeat_Contact"] = "Yes"


df.to_csv(
    DIRTY_FILE,
    index=False
)

print(f"Dirty dataset: {len(df)} rows")


# ============================================================
# 4. DATA QUALITY AUDIT
# ============================================================

print("\n[3/8] Auditing dirty data...")

audit = {
    "Rows": len(df),
    "Columns": len(df.columns),
    "Missing cells": int(df.isna().sum().sum()),
    "Exact duplicate rows": int(df.duplicated().sum()),
    "Duplicate Customer IDs": int(
        df["Customer_ID"]
        .duplicated()
        .sum()
    )
}

print("\nDATA QUALITY AUDIT")

for key, value in audit.items():
    print(f"{key}: {value}")


# ============================================================
# 5. CLEAN DATA
# ============================================================

print("\n[4/8] Cleaning dataset...")

cleaned = df.copy()

cleaned.columns = (
    cleaned.columns
    .str.strip()
    .str.replace(" ", "_")
)


# ------------------------------------------------------------
# Customer IDs
# ------------------------------------------------------------

cleaned["Customer_ID"] = (
    cleaned["Customer_ID"]
    .astype("string")
    .str.strip()
    .str.upper()
)

cleaned["Customer_ID"] = (
    cleaned["Customer_ID"]
    .str.replace(
        "CUSTOMER",
        "C",
        regex=False
    )
    .str.replace(
        "-",
        "",
        regex=False
    )
)

numeric_ids = cleaned[
    "Customer_ID"
].str.fullmatch(r"\d+")

cleaned.loc[
    numeric_ids,
    "Customer_ID"
] = (
    "C"
    + cleaned.loc[
        numeric_ids,
        "Customer_ID"
    ].str.zfill(3)
)


# ------------------------------------------------------------
# Product
# ------------------------------------------------------------

cleaned["Product"] = (
    cleaned["Product"]
    .astype("string")
    .str.strip()
    .str.upper()
)

cleaned["Product"] = cleaned[
    "Product"
].replace({
    "SUV": "SUV",
    "SEDAN": "Sedan",
    "TRUCK": "Truck"
})


# ------------------------------------------------------------
# Issue Type
# ------------------------------------------------------------

cleaned["Issue_Type"] = (
    cleaned["Issue_Type"]
    .astype("string")
    .str.strip()
    .str.title()
)


# ------------------------------------------------------------
# Channel
# ------------------------------------------------------------

cleaned["Channel"] = (
    cleaned["Channel"]
    .astype("string")
    .str.strip()
    .str.lower()
)

cleaned["Channel"] = cleaned[
    "Channel"
].replace({
    "phone": "Phone",
    "email": "Email",
    "whatsapp": "WhatsApp",
    "whatapp": "WhatsApp",
    "watsapp": "WhatsApp",
    "whats app": "WhatsApp"
})


# ------------------------------------------------------------
# Repeat Contact
# ------------------------------------------------------------

cleaned["Repeat_Contact"] = (
    cleaned["Repeat_Contact"]
    .astype("string")
    .str.strip()
    .str.lower()
)

cleaned["Repeat_Contact"] = (
    cleaned["Repeat_Contact"]
    .replace({
        "yes": "Yes",
        "no": "No"
    })
)


# ------------------------------------------------------------
# Dates
# ------------------------------------------------------------

cleaned["Date"] = pd.to_datetime(
    cleaned["Date"],
    errors="coerce",
    dayfirst=True
)


# ------------------------------------------------------------
# Numeric columns
# ------------------------------------------------------------

cleaned["Resolution_Time"] = pd.to_numeric(
    cleaned["Resolution_Time"],
    errors="coerce"
)

cleaned["Satisfaction_Score"] = pd.to_numeric(
    cleaned["Satisfaction_Score"],
    errors="coerce"
)


# ------------------------------------------------------------
# Validate satisfaction
# ------------------------------------------------------------

invalid_satisfaction = (
    (cleaned["Satisfaction_Score"] < 1)
    |
    (cleaned["Satisfaction_Score"] > 5)
)

cleaned.loc[
    invalid_satisfaction,
    "Satisfaction_Score"
] = np.nan


# ------------------------------------------------------------
# Validate resolution time
# ------------------------------------------------------------

invalid_resolution = (
    (cleaned["Resolution_Time"] <= 0)
    |
    (cleaned["Resolution_Time"] > 480)
)

cleaned.loc[
    invalid_resolution,
    "Resolution_Time"
] = np.nan


# ------------------------------------------------------------
# Missing numeric values
# ------------------------------------------------------------

cleaned["Resolution_Time"] = (
    cleaned["Resolution_Time"]
    .fillna(
        cleaned["Resolution_Time"].median()
    )
)

cleaned["Satisfaction_Score"] = (
    cleaned["Satisfaction_Score"]
    .fillna(
        cleaned["Satisfaction_Score"].median()
    )
)


# ------------------------------------------------------------
# Missing categorical values
# ------------------------------------------------------------

for column in [
    "Product",
    "Issue_Type",
    "Channel",
    "Repeat_Contact"
]:

    cleaned[column] = (
        cleaned[column]
        .fillna("Unknown")
    )


# ------------------------------------------------------------
# Missing dates
# ------------------------------------------------------------

cleaned["Date"] = (
    cleaned["Date"]
    .fillna(
        cleaned["Date"].median()
    )
)


# ------------------------------------------------------------
# Remove exact duplicates
# ------------------------------------------------------------

before = len(cleaned)

cleaned = cleaned.drop_duplicates()

duplicates_removed = (
    before - len(cleaned)
)


# ------------------------------------------------------------
# Remove conflicting Customer IDs
# ------------------------------------------------------------

duplicate_ids = (
    cleaned["Customer_ID"]
    .duplicated(keep=False)
)

duplicate_id_count = (
    cleaned.loc[
        duplicate_ids,
        "Customer_ID"
    ].nunique()
)

cleaned = cleaned.drop_duplicates(
    subset=["Customer_ID"],
    keep="first"
)


# ============================================================
# 6. VALIDATION
# ============================================================

print("\n[5/8] Validating cleaned data...")

cleaned["Date"] = (
    cleaned["Date"]
    .dt.strftime("%Y-%m-%d")
)

validation_results = {}

validation_results[
    "No missing values"
] = (
    cleaned.isna().sum().sum() == 0
)

validation_results[
    "Customer IDs valid"
] = (
    cleaned["Customer_ID"]
    .str.match(r"^C\d{3}$")
    .all()
)

validation_results[
    "Satisfaction scores valid"
] = (
    cleaned["Satisfaction_Score"]
    .between(1, 5)
    .all()
)

validation_results[
    "Resolution times valid"
] = (
    cleaned["Resolution_Time"]
    .between(0, 480)
    .all()
)

validation_results[
    "No duplicate Customer IDs"
] = (
    cleaned["Customer_ID"]
    .is_unique
)

print("\nVALIDATION RESULTS")

for test, passed in validation_results.items():

    status = "PASS" if passed else "FAIL"

    print(
        f"{status}: {test}"
    )


all_valid = all(
    validation_results.values()
)


cleaned.to_csv(
    VALIDATED_FILE,
    index=False
)


# ============================================================
# 7. ANALYSIS
# ============================================================

print("\n[6/8] Analysing validated dataset...")

analysis_df = cleaned.copy()

analysis_df["Date"] = pd.to_datetime(
    analysis_df["Date"]
)

analysis_df["Resolution_Time"] = (
    pd.to_numeric(
        analysis_df["Resolution_Time"]
    )
)

analysis_df["Satisfaction_Score"] = (
    pd.to_numeric(
        analysis_df["Satisfaction_Score"]
    )
)


# ------------------------------------------------------------
# Overall KPIs
# ------------------------------------------------------------

total_cases = len(analysis_df)

average_resolution = (
    analysis_df["Resolution_Time"]
    .mean()
)

average_satisfaction = (
    analysis_df["Satisfaction_Score"]
    .mean()
)

repeat_rate = (
    analysis_df["Repeat_Contact"]
    .eq("Yes")
    .mean()
    * 100
)


# ------------------------------------------------------------
# Issue analysis
# ------------------------------------------------------------

issue_analysis = (
    analysis_df
    .groupby("Issue_Type")
    .agg(
        Cases=(
            "Customer_ID",
            "count"
        ),
        Average_Resolution_Time=(
            "Resolution_Time",
            "mean"
        ),
        Average_Satisfaction=(
            "Satisfaction_Score",
            "mean"
        )
    )
    .sort_values(
        "Cases",
        ascending=False
    )
)


# ------------------------------------------------------------
# Channel analysis
# ------------------------------------------------------------

channel_analysis = (
    analysis_df
    .groupby("Channel")
    .agg(
        Cases=(
            "Customer_ID",
            "count"
        ),
        Average_Resolution_Time=(
            "Resolution_Time",
            "mean"
        ),
        Average_Satisfaction=(
            "Satisfaction_Score",
            "mean"
        )
    )
)

channel_analysis[
    "Repeat_Contact_Rate"
] = (
    analysis_df
    .groupby("Channel")[
        "Repeat_Contact"
    ]
    .apply(
        lambda x:
        (x == "Yes").mean() * 100
    )
)


# ------------------------------------------------------------
# Monthly analysis
# ------------------------------------------------------------

analysis_df["Month"] = (
    analysis_df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_analysis = (
    analysis_df
    .groupby("Month")
    .agg(
        Cases=(
            "Customer_ID",
            "count"
        ),
        Average_Resolution_Time=(
            "Resolution_Time",
            "mean"
        ),
        Average_Satisfaction=(
            "Satisfaction_Score",
            "mean"
        )
    )
)


# ------------------------------------------------------------
# Repeat contact vs satisfaction
# ------------------------------------------------------------

repeat_analysis = (
    analysis_df
    .groupby("Repeat_Contact")
    .agg(
        Customers=(
            "Customer_ID",
            "count"
        ),
        Average_Satisfaction=(
            "Satisfaction_Score",
            "mean"
        ),
        Average_Resolution_Time=(
            "Resolution_Time",
            "mean"
        )
    )
)


# ------------------------------------------------------------
# Resolution vs satisfaction correlation
# ------------------------------------------------------------

resolution_satisfaction_corr = (
    analysis_df[
        [
            "Resolution_Time",
            "Satisfaction_Score"
        ]
    ]
    .corr()
    .loc[
        "Resolution_Time",
        "Satisfaction_Score"
    ]
)


# ============================================================
# 8. VISUALISATIONS
# ============================================================

print("\n[7/8] Generating visualisations...")


# ------------------------------------------------------------
# 01 Executive Dashboard
# ------------------------------------------------------------

fig = plt.figure(
    figsize=(16, 10)
)

fig.suptitle(
    "Customer Service Performance Dashboard",
    fontsize=20
)

ax1 = plt.subplot(2, 2, 1)

issue_analysis[
    "Cases"
].sort_values().plot(
    kind="barh",
    ax=ax1
)

ax1.set_title(
    "Cases by Issue Type"
)

ax1.set_xlabel("Cases")


ax2 = plt.subplot(2, 2, 2)

issue_analysis[
    "Average_Resolution_Time"
].sort_values().plot(
    kind="barh",
    ax=ax2
)

ax2.set_title(
    "Average Resolution Time"
)

ax2.set_xlabel("Minutes")


ax3 = plt.subplot(2, 2, 3)

channel_analysis[
    "Average_Satisfaction"
].sort_values().plot(
    kind="bar",
    ax=ax3
)

ax3.set_title(
    "Average Satisfaction by Channel"
)

ax3.set_ylabel("Score")


ax4 = plt.subplot(2, 2, 4)

monthly_analysis[
    "Cases"
].plot(
    kind="line",
    marker="o",
    ax=ax4
)

ax4.set_title(
    "Monthly Case Volume"
)

ax4.set_xlabel("Month")
ax4.set_ylabel("Cases")

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "01_executive_dashboard.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 02 Issue Resolution Time
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

issue_analysis[
    "Average_Resolution_Time"
].sort_values().plot(
    kind="barh"
)

plt.title(
    "Average Resolution Time by Issue Type"
)

plt.xlabel(
    "Average Resolution Time (minutes)"
)

plt.ylabel("Issue Type")

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "02_issue_resolution_time.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 03 Satisfaction by Issue
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

issue_analysis[
    "Average_Satisfaction"
].sort_values().plot(
    kind="barh"
)

plt.title(
    "Average Customer Satisfaction by Issue Type"
)

plt.xlabel(
    "Average Satisfaction Score"
)

plt.ylabel("Issue Type")

plt.xlim(0, 5)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "03_satisfaction_by_issue.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 04 Repeat Contact by Channel
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

channel_analysis[
    "Repeat_Contact_Rate"
].sort_values().plot(
    kind="bar"
)

plt.title(
    "Repeat Contact Rate by Channel"
)

plt.xlabel("Channel")

plt.ylabel(
    "Repeat Contact Rate (%)"
)

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "04_repeat_contact_by_channel.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 05 Issue Volume
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

issue_analysis[
    "Cases"
].sort_values().plot(
    kind="barh"
)

plt.title(
    "Customer Cases by Issue Type"
)

plt.xlabel("Number of Cases")

plt.ylabel("Issue Type")

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "05_issue_volume.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 06 Monthly Trends
# ------------------------------------------------------------

fig, ax1 = plt.subplots(
    figsize=(11, 6)
)

ax1.plot(
    monthly_analysis.index,
    monthly_analysis[
        "Cases"
    ],
    marker="o"
)

ax1.set_xlabel("Month")
ax1.set_ylabel("Cases")

ax1.tick_params(
    axis="x",
    rotation=45
)

ax2 = ax1.twinx()

ax2.plot(
    monthly_analysis.index,
    monthly_analysis[
        "Average_Satisfaction"
    ],
    marker="s"
)

ax2.set_ylabel(
    "Average Satisfaction"
)

plt.title(
    "Monthly Customer Service Trends"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "06_monthly_trends.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 07 Resolution vs Satisfaction
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    analysis_df["Resolution_Time"],
    analysis_df["Satisfaction_Score"],
    alpha=0.65
)

plt.title(
    "Resolution Time vs Customer Satisfaction"
)

plt.xlabel(
    "Resolution Time (minutes)"
)

plt.ylabel(
    "Satisfaction Score"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "07_resolution_vs_satisfaction.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 08 Satisfaction Distribution
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

(
    analysis_df[
        "Satisfaction_Score"
    ]
    .round()
    .value_counts()
    .sort_index()
    .plot(kind="bar")
)

plt.title(
    "Customer Satisfaction Score Distribution"
)

plt.xlabel(
    "Satisfaction Score"
)

plt.ylabel(
    "Number of Customers"
)

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "08_satisfaction_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 9. AUTOMATED FINDINGS REPORT
# ============================================================

print("\n[8/8] Creating findings report...")

highest_volume_issue = (
    issue_analysis["Cases"].idxmax()
)

highest_volume_cases = (
    issue_analysis.loc[
        highest_volume_issue,
        "Cases"
    ]
)

slowest_issue = (
    issue_analysis[
        "Average_Resolution_Time"
    ].idxmax()
)

slowest_issue_time = (
    issue_analysis.loc[
        slowest_issue,
        "Average_Resolution_Time"
    ]
)

lowest_satisfaction_issue = (
    issue_analysis[
        "Average_Satisfaction"
    ].idxmin()
)

lowest_satisfaction = (
    issue_analysis.loc[
        lowest_satisfaction_issue,
        "Average_Satisfaction"
    ]
)

highest_repeat_channel = (
    channel_analysis[
        "Repeat_Contact_Rate"
    ].idxmax()
)

highest_repeat_rate = (
    channel_analysis.loc[
        highest_repeat_channel,
        "Repeat_Contact_Rate"
    ]
)

fastest_channel = (
    channel_analysis[
        "Average_Resolution_Time"
    ].idxmin()
)

highest_satisfaction_channel = (
    channel_analysis[
        "Average_Satisfaction"
    ].idxmax()
)


report = f"""
CUSTOMER SERVICE DATA ANALYSIS
==============================

DATASET
-------
Validated records: {total_cases}

Average resolution time:
{average_resolution:.2f} minutes

Average satisfaction:
{average_satisfaction:.2f}/5

Repeat-contact rate:
{repeat_rate:.2f}%


DATA QUALITY
------------
Dirty dataset records: {len(df)}
Exact duplicate records removed: {duplicates_removed}
Duplicate Customer IDs detected: {duplicate_id_count}
Validation status: {"PASSED" if all_valid else "REVIEW REQUIRED"}


KEY FINDINGS
------------

1. Highest case volume
{highest_volume_issue}: {highest_volume_cases} cases.

2. Slowest issue category
{slowest_issue}: {slowest_issue_time:.2f} minutes average resolution time.

3. Lowest average satisfaction
{lowest_satisfaction_issue}: {lowest_satisfaction:.2f}/5.

4. Highest repeat-contact channel
{highest_repeat_channel}: {highest_repeat_rate:.2f}% repeat-contact rate.

5. Fastest channel by average resolution time
{fastest_channel}.

6. Highest average satisfaction by channel
{highest_satisfaction_channel}.

7. Resolution time and satisfaction
Correlation coefficient: {resolution_satisfaction_corr:.3f}


INTERPRETATION
--------------
These findings identify areas that may warrant further investigation,
particularly issue categories with higher resolution times, channels
with higher repeat-contact rates, and areas associated with lower
customer satisfaction.

Correlation does not establish causation. Operational decisions
should consider additional business context and data.


FILES CREATED
-------------
customer_service_clean.csv
customer_service_dirty.csv
customer_service_validated.csv

Visualisations:
01_executive_dashboard.png
02_issue_resolution_time.png
03_satisfaction_by_issue.png
04_repeat_contact_by_channel.png
05_issue_volume.png
06_monthly_trends.png
07_resolution_vs_satisfaction.png
08_satisfaction_distribution.png
"""

with open(
    FINDINGS_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)


# ============================================================
# 10. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETE")
print("=" * 70)

print(
    f"\nValidated dataset: "
    f"{VALIDATED_FILE}"
)

print(
    f"Findings report: "
    f"{FINDINGS_FILE}"
)

print(
    f"Visualisations generated: "
    f"{len(os.listdir(VISUAL_FOLDER))}"
)

print("\nYour customer-service analytics workflow is complete.")
