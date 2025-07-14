import json
import csv
import time
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
def handle_comments(ticket, last_handled_timestamp=None):
    """
    Process every ticket comment newer than last_handled_timestamp,
    in chronological order.
    Returns the timestamp of the newest comment handled.
    """
    ticket_id = ticket["ticket_id"]
    vuln_type = ticket["vulnerability_type"]
    comments = sorted(ticket["comments"], key=lambda c: c["timestamp"])
    newest_time = last_handled_timestamp

    for comment in comments:
        ts = comment["timestamp"]
        if last_handled_timestamp is not None and ts <= last_handled_timestamp:
            continue  # already handled

        text = comment["text"]
        time.sleep(1)
        print(f"\n🎟️ Ticket: {ticket_id}")
        print(f"📝 Comment ({ts}): {text}")
        time.sleep(1)

        # Initial “we’re looking” response
        print("💬 Bot: Hi team, AppSec team is reviewing the comment and will get back shortly..")
        log_action(ticket_id, "Initial-response")
        time.sleep(1)

        # Decide how to respond
        if "need help" in text.lower():
            print("🤖 Bot: Generating remediation via LLM…")
            time.sleep(2)
            resp = get_remediation_response(vuln_type, text)
            print(f"💬 LLM Response:\n{resp}")
            log_action(ticket_id, "LLM-response")

        elif any(kw in text.lower() for kw in ["fixed", "resolved", "done", "closed"]):
            time.sleep(1)
            update_ticket_status(ticket, "In Testing")
            print("✅ Bot: Status updated to 'In Testing'.")
            log_action(ticket_id, "Fixed", "In Testing")

        else:
            print("🤖 Bot: Posting default template…")
            tpl = get_bot_template(vuln_type)
            print(f"💬 Template Response: {tpl}")
            log_action(ticket_id, "Template-response")

        print(f"📌 New Status: {ticket['status']}")
        newest_time = ts
        time.sleep(1)

    return newest_time

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
            new_seen = handle_comments(ticket, last_seen)
            ticket_states[ticket["ticket_id"]] = new_seen

    print("\n\u2705 Polling cycle complete.")

if __name__ == "__main__":
    main()
