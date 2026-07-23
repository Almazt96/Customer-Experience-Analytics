-- database/schema.sql

-- Enable UUID extension if needed in the future
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------
-- 1. Banks Table (Dimension / Parent Entity)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for exact bank name lookups
CREATE INDEX IF NOT EXISTS idx_banks_bank_name ON banks(bank_name);


-- -----------------------------------------------------------------------------
-- 2. Reviews Table (Fact / Child Entity)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT NOT NULL,
    user_name VARCHAR(255),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    cleaned_text TEXT,
    sentiment_label VARCHAR(50),
    sentiment_score NUMERIC(5, 4),
    review_date TIMESTAMP WITH TIME ZONE,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraint with Cascading Delete
    CONSTRAINT fk_reviews_bank
        FOREIGN KEY (bank_id) 
        REFERENCES banks(bank_id) 
        ON DELETE CASCADE
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);