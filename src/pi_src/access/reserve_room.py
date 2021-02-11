# import sys
# sys.path.append('../')

# from line import line_func

import notification
class reserve:
    def __init__(self):
        self.notify = notification.notify()

    def line_push_pre(self):
        self.notify.get_user_info(True)
        self.notify.resv_info_create()
        self.notify.line.line_push_pre(self.notify.resv_info)


if __name__ == "__main__":
    reserve = reserve()
    reserve.line_push_pre()