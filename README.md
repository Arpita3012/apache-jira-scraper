This Apache Jira Scraper and Transformer project extracts, processes and structures data from three of the Apache's Jira Public projects.
It automates the collection of issues data for example metadata,comments , descriptions as well as handles real-world data inconsistencies. 
It transforms them into a clean JSONL Corpus suitable for LLMS Training or the data analytics.

Setup Instructions and Environment Configuration

Open in Google Colab
Clone the repository and open it in Colab:

!git clone https://github.com/Arpita3012/apache-jira-scraper.git
%cd apache-jira-scraper


Install Dependencies

!pip install requests pandas numpy tqdm

Used the Requirements Library (Python)

Run the Code
Execute the notebook cells in order to scrape, transform, and save the data.
The cleaned JSONL file will be generated in the data/ folder.

Architecture Overview and Design Reasoning
Project Structure:
    apache-jira-scraper/
    │
    ├── scraper.py
    ├── transform.py
    ├── utils.py
    ├── apache_scraper.ipynb
    │
    ├── data/
    │   ├── raw/
    │   │   ├── ACCUMULO.json
    │   │   ├── ACE.json
    │   │   └── ARTEMIS.json
    │   └── processed/
    │       └── apache_issues.jsonl
    │
    └── README.md
    
 Scraper Module: Manages data collection, pagination, retries, and API calls.

 Transformer Module: Normalises timestamps, handles missing data, cleans text, and converts to JSONL.

 Fault Tolerance: Made to continue from the most recent successful fetch in the event that it is interrupted.

 Scalability: Simple to integrate with databases or expand to new Jira projects.


EDGE CASES HANDLED ARE:
1. Null or missing values:
   Some issues in the project are handeled without a reporter, assignee or description.
   The defaults are generally get() and None.
   Example:
   { "fields": { "summary": "Bug found in build process", "description": null, "assignee": null }}

2. Truncated or Empty API Responses:
     Sometimes rate limits and some pagination problems/difficulties cause Jira API'S to give empty result sets.
     Therefore, before writing to a file , scraper reports any records that are maybe skipped and then verifies the length of the answer too.

3. Disruptions to the Network:
   The current checkpoint, or last successfully scraped index, is saved in checkpoint in the event that the connection stops during the scrape.
  JSONenables data loss-free safe restart.

4. Duplicate Problems:
 Jira pagination peculiarities may cause some problems to show up in overlapping pages.
 Unique issue key (issue['key'])-based deduplication.

5. Characters That Are Not UTF-8:
 Emojis and non-ASCII symbols may be present in Jira text fields (such as comments).
 To avoid decoding issues, encoding="utf-8" is used when reading and writing all files.

6. Complex or Nested Comments:
 Comments may have markdown-like content or nested bodies.
 They are flattened by the transformer into a single block of text with newlines between each line.

7. JSON Lines That Are Invalid:
 Sometimes, partially written or distorted JSON objects can be found in raw files.
 To safely avoid invalid entries, each line is parsed inside a try-except block (a suggested improvement).

8. Limiting API Rates:
 Jira might limit the number of API calls per minute.
 To adhere to rate constraints, the scraper incorporates an exponential backoff and a tiny delay.

9. Large Files or Overflowing Data:
   Some projects or files having thousands of issues which maybe time consuming to solve.
   So, the transfomer processes the data line by line reducing the chances of missing some issues.

10. Missing Project Metadata:
  Some older projects in Apache JIRA might lack metadata like project key or category.
  Such issues are skipped or tagged as "Unknown" to maintain consistency.

OPTIMIZATION:
  1. Batch Requests: It reduces the API Latency as well as keeping in check for the late limits.
  2. Incremental Updates: It only fetches new or the updated ones when the code is re runed.
  3. Caching: It avoids the API calls to not to be redundant.
  4. DataFrame Transformation

Future Improvements:
  1. Integrating the project with some database like MySQL for making it more scalable.
  2. Visualization can also be incorporated using PowerBI/Tabeleu.
  3. Some machine learning models can be added for some high-risk or classification type projects.
  4. Authentication
  5. Cloud Deployment
