from functools import reduce as functional_reduce

class Stream:
    """
    A lazy-evaluation stream processor using Python Generators.
    """
    def __init__(self, source):
        self.source = source

    def map(self, func):
        def generator():
            for item in self.source:
                yield func(item)
        return Stream(generator())

    def filter(self, predicate):
        def generator():
            for item in self.source:
                if predicate(item):
                    yield item
        return Stream(generator())

    def distinct(self, key_func):
        def generator():
            seen = set()
            for item in self.source:
                key = key_func(item)
                if key not in seen:
                    seen.add(key)
                    yield item
        return Stream(generator())

    def sorted(self, key=None, reverse=False):
        # Stateful operation: Must load list into memory to sort
        sorted_items = sorted(self.source, key=key, reverse=reverse)
        return Stream(sorted_items)

    def group_by(self, key_func):
        groups = {}
        for item in self.source:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups

    def reduce(self, func, initial):
        return functional_reduce(func, self.source, initial)
    
    def collect(self):
        return list(self.source)