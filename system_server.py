import os
import socket
import threading
import time
from datetime import datetime

import yaml

import const

host = const.HANDIN_HOST
port = const.HANDIN_PORT


def get_file_content(path, mode='r'):
    with open(path, mode=mode, encoding='utf-8') as f:
        content = f.read()
    return content


def get_total_attempts(module_code, week_number) -> int:
    # read /**weekNum**/params.yaml file to get totalAttempts value
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/params.yaml"
    with open(path, 'r') as stream:
        data: dict = yaml.safe_load(stream)
    return data.get("totalAttempts")


def RetrCommand(name, sock: socket.socket):
    msg = sock.recv(1024).decode()
    print("Received command \"%s\"" % msg)
    if msg == "File Request":
        time.sleep(.1)
        RetrFile(name, sock)
    elif msg == "Authentication":
        time.sleep(.1)
        authentication_of_student(name, sock)
    elif msg == "Check attempts left":
        time.sleep(.1)
        checkAttemptsLeft(name, sock)
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
    elif msg == "Create vars file":
        time.sleep(.1)
        createVarsFile(name, sock)
    elif msg == "Init vars file":
        time.sleep(.1)
        initVarsFile(name, sock)
    elif msg == "Check late penalty":
        time.sleep(.1)
        checkLatePenalty(name, sock)
    else:
        print(f"Unknown Message: {msg}")


def RetrFile(name, sock):
    pass
    RetrCommand(name, sock)


def authentication_of_student(name, sock):
    """check if student_id exist in the class list"""
    sock.sendall(b"OK")
    # get current module code
    module_code = sock.recv(1024).decode()
    # get student id
    student_id = sock.recv(1024).decode()
    class_list_file_path = const.get_class_list_file_path(module_code=module_code.lower())
    if os.path.exists(class_list_file_path):
        with open(class_list_file_path, 'r') as f:
            for line in f:
                if student_id in line:
                    sock.sendall(b"True")
                    print(student_id + " has been authenticated ...")
                    RetrCommand(name, sock)
                    return
    sock.sendall(b"False")
    RetrCommand(name, sock)


def checkAttemptsLeft(name, sock):
    """check number of attempts left"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    student_id = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    # read vars.yaml file to get attemptsLeft value
    path = const.DIR_ROOT + "/module/" + module_code + "/data/" \
                + student_id + "/" + week_number + "/"
    filename = path + "vars.yaml"
    with open(filename, 'r') as stream:
        data: dict = yaml.safe_load(stream)
    if data.get("attemptsLeft"):
        sock.sendall(str(data.get("attemptsLeft")).encode('utf-8'))
    else:
        sock.sendall(b"False")
        print("ERROR: attemptsLeft doesn't exist!!!")
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


def createVarsFile(name, sock):
    """Create vars file for a specific student"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    student_id = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/" + module_code + "/data/" \
                + student_id + "/" + week_number + "/"
    filename = path + "vars.yaml"
    if not os.path.exists(filename):
        with open(filename, 'w'):
            pass
        sock.sendall(b"Success")
        RetrCommand(name, sock)
        return
    sock.sendall(b"Failed")
    RetrCommand(name, sock)


def initVarsFile(name, sock):
    """init vars.yaml file"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    student_id = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/" + module_code + "/data/" \
                + student_id + "/" + week_number + "/"
    filename = path + "vars.yaml"
    data = {
        "attemptsLeft": get_total_attempts(module_code, week_number),
    }
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    RetrCommand(name, sock)


def checkLatePenalty(name, sock):
    """Get late penalty"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()

    penalty_per_day: str = getPenaltyPerDay(module_code, week_number)
    if penalty_per_day == "False":
        sock.sendall(b"ERROR: penaltyPerDay doesn't exist!!!")

    start_day: str = getStartDay(module_code, week_number)
    if start_day == "False":
        sock.sendall(b"ERROR: startDay doesn't exist!!!")

    end_day: str = getEndDay(module_code, week_number)
    if end_day == "False":
        sock.sendall(b"ERROR: endDay doesn't exist!!!")

    cutoff_day: str = getCutoffDay(module_code, week_number)
    if cutoff_day == "False":
        sock.sendall(b"ERROR: cutoffDay doesn't exist!!!")

    dt_format = "%d/%m/%Y %H:%M"
    start_day: datetime = datetime.strptime(start_day, dt_format)
    end_day: datetime = datetime.strptime(end_day, dt_format)
    cutoff_day: datetime = datetime.strptime(cutoff_day, dt_format)
    now: datetime = datetime.now()
    if now < start_day:
        sock.sendall(b"Submission to early!")
    elif now > cutoff_day:
        sock.sendall(b"You have missed the cutoff day, you are not allow to submit now!")
    elif start_day < now < end_day:
        # no late penalty applied
        sock.sendall(b"0")
    elif end_day < now < cutoff_day:
        hours_delta = (now - end_day).seconds // 3600
        sock.sendall(str((hours_delta // 24 + 1) * penalty_per_day).encode('utf-8'))
    RetrCommand(name, sock)


def getPenaltyPerDay(module_code, week_number):
    """get penalty per day for a module"""
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("penaltyPerDay"):
        return str(data.get("penaltyPerDay"))
    else:
        print("ERROR: penaltyPerDay doesn't exist!!!")
        return "False"


def getStartDay(module_code, week_number):
    """get start day for a module"""
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("startDay"):
        return str(data.get("startDay"))
    else:
        print("ERROR: startDay doesn't exist!!!")
        return "False"


def getEndDay(module_code, week_number):
    """get end day for a module"""
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("endDay"):
        return str(data.get("endDay"))
    else:
        print("ERROR: endDay doesn't exist!!!")
        return "False"


def getCutoffDay(module_code, week_number):
    """get cutoff day for a module"""
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("cutoffDay"):
        return str(data.get("cutoffDay"))
    else:
        print("ERROR: cutoffDay doesn't exist!!!")
        return "False"


if __name__ == '__main__':
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print("Server started ...")
    while True:
        c, addr = s.accept()
        print("client connected ip: <" + str(addr) + ">")
        t = threading.Thread(target=RetrCommand, args=("RetrCommand", c))
        t.start()
