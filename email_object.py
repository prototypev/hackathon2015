


class Email:
    def __init__(self, fromEmail, toEmail, cc, date, subject):
        self.fromEmail = fromEmail
        self.toEmail = toEmail
        self.cc = cc
        self.date = date
        self.subject = subject

    def __repr__(self):
        return self.fromEmail + ',' + self.toEmail + ',' + self.cc + ',' + self.date + ',' + self.subject
