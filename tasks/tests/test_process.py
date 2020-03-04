import unittest
from unittest.mock import Mock, patch

from tasks.process import _non_interactive, _filter_tasks


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


class TestFilterTasks(unittest.TestCase):

    def task(self):
        t = Mock()
        t.title = "test"
        t.notes = "test notes"
        t.sub_tasks = []
        return t

    def test_strategy_not_found(self):
        with self.assertRaises(ValueError):
            _filter_tasks([], match='a', strategy='unknown')


class TestFilterTasksDefaultStrategy(TestFilterTasks):

    def test_filter_empty_list(self):
        tasks = _filter_tasks([], match="a")
        assert tasks == []

    def test_single_task_getting_filtered_out(self):
        t = self.task()
        tasks = _filter_tasks([t], match="a")
        assert tasks == []

    def test_single_task_getting_filtered_in(self):
        t = self.task()
        t.title = 'a'
        tasks = _filter_tasks([t], match="a")
        assert tasks == [t]

    def test_children_getting_filtered_out(self):
        t = self.task()
        t.title = 'a'
        t.sub_tasks = [self.task(), self.task()]
        tasks = _filter_tasks([t], match="a")

        assert tasks == [t]
        assert tasks[0].sub_tasks == []

    def test_single_child_filtered_in(self):
        t = self.task()
        t.title = 'a'
        c = self.task()
        c.notes = 'contains an a'
        t.sub_tasks = [c, self.task()]

        tasks = _filter_tasks([t], match="a")

        assert tasks == [t]
        assert tasks[0].sub_tasks == [c]


class TestFilterTasksParentMatchStrategy(TestFilterTasks):
    def test_children_are_kept_if_only_parent_matches(self):
        t = self.task()
        t.title = 'a'
        c = self.task()
        c.title = 'b'
        t.sub_tasks = [c, c]

        tasks = _filter_tasks([t], match="a", strategy="parent-match")

        assert tasks == [t]
        assert tasks[0].sub_tasks == [c, c]

    def test_children_are_kept_if_they_match_too(self):
        t = self.task()
        t.title = 'a'
        c = self.task()
        c.title = 'a'
        t.sub_tasks = [c, c]

        tasks = _filter_tasks([t], match="a", strategy="parent-match")

        assert tasks == [t]
        assert tasks[0].sub_tasks == [c, c]

    def test_child_matches_but_not_parent(self):
        t = self.task()
        t.title = 'a'
        c = self.task()
        c.title = 'b'
        t.sub_tasks = [c, c]

        tasks = _filter_tasks([t], match="b", strategy="parent-match")

        assert tasks == []
