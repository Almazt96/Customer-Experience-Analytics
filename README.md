# Fintech Review Analytics

An automated pipeline designed to harvest, clean, and analyze user sentiment from retail banking and fintech applications found on the Google Play Store.

## Data Collection & Preprocessing Methodology

### 1. Web Scraping Strategy
Data extraction is handled programmatically via the `google-play-scraper` library. The pipeline directly hits the Google Play Store API endpoints dynamically, targets English-language variants, and filters for recent engagement.

* **Target Apps:** Chime (`com.chimebanking`), Revolut (`com.revolut.revolut`), Monzo (`co.uk.monzo`).
* **Target Volume:** Minimum of 400+ reviews scraped per application to build a baseline collection of 1,200+ global entries.
* **Fields Captured:** Raw review text, user rating score (1–5), timestamp, application source identity, and origin tracker (`Google Play`).

### 2. Cleaning and Transformation Pipeline
Raw payloads pass through a validation processing engine:
* **De-duplication:** Drops duplicate responses utilizing unique transaction string IDs (`reviewId`).
* **Null Pruning:** Strict drops enforced against records missing text strings or categorical integer ratings.
* **Date Normalization:** Dates are parsed and standardized into strict ISO `YYYY-MM-DD` string values.

### 3. Limitations Encountered
* **App Store Pagination Boundaries:** The Google Play Store caps depth limits on history pulls. Very old reviews may not be dynamically accessible without expanding regional localization parameters.
* **Language Nuances:** Limiting requests exclusively to English (`lang='en'`)

## Project Context
Brief overview of what this project achieves and why it is being conducted.

## Data Collection & Scraping Methodology
* **Target Entities:** [CBE], [BOA], and [Dashen].
* **Exact Target Date Range:** From `YYYY-MM-DD` to `YYYY-MM-DD`.
* **Data Fields Extracted:** `review_id`, `review_date`, `rating`, `review_text`, etc.

### Scraping Limitations & Constraints
* **Pagination:** Limited to the first X pages due to site protection/performance.
* **Language:** Restricted to [English/Amharic/etc.] reviews.
* **API/Anti-Scraping:** Details on dynamic loading handling (e.g., Selenium/Playwright workarounds used or rate-limiting delays applied).

## Generated Artifacts
* **Preprocessed Dataset:** Located at `data/processed/`. Dates normalized to `YYYY-MM-DD`.
* **Sentiment Output Model:** Contains fields `sentiment_label` and `sentiment_score` persisted to [CSV/Database].

<!-- Data Scope & Context
Target Entities: This project analyzes data from the following Ethiopian banks:

[Commercial Bank of Ethiopia (CBE)]

[Abysinia Bank]

[Dashen Bank]

Date Range: The dataset covers observations and transactions spanning from [Start Date, e.g., January 1, 2025] to [End Date, e.g., December 31, 2025]. -->