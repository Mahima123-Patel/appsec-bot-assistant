import json
from utils.llm_handler import get_remediation_response

# Load mock tickets
with open("data/tickets.json", "r") as file:
    tickets = json.load(file)

# Process each ticket
for ticket in tickets:
    ticket_id = ticket["ticket_id"]
    vuln_type = ticket["vulnerability_type"]
    status = ticket["status"]
    comments = ticket["comments"]

    latest_comment = comments[-1]["text"]
    print(f"\n🎟️ Ticket: {ticket_id}")
    print(f"📝 Latest Comment: {latest_comment}")

    # Simple logic based on comment
    if "Need help" in latest_comment:
        print("🤖 Bot: Sending request to Hugging Face model...")
        response = get_remediation_response(vuln_type, latest_comment)
        print(f"💬 HF Response:\n{response}")
    
    elif "fixed" in latest_comment.lower():
        ticket["status"] = "In Testing"
        print("✅ Bot: Status updated to 'In Testing'.")

    else:
        print("🤖 Bot: No action required.")

print("\n✅ Done processing all tickets.")




# import json
# from utils.llm_handler import get_remediation_response

# # Load mock tickets
# with open("data/tickets.json", "r") as file:
#     tickets = json.load(file)

# # Process each ticket
# for ticket in tickets:
#     ticket_id = ticket["ticket_id"]
#     vuln_type = ticket["vulnerability_type"]
#     status = ticket["status"]
#     comments = ticket["comments"]

#     latest_comment = comments[-1]["text"]
#     print(f"\n🎟️ Ticket: {ticket_id}")
#     print(f"📝 Latest Comment: {latest_comment}")

#     # Simple logic based on comment
#     if "Need help" in latest_comment:
#         print("🤖 Bot: Sending request to LLM...")
#         response = get_remediation_response(vuln_type, latest_comment)
#         print(f"💬 LLM Response:\n{response}")
    
#     elif "fixed" in latest_comment.lower():
#         ticket["status"] = "In Testing"
#         print("✅ Bot: Status updated to 'In Testing'.")

#     else:
#         print("🤖 Bot: No action required.")

# print("\n✅ Done processing all tickets.")
