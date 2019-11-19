import unittest
from unittest.mock import Mock

from tasks.backup import _organize_tasks


class TestBackupOrganizeTasks(unittest.TestCase):

    def task(self):
        task = Mock()
        task.parent = None
        return task

    def test_empty(self):
        assert _organize_tasks([]) == []

    def test_single_parent_length(self):
        task = self.task()
        assert len(_organize_tasks([task])) == 1

    def test_single_parent(self):
        task = self.task()
        assert _organize_tasks([task]) == [task]

    def test_parent_with_child(self):
        parent = self.task()
        parent.id = "123"
        child = self.task()
        child.parent = Mock(id="123")

        orged = _organize_tasks([parent, child])
        assert len(orged) == 1
        parent, = orged
        assert parent.sub_tasks == [child]

    def test_chain_of_three(self):
        grandparent = self.task()
        grandparent.id = "grandparent"

        parent = self.task()
        parent.id = "parent"
        parent.parent = Mock(id="grandparent")

        child = self.task()
        child.parent = Mock(id="parent")

        orged = _organize_tasks([grandparent, parent, child])
        assert len(orged) == 1
        g_parent, = orged

        assert g_parent.sub_tasks == [parent]
        assert g_parent.sub_tasks[0].sub_tasks == [child]

    def test_two_children_same_parent(self):
        parent = self.task()
        parent.id = "123"
        child1 = self.task()
        child1.parent = Mock(id="123")
        child2 = self.task()
        child2.parent = Mock(id="123")

        orged = _organize_tasks([parent, child1, child2])
        assert len(orged) == 1
        parent, = orged
        assert parent.sub_tasks == [child1, child2]
