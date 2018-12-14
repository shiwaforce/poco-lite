import os
import shutil
from .abstract_command import AbstractCommand
from ..services.console_logger import ColorPrint
from ..services.state_utils import StateUtils
from ..services.file_utils import FileUtils
from ..services.state import StateHolder


class Init(AbstractCommand):

    command = "init"
    args = ["[<name>]"]
    args_descriptions = {"[<name>]": "Name of the project or the actual directory if it is empty"}
    description = "Run: 'poco init nginx' or 'poco project init nginx' to initialize poco project, poco.yml " \
                  "and docker-compose.yml will be created if they don't exist in nginx project directory"

    def prepare_states(self):
        StateHolder.work_dir = StateHolder.work_dir
        StateHolder.name = FileUtils.get_parameter_or_directory_name('<name>')
        StateUtils.prepare("project_repo")

    def resolve_dependencies(self):
        pass

    def execute(self):
        file = FileUtils.get_backward_compatible_poco_file(directory=os.getcwd())
        if file is None:
            Init.fix_file(os.path.join(os.getcwd(), 'poco.yml'))
        ColorPrint.print_info("Project init completed")

    @staticmethod
    def fix_file(target_file):
        if not os.path.exists(target_file):
            src_file = os.path.join(os.path.dirname(__file__), '../resources/poco.yml')
            shutil.copyfile(src=src_file, dst=target_file)
            default_compose = os.path.join(os.path.dirname(target_file), 'docker-compose.yml')
            if not os.path.exists(default_compose):
                src_file = os.path.join(os.path.dirname(__file__), '../resources/docker-compose.yml')
                shutil.copyfile(src=src_file, dst=default_compose)
