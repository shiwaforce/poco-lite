import os
from .console_logger import ColorPrint
from .compose_handler import ComposeHandler
from .file_utils import FileUtils
from .state import StateHolder
from .yaml_utils import YamlUtils


class StateUtils:

    PREPARE_STATES = ["project_file", "compose_handler"]

    @staticmethod
    def prepare(prepareable=None):
        if prepareable not in StateUtils.PREPARE_STATES:
            ColorPrint.print_info(message="Unknown prepare command : " + str(prepareable), lvl=1)
            return

        StateUtils.calculate_name_and_work_dir()
        if prepareable is "compose_handler":
            StateHolder.compose_handler = ComposeHandler(StateHolder.poco_file)
        StateHolder.process_extra_args()

    @staticmethod
    def prepare_project_file():

        if not StateHolder.name == FileUtils.get_directory_name():  # need check for valid plan handling
            StateHolder.plan = StateHolder.name
            StateHolder.name = FileUtils.get_directory_name()

    @staticmethod
    def calculate_name_and_work_dir():
        StateHolder.poco_file = FileUtils.get_backward_compatible_poco_file(directory=StateHolder.work_dir)
        arg = StateHolder.args.get('<project/plan>')
        if arg is None:  # if empty
            StateHolder.name = FileUtils.get_directory_name()
        elif '/' in arg:  # if have '/'
            project_and_plan = arg.split("/", 1)
            StateHolder.name = project_and_plan[0]
            StateHolder.plan = project_and_plan[1]
        elif YamlUtils.check_file(StateHolder.poco_file, arg):
            StateHolder.name = FileUtils.get_directory_name()
            StateHolder.plan = arg
        else:
            StateHolder.name = arg

    @staticmethod
    def check_variable(var):
        if getattr(StateHolder, var) is None:
            return False
        return True

