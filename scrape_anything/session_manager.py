import uuid
import datetime


class SessionManager:
    def __init__(self):
        self.client_to_server_sessions = {}
        self.server_to_client_sessions = {}
        # self.close_sessions = {}

    def create_session(self, client_session_id):
        server_session_id = str(uuid.uuid4())
        self.client_to_server_sessions[client_session_id] = server_session_id
        self.server_to_client_sessions[server_session_id] = client_session_id
        return server_session_id

    def get_server_session(self, client_session_id):
        if client_session_id in self.client_to_server_sessions:
            return self.client_to_server_sessions[client_session_id]
        else:
            return self.create_session(client_session_id)

    def mark_session_as_closed(self, server_session_id):
        if server_session_id in self.server_to_client_sessions:
            client_session_id = self.server_to_client_sessions.pop(server_session_id)
            assert (
                self.client_to_server_sessions.pop(client_session_id)
                == server_session_id
            )

            # self.close_sessions[f"{client_session_id}{datetime.datetime.now().strftime()}"] = server_session_id
        else:
            raise Exception(f"can't close session {client_session_id}, doesn't exists.")
