import json
import os

RAW_DIR = "data/raw"
PROCESSED_FILE = "data/processed/apache_issues.jsonl"

def extract_text(issue):
    fields = issue.get("fields", {})
    return {
        "project": fields.get("project", {}).get("key"),
        "issue_key": issue.get("key"),
        "title": fields.get("summary"),
        "description": fields.get("description"),
        "status": fields.get("status", {}).get("name"),
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
        "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
        "labels": fields.get("labels"),
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "comments": "\n".join(
            c.get("body", "") for c in (fields.get("comment", {}).get("comments", []))
        ),
        "task": "summarization"
    }

def transform_to_jsonl():
    with open(PROCESSED_FILE, "w", encoding="utf-8") as out_f:
        for raw_file in os.listdir(RAW_DIR):
            path = os.path.join(RAW_DIR, raw_file)
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    issue = json.loads(line)
                    transformed = extract_text(issue)
                    json.dump(transformed, out_f)
                    out_f.write("\n")
    print("✅ Transformation complete → data/processed/apache_issues.jsonl")

if __name__ == "__main__":
    transform_to_jsonl()
