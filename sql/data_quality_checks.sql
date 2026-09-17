-- ============================================================
-- CUSTOMER OPERATIONS & DATA QUALITY ANALYSIS
-- Data Quality Checks
-- ============================================================

-- 1. Check the total number of records
SELECT COUNT(*) AS total_records
FROM customer_service;


-- 2. Check for duplicate Customer IDs
SELECT
    Customer_ID,
    COUNT(*) AS record_count
FROM customer_service
GROUP BY Customer_ID
HAVING COUNT(*) > 1;


-- 3. Check for missing satisfaction scores
SELECT COUNT(*) AS missing_satisfaction_scores
FROM customer_service
WHERE Satisfaction_Score IS NULL;


-- 4. Check for missing resolution times
SELECT COUNT(*) AS missing_resolution_times
FROM customer_service
WHERE Resolution_Time IS NULL;


-- 5. Check the different issue-type values
-- This helps identify inconsistent categories such as
-- 'Technical' and 'technical'.
SELECT DISTINCT Issue_Type
FROM customer_service
ORDER BY Issue_Type;


-- 6. Check the different customer-service channels
SELECT DISTINCT Channel
FROM customer_service
ORDER BY Channel;


-- 7. Check satisfaction score range
SELECT
    MIN(Satisfaction_Score) AS minimum_score,
    MAX(Satisfaction_Score) AS maximum_score
FROM customer_service;


-- 8. Identify records with unusually long resolution times
SELECT *
FROM customer_service
WHERE Resolution_Time > 60
ORDER BY Resolution_Time DESC;
