# DeltaJobs
Scraping Data Engineering jobs from LinkedIn and storing in Delta Lake using Spark.

Unified Stream and batch jobs.

JobScraper Stream -> Spark -> Delta Lake

Delta:
- Bronze (Job)  -> Silver (Job + Terms) -> Gold (AggByDate, AggByTerms and AggByCountry)
- Bronze: bronze_job
- Silver: silver_job and silver_term
- Gold: gold_jobs_agg_by_date, gold_jobs_agg_by_term, gold_jobs_agg_by_country
