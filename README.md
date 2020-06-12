# DeltaJobs
Scraping Data Engineering jobs from LinkedIn and storing in Delta Lake using Spark.

Unified Stream and batch jobs.

Delta:
- Bronze (Job)  -> Silver (Job + Terms) -> Gold (Agg by Date and Agg by Terms)


JobScraper Stream -> Spark -> Delta Lake
