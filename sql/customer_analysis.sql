-- ============================================================
-- CUSTOMER SERVICE SQL ANALYSIS
-- ============================================================


-- ============================================================
-- 1. DATASET OVERVIEW
-- ============================================================

SELECT
    COUNT(*) AS total_customers
FROM customer_service;


-- ============================================================
-- 2. CHECK FOR MISSING VALUES
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(Customer_ID) AS customer_ids_present,
    COUNT(Date) AS dates_present,
    COUNT(Product) AS products_present,
    COUNT(Issue_Type) AS issues_present,
    COUNT(Channel) AS channels_present,
    COUNT(Resolution_Time) AS resolution_times_present,
    COUNT(Satisfaction_Score) AS satisfaction_scores_present,
    COUNT(Repeat_Contact) AS repeat_contact_present
FROM customer_service;


-- ============================================================
-- 3. OVERALL KPIs
-- ============================================================

SELECT
    COUNT(*) AS total_cases,
    ROUND(AVG(Resolution_Time), 2)
        AS average_resolution_time,
    ROUND(AVG(Satisfaction_Score), 2)
        AS average_satisfaction,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Repeat_Contact = 'Yes'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS repeat_contact_rate
FROM customer_service;


-- ============================================================
-- 4. CASE VOLUME BY ISSUE
-- ============================================================

SELECT
    Issue_Type,
    COUNT(*) AS cases
FROM customer_service
GROUP BY Issue_Type
ORDER BY cases DESC;


-- ============================================================
-- 5. ISSUE PERFORMANCE
-- ============================================================

SELECT
    Issue_Type,
    COUNT(*) AS cases,
    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time,
    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction
FROM customer_service
GROUP BY Issue_Type
ORDER BY average_resolution_time DESC;


-- ============================================================
-- 6. CHANNEL PERFORMANCE
-- ============================================================

SELECT
    Channel,
    COUNT(*) AS cases,
    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time,
    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Repeat_Contact = 'Yes'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS repeat_contact_rate
FROM customer_service
GROUP BY Channel
ORDER BY cases DESC;


-- ============================================================
-- 7. PRODUCT PERFORMANCE
-- ============================================================

SELECT
    Product,
    COUNT(*) AS cases,
    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time,
    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction
FROM customer_service
GROUP BY Product
ORDER BY cases DESC;


-- ============================================================
-- 8. REPEAT CONTACT VS SATISFACTION
-- ============================================================

SELECT
    Repeat_Contact,
    COUNT(*) AS customers,
    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction,
    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time
FROM customer_service
GROUP BY Repeat_Contact;


-- ============================================================
-- 9. MONTHLY PERFORMANCE
-- ============================================================

SELECT
    DATE_TRUNC(
        'month',
        Date
    ) AS month,
    COUNT(*) AS cases,
    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time,
    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction
FROM customer_service
GROUP BY month
ORDER BY month;


-- ============================================================
-- 10. LOW SATISFACTION CASES
-- ============================================================

SELECT
    Customer_ID,
    Date,
    Product,
    Issue_Type,
    Channel,
    Resolution_Time,
    Satisfaction_Score,
    Repeat_Contact
FROM customer_service
WHERE Satisfaction_Score <= 2
ORDER BY Satisfaction_Score ASC,
         Resolution_Time DESC;


-- ============================================================
-- 11. LONG RESOLUTION CASES
-- ============================================================

SELECT
    Customer_ID,
    Issue_Type,
    Channel,
    Resolution_Time,
    Satisfaction_Score,
    Repeat_Contact
FROM customer_service
WHERE Resolution_Time > 60
ORDER BY Resolution_Time DESC;


-- ============================================================
-- 12. CHANNEL + ISSUE ANALYSIS
-- ============================================================

SELECT
    Channel,
    Issue_Type,
    COUNT(*) AS cases,
    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time,
    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction
FROM customer_service
GROUP BY
    Channel,
    Issue_Type
ORDER BY
    Channel,
    cases DESC;
