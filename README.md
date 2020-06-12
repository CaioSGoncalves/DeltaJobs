# DeltaJobs
Scraping Data Engineering jobs from LinkedIn and storing in Delta Lake using Spark.

Unified Stream and batch jobs.

JobScraper Stream -> Spark -> Delta Lake

Delta:
- Bronze (Job)  -> Silver (Job + Terms) -> Gold (AggByDate, AggByTerms and AggByCountry)
