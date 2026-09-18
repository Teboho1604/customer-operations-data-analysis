-- ============================================================
-- CUSTOMER OPERATIONS & DATA QUALITY ANALYSIS
-- Extended Data Quality + Business Analysis
-- ============================================================


-- ============================================================
-- 9. Check for missing values across all important columns
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(Customer_ID) AS customer_ids_present,
    COUNT(Date) AS dates_present,
    COUNT(Product) AS products_present,
    COUNT(Issue_Type) AS issue_types_present,
    COUNT(Channel) AS channels_present,
    COUNT(Resolution_Time) AS resolution_times_present,
    COUNT(Satisfaction_Score) AS satisfaction_scores_present,
    COUNT(Repeat_Contact) AS repeat_contact_present
FROM customer_service;


-- ============================================================
-- 10. Check for invalid satisfaction scores
-- Valid range: 1 to 5
-- ============================================================

SELECT *
FROM customer_service
WHERE Satisfaction_Score < 1
   OR Satisfaction_Score > 5;


-- ============================================================
-- 11. Check for invalid resolution times
-- ============================================================

SELECT *
FROM customer_service
WHERE Resolution_Time <= 0
   OR Resolution_Time > 480
ORDER BY Resolution_Time DESC;


-- ============================================================
-- 12. Check for inconsistent Product values
-- ============================================================

SELECT DISTINCT Product
FROM customer_service
ORDER BY Product;


-- ============================================================
-- 13. Check Repeat_Contact values
-- ============================================================

SELECT DISTINCT Repeat_Contact
FROM customer_service
ORDER BY Repeat_Contact;


-- ============================================================
-- 14. Overall customer-service KPIs
-- ============================================================

SELECT
    COUNT(*) AS total_cases,

    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time,

    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction,

    ROUND(
        100.0 *
        SUM(
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
-- 15. Case volume by Issue Type
-- ============================================================

SELECT
    Issue_Type,
    COUNT(*) AS total_cases
FROM customer_service
GROUP BY Issue_Type
ORDER BY total_cases DESC;


-- ============================================================
-- 16. Issue Type performance
-- ============================================================

SELECT
    Issue_Type,

    COUNT(*) AS total_cases,

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
-- 17. Channel performance
-- ============================================================

SELECT
    Channel,

    COUNT(*) AS total_cases,

    ROUND(
        AVG(Resolution_Time),
        2
    ) AS average_resolution_time,

    ROUND(
        AVG(Satisfaction_Score),
        2
    ) AS average_satisfaction,

    ROUND(
        100.0 *
        SUM(
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

ORDER BY total_cases DESC;


-- ============================================================
-- 18. Product performance
-- ============================================================

SELECT
    Product,

    COUNT(*) AS total_cases,

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

ORDER BY total_cases DESC;


-- ============================================================
-- 19. Repeat Contact vs Customer Satisfaction
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
-- 20. Low-satisfaction customers
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

ORDER BY
    Satisfaction_Score ASC,
    Resolution_Time DESC;


-- ============================================================
-- 21. Long-resolution cases
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
-- 22. Issue Type + Channel analysis
-- ============================================================

SELECT
    Issue_Type,
    Channel,

    COUNT(*) AS total_cases,

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
    Issue_Type,
    Channel

ORDER BY
    total_cases DESC;


-- ============================================================
-- 23. Monthly performance
-- ============================================================

SELECT
    EXTRACT(
        YEAR FROM Date
    ) AS year,

    EXTRACT(
        MONTH FROM Date
    ) AS month,

    COUNT(*) AS total_cases,

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
    year,
    month

ORDER BY
    year,
    month;
