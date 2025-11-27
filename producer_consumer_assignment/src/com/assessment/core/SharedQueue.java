package com.assessment.core;

import java.util.LinkedList;
import java.util.Queue;

// A custom thread-safe queue implementation using a monitor lock (synchronized/wait/notify)
public class SharedQueue<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;
    private final Object lock = new Object();

    public SharedQueue(int capacity) {
        this.capacity = capacity;
    }

    // Method to add an item to the queue (Producer calls this)
    public void put(T item) throws InterruptedException {
        synchronized (lock) {
            // Check if the queue is full. Use a while loop to handle spurious wakeups.
            while (queue.size() == capacity) {
                System.out.println("\t[Queue] FULL (" + queue.size() + "/" + capacity + "). Producer waiting...");
                // Release the lock and wait until notified by the consumer
                lock.wait();
            }

            queue.add(item);
            // VISUALIZATION UPDATE:
            System.out.println("Produced: " + item + " | Queue State: " + queue + " (Size: " + queue.size() + ")");

            // Notify all waiting threads (specifically the consumer) that the queue is no
            // longer empty
            lock.notifyAll();
        }
    }

    // Method to remove and return an item from the queue (Consumer calls this)
    public T take() throws InterruptedException {
        synchronized (lock) {
            // Check if the queue is empty. Use a while loop to handle spurious wakeups.
            while (queue.isEmpty()) {
                System.out.println("\t[Queue] EMPTY (0/" + capacity + "). Consumer waiting...");
                // Release the lock and wait until notified by the producer
                lock.wait();
            }

            T item = queue.remove();
            // VISUALIZATION UPDATE:
            System.out.println("Consumed: " + item + " | Queue State: " + queue + " (Size: " + queue.size() + ")");

            // Notify all waiting threads (specifically the producer) that the queue is no
            // longer full
            lock.notifyAll();
            return item;
        }
    }
}