from functools import reduce as functional_reduce

class Stream:
    """
    A custom implementation of a lazy-evaluation stream processor.
    It wraps a Python generator (or iterable) and allows chaining functional operations
    (map, filter, reduce) without loading the entire dataset into memory.
    """
    def __init__(self, source):
        # The source can be any iterable, typically a generator for lazy loading
        self.source = source

    def map(self, func):
        # Transforms each item in the stream using the provided function.
        # Returns a new Stream wrapping a generator that yields transformed items one by one.
        def generator():
            for item in self.source:
                yield func(item)
        return Stream(generator())

    def filter(self, predicate):
        # Filters items based on a boolean predicate.
        # Only items for which predicate(item) is True are yielded downstream.
        def generator():
            for item in self.source:
                if predicate(item):
                    yield item
        return Stream(generator())

    def distinct(self, key_func):
        # Yields unique items based on a key derived from the item.
        # Note: This maintains a 'seen' set in memory, so it grows with the number of unique keys.
        def generator():
            seen = set()
            for item in self.source:
                key = key_func(item)
                if key not in seen:
                    seen.add(key)
                    yield item
        return Stream(generator())

    def sorted(self, key=None, reverse=False):
        # Stateful operation: Breaking the lazy chain.
        # We must consume the entire stream into memory to sort it effectively.
        sorted_items = sorted(self.source, key=key, reverse=reverse)
        return Stream(sorted_items)

    def group_by(self, key_func):
        # Terminal operation (for now) that consumes the stream to group items.
        # Returns a dictionary mapping keys to lists of items.
        groups = {}
        for item in self.source:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups

    def reduce(self, func, initial):
        # Terminal operation that reduces the stream to a single value using an accumulator.
        return functional_reduce(func, self.source, initial)
    
    def collect(self):
        # Terminal operation that materializes the stream into a standard Python list.
        return list(self.source)