package com.assessment.workers;

import java.util.List;
import java.util.Random;
import com.assessment.core.SimpleBlockingQueue;

public class Consumer implements Runnable {
    private final SimpleBlockingQueue<Integer> queue;
    private final List<Integer> destinationList;
    private final Random random = new Random(); // Initialize Random

    public Consumer(SimpleBlockingQueue<Integer> queue, List<Integer> destinationList) {
        this.queue = queue;
        this.destinationList = destinationList;
    }

    @Override
    public void run() {
        try {
            while (true) {
                // DYNAMIC SPEED: Random sleep between 100ms and 800ms
                // Placed at the start to vary the "pickup" time
                int delay = 100 + random.nextInt(700);
                Thread.sleep(delay);

                Integer item = queue.take();

                if (item == -1) {
                    System.out.println("[Consumer] Caught POISON PILL. Stopping...");
                    break;
                }

                destinationList.add(item);
                System.out.println("\t[Destination] Added " + item + " | Current Dest: " + destinationList + " (Size: "
                        + destinationList.size() + ")");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}