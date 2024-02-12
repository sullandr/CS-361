class Users:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password

class Entries:
    def __init__(self, date, time, table_type, racks, ballcount, practice_type):
        self.date = date
        self.time = time
        self.table_type = table_type
        self.racks = racks
        self.ballcount = ballcount
        self.practice_type = practice_type