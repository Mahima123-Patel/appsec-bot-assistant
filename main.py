import json
import csv
from datetime import datetime
from utils.llm_handler import get_remediation_response
from utils.jira_handler import load_tickets, update_ticket_status, load_new_comments, merge_comments_into_tickets

# -------------------------------
# 1. Templates for common vulns
# -------------------------------
def get_bot_template(vuln_type):
    templates = {
        "XSS": "To fix XSS, ensure you're encoding output and using Content Security Policy.",
        "SQLi": "To remediate SQL injection, use parameterized queries and ORM tools.",
        "Secrets": "Avoid secrets in code; use environment variables or secrets managers."
    }
    return templates.get(vuln_type, "The AppSec team will provide further guidance.")

# -------------------------------
# 2. Logging each action
# -------------------------------
def log_action(ticket_id, comment_type, status=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [ticket_id, comment_type, status, timestamp]

    with open("logs/log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)

# -------------------------------
# 3. Handle a single ticket comment
# -------------------------------
def handle_comment(ticket, last_handled_timestamp=None):
    ticket_id = ticket["ticket_id"]
    vuln_type = ticket["vulnerability_type"]
    comments = ticket["comments"]
    latest_comment = comments[-1]
    latest_text = latest_comment["text"]
    latest_time = latest_comment["timestamp"]

    print(f"\n\U0001F39F️ Ticket: {ticket_id}")
    print(f"\U0001F4DD Latest Comment: {latest_text}")

    if last_handled_timestamp == latest_time:
        print("\u23ED\uFE0F Bot: No new comment to handle.")
        return last_handled_timestamp

    print("💬 Bot: Hi team, AppSec team is reviewing the comment and will get back shortly..")
    log_action(ticket_id, "Initial-response")
    
    if "Need help" in latest_text:
        print("\U0001F916 Bot: Generating response using Hugging Face model...")
        response = get_remediation_response(vuln_type, latest_text)
        print(f"\U0001F4AC LLM Response:\n{response}")
        log_action(ticket_id, "LLM-response")

    elif "fixed" in latest_text.lower():
        update_ticket_status(ticket, "In Testing")
        print("\u2705 Bot: Status updated to 'In Testing'.")
        log_action(ticket_id, "Fixed", "In Testing")

    else:
        print("\U0001F916 Bot: Posting default template...")
        template = get_bot_template(vuln_type)
        print(f"\U0001F4AC Template Response: {template}")
        log_action(ticket_id, "Template-response")

    print("\U0001F4CC Status:", ticket["status"])
    return latest_time

# -------------------------------
# 4. Simulated Polling Loop
# -------------------------------
def main():
    tickets = load_tickets()
    new_comments = load_new_comments()
    merge_comments_into_tickets(tickets, new_comments)

    ticket_states = {}

    print("\n\U0001F501 Simulating polling with comment updates...")

    for ticket in tickets:
        if ticket["risk"] in ["High", "Critical"]:
            last_seen = ticket_states.get(ticket["ticket_id"])
            new_seen = handle_comment(ticket, last_seen)
            ticket_states[ticket["ticket_id"]] = new_seen

    print("\n\u2705 Polling cycle complete.")

if __name__ == "__main__":
    main()
