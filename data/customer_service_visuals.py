import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================================================
# CUSTOMER SERVICE ANALYTICS — VISUAL DASHBOARD
# ============================================================

# 1. Embedded Dataset
csv_data = """Customer_ID,Date,Product,Issue_Type,Channel,Resolution_Time,Satisfaction_Score,Repeat_Contact
C001,2026-01-03,SUV,Billing,Phone,18,4,No
C002,2026-01-03,Sedan,Technical,Email,46,2,Yes
C003,2026-01-04,SUV,Delivery,WhatsApp,31,3,No
C004,2026-01-04,Truck,Technical,Phone,72,2,Yes
C005,2026-01-05,Sedan,Billing,Email,15,5,No
C006,2026-01-05,SUV,technical,Phone,61,2,Yes
C007,2026-01-06,Truck,Delivery,WhatsApp,27,4,No
C008,2026-01-06,SUV,Billing,Phone,39,3,Yes
C009,2026-01-07,Sedan,Delivery,Email,22,4,No
C010,2026-01-07,Truck,Technical,Phone,85,1,Yes
C011,2026-01-08,SUV,Delivery,WhatsApp,29,4,No
C012,2026-01-08,Sedan,Billing,Email,17,5,No
C013,2026-01-09,Truck,technical,Phone,58,2,Yes
C014,2026-01-09,SUV,Billing,Email,42,3,No
C015,2026-01-10,Sedan,Technical,Phone,51,3,Yes
C016,2026-01-10,SUV,Delivery,WhatsApp,24,5,No
C017,2026-01-11,Truck,Billing,Phone,33,4,No
C018,2026-01-11,Sedan,Technical,Email,67,2,Yes
C019,2026-01-12,SUV,Billing,Phone,37,3,No
C020,2026-01-12,Truck,Delivery,WhatsApp,19,5,No
C021,2026-01-13,Sedan,Billing,Email,21,4,No
C022,2026-01-13,SUV,Technical,Phone,74,2,Yes
C023,2026-01-14,Truck,Delivery,WhatsApp,26,4,No
C024,2026-01-14,Sedan,Technical,Phone,63,2,Yes
C025,2026-01-15,SUV,Billing,Email,14,5,No
C026,2026-01-15,Truck,Technical,Phone,81,1,Yes
C027,2026-01-16,Sedan,Delivery,WhatsApp,28,4,No
C028,2026-01-16,SUV,Technical,Phone,56,3,Yes
C029,2026-01-17,Truck,Billing,Email,36,3,No
C030,2026-01-17,Sedan,Delivery,WhatsApp,23,5,No"""

# ============================================================
# 2. LOAD & CLEAN DATA
# ============================================================

df = pd.read_csv(io.StringIO(csv_data))

# Normalize issue names
df["Issue_Type"] = df["Issue_Type"].str.strip().str.capitalize()

# Convert repeat contact to numeric
df["Repeat_Numeric"] = (
    df["Repeat_Contact"]
    .str.strip()
    .str.lower()
    .eq("yes")
    .astype(int)
)

# ============================================================
# 3. CALCULATE KPIs
# ============================================================

total_cases = len(df)
avg_resolution = df["Resolution_Time"].mean()
avg_csat = df["Satisfaction_Score"].mean()
repeat_rate = df["Repeat_Numeric"].mean() * 100

# ============================================================
# 4. DASHBOARD STYLE
# ============================================================

sns.set_theme(
    style="whitegrid",
    font_scale=1.0
)

fig = plt.figure(figsize=(16, 11))

fig.patch.set_facecolor("#F7F9FC")

# Main dashboard title
fig.suptitle(
    "CUSTOMER SERVICE ANALYTICS DASHBOARD",
    fontsize=22,
    fontweight="bold",
    x=0.05,
    y=0.98,
    ha="left"
)

fig.text(
    0.05,
    0.945,
    "Operational performance, customer satisfaction and repeat-contact analysis",
    fontsize=11,
    color="#5F6B7A"
)

# ============================================================
# 5. KPI CARDS
# ============================================================

kpi_positions = [
    (0.05, 0.82, 0.20, 0.08),
    (0.28, 0.82, 0.20, 0.08),
    (0.51, 0.82, 0.20, 0.08),
    (0.74, 0.82, 0.20, 0.08)
]

kpi_values = [
    f"{total_cases}",
    f"{avg_resolution:.1f} hrs",
    f"{avg_csat:.2f}/5",
    f"{repeat_rate:.1f}%"
]

kpi_labels = [
    "TOTAL CASES",
    "AVG RESOLUTION TIME",
    "AVG CSAT",
    "REPEAT CONTACT RATE"
]

for position, value, label in zip(
    kpi_positions,
    kpi_values,
    kpi_labels
):

    ax = fig.add_axes(position)

    ax.set_facecolor("white")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.text(
        0.05,
        0.65,
        value,
        fontsize=20,
        fontweight="bold",
        transform=ax.transAxes
    )

    ax.text(
        0.05,
        0.18,
        label,
        fontsize=8.5,
        fontweight="bold",
        color="#6B7280",
        transform=ax.transAxes
    )

# ============================================================
# 6. CHART 1 — RESOLUTION TIME BY ISSUE
# ============================================================

ax1 = fig.add_axes([0.05, 0.50, 0.42, 0.25])

issue_res = (
    df.groupby("Issue_Type")["Resolution_Time"]
    .mean()
    .sort_values(ascending=False)
)

bars = ax1.bar(
    issue_res.index,
    issue_res.values,
    width=0.55
)

ax1.set_title(
    "Average Resolution Time by Issue",
    fontsize=13,
    fontweight="bold",
    loc="left"
)

ax1.set_ylabel("Hours")

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

for bar in bars:

    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{bar.get_height():.1f}h",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

# ============================================================
# 7. CHART 2 — CSAT BY ISSUE
# ============================================================

ax2 = fig.add_axes([0.53, 0.50, 0.42, 0.25])

issue_csat = (
    df.groupby("Issue_Type")["Satisfaction_Score"]
    .mean()
    .sort_values(ascending=False)
)

bars = ax2.bar(
    issue_csat.index,
    issue_csat.values,
    width=0.55
)

ax2.set_title(
    "Average Customer Satisfaction by Issue",
    fontsize=13,
    fontweight="bold",
    loc="left"
)

ax2.set_ylabel("CSAT Score")

ax2.set_ylim(0, 5.5)

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

for bar in bars:

    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.12,
        f"{bar.get_height():.2f}",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

# ============================================================
# 8. CHART 3 — REPEAT CONTACT BY CHANNEL
# ============================================================

ax3 = fig.add_axes([0.05, 0.14, 0.42, 0.25])

channel_repeat = (
    df.groupby("Channel")["Repeat_Numeric"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

bars = ax3.bar(
    channel_repeat.index,
    channel_repeat.values,
    width=0.55
)

ax3.set_title(
    "Repeat Contact Rate by Channel",
    fontsize=13,
    fontweight="bold",
    loc="left"
)

ax3.set_ylabel("Repeat Contact (%)")

ax3.set_ylim(0, max(channel_repeat.values) + 15)

ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

for bar in bars:

    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{bar.get_height():.1f}%",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

# ============================================================
# 9. CHART 4 — PRODUCT PERFORMANCE
# ============================================================

ax4 = fig.add_axes([0.53, 0.14, 0.42, 0.25])

product_metrics = (
    df.groupby("Product")
    .agg(
        Avg_Resolution=("Resolution_Time", "mean"),
        Avg_CSAT=("Satisfaction_Score", "mean")
    )
    .reset_index()
)

x = np.arange(len(product_metrics))

width = 0.35

bars1 = ax4.bar(
    x - width / 2,
    product_metrics["Avg_Resolution"],
    width,
    label="Resolution Time (hrs)"
)

bars2 = ax4.bar(
    x + width / 2,
    product_metrics["Avg_CSAT"] * 10,
    width,
    label="CSAT ×10"
)

ax4.set_title(
    "Product Performance Comparison",
    fontsize=13,
    fontweight="bold",
    loc="left"
)

ax4.set_xticks(x)

ax4.set_xticklabels(
    product_metrics["Product"]
)

ax4.set_ylabel(
    "Value"
)

ax4.legend(
    frameon=False,
    fontsize=9
)

ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)

for bar in bars1:

    ax4.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{bar.get_height():.1f}",
        ha="center",
        fontsize=9
    )

for bar, value in zip(
    bars2,
    product_metrics["Avg_CSAT"]
):

    ax4.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{value:.1f}",
        ha="center",
        fontsize=9
    )

# ============================================================
# 10. FOOTER
# ============================================================

fig.text(
    0.05,
    0.035,
    "Source: Customer service case dataset | Analysis prepared using Python",
    fontsize=8.5,
    color="#6B7280"
)

# ============================================================
# 11. EXPORT
# ============================================================

plt.savefig(
    "customer_service_dashboard.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.show()

print("Dashboard generated successfully:")
print("customer_service_dashboard.png")
