class SessionManager:
    """
    A utility class to manage user sessions.
    """
    def __init__(self):
        self.sessions = {}  # Map of user IDs to session IDs

    def add_session(self, user_id, sid):
        self.sessions[user_id] = sid

    def remove_session(self, sid):
        user_id = self.get_user_by_sid(sid)
        if user_id:
            del self.sessions[user_id]
            return user_id
        return None

    def get_user_by_sid(self, sid):
        for user_id, session_id in self.sessions.items():
            if session_id == sid:
                return user_id
        return None