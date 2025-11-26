package com.assessment.workers;

import java.util.List;
import java.util.Random;
import com.assessment.core.SimpleBlockingQueue;

// The Producer task that generates data and puts it into the shared queue
public class Producer implements Runnable {
    private final SimpleBlockingQueue<Integer> queue;
    private final List<Integer> sourceData;
    private final Random random = new Random();

    public Producer(SimpleBlockingQueue<Integer> queue, List<Integer> sourceData) {
        this.queue = queue;
        this.sourceData = sourceData;
    }

    // The main execution logic for the producer thread
    @Override
    public void run() {
        try {
            System.out.println("\n[Producer] Starting to process " + sourceData.size() + " items.");

            for (Integer item : sourceData) {
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