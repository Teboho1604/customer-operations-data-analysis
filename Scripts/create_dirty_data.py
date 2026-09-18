import pandas as pd
import random
import numpy as np

# ============================================================
# CUSTOMER SERVICE DATASET — DIRTY DATA GENERATOR
# ============================================================

random.seed(42)
np.random.seed(42)

# Load your clean dataset
df = pd.read_csv("customer_service_clean.csv")

# ------------------------------------------------------------
# 1. Inconsistent capitalization
# ------------------------------------------------------------

df.loc[5, "Product"] = "suv"
df.loc[18, "Product"] = "SUV "
df.loc[42, "Product"] = "sedan"
df.loc[73, "Product"] = "Truck "
df.loc[109, "Product"] = "sUv"
df.loc[155, "Product"] = "SEDAN"

# ------------------------------------------------------------
# 2. Inconsistent Issue_Type values
# ------------------------------------------------------------

df.loc[12, "Issue_Type"] = "technical"
df.loc[31, "Issue_Type"] = " Technical"
df.loc[58, "Issue_Type"] = "BILLING"
df.loc[94, "Issue_Type"] = "delivery"
df.loc[137, "Issue_Type"] = " Delivery "
df.loc[201, "Issue_Type"] = "TECHNICAL"

# ------------------------------------------------------------
# 3. Inconsistent Channel values
# ------------------------------------------------------------

df.loc[8, "Channel"] = "phone"
df.loc[27, "Channel"] = " Phone "
df.loc[49, "Channel"] = "EMAIL"
df.loc[81, "Channel"] = "email"
df.loc[124, "Channel"] = "whatsapp"
df.loc[174, "Channel"] = "WhatsApp "
df.loc[236, "Channel"] = "PHONE"

# ------------------------------------------------------------
# 4. Inconsistent Repeat_Contact values
# ------------------------------------------------------------

df.loc[15, "Repeat_Contact"] = "YES"
df.loc[37, "Repeat_Contact"] = "yes"
df.loc[69, "Repeat_Contact"] = "NO"
df.loc[105, "Repeat_Contact"] = "no"
df.loc[149, "Repeat_Contact"] = " Yes "
df.loc[188, "Repeat_Contact"] = " No "

# ------------------------------------------------------------
# 5. Missing values
# ------------------------------------------------------------

df.loc[22, "Resolution_Time"] = np.nan
df.loc[47, "Satisfaction_Score"] = np.nan
df.loc[76, "Channel"] = np.nan
df.loc[101, "Issue_Type"] = np.nan
df.loc[129, "Product"] = np.nan
df.loc[163, "Resolution_Time"] = np.nan
df.loc[214, "Satisfaction_Score"] = np.nan
df.loc[258, "Channel"] = np.nan

# ------------------------------------------------------------
# 6. Invalid satisfaction scores
# ------------------------------------------------------------

df.loc[34, "Satisfaction_Score"] = 6
df.loc[88, "Satisfaction_Score"] = 0
df.loc[142, "Satisfaction_Score"] = 7
df.loc[197, "Satisfaction_Score"] = -1
df.loc[241, "Satisfaction_Score"] = 10

# ------------------------------------------------------------
# 7. Unrealistic resolution times
# ------------------------------------------------------------

df.loc[55, "Resolution_Time"] = 0
df.loc[117, "Resolution_Time"] = -15
df.loc[181, "Resolution_Time"] = 999
df.loc[225, "Resolution_Time"] = 1500

# ------------------------------------------------------------
# 8. Dates in inconsistent formats
# ------------------------------------------------------------

df.loc[29, "Date"] = "03/02/2026"
df.loc[63, "Date"] = "2026/02/09"
df.loc[96, "Date"] = "10-03-2026"
df.loc[145, "Date"] = "2026.04.11"
df.loc[203, "Date"] = "05/05/2026"

# ------------------------------------------------------------
# 9. Extra whitespace
# ------------------------------------------------------------

df.loc[39, "Customer_ID"] = " C038"
df.loc[72, "Customer_ID"] = "C073 "
df.loc[116, "Customer_ID"] = " C117 "
df.loc[154, "Customer_ID"] = "C155 "
df.loc[219, "Customer_ID"] = " C220"

# ------------------------------------------------------------
# 10. Customer ID formatting problems
# ------------------------------------------------------------

df.loc[91, "Customer_ID"] = "c091"
df.loc[133, "Customer_ID"] = "C-133"
df.loc[177, "Customer_ID"] = "091"
df.loc[247, "Customer_ID"] = "CUSTOMER248"

# ------------------------------------------------------------
# 11. Duplicate records
# ------------------------------------------------------------

duplicates = df.iloc[[10, 35, 80, 150, 220]].copy()

df = pd.concat([df, duplicates], ignore_index=True)

# ------------------------------------------------------------
# 12. Duplicate Customer IDs with different information
# ------------------------------------------------------------

df.loc[300, "Customer_ID"] = "C050"
df.loc[301, "Customer_ID"] = "C120"
df.loc[302, "Customer_ID"] = "C200"

# ------------------------------------------------------------
# 13. Additional spelling inconsistencies
# ------------------------------------------------------------

df.loc[52, "Product"] = "Suv"
df.loc[119, "Product"] = "sEDAN"
df.loc[189, "Product"] = "TRUCK"

df.loc[67, "Channel"] = "WhatApp"
df.loc[128, "Channel"] = "Watsapp"
df.loc[198, "Channel"] = "Whats App"

# ------------------------------------------------------------
# 14. Save dirty dataset
# ------------------------------------------------------------

df.to_csv("customer_service_dirty.csv", index=False)

print("Dirty dataset created successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print()
print("Output file: customer_service_dirty.csv")
