package com.assessment.core;

import java.util.LinkedList;
import java.util.Queue;

public class SimpleBlockingQueue<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;
    private final Object lock = new Object();

    public SimpleBlockingQueue(int capacity) {
        this.capacity = capacity;
    }

    public void put(T item) throws InterruptedException {
        synchronized (lock) {
            while (queue.size() == capacity) {
                System.out.println("\t[Queue] FULL (" + queue.size() + "/" + capacity + "). Producer waiting...");
                lock.wait();
            }

            queue.add(item);
            // VISUALIZATION UPDATE:
            System.out.println("Produced: " + item + " | Queue State: " + queue + " (Size: " + queue.size() + ")");

            lock.notifyAll();
        }
    }

    public T take() throws InterruptedException {
        synchronized (lock) {
            while (queue.isEmpty()) {
                System.out.println("\t[Queue] EMPTY (0/" + capacity + "). Consumer waiting...");
                lock.wait();
            }

            T item = queue.remove();
            // VISUALIZATION UPDATE:
            System.out.println("Consumed: " + item + " | Queue State: " + queue + " (Size: " + queue.size() + ")");

            lock.notifyAll();
            return item;
        }
    }
}