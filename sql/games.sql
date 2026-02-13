----------------Competition Analysis Queries-------------------

-- 1. List all competitions with their category names
SELECT
    c.competition_id,
    c.competition_name,
    cat.category_name
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id;

-- 2. Count competitions per category
SELECT
    cat.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM categories cat
LEFT JOIN competitions c
    ON cat.category_id = c.category_id
GROUP BY cat.category_name;

-- 3. List competitions of type 'doubles'
SELECT
    competition_id,
    competition_name,
    type
FROM competitions
WHERE type = 'doubles';

-- 4. Competitions under a specific category
SELECT
    c.competition_id,
    c.competition_name,
    cat.category_name
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

-- 5. Parent and sub-competitions hierarchy
SELECT
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM competitions parent
JOIN competitions child
    ON parent.competition_id = child.parent_id;

-- 6. Competition type distribution by category
SELECT
    cat.category_name,
    c.type,
    COUNT(*) AS competition_count
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, competition_count DESC;

-- 7. Competitions with no parent
SELECT
    competition_id,
    competition_name
FROM competitions
WHERE parent_id IS NULL;

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

----------------Venue & Complex Analysis Queries-------------------

-- 8. Venues with their complex names
SELECT
    v.venue_id,
    v.venue_name,
    c.complex_name
FROM venues v
JOIN complexes c
    ON v.complex_id = c.complex_id;

-- 9. Count venues per complex
SELECT
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
LEFT JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY c.complex_name;

-- 10. Venues in a specific country
SELECT
    venue_id,
    venue_name,
    city_name,
    country_name
FROM venues
WHERE country_name = 'Chile';

-- 11. Venue timezones
SELECT
    venue_name,
    timezone
FROM venues;

-- 12. Complexes with more than one venue
SELECT
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;

-- 13. Venue count by country
SELECT
    country_name,
    COUNT(venue_id) AS total_venues
FROM venues
GROUP BY country_name
ORDER BY total_venues DESC;

-- 14. Venues for a specific complex
SELECT
    v.venue_id,
    v.venue_name,
    c.complex_name
FROM venues v
JOIN complexes c
    ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Nacional';

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

----------------Competitor Ranking Analysis Queries-------------------

-- 15. Competitors with rank and points
SELECT 
    c.name,
    cr.rank_position,
    cr.points
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
ORDER BY cr.rank_position;

-- 16. Top 5 ranked competitors
SELECT 
    c.name,
    cr.rank_position,
    cr.points
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE cr.rank_position <= 5
ORDER BY cr.rank_position;

-- 17. Competitors with no rank movement
SELECT 
    c.name,
    cr.rank_position,
    cr.movement
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE cr.movement = 0;

-- 18. Total points by country (e.g., Croatia)
SELECT 
    c.country,
    SUM(cr.points) AS total_points
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;

-- 19. Competitor count per country
SELECT 
    country,
    COUNT(*) AS total_competitors
FROM competitors
GROUP BY country
ORDER BY total_competitors DESC;

-- 20. Competitors with highest points
SELECT 
    c.name,
    cr.points
FROM competitors c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE cr.points = (
    SELECT MAX(points)
    FROM competitor_rankings
);
