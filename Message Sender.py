import win32gui
import win32api
import win32con
import win32clipboard as w
import time
import random

lang = {"ZH": "微信", "EN": "WeChat"}

def get_data():
    global plan_title, plan_message, plan_time
    try:
        f = open("./data.txt", encoding="utf-8")

        plan_title = lang[f.readline()[1:-2].strip()]
        # print(plan_title)

        plan_message = f.readline()[:-1].strip()
        plan_message = plan_message.replace("[t]", "36."+str(random.randint(3,9))+"°C")
        # print(plan_message)

        plan_time = int(f.readline()[:-1].strip())
        # print(plan_time)

        f.close()

    except Exception as err:
        print("Failed to read data file")
        print(err)

def get_time():
    req_time = time.localtime(time.time())
    curr_time = req_time.tm_hour * 100 + req_time.tm_min
    return curr_time 

def copy_text(text):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, text)
    w.CloseClipboard()

def paste_text():
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

def press_send(): 
    win32api.keybd_event(18, 0, 0, 0)  
    win32api.keybd_event(83, 0, 0, 0)
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)

def send_message(message):
    copy_text(message)
    # try:
    #     handle = win32gui.FindWindow(None, plan_title)
    #     win32gui.SetForegroundWindow(handle) 
    # except Exception as err:
    #     print("WindowError")
    #     print(err)

    paste_text()
    press_send()

def schedule(gap):
    while True:
        if get_time() == plan_time:
        # if True:
            send_message(plan_message)
            break
        print("Time checked. Current time:", get_time())
        time.sleep(gap)

def MAIN():
    get_data()
    schedule(60)
    # time.sleep(600)
    send_message(plan_message)

if __name__ == '__main__':
    MAIN()
