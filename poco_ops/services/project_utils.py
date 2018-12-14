import os
from .file_repository import FileRepository
from .file_utils import FileUtils
from .state import StateHolder
from .console_logger import *


class ProjectUtils:

    @staticmethod
    def get_project_repository(project_element):
        """Get and store repository handler for named project"""
        repo_handler = FileRepository(target_dir=ProjectUtils.get_target_dir(project_element=project_element))
        StateHolder.repositories[StateHolder.name] = repo_handler
        return repo_handler

    @staticmethod
    def add_repository(target_dir):

        repo_handler = FileRepository(target_dir=target_dir)
        StateHolder.repositories[StateHolder.name] = repo_handler
        return repo_handler

    @staticmethod
    def get_compose_file(silent=False):
        """Get compose file from project repository """

        if StateHolder.config is None:
            ProjectUtils.add_repository(target_dir=StateHolder.work_dir)
            file = FileUtils.get_backward_compatible_poco_file(directory=StateHolder.work_dir, silent=True)
        else:
            file = ProjectUtils.get_file_from_project(file_element=StateHolder.catalog_element.get('file'),
                                                      repo_handler=StateHolder.repository)

        if not os.path.exists(file):
            if silent:
                return None
            ColorPrint.exit_after_print_messages(
                message="Compose file : %s not exists in project : %s " % (str(file), str(StateHolder.name)),
                doc=Doc.POCO_CATALOG)
        return file

    @staticmethod
    def get_file_from_project(file_element, repo_handler):
        if file_element is not None:
            return repo_handler.get_file(file=file_element)
        else:  # TODO remove later
            file = FileUtils.get_backward_compatible_poco_file(directory=repo_handler.target_dir, silent=True)
            return file if file is not None else os.path.join(repo_handler.target_dir, "poco.yaml")

    @staticmethod
    def get_file(file):
        """Get file from project repository"""
        repo = StateHolder.repositories.get(StateHolder.name)
        if repo is not None:
            return repo.get_file(file)
        return os.path.join(os.getcwd(), file)

    @staticmethod
    def get_target_dir(project_element):
        return os.path.join(StateHolder.work_dir, project_element.get('repository_dir', StateHolder.name))

    @staticmethod
    def get_list_value(value):
        """Get list format, doesn't matter the config use one or list plan"""
        lst = list()
        if type(value) is list:
            lst.extend(value)
        else:
            lst.append(value)
        return lst
