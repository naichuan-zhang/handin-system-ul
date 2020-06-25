import os
import socket
import threading
import time

import const

host = const.HANDIN_HOST
port = const.HANDIN_PORT


def get_file_content(path, mode='r'):
    with open(path, mode=mode, encoding='utf-8') as f:
        content = f.read()
    return content


def Main():
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print("Server started ...")
    while True:
        c, addr = s.accept()
        print("client connected ip: <" + str(addr) + ">")
        t = threading.Thread(target=RetrCommand, args=("RetrCommand", c))
        t.start()


def RetrCommand(name, sock: socket.socket):
    data = sock.recv(1024)
    msg = data.decode()
    if msg == "File Request":
        time.sleep(.1)
        RetrFile(name, sock)
    elif msg == "Authentication":
        time.sleep(.1)
        authentication_of_student(name, sock)
    elif msg == "Check for attempts":
        time.sleep(.1)
        check_for_attempts(name, sock)
    elif msg == "What code is required":
        time.sleep(.1)
        code_requirements(name, sock)
    elif msg == "Sending a submission report":
        time.sleep(.1)
        submission_report(name, sock)
    elif msg == "Sending a code":
        time.sleep(.1)
        recvCode(name, sock)
    elif msg == "Checking Assignment Week":
        time.sleep(.1)
        checkIfAssignmentWeek(name, sock)
    elif msg == "Check module exists":
        time.sleep(.1)
        checkIfModuleExists(name, sock)
    elif msg == "What is semester start date":
        time.sleep(.1)
        getSemStartDate(name, sock)
    elif msg == "Get most recent attempt":
        time.sleep(.1)
        getRecentAttempt(name, sock)
    else:
        print(f"Unknown Message: {msg}")


def RetrFile(name, sock):
    pass
    RetrCommand(name, sock)


def authentication_of_student(name, sock):
    """check if student_id exist in the class list"""
    sock.sendall(b"OK")
    # get current module code
    module_code = sock.recv(1024).decode().lower()
    # get student id
    student_id = sock.recv(1024).decode()
    class_list_file_path = const.get_class_list_file_path(module_code=module_code)
    if os.path.exists(class_list_file_path):
        with open(class_list_file_path, 'r') as f:
            for line in f:
                if student_id in line:
                    sock.sendall(b'Authenticated')
                    print(student_id + " has been authenticated ...")
    RetrCommand(name, sock)


def check_for_attempts(name, sock):
    pass
    RetrCommand(name, sock)


def code_requirements(name, sock):
    pass
    RetrCommand(name, sock)


def submission_report(name, sock):
    pass
    RetrCommand(name, sock)


def recvCode(name, sock):
    pass
    RetrCommand(name, sock)


def checkIfModuleExists(name, sock):
    """check if the moduleCode exists"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/"
    if os.path.exists(path):
        modules = [name.lower() for name in os.listdir(path)]
        if module_code.lower() in modules:
            sock.sendall(b"True")
        else:
            sock.sendall(b"False")
    else:
        sock.sendall(b"False")
    RetrCommand(name, sock)


def checkIfAssignmentWeek(name, sock):
    """check if an assignment week"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/" + module_code + "/"
    if os.path.exists(path):
        weeks = [name for name in os.listdir(path)]
        if week_number in weeks:
            sock.sendall(b"True")
        else:
            sock.sendall(b"False")
    else:
        sock.sendall(b"False")
    RetrCommand(name, sock)


def getSemStartDate(name, sock):
    pass
    RetrCommand(name, sock)


def getRecentAttempt(name, sock):
    pass
    RetrCommand(name, sock)


if __name__ == '__main__':
    Main()
