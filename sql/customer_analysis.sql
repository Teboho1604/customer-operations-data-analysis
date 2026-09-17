-- ============================================================
-- CUSTOMER OPERATIONS & DATA QUALITY ANALYSIS
-- Customer Operations Analysis
-- ============================================================


-- ============================================================
-- 1. TOTAL CUSTOMER SERVICE CASES
-- ============================================================

SELECT
    COUNT(*) AS total_cases
FROM customer_service;


-- ============================================================
-- 2. CASES BY ISSUE TYPE
-- ============================================================

SELECT
    Issue_Type,
    COUNT(*) AS total_cases
FROM customer_service
GROUP BY Issue_Type
ORDER BY total_cases DESC;


-- ============================================================
-- 3. AVERAGE RESOLUTION TIME BY ISSUE TYPE
-- ============================================================

SELECT
    Issue_Type,
    ROUND(AVG(Resolution_Time), 2) AS average_resolution_time
FROM customer_service
GROUP BY Issue_Type
ORDER BY average_resolution_time DESC;


-- ============================================================
-- 4. AVERAGE CUSTOMER SATISFACTION BY ISSUE TYPE
-- ============================================================

SELECT
    Issue_Type,
    ROUND(AVG(Satisfaction_Score), 2) AS average_satisfaction
FROM customer_service
GROUP BY Issue_Type
ORDER BY average_satisfaction ASC;


-- ============================================================
-- 5. CUSTOMER SERVICE CHANNEL PERFORMANCE
-- ============================================================

SELECT
    Channel,
    COUNT(*) AS total_cases,
    ROUND(AVG(Resolution_Time), 2) AS average_resolution_time,
    ROUND(AVG(Satisfaction_Score), 2) AS average_satisfaction
FROM customer_service
GROUP BY Channel
ORDER BY average_satisfaction ASC;


-- ============================================================
-- 6. REPEAT CONTACTS BY PRODUCT
-- ============================================================

SELECT
    Product,
    COUNT(*) AS repeat_contacts
FROM customer_service
WHERE Repeat_Contact = 'Yes'
GROUP BY Product
ORDER BY repeat_contacts DESC;


-- ============================================================
-- 7. REPEAT CONTACT RATE BY PRODUCT
-- ============================================================

SELECT
    Product,
    COUNT(*) AS total_cases,
    SUM(
        CASE
            WHEN Repeat_Contact = 'Yes' THEN 1
            ELSE 0
        END
    ) AS repeat_contacts,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Repeat_Contact = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS repeat_contact_rate
FROM customer_service
GROUP BY Product
ORDER BY repeat_contact_rate DESC;


-- ============================================================
-- 8. LOW SATISFACTION CASES
-- ============================================================

SELECT
    Customer_ID,
    Product,
    Issue_Type,
    Channel,
    Resolution_Time,
    Satisfaction_Score,
    Repeat_Contact
FROM customer_service
WHERE Satisfaction_Score <= 2
ORDER BY Satisfaction_Score ASC, Resolution_Time DESC;


-- ============================================================
-- 9. LONG RESOLUTION TIMES AND LOW SATISFACTION
-- ============================================================

SELECT
    Customer_ID,
    Product,
    Issue_Type,
    Resolution_Time,
    Satisfaction_Score,
    Repeat_Contact
FROM customer_service
WHERE Resolution_Time > 60
AND Satisfaction_Score <= 3
ORDER BY Resolution_Time DESC;


-- ============================================================
-- 10. RELATIONSHIP BETWEEN RESOLUTION TIME
--     AND CUSTOMER SATISFACTION
-- ============================================================

SELECT
    CASE
        WHEN Resolution_Time <= 30 THEN '0-30 minutes'
        WHEN Resolution_Time <= 60 THEN '31-60 minutes'
        ELSE '60+ minutes'
    END AS resolution_time_group,
    COUNT(*) AS total_cases,
    ROUND(AVG(Satisfaction_Score), 2) AS average_satisfaction
FROM customer_service
GROUP BY resolution_time_group
ORDER BY average_satisfaction ASC;


-- ============================================================
-- 11. PRODUCT PERFORMANCE
-- ============================================================

SELECT
    Product,
    COUNT(*) AS total_cases,
    ROUND(AVG(Resolution_Time), 2) AS average_resolution_time,
    ROUND(AVG(Satisfaction_Score), 2) AS average_satisfaction
FROM customer_service
GROUP BY Product
ORDER BY average_satisfaction ASC;


-- ============================================================
-- 12. IDENTIFY POTENTIAL AT-RISK CASES
-- ============================================================

SELECT
    Customer_ID,
    Product,
    Issue_Type,
    Channel,
    Resolution_Time,
    Satisfaction_Score,
    Repeat_Contact
FROM customer_service
WHERE Satisfaction_Score <= 2
   OR Repeat_Contact = 'Yes'
ORDER BY Satisfaction_Score ASC, Resolution_Time DESC;
