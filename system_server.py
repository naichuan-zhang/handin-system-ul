import os
import socket
import threading
import time
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
    elif msg == "Get penalty per day":
        time.sleep(.1)
        getPenaltyPerDay(name, sock)
    elif msg == "Get start day":
        time.sleep(.1)
        getStartDay(name, sock)
    elif msg == "Get end day":
        time.sleep(.1)
        getEndDay(name, sock)
    elif msg == "Get cutoff day":
        time.sleep(.1)
        getCutoffDay(name, sock)
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


def getPenaltyPerDay(name, sock):
    """get penalty per day for a module"""
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("penaltyPerDay"):
        sock.sendall(str(data.get("penaltyPerDay")).encode('utf-8'))
    else:
        sock.sendall(b"False")
        print("ERROR: penaltyPerDay doesn't exist!!!")
    RetrCommand(name, sock)


def getStartDay(name, sock):
    """get start day for a module"""
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("startDay"):
        sock.sendall(str(data.get("startDay")).encode('utf-8'))
    else:
        sock.sendall(b"False")
        print("ERROR: startDay doesn't exist!!!")
    RetrCommand(name, sock)


def getEndDay(name, sock):
    """get end day for a module"""
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("endDay"):
        sock.sendall(str(data.get("endDay")).encode('utf-8'))
    else:
        sock.sendall(b"False")
        print("ERROR: endDay doesn't exist!!!")
    RetrCommand(name, sock)


def getCutoffDay(name, sock):
    """get cutoff day for a module"""
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    path = const.DIR_ROOT + "/module/" + module_code + "/" + week_number + "/"
    filename = path + "params.yaml"
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("cutoffDay"):
        sock.sendall(str(data.get("cutoffDay")).encode('utf-8'))
    else:
        sock.sendall(b"False")
        print("ERROR: cutoffDay doesn't exist!!!")
    RetrCommand(name, sock)


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
