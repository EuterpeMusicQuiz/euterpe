# -*- coding: utf-8 -*-


class Task(object):
    def __init__(self):
        pass
    
    def run(self):
        pass

    def __str__(self):
        '''Keep it short on one line'''
        return "Empty task"

_TASKS = []
class tasks(object):

    @classmethod
    def add(cls, task):
        if not isinstance(task, Task):
            if isinstance(task, list):
                for t in task:
                    tasks.add(t)
            return
        global _TASKS
        _TASKS.append(task)

    @classmethod
    def remove(cls, item):
        if type(item) is int:
            item = slice(item, item+1)
        global _TASKS
        _TASKS[item] = []

    @classmethod
    def run(cls):
        global _TASKS
        for t in tasks:
            t.run()
    
    @classmethod
    def display(cls):
        global _TASKS
        for i in range(len(_TASKS)):
            print("{}\t{}".format(i, _TASKS[i]))
