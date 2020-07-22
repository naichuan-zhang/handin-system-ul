import os
import socket
import string
import threading
import time
from datetime import datetime
from subprocess import Popen, PIPE
import shutil
import yaml

import const

host = const.HANDIN_HOST
port = const.HANDIN_PORT


def get_file_content(path, mode='r'):
    with open(path, mode=mode, encoding='utf-8') as f:
        content = f.read()
    return content


def get_total_attempts(module_code, week_number) -> int:
    """read /**weekNum**/params.yaml file to get totalAttempts value"""
    path = const.get_params_file_path(module_code, week_number)
    with open(path, 'r') as stream:
        data: dict = yaml.safe_load(stream)
    return data.get("totalAttempts")


def getPenaltyPerDay(module_code, week_number):
    """get penalty per day for a module"""
    params_filepath = const.get_params_file_path(module_code, week_number)
    with open(params_filepath, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("penaltyPerDay"):
        return str(data.get("penaltyPerDay"))
    else:
        print("ERROR: penaltyPerDay doesn't exist!!!")
        return "False"


def getStartDay(module_code, week_number):
    """get start day for a module"""
    params_filepath = const.get_params_file_path(module_code, week_number)
    with open(params_filepath, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("startDay"):
        return str(data.get("startDay"))
    else:
        print("ERROR: startDay doesn't exist!!!")
        return "False"


def getEndDay(module_code, week_number):
    """get end day for a module"""
    params_filepath = const.get_params_file_path(module_code, week_number)
    with open(params_filepath, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("endDay"):
        return str(data.get("endDay"))
    else:
        print("ERROR: endDay doesn't exist!!!")
        return "False"


def getCutoffDay(module_code, week_number):
    """get cutoff day for a module"""
    params_filepath = const.get_params_file_path(module_code, week_number)
    with open(params_filepath, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("cutoffDay"):
        return str(data.get("cutoffDay"))
    else:
        print("ERROR: cutoffDay doesn't exist!!!")
        return "False"


def get_required_code_filename(module_code, week_number) -> str:
    params_path = const.get_params_file_path(module_code, week_number)
    with open(params_path, 'r') as stream:
        data = yaml.safe_load(stream)
    return data.get("collectionFilename") if data.get("collectionFilename") else ""


def RetrCommand(name, sock: socket.socket):
    msg = sock.recv(1024).decode()
    print("Received command \"%s\"" % msg)

    if msg == "Authentication":
        time.sleep(.1)
        authentication_of_student(name, sock)
    elif msg == "Check attempts left":
        time.sleep(.1)
        checkAttemptsLeft(name, sock)
    elif msg == "Checking Assignment Week":
        time.sleep(.1)
        checkIfAssignmentWeek(name, sock)
    elif msg == "Check module exists":
        time.sleep(.1)
        checkIfModuleExists(name, sock)
    elif msg == "Create vars file":
        time.sleep(.1)
        createVarsFile(name, sock)
    elif msg == "Init vars file":
        time.sleep(.1)
        initVarsFile(name, sock)
    elif msg == "Check late penalty":
        time.sleep(.1)
        checkLatePenalty(name, sock)
    elif msg == "Check collection filename":
        time.sleep(.1)
        checkCollectionFilename(name, sock)
    elif msg == "Send file to server":
        time.sleep(.1)
        sendFileToServer(name, sock)
    elif msg == "Get exec result":
        time.sleep(.1)
        getExecResult(name, sock)
    else:
        print(f"Unknown Message: {msg}")


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
    vars_filepath = const.get_vars_file_path(module_code, week_number, student_id)
    with open(vars_filepath, 'r') as stream:
        data: dict = yaml.safe_load(stream)
    if data.get("attemptsLeft"):
        sock.sendall(str(data.get("attemptsLeft")).encode('utf-8'))
    else:
        sock.sendall(b"False")
        print("ERROR: attemptsLeft doesn't exist!!!")
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


def createVarsFile(name, sock):
    """Create vars file for a specific student"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    student_id = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    vars_filepath = const.get_vars_file_path(module_code, week_number, student_id)
    if not os.path.exists(vars_filepath):
        with open(vars_filepath, 'w'):
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
    vars_filepath = const.get_vars_file_path(module_code, week_number, student_id)
    data = {
        "attemptsLeft": get_total_attempts(module_code, week_number),
        "marks": 0,
    }
    with open(vars_filepath, 'w') as f:
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


def checkCollectionFilename(name, sock):
    """check if the submitted filename matches the required filename"""
    sock.sendall(b"OK")
    filename = sock.recv(1024).decode()
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()

    params_filepath = const.get_params_file_path(module_code, week_number)
    with open(params_filepath, 'r') as stream:
        data = yaml.safe_load(stream)
    if data.get("collectionFilename") and str(data.get("collectionFilename")) == filename:
        sock.sendall(b"True")
    else:
        sock.sendall((str(data.get("collectionFilename")) + " is required!").encode('utf-8'))
    RetrCommand(name, sock)


def sendFileToServer(name, sock):
    """Copy code file to server side"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    student_id = sock.recv(1024).decode()
    filepath = sock.recv(1024).decode()
    filename = os.path.basename(filepath)
    path = const.get_program_file_path(module_code, week_number, student_id, filename)
    sock.sendall(b"Start sending")
    with open(path, 'wb') as f:
        while True:
            data = sock.recv(1024)
            if data.decode().endswith("DONE"):
                content, done_str = data.decode().split("DONE")
                f.write(str(content).encode())
                break
            f.write(data)
    sock.sendall(b"End sending")
    RetrCommand(name, sock)


def getExecResult(name, sock):
    """Exec the program and get exec result"""
    sock.sendall(b"OK")
    module_code = sock.recv(1024).decode()
    week_number = sock.recv(1024).decode()
    student_id = sock.recv(1024).decode()
    file_suffix = sock.recv(1024).decode()
    penalty = sock.recv(1024).decode()

    if file_suffix == "cc" or file_suffix == "cpp":
        lang = "c++"
    elif file_suffix == "java":
        lang = "java"

    curr_marks: int = 0
    result_msg: str = ""
    required_code_filename = get_required_code_filename(module_code, week_number)
    code_filepath = const.get_program_file_path(module_code, week_number, student_id, required_code_filename)
    params_filepath = const.get_params_file_path(module_code, week_number)
    vars_filepath = const.get_vars_file_path(module_code, week_number, student_id)
    with open(params_filepath, 'r') as stream:
        data: dict = yaml.safe_load(stream)
    with open(vars_filepath, 'r') as stream:
        vars_data: dict = yaml.safe_load(stream)

    # check if attempts left
    if vars_data["attemptsLeft"] and vars_data["attemptsLeft"] > 0:
        if data["tests"]:
            # if attendance exists, check attendance, assign marks
            if data["tests"]["attendance"]:
                attendance_marks = int(data["tests"]["attendance"]["marks"])
                attendance_tag = data["tests"]["attendance"]["tag"]
                curr_marks = curr_marks + attendance_marks
                result_msg += "%s: %d/%d\n" % (attendance_tag, attendance_marks, attendance_marks)
                vars_data["attendance"] = attendance_marks

            # if compilation exists, check compilation, assign marks
            if data["tests"]["compilation"]:
                compilation_marks = int(data["tests"]["compilation"]["marks"])
                compilation_tag = data["tests"]["compilation"]["tag"]
                compilation_command = data["tests"]["compilation"]["command"]

                # change working directory
                os.chdir(os.path.dirname(code_filepath))

                p = Popen(compilation_command, stdout=PIPE, shell=True)
                return_code = p.wait()
                if return_code == 0:
                    # compilation successful
                    curr_marks = curr_marks + compilation_marks
                    result_msg += "%s: %d/%d\n" % (compilation_tag, compilation_marks, compilation_marks)
                    vars_data["compilation"] = compilation_marks

                    # execute the rest of custom tests when compilation success
                    for key in data["tests"].keys():
                        if key.startswith("test"):
                            test_marks = int(data["tests"][key]["marks"])
                            test_tag = data["tests"][key]["tag"]
                            test_command = data["tests"][key]["command"]
                            input_data_file_path = data["tests"][key]["inputDataFile"]
                            answer_file_path = data["tests"][key]["answerFile"]
                            filter_file_path = data["tests"][key]["filterFile"]
                            filter_command = data["tests"][key]["filterCommand"]
                            if input_data_file_path is not None and input_data_file_path != '':
                                input_data_file = open(input_data_file_path, 'r')

                                # change working directory
                                os.chdir(os.path.dirname(code_filepath))
                                proc = Popen(test_command, stdin=input_data_file, stdout=PIPE, stderr=PIPE, shell=False)
                                output, stderr = proc.communicate()  # bytes

                                # compare stdout with the answer file
                                if answer_file_path is not None and answer_file_path != '':
                                    answer_file = open(answer_file_path, 'rb')
                                    answer: bytes = answer_file.read()

                                    # use stdout and answer as two argv of filter file, then perform filtering
                                    # TODO: may need to be changed ...
                                    if (filter_file_path is not None and filter_file_path != '') and \
                                            (filter_command is not None and filter_command != ''):
                                        try:
                                            # copy filter file to student dir
                                            filter_filename = os.path.basename(filter_file_path)
                                            filter_file_path_dst = os.path.join(os.path.dirname(code_filepath), filter_filename)
                                            with open(filter_file_path_dst, 'w'):
                                                pass
                                            shutil.copyfile(filter_file_path, filter_file_path_dst)

                                            os.chdir(os.path.dirname(filter_file_path_dst))
                                            output = replace_whitespace_with_underscore(output.decode('utf-8')).encode('utf-8')
                                            answer = replace_whitespace_with_underscore(answer.decode('utf-8')).encode('utf-8')
                                            command: str = (filter_command + " %s %s") % (output.decode('utf-8'), answer.decode('utf-8'))
                                            filter_proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                                            stdout, stderr = filter_proc.communicate()
                                            output, answer = stdout.decode('utf-8').split(' ')
                                        except Exception as e:
                                            print(e)

                                    if compare_output_with_answer(str(output), str(answer)):
                                        # custom test success
                                        curr_marks = curr_marks + test_marks
                                        result_msg += "%s: %d/%d</br>" % (test_tag, test_marks, test_marks)
                                        vars_data[key] = test_marks
                                    else:
                                        # custom test failed
                                        result_msg += "%s: %d/%d</br>" % (test_tag, 0, test_marks)
                                        vars_data[key] = 0

                else:
                    # compilation failed
                    result_msg += "%s: %d/%d\n" % (compilation_tag, 0, compilation_marks)
                    vars_data["compilation"] = 0

                with open(vars_filepath, 'w') as f:
                    yaml.dump(vars_data, f)

            # check assignment attempts left and update attempts left
            vars_filepath = const.get_vars_file_path(module_code, week_number, student_id)
            with open(vars_filepath, 'r') as stream:
                vars_data: dict = yaml.safe_load(stream)
            if vars_data["attemptsLeft"]:
                vars_data["attemptsLeft"] = vars_data["attemptsLeft"] - 1
                if vars_data["attemptsLeft"] <= 0:
                    vars_data["attemptsLeft"] = 0
            with open(vars_filepath, 'w') as f:
                yaml.dump(vars_data, f)
            result_msg += "\n\nYou have %s attempts left\n\n" % str(vars_data["attemptsLeft"])

            # apply penalty
            curr_marks = curr_marks - int(penalty)
            result_msg += "\n\nPenalty: %s\n\n" % str(penalty)

            # update student marks
            with open(vars_filepath, 'r') as stream:
                vars_data2: dict = yaml.safe_load(stream)
            if "marks" in vars_data2.keys():
                vars_data2["marks"] = curr_marks
            with open(vars_filepath, 'w') as f:
                yaml.dump(vars_data2, f)
            result_msg += "\n\nTotal marks: %s\n\n" % str(curr_marks)
    else:
        result_msg = "Sorry, you have no attempts left for this assignment!"

    sock.sendall(result_msg.encode())
    RetrCommand(name, sock)


def compare_output_with_answer(output: str, answer: str) -> bool:
    remove = string.punctuation + string.whitespace
    return output.maketrans(dict.fromkeys(remove)) == answer.maketrans(dict.fromkeys(remove))


def replace_whitespace_with_underscore(text: str) -> str:
    return text.replace(' ', '_').replace('\r', '_').replace('\n', '_')


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
