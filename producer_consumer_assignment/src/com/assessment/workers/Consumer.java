package com.assessment.workers;

import java.util.List;
import java.util.Random;
import com.assessment.core.SharedQueue;

// The Consumer task that takes data from the shared queue and processes it
public class Consumer implements Runnable {
    private final SharedQueue<Integer> queue;
    private final List<Integer> destinationContainer;
    private final Random random = new Random();

    public Consumer(SharedQueue<Integer> queue, List<Integer> destinationContainer) {
        this.queue = queue;
        this.destinationContainer = destinationContainer;
    }

    // The main execution logic for the consumer thread
    @Override
    public void run() {
        try {
            // Infinite loop to continuously consume items until the poison pill is found
            while (true) {
                // DYNAMIC SPEED: Random sleep between 100ms and 800ms
                // Placed at the start to vary the "pickup" time
                int delay = 100 + random.nextInt(700);
                Thread.sleep(delay);

                Integer item = queue.take();

                // Check if the retrieved item is the "poison pill" (-1)
                if (item == -1) {
                    System.out.println("[Consumer] Caught POISON PILL. Stopping...");
                    break;
                }

                destinationContainer.add(item);
                System.out.println(
                        "\t[Destination] Added " + item + " | Current Dest: " + destinationContainer + " (Size: "
                                + destinationContainer.size() + ")");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}