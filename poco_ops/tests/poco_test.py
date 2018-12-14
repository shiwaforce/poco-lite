import poco_ops.poco as poco
from .abstract_test import AbstractTestSuite
from ..services.file_utils import FileUtils


class PocoTestSuite(AbstractTestSuite):

    def test_without_command(self):
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                self.run_poco_command()
            self.assertIsNotNone(context.exception)
        self.assertIn(poco.__doc__.strip(), out.getvalue().strip())
        self.assertIn(poco.END_STRING.strip(), out.getvalue().strip())

    def test_version(self):
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                self.run_poco_command("--version")
            self.assertIsNotNone(context.exception)
        self.assertIn(poco.__version__, out.getvalue().strip())

    def test_help_command(self):
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                self.run_poco_command("help")
            self.assertIsNotNone(context.exception)
        self.assertIn(poco.__doc__.strip(), out.getvalue().strip())

    def test_help_command_with_everything(self):
        self.init_empty_compose_file()
        self.init_poco_file()
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                self.run_poco_command("help")
            self.assertIsNotNone(context.exception)
        self.assertIn(poco.__doc__.strip(), out.getvalue().strip())

    def test_subcommand_help(self):
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                self.run_poco_command("project")
            self.assertIsNotNone(context.exception)
        output = out.getvalue().strip()
        self.assertIn("Poco project commands\n", output)
        self.assertIn("Usage:", output)

    def test_wrong_parameters(self):
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                self.run_poco_command("notexistcommand")
            self.assertIsNotNone(context.exception)
        self.assertIn("is not a poco command. See 'poco help'.", out.getvalue().strip())

    def test_init(self):
        self.assertIsNone(FileUtils.get_file_with_extension('poco', directory=self.ws_dir))
        self.assertIsNone(FileUtils.get_file_with_extension('docker-compose', directory=self.ws_dir))
        with self.captured_output() as (out, err):
            self.run_poco_command("project", "init")
        self.assertEqual(0, len(err.getvalue().strip()))
        self.assertIsNotNone(FileUtils.get_file_with_extension('poco', directory=self.ws_dir))
        self.assertIsNotNone(FileUtils.get_file_with_extension('docker-compose', directory=self.ws_dir))

    def test_plan_list_with_not_exists_project(self):
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                self.run_poco_command("plan", "ls")
            self.assertIsNotNone(context.exception)
        self.assertIn("Poco file not found in directory:", out.getvalue())

    def test_plan_list(self):
        with self.captured_output() as (out, err):
            self.run_poco_command("project", "init")
            self.run_poco_command("plan", "ls")
        self.assertEqual(0, len(err.getvalue()))
        self.assertIn("default", out.getvalue())