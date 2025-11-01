import requests
import json
import time
from tqdm import tqdm
from utils import save_checkpoint, load_checkpoint, log_message

BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"
PROJECTS = ["ACCUMULO", "ACE", "ARTEMIS"]  # Updated project list ✅
PAGE_SIZE = 500
MAX_RETRIES = 3

def fetch_issues(project, start_at):
    params = {
        "jql": f"project={project}",
        "maxResults": PAGE_SIZE,
        "startAt": start_at
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(BASE_URL, params=params, timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                log_message("Rate limit hit. Sleeping 30s...")
                time.sleep(30)
            elif 500 <= response.status_code < 600:
                log_message(f"Server error {response.status_code}. Retry {attempt+1}/{MAX_RETRIES}")
                time.sleep(5)
            else:
                log_message(f"Unexpected status {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            log_message(f"Request failed: {e}")
            time.sleep(5)
    return None


def scrape_project(project):
    checkpoint = load_checkpoint()
    start_at = checkpoint.get(project, 0)
    all_issues = []

    while True:
        data = fetch_issues(project, start_at)
        if not data or "issues" not in data:
            break

        issues = data["issues"]
        if not issues:
            break

        for issue in issues:
            all_issues.append(issue)

        with open(f"data/raw/{project}.json", "a", encoding="utf-8") as f:
            for issue in issues:
                json.dump(issue, f)
                f.write("\n")

        start_at += len(issues)
        save_checkpoint(project, start_at)
        log_message(f"{project}: fetched {len(issues)} issues, total so far {start_at}")

        if len(issues) < PAGE_SIZE:
            break

        time.sleep(1)

    log_message(f"{project}: completed scraping {start_at} issues.")
    return all_issues


if __name__ == "__main__":
    for project in PROJECTS:
        log_message(f"Starting scraping for {project}")
        scrape_project(project)
        log_message(f"Finished scraping {project}\n")
