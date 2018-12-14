import os


class StateHolder:

    # repositories
    repositories = dict()

    # input arguments
    args = dict()

    # Working directory
    work_dir = os.getcwd()

    # Mode and mode properties
    mode_properties = ['offline', 'always_update']
    offline = True
    always_update = False

    # Project properties
    name = None
    plan = None
    repository = None

    poco_file = None

    # Virtualization type
    container_mode = "Docker"
    test_mode = False  # Not running scrips and virtualization types

    # Handlers
    compose_handler = None

    @staticmethod
    def has_args(*args):
        for arg in args:
            if not StateHolder.args.get(arg):
                return False
        return True

    @staticmethod
    def has_least_one_arg(*args):
        for arg in args:
            if StateHolder.args.get(arg):
                return True
        return False

    @staticmethod
    def process_extra_args():
        for prop in StateHolder.mode_properties:
            param_name = "--" + prop.replace("_", "-")
            val = StateHolder.args.get(param_name)
            if val:
                setattr(StateHolder, prop, val)
