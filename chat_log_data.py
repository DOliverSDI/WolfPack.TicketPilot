# FILE: chat_log_data.py

class ChatLogData:
    def __init__(self, date, ticket_id, initial_request, request_updates):
        self.sample_chat_data = {
            "date": date,
            "ticket_id": ticket_id,
            "initial_request": initial_request,
            "request_updates": request_updates
        }
