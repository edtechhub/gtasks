import unittest
from unittest.mock import Mock, patch

from tasks.process import _non_interactive


class TestNonInteractive(unittest.TestCase):
    def actionator(self):
        return Mock()

    def piper(self):
        return Mock()

    @patch("tasks.process._print_single_task", new=Mock())
    @patch("tasks.process._serialize_task")
    def test_one_pipe_call_when_not_piping_serparately(self, serializer):
        actionator = self.actionator()
        piper = self.piper()

        tasks = [1, 2, 3, 4, 5]
        _non_interactive(tasks, actionator, piper, pipe_separately=False)
        assert len(piper.pipe.mock_calls) == 1

    @patch("tasks.process._print_single_task", new=Mock())
    @patch("tasks.process._serialize_task")
    def test_multiple_pipe_calls_when_piping_serparately(self, serializer):
        actionator = self.actionator()
        piper = self.piper()

        tasks = [1, 2, 3, 4, 5]
        _non_interactive(tasks, actionator, piper, pipe_separately=True)
        assert len(piper.pipe.mock_calls) == 5
