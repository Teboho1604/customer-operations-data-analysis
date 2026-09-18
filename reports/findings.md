# ============================================================
# 11. GENERATE FINDINGS REPORT
# ============================================================

total_cases = len(df)
avg_resolution = df["Resolution_Time"].mean()
avg_satisfaction = df["Satisfaction_Score"].mean()
repeat_rate = (df["Repeat_Contact"].eq("Yes").mean()) * 100

long_cases = (df["Resolution_Time"] > 60).sum()
low_satisfaction = (df["Satisfaction_Score"] <= 2).sum()

at_risk_cases = (
    (df["Satisfaction_Score"] <= 2) &
    (df["Repeat_Contact"] == "Yes")
).sum()

top_issue = (
    df["Issue_Type"]
    .value_counts()
    .idxmax()
)

top_product_repeat = (
    df.groupby("Product")["Repeat_Contact"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .idxmax()
)

top_channel = (
    df.groupby("Channel")["Satisfaction_Score"]
    .mean()
    .idxmax()
)

worst_channel = (
    df.groupby("Channel")["Satisfaction_Score"]
    .mean()
    .idxmin()
)

issue_resolution = (
    df.groupby("Issue_Type")["Resolution_Time"]
    .mean()
    .sort_values(ascending=False)
)

longest_issue = issue_resolution.index[0]

issue_satisfaction = (
    df.groupby("Issue_Type")["Satisfaction_Score"]
    .mean()
    .sort_values()
)

lowest_satisfaction_issue = issue_satisfaction.index[0]

correlation = df[
    ["Resolution_Time", "Satisfaction_Score"]
].corr().iloc[0, 1]


findings_report = f"""
CUSTOMER OPERATIONS ANALYSIS — FINDINGS REPORT
============================================================

1. OVERVIEW
------------------------------------------------------------

This analysis examined customer-service records to identify
patterns in customer satisfaction, resolution times, repeat
contacts, products, issue types, and service channels.

The objective was to identify operational areas that may
require further investigation and improvement.

The validated dataset contained {total_cases:,} customer-service
records.


2. KEY PERFORMANCE INDICATORS
------------------------------------------------------------

Total customer-service cases: {total_cases:,}

Average resolution time: {avg_resolution:.1f} minutes

Average customer satisfaction: {avg_satisfaction:.2f} / 5

Repeat-contact rate: {repeat_rate:.1f}%


3. DATA QUALITY OBSERVATIONS
------------------------------------------------------------

Initial data-quality checks were performed before interpreting
the results.

The checks included:

- Duplicate customer identifiers
- Missing satisfaction scores
- Missing resolution times
- Inconsistent issue-type categories
- Customer-service channel values
- Satisfaction-score ranges
- Unusually long resolution times
- Inconsistent Customer_ID formats
- Inconsistent date formats

Examples of categorical inconsistencies included variations
such as "Technical" and "technical".

Customer-service channel values also contained inconsistent
capitalisation and spelling.

These inconsistencies could affect grouping, filtering and
reporting if they are not standardized before analysis.

The cleaning process therefore standardized categorical values,
validated numeric ranges, handled missing values and removed
duplicate records before analysis.


4. CUSTOMER SATISFACTION
------------------------------------------------------------

The overall average customer satisfaction score was
{avg_satisfaction:.2f} out of 5.

A total of {low_satisfaction:,} cases had a satisfaction score
of 2 or below.

The issue type with the lowest average satisfaction in the
validated sample was:

{lowest_satisfaction_issue}

Satisfaction was also compared across products and service
channels to identify differences that may warrant further
investigation.


5. RESOLUTION TIME
------------------------------------------------------------

The average resolution time was {avg_resolution:.1f} minutes.

A total of {long_cases:,} cases had resolution times exceeding
60 minutes.

The issue type with the highest average resolution time was:

{longest_issue}

Resolution time was compared with satisfaction to examine
whether longer interactions were associated with lower
customer satisfaction.

The correlation between resolution time and satisfaction in
this sample was {correlation:.2f}.

Correlation alone does not establish that resolution time causes
changes in customer satisfaction.


6. REPEAT CUSTOMER CONTACTS
------------------------------------------------------------

The overall repeat-contact rate was {repeat_rate:.1f}%.

Repeat contacts were analyzed across products, issue types and
service channels.

The product with the highest repeat-contact rate in this sample
was:

{top_product_repeat}

A high repeat-contact rate can be used as an operational
indicator because it may highlight cases where customers
require additional assistance after their initial interaction.

Further investigation would be required to determine the
underlying reasons for repeat contacts.


7. ISSUE-TYPE ANALYSIS
------------------------------------------------------------

The most frequently recorded issue type in the dataset was:

{top_issue}

Issue types were compared using:

- Case volume
- Average resolution time
- Average satisfaction
- Repeat-contact rate

This allows operational teams to distinguish between issues
that occur frequently and issues that may require more time or
result in lower satisfaction.


8. CHANNEL ANALYSIS
------------------------------------------------------------

Customer-service channels were compared using resolution time,
satisfaction and repeat-contact rate.

The channel with the highest average satisfaction in this
sample was:

{top_channel}

The channel with the lowest average satisfaction in this
sample was:

{worst_channel}

These differences should be investigated further before drawing
operational conclusions because channel performance can also be
affected by the types of issues customers use each channel to
report.


9. CASES FOR FURTHER INVESTIGATION
------------------------------------------------------------

Potential cases for further investigation were identified using
two indicators:

- Customer satisfaction score of 2 or below
- Repeat customer contact

Cases meeting both conditions:

{at_risk_cases:,}

These indicators do not prove that a customer will leave the
company.

Instead, they identify records that could be prioritized for
additional investigation, quality review or follow-up.


10. BUSINESS RECOMMENDATIONS
------------------------------------------------------------

Based on the analysis framework, the company could consider:

1. Investigating customer cases with consistently low
   satisfaction scores.

2. Reviewing cases with unusually long resolution times.

3. Investigating products with higher repeat-contact rates.

4. Standardizing categorical data before operational reporting.

5. Monitoring service channels for differences in satisfaction,
   resolution time and repeat-contact performance.

6. Introducing regular automated data-quality checks.

7. Monitoring issue types that combine high case volume with
   lower satisfaction or longer resolution times.

8. Using recurring reporting to monitor whether operational
   performance changes over time.


11. LIMITATIONS
------------------------------------------------------------

This project uses a fictional dataset created for portfolio and
learning purposes.

The results therefore should not be interpreted as representing
the performance of a real company.

The analysis identifies patterns within the sample but does not
establish causation.

Additional operational data would be required to determine why
customers are dissatisfied, why repeat contacts occur or why
certain issues require longer resolution times.


12. NEXT STEPS
------------------------------------------------------------

Future analysis could include:

- Building an Excel dashboard
- Expanding monthly performance reporting
- Segmenting customers using additional characteristics
- Creating automated data-quality checks
- Comparing first-contact resolution across channels
- Tracking repeat-contact trends over time
- Developing a recurring operational reporting process
- Adding additional operational KPIs

============================================================
END OF CUSTOMER OPERATIONS ANALYSIS
============================================================
"""

with open(
    "reports/customer_service_findings.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(findings_report)

print("✓ Findings report generated")
