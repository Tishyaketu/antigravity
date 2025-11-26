from functools import reduce as functional_reduce

class Stream:
    """
    A lightweight, lazy-evaluation stream processing class.
    
    Design Choice:
    Uses Python generators to process data one item at a time (O(1) memory),
    mimicking the behavior of Java Streams or Big Data pipelines.
    """
    def __init__(self, source):
        # Source can be any iterable (list, generator, file object)
        self.source = source

    def map(self, func):
        """
        Transform elements. 
        Returns a NEW Stream (Lazy).
        """
        def generator():
            for item in self.source:
                yield func(item)
        return Stream(generator())

    def filter(self, predicate):
        """
        Select elements based on a condition.
        Returns a NEW Stream (Lazy).
        """
        def generator():
            for item in self.source:
                if predicate(item):
                    yield item
        return Stream(generator())

    def distinct(self, key_func):
        """
        Stateful Filter.
        Removes duplicates based on a key (e.g., product name).
        Keeps the first occurrence and discards subsequent ones.
        """
        def generator():
            seen = set()
            for item in self.source:
                key = key_func(item)
                if key not in seen:
                    seen.add(key)
                    yield item
        return Stream(generator())

    def sorted(self, key=None, reverse=False):
        """
        Sort elements.
        NOTE: This is a 'Stateful Intermediate Operation'.
        It MUST load the current stream into memory to sort it, 
        breaking the lazy evaluation chain temporarily.
        """
        # 1. Consume generator into a list
        # 2. Sort the list
        # 3. Return a new Stream from the sorted list
        sorted_items = sorted(self.source, key=key, reverse=reverse)
        return Stream(sorted_items)

    def group_by(self, key_func):
        """
        Terminal Operation.
        Groups elements into a dictionary based on the key_func.
        Useful for aggregation (e.g., Average rating BY category).
        """
        groups = {}
        for item in self.source:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups

    def reduce(self, func, initial):
        """
        Terminal Operation.
        Aggregates the stream into a single result.
        """
        return functional_reduce(func, self.source, initial)
    
    def collect(self):
        """
        Terminal Operation.
        Materializes the stream into a standard Python list.
        """
        return list(self.source)