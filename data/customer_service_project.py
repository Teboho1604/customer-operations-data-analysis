# ============================================================
# CUSTOMER SERVICE DATA ANALYSIS PROJECT
# ============================================================
#
# Workflow:
# 1. Load clean 300-row dataset
# 2. Save clean dataset
# 3. Create realistic dirty dataset
# 4. Clean and validate dirty dataset
# 5. Save validated dataset
# 6. Analyse customer-service performance
# 7. Automatically generate visualisations
# 8. Print data-quality report and business findings
#
# ============================================================

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. SETUP
# ============================================================

random.seed(42)
np.random.seed(42)

DATA_FOLDER = "data"
VISUAL_FOLDER = "visuals"

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(VISUAL_FOLDER, exist_ok=True)

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


# ============================================================
# 2. LOAD ORIGINAL CLEAN DATA
# ============================================================

print("=" * 70)
print("CUSTOMER SERVICE DATA ANALYSIS PROJECT")
print("=" * 70)

print("\nLoading clean dataset...")

clean_df = pd.read_csv(SOURCE_FILE)

print(f"Original rows: {len(clean_df)}")
print(f"Original columns: {len(clean_df.columns)}")

# Save a clean copy inside the project data folder.
clean_df.to_csv(CLEAN_FILE, index=False)

print(f"Clean dataset saved to: {CLEAN_FILE}")


# ============================================================
# 3. CREATE DIRTY DATASET
# ============================================================

print("\n" + "=" * 70)
print("CREATING DIRTY DATA")
print("=" * 70)

df = clean_df.copy()


# ------------------------------------------------------------
# 3.1 Inconsistent Product values
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
# 3.2 Inconsistent Issue_Type values
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
# 3.3 Inconsistent Channel values
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
# 3.4 Inconsistent Repeat_Contact values
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
# 3.5 Missing values
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
# 3.6 Invalid satisfaction scores
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
# 3.7 Unrealistic resolution times
# ------------------------------------------------------------

invalid_resolution_times = {
    55: 0,
    117: -15,
    181: 999,
    225: 1500
}

for index, value in invalid_resolution_times.items():
    if index < len(df):
        df.loc[index, "Resolution_Time"] = value


# ------------------------------------------------------------
# 3.8 Inconsistent date formats
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
# 3.9 Customer ID whitespace
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
# 3.10 Customer ID formatting problems
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
# 3.11 Create exact duplicate records
# ------------------------------------------------------------

duplicate_indexes = [
    10,
    35,
    80,
    150,
    220
]

duplicates = df.iloc[duplicate_indexes].copy()

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)


# ------------------------------------------------------------
# 3.12 Duplicate Customer IDs with different information
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


# ------------------------------------------------------------
# Save dirty dataset
# ------------------------------------------------------------

df.to_csv(DIRTY_FILE, index=False)

print(f"Dirty dataset saved to: {DIRTY_FILE}")
print(f"Dirty rows: {len(df)}")


# ============================================================
# 4. DATA QUALITY REPORT BEFORE CLEANING
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY REPORT — BEFORE CLEANING")
print("=" * 70)

print("\nMissing values:")

missing_report = df.isna().sum()

for column, count in missing_report.items():

    if count > 0:
        print(f"{column}: {count}")


print("\nDuplicate rows:")
print(df.duplicated().sum())


# ============================================================
# 5. CLEAN AND VALIDATE DATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING AND VALIDATION")
print("=" * 70)

cleaned = df.copy()


# ------------------------------------------------------------
# 5.1 Clean column names
# ------------------------------------------------------------

cleaned.columns = (
    cleaned.columns
    .str.strip()
    .str.replace(" ", "_")
)


# ------------------------------------------------------------
# 5.2 Clean Customer IDs
# ------------------------------------------------------------

cleaned["Customer_ID"] = (
    cleaned["Customer_ID"]
    .astype("string")
    .str.strip()
    .str.upper()
)


# Convert common malformed ID patterns.
cleaned["Customer_ID"] = (
    cleaned["Customer_ID"]
    .str.replace("CUSTOMER", "C", regex=False)
    .str.replace("-", "", regex=False)
)

# Add C prefix to numeric IDs.
numeric_id_mask = cleaned["Customer_ID"].str.fullmatch(r"\d+")

cleaned.loc[numeric_id_mask, "Customer_ID"] = (
    "C" +
    cleaned.loc[numeric_id_mask, "Customer_ID"].str.zfill(3)
)


# ------------------------------------------------------------
# 5.3 Standardise Product
# ------------------------------------------------------------

cleaned["Product"] = (
    cleaned["Product"]
    .astype("string")
    .str.strip()
    .str.upper()
)

product_map = {
    "SUV": "SUV",
    "SEDAN": "Sedan",
    "TRUCK": "Truck"
}

cleaned["Product"] = cleaned["Product"].replace(product_map)


# ------------------------------------------------------------
# 5.4 Standardise Issue Type
# ------------------------------------------------------------

cleaned["Issue_Type"] = (
    cleaned["Issue_Type"]
    .astype("string")
    .str.strip()
    .str.title()
)


# ------------------------------------------------------------
# 5.5 Standardise Channel
# ------------------------------------------------------------

cleaned["Channel"] = (
    cleaned["Channel"]
    .astype("string")
    .str.strip()
    .str.lower()
)

channel_map = {
    "phone": "Phone",
    "email": "Email",
    "whatsapp": "WhatsApp",
    "whatapp": "WhatsApp",
    "watsapp": "WhatsApp",
    "whats app": "WhatsApp"
}

cleaned["Channel"] = cleaned["Channel"].replace(channel_map)


# ------------------------------------------------------------
# 5.6 Standardise Repeat Contact
# ------------------------------------------------------------

cleaned["Repeat_Contact"] = (
    cleaned["Repeat_Contact"]
    .astype("string")
    .str.strip()
    .str.lower()
)

repeat_map = {
    "yes": "Yes",
    "no": "No"
}

cleaned["Repeat_Contact"] = (
    cleaned["Repeat_Contact"]
    .replace(repeat_map)
)


# ------------------------------------------------------------
# 5.7 Convert dates
# ------------------------------------------------------------

cleaned["Date"] = pd.to_datetime(
    cleaned["Date"],
    errors="coerce",
    dayfirst=True
)


# ------------------------------------------------------------
# 5.8 Convert numeric columns
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
# 5.9 Validate Satisfaction Score
# ------------------------------------------------------------

invalid_satisfaction = (
    (cleaned["Satisfaction_Score"] < 1) |
    (cleaned["Satisfaction_Score"] > 5)
)

cleaned.loc[
    invalid_satisfaction,
    "Satisfaction_Score"
] = np.nan


# ------------------------------------------------------------
# 5.10 Validate Resolution Time
# ------------------------------------------------------------

invalid_resolution = (
    (cleaned["Resolution_Time"] <= 0) |
    (cleaned["Resolution_Time"] > 480)
)

cleaned.loc[
    invalid_resolution,
    "Resolution_Time"
] = np.nan


# ------------------------------------------------------------
# 5.11 Handle missing numeric values
# ------------------------------------------------------------

cleaned["Resolution_Time"] = (
    cleaned["Resolution_Time"]
    .fillna(cleaned["Resolution_Time"].median())
)

cleaned["Satisfaction_Score"] = (
    cleaned["Satisfaction_Score"]
    .fillna(cleaned["Satisfaction_Score"].median())
)


# ------------------------------------------------------------
# 5.12 Handle missing categorical values
# ------------------------------------------------------------

categorical_columns = [
    "Product",
    "Issue_Type",
    "Channel",
    "Repeat_Contact"
]

for column in categorical_columns:

    cleaned[column] = (
        cleaned[column]
        .fillna("Unknown")
    )


# ------------------------------------------------------------
# 5.13 Handle missing dates
# ------------------------------------------------------------

if cleaned["Date"].isna().sum() > 0:

    cleaned["Date"] = cleaned["Date"].fillna(
        cleaned["Date"].median()
    )


# ------------------------------------------------------------
# 5.14 Remove exact duplicate records
# ------------------------------------------------------------

before_duplicates = len(cleaned)

cleaned = cleaned.drop_duplicates()

duplicates_removed = (
    before_duplicates -
    len(cleaned)
)


# ------------------------------------------------------------
# 5.15 Handle duplicate Customer IDs
# ------------------------------------------------------------

duplicate_customer_ids = (
    cleaned["Customer_ID"]
    .duplicated(keep=False)
)

duplicate_id_count = (
    cleaned.loc[
        duplicate_customer_ids,
        "Customer_ID"
    ].nunique()
)

# Keep the first valid record for each Customer ID.
cleaned = cleaned.drop_duplicates(
    subset=["Customer_ID"],
    keep="first"
)


# ============================================================
# 6. FINAL VALIDATION
# ============================================================

cleaned["Date"] = cleaned["Date"].dt.strftime("%Y-%m-%d")

cleaned.to_csv(
    VALIDATED_FILE,
    index=False
)

print(f"\nValidated dataset saved to: {VALIDATED_FILE}")

print("\nCleaning results:")
print(f"Dirty rows: {len(df)}")
print(f"Validated rows: {len(cleaned)}")
print(f"Exact duplicate rows removed: {duplicates_removed}")
print(
    f"Customer IDs with duplicates detected: "
    f"{duplicate_id_count}"
)

print("\nRemaining missing values:")

remaining_missing = cleaned.isna().sum().sum()

print(remaining_missing)


# ============================================================
# 7. ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER SERVICE ANALYSIS")
print("=" * 70)

# Convert required columns back to numeric.
cleaned["Resolution_Time"] = pd.to_numeric(
    cleaned["Resolution_Time"]
)

cleaned["Satisfaction_Score"] = pd.to_numeric(
    cleaned["Satisfaction_Score"]
)


# ------------------------------------------------------------
# Overall KPIs
# ------------------------------------------------------------

total_customers = len(cleaned)

average_resolution = (
    cleaned["Resolution_Time"].mean()
)

average_satisfaction = (
    cleaned["Satisfaction_Score"].mean()
)

repeat_contact_rate = (
    cleaned["Repeat_Contact"]
    .eq("Yes")
    .mean() * 100
)

print("\nKEY PERFORMANCE INDICATORS")

print(f"Customers analysed: {total_customers}")
print(
    f"Average resolution time: "
    f"{average_resolution:.1f} minutes"
)

print(
    f"Average satisfaction score: "
    f"{average_satisfaction:.2f}/5"
)

print(
    f"Repeat-contact rate: "
    f"{repeat_contact_rate:.1f}%"
)


# ============================================================
# 8. ISSUE TYPE ANALYSIS
# ============================================================

issue_analysis = (
    cleaned
    .groupby("Issue_Type")
    .agg(
        Cases=("Customer_ID", "count"),
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

print("\nISSUE TYPE ANALYSIS")
print(issue_analysis.round(2))


# ============================================================
# 9. CHANNEL ANALYSIS
# ============================================================

channel_analysis = (
    cleaned
    .groupby("Channel")
    .agg(
        Cases=("Customer_ID", "count"),
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

channel_repeat = (
    cleaned
    .groupby("Channel")["Repeat_Contact"]
    .apply(
        lambda x:
        (x == "Yes").mean() * 100
    )
)

channel_analysis[
    "Repeat_Contact_Rate"
] = channel_repeat

print("\nCHANNEL ANALYSIS")
print(channel_analysis.round(2))


# ============================================================
# 10. PRODUCT ANALYSIS
# ============================================================

product_analysis = (
    cleaned
    .groupby("Product")
    .agg(
        Cases=("Customer_ID", "count"),
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

print("\nPRODUCT ANALYSIS")
print(product_analysis.round(2))


# ============================================================
# 11. AUTOMATIC VISUALISATIONS
# ============================================================

print("\n" + "=" * 70)
print("GENERATING VISUALS")
print("=" * 70)


# ------------------------------------------------------------
# Visual 1 — Resolution Time by Issue Type
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

plt.xlabel("Average Resolution Time (minutes)")
plt.ylabel("Issue Type")

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "01_issue_resolution_time.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Visual 2 — Satisfaction by Issue Type
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

plt.xlabel("Average Satisfaction Score")
plt.ylabel("Issue Type")

plt.xlim(0, 5)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "02_satisfaction_by_issue.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Visual 3 — Repeat Contact by Channel
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
plt.ylabel("Repeat Contact Rate (%)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "03_repeat_contact_by_channel.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Visual 4 — Issue Volume
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

issue_counts = (
    cleaned["Issue_Type"]
    .value_counts()
    .sort_values()
)

issue_counts.plot(
    kind="barh"
)

plt.title("Customer Cases by Issue Type")

plt.xlabel("Number of Cases")
plt.ylabel("Issue Type")

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "04_issue_volume.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Visual 5 — Channel Performance
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

channel_analysis[
    "Average_Resolution_Time"
].sort_values().plot(
    kind="bar"
)

plt.title(
    "Average Resolution Time by Channel"
)

plt.xlabel("Channel")
plt.ylabel("Average Resolution Time (minutes)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "05_channel_performance.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Visual 6 — Resolution Time Distribution
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    cleaned["Resolution_Time"],
    bins=20
)

plt.title(
    "Distribution of Customer Resolution Times"
)

plt.xlabel("Resolution Time (minutes)")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "06_resolution_distribution.png"
    ),
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Visual 7 — Satisfaction Distribution
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

satisfaction_counts = (
    cleaned["Satisfaction_Score"]
    .round()
    .value_counts()
    .sort_index()
)

satisfaction_counts.plot(
    kind="bar"
)

plt.title(
    "Customer Satisfaction Score Distribution"
)

plt.xlabel("Satisfaction Score")
plt.ylabel("Number of Customers")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_FOLDER,
        "07_satisfaction_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 12. BUSINESS FINDINGS
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS FINDINGS")
print("=" * 70)


# Highest-volume issue
highest_volume_issue = (
    issue_analysis["Cases"]
    .idxmax()
)

highest_volume_cases = (
    issue_analysis.loc[
        highest_volume_issue,
        "Cases"
    ]
)

# Slowest issue
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

# Lowest satisfaction issue
lowest_satisfaction_issue = (
    issue_analysis[
        "Average_Satisfaction"
    ].idxmin()
)

lowest_satisfaction_score = (
    issue_analysis.loc[
        lowest_satisfaction_issue,
        "Average_Satisfaction"
    ]
)

# Highest repeat-contact channel
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


print(
    f"\n1. Highest case volume: "
    f"{highest_volume_issue} "
    f"({highest_volume_cases} cases)."
)

print(
    f"\n2. Slowest issue category: "
    f"{slowest_issue}, averaging "
    f"{slowest_issue_time:.1f} minutes."
)

print(
    f"\n3. Lowest average satisfaction: "
    f"{lowest_satisfaction_issue}, "
    f"with a score of "
    f"{lowest_satisfaction_score:.2f}/5."
)

print(
    f"\n4. Highest repeat-contact channel: "
    f"{highest_repeat_channel}, "
    f"with a repeat-contact rate of "
    f"{highest_repeat_rate:.1f}%."
)


# ============================================================
# 13. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETE")
print("=" * 70)

print("\nFiles created:")

print(f"✓ {CLEAN_FILE}")
print(f"✓ {DIRTY_FILE}")
print(f"✓ {VALIDATED_FILE}")

print("\nVisuals created:")

visual_files = sorted(
    os.listdir(VISUAL_FOLDER)
)

for file in visual_files:
    print(f"✓ {file}")

print("\nThe complete customer-service analysis workflow is finished.")
