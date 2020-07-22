import cgi
import io
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

import const

""" ###########################################
    Server for student to access and download handin.py file
"""

# TODO: config module code and name here...
MODULE_CODE = "cs4115"
MODULE_NAME = "Default"

HOST = "127.0.0.1"
PORT = 8000

ADDR = (HOST, PORT)

DIR_ROOT = os.path.dirname(__file__)

# directory to save handin.py file temperately
DIR_TEMP = "/temp/"
DIR_DATA = f"/module/{MODULE_CODE}/data/"
DIR_MODULE = f"/module/{MODULE_CODE}/"


class BaseCase(object):
    @staticmethod
    def handle_file(handler, full_path):
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    @staticmethod
    def index_path(handler):
        return os.path.join(handler.full_path, 'handin.html')

    def test(self, handler):
        raise NotImplementedError("Not implemented")

    def act(self, handler):
        raise NotImplementedError("Not implemented")


class CaseDirectoryIndexFile(BaseCase):
    def test(self, handler):
        return os.path.isdir(handler.full_path) \
               and os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


class CaseNoFile(BaseCase):
    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class CaseCgiFile(BaseCase):
    @staticmethod
    def run_cgi(handler):
        content = subprocess.check_output(["python", handler.full_path])
        handler.send_content(content)

    def test(self, handler):
        return os.path.isfile(handler.full_path) \
               and handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler)


class CaseExistingFile(BaseCase):
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


class CaseDefault(BaseCase):
    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))


def check_if_student_id_in_file(student_id):
    # TODO: dynamically identify module code
    with open(DIR_ROOT + DIR_MODULE + 'class-list', 'r') as f:
        for line in f:
            if student_id in line:
                return True
    return False


class RequestHandler(BaseHTTPRequestHandler):
    """Handle request and return page"""

    error_page = """\
    <html>
    <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    """

    cases = [
        CaseNoFile(),
        CaseCgiFile(),
        CaseExistingFile(),
        CaseDirectoryIndexFile(),
        CaseDefault(),
    ]

    base_path = DIR_ROOT
    handin_file_path = DIR_ROOT + DIR_TEMP
    student_data_path = DIR_ROOT + DIR_DATA

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as e:
            self.handle_error(e)

    def do_POST(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                },
            )
            self.send_response(200)
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.end_headers()
            out = io.TextIOWrapper(
                self.wfile,
                encoding='utf-8',
                line_buffering=False,
                write_through=True,
            )
            for field in form.keys():
                out.write('<p>{}={}</p>'.format(
                    field, form[field].value))

            student_id = form['studentID'].value
            student_name = form['studentName'].value

            out.write('<a href="/temp/handin_{}.txt" download="handin.py">Download handin.py</a>'.format(student_id))
            out.detach()

            self.create_handin_file(student_id)
            self.update_handin_file(student_id, student_name)
            self.create_student_directory(student_id)
            self.add_student_to_class_list(student_id)

        except Exception as e:
            self.handle_error(e)

    def create_handin_file(self, student_id):
        # create /temp/ file directory if not exists
        if not os.path.exists(self.handin_file_path):
            os.mkdir(self.handin_file_path)
        # the /temp/handin_xxx.txt must be in .txt format. It is downloaded as handin.py file
        filename = "handin_" + student_id + ".txt"
        if not os.path.exists(self.handin_file_path + filename):
            with open(self.handin_file_path + filename, 'w'):
                pass

    def update_handin_file(self, student_id, student_name):
        """write content to handin.py file"""
        # check if handin_xxx.txt file exists
        filename = "handin_" + student_id + ".txt"
        if not os.path.exists(self.handin_file_path + filename):
            self.create_handin_file(student_id)
        # write content of handin_student_template.py to handin_xxx.txt
        with open(self.handin_file_path + filename, 'wb') as f:
            content_bytes: bytes = open('handin_student_template.py', 'rb').read()
            content = content_bytes.decode('utf-8').format(
                        str(const.HANDIN_HOST),  # host
                        str(const.HANDIN_PORT),  # port
                        str(student_name),       # student name
                        str(student_id),         # student id
                        str(MODULE_CODE),        # module code
                        str(MODULE_NAME),        # module name
                    ).encode('utf-8')
            f.write(content)

    def create_student_directory(self, student_id):
        """create /data/**student_id**/ directory AND all weekNumbers directory"""
        if not os.path.exists(self.student_data_path):
            os.mkdir(self.student_data_path)
        subdir = str(student_id)
        if not os.path.exists(self.student_data_path + subdir):
            os.mkdir(self.student_data_path + subdir)
        folders = ["w01", "w02", "w03", "w04", "w05", "w06",
                   "w07", "w08", "w09", "w10", "w11", "w12", "w13"]
        for folder in folders:
            week_dir = self.student_data_path + subdir + "/" + folder
            if not os.path.exists(week_dir):
                os.mkdir(week_dir)

    def add_student_to_class_list(self, student_id):
        """add student id to class list file"""
        # create class-list.txt file if not exists
        filename = DIR_ROOT + DIR_MODULE + "class-list"
        if os.path.exists(filename):
            append_write = 'a'
        else:
            append_write = 'w'
        if not check_if_student_id_in_file(student_id):
            class_list = open(filename, append_write)
            class_list.write(str(student_id) + '\n')
            class_list.close()

    def handle_error(self, msg):
        content = self.error_page.format(path=self.path, msg=msg)
        self.send_content(bytes(content.encode('utf-8')), status=404)

    def send_content(self, content: bytes, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


class ServerException(Exception):
    """Server Exception"""
    pass


if __name__ == '__main__':
    serverAddr = ADDR
    server = HTTPServer(server_address=serverAddr, RequestHandlerClass=RequestHandler)
    print('Starting server ...')
    print('Open http://{}:{}'.format(HOST, PORT))
    server.serve_forever()
