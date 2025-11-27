package com.assessment.workers;

import java.util.List;
import java.util.Random;
import com.assessment.core.SharedQueue;

// The Producer task that generates data and puts it into the shared queue
public class Producer implements Runnable {
    private final SharedQueue<Integer> queue;
    private final List<Integer> sourceContainer;
    private final Random random = new Random();

    public Producer(SharedQueue<Integer> queue, List<Integer> sourceContainer) {
        this.queue = queue;
        this.sourceContainer = sourceContainer;
    }

    // The main execution logic for the producer thread
    @Override
    public void run() {
        try {
            System.out.println("\n[Producer] Starting to process " + sourceContainer.size() + " items.");

            for (Integer item : sourceContainer) {
                System.out.println("[Producer] Reading from source: " + item);
                queue.put(item);

                // DYNAMIC SPEED: Random sleep between 100ms and 800ms
                int delay = 100 + random.nextInt(700);
                Thread.sleep(delay);
            }

            System.out.println("[Producer] Work finished. Sending POISON PILL (-1)...");
            // Send the "poison pill" (-1) to signal the consumer to stop
            queue.put(-1);

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}