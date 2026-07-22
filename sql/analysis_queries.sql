-- 1. Which job categories have the most postings?
SELECT c.category_name, COUNT(*) AS job_count
FROM jobs j
JOIN categories c ON j.category_id = c.category_id
GROUP BY c.category_name
ORDER BY job_count DESC
LIMIT 10;

-- 2. Which postal codes (districts) have the most entry-level job postings?
SELECT l.plz, l.ort, COUNT(*) AS job_count
FROM jobs j
JOIN locations l ON j.location_id = l.location_id
WHERE l.plz != ''
GROUP BY l.plz, l.ort
ORDER BY job_count DESC
LIMIT 10;

-- 3. What share of jobs are full-time vs part-time?
SELECT vollzeit, COUNT(*) AS job_count
FROM jobs
GROUP BY vollzeit;

-- 4. Which employers post the most jobs (biggest hirers)?
SELECT firma, COUNT(*) AS job_count
FROM jobs
GROUP BY firma
ORDER BY job_count DESC
LIMIT 10;

-- 5. Average HOURLY pay by category (filtered to hourly-wage postings only)
SELECT c.category_name, ROUND(AVG(j.festgehalt), 2) AS avg_hourly_pay, COUNT(*) AS job_count
FROM jobs j
JOIN categories c ON j.category_id = c.category_id
WHERE j.festgehalt IS NOT NULL
  AND j.verguetungsangabe = 'STUNDENLOHN'
GROUP BY c.category_name
HAVING COUNT(*) > 5
ORDER BY avg_hourly_pay DESC;

-- 6. How many jobs are open to career changers (Quereinstieg)?
SELECT quereinstieg_geeignet, COUNT(*) AS job_count
FROM jobs
GROUP BY quereinstieg_geeignet;

-- 7. Posting trend over time - how many jobs were first published per month?
SELECT DATE_TRUNC('month', veroeffentlicht_am) AS month, COUNT(*) AS job_count
FROM jobs
WHERE veroeffentlicht_am IS NOT NULL
GROUP BY month
ORDER BY month;

-- 8. Widest HOURLY pay range by category (filtered to hourly-wage postings only)
SELECT c.category_name,
       MIN(j.gehaltsspanne_von) AS min_pay,
       MAX(j.gehaltsspanne_bis) AS max_pay,
       COUNT(*) AS job_count
FROM jobs j
JOIN categories c ON j.category_id = c.category_id
WHERE j.gehaltsspanne_von IS NOT NULL
  AND j.verguetungsangabe = 'STUNDENLOHN'
GROUP BY c.category_name
HAVING COUNT(*) > 3
ORDER BY (MAX(j.gehaltsspanne_bis) - MIN(j.gehaltsspanne_von)) DESC
LIMIT 10;

-- 9. Average ANNUAL salary by category (separate from hourly)
SELECT c.category_name, ROUND(AVG(j.festgehalt), 2) AS avg_annual_salary, COUNT(*) AS job_count
FROM jobs j
JOIN categories c ON j.category_id = c.category_id
WHERE j.festgehalt IS NOT NULL
  AND j.verguetungsangabe = 'JAHRESGEHALT'
GROUP BY c.category_name
ORDER BY avg_annual_salary DESC;
