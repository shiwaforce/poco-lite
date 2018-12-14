import unittest
import os
import sys
import shutil
import tempfile
import yaml
from contextlib import contextmanager
import poco_ops.poco as poco
from ..services.file_utils import FileUtils
from ..services.state import StateHolder
from ..services.console_logger import ColorPrint
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class AbstractTestSuite(unittest.TestCase):

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='poco-home')
        self.ws_dir = os.path.join(self.tmpdir, 'ws')
        os.makedirs(self.ws_dir)
        self.orig_dir = os.getcwd()
        os.chdir(self.ws_dir)

        self.clean_states()
        StateHolder.work_dir = self.ws_dir

    def tearDown(self):
        os.chdir(self.orig_dir)
        try:
            shutil.rmtree(self.tmpdir, onerror=FileUtils.remove_readonly)
        except Exception:
            ColorPrint.print_warning("Failed to delete test directory: " + self.tmpdir)

    @staticmethod
    def clean_states():

        StateHolder.home_dir = None
        StateHolder.args = dict()
        StateHolder.base_work_dir = os.path.join(os.path.expanduser(path='~'), 'workspace')
        StateHolder.work_dir = None
        StateHolder.offline = True
        StateHolder.always_update = False
        StateHolder.name = None
        StateHolder.plan = None
        StateHolder.repository = None
        StateHolder.container_mode = "Docker"
        StateHolder.test_mode = False
        StateHolder.compose_handler = None

        StateHolder.repositories = dict()

    def init_empty_compose_file(self):
        compose_file = dict()
        compose_file['services'] = dict()
        with open(os.path.join(self.ws_dir, 'docker-compose.yaml'), 'w+') as stream:
            yaml.dump(data=compose_file, stream=stream, default_flow_style=False,
                      default_style='', indent=4)

    def init_poco_file(self):
        poco_file = dict()
        poco_file['plan'] = dict()
        poco_file['plan']['default'] = 'docker-compose.yaml'
        with open(os.path.join(self.ws_dir, 'poco.yaml'), 'w+') as stream:
            yaml.dump(data=poco_file, stream=stream, default_flow_style=False,
                      default_style='', indent=4)

    def run_poco_command(self, *args):
        runnable = poco.Poco(argv=list(args))
        runnable.start_flow()
