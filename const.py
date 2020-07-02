import os

# Handin System Server Configs
HANDIN_HOST = '127.0.0.1'
HANDIN_PORT = 5000

DIR_ROOT = os.path.dirname(__file__)


def get_class_list_file_path(module_code):
    return DIR_ROOT + "/module/" + module_code + "/class-list"


def get_definitions_file_path(module_code):
    return DIR_ROOT + "/module/" + module_code + "/definitions.yaml"


def get_params_file_path(module_code, week_number):
    return DIR_ROOT + "/module/" + module_code + "/" + week_number + "/params.yaml"


def get_vars_file_path(module_code, week_number, student_id):
    return DIR_ROOT + "/module/" + module_code + "/data/" + student_id + "/" + week_number + "/vars.yaml"


def get_program_file_path(module_code, week_number, student_id, filename_code):
    return DIR_ROOT + "/module/" + module_code + "/data/" + student_id + "/" + week_number + "/" + filename_code


