from pi_src.notification import notify

class reserve:
    def __init__(self):
        self.notify = notify()

    def line_push_pre(self):
        self.line.line_push_pre(self.notify.form_info)


if __name__ == "__main__":
    reserve = reserve()
    reserve.line_push_pre()