-- ===============================
-- Categories Table
-- ===============================
CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- ===============================
-- Competitions Table
-- ===============================
CREATE TABLE IF NOT EXISTS competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    category_id VARCHAR(50),

    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

-- ===============================
-- Complexes Table
-- ===============================
CREATE TABLE IF NOT EXISTS complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

-- ===============================
-- Venues Table
-- ===============================
CREATE TABLE IF NOT EXISTS venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),

    CONSTRAINT fk_complex
        FOREIGN KEY (complex_id)
        REFERENCES complexes(complex_id)
);
-- ===============================
-- Competitors Table
-- ===============================
CREATE TABLE IF NOT EXISTS competitors (
    competitor_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL
);

-- ===============================
-- Competitor Rankings Table
-- ===============================
CREATE TABLE IF NOT EXISTS competitor_rankings (
    rank_id INT PRIMARY KEY,
    rank_position INT NOT NULL,   -- renamed from `rank` (reserved keyword)
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id INT NOT NULL,

    CONSTRAINT fk_competitor
        FOREIGN KEY (competitor_id)
        REFERENCES competitors(competitor_id)
);
