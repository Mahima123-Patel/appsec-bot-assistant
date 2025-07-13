import json

def load_tickets(path="data/tickets.json"):
    with open(path, "r") as file:
        return json.load(file)

def load_new_comments(path="data/comments.json"):
    with open(path, "r") as file:
        return json.load(file)

def merge_comments_into_tickets(tickets, new_comments):
    for comment in new_comments:
        for ticket in tickets:
            if ticket["ticket_id"] == comment["ticket_id"]:
                ticket["comments"].append({
                    "author": comment["author"],
                    "text": comment["text"],
                    "timestamp": comment["timestamp"]
                })

def update_ticket_status(ticket, new_status):
    ticket["status"] = new_status
