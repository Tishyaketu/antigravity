package com.assessment.app;

import java.util.*;
import com.assessment.core.SimpleBlockingQueue;
import com.assessment.workers.Consumer;
import com.assessment.workers.Producer;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        // 1. Generate Random Source Data
        Set<Integer> uniqueNumbers = new HashSet<>();
        int randomLength = random.nextInt(15); // Length 0 to 14

        System.out.println("Generating " + randomLength + " unique items...");

        while (uniqueNumbers.size() < randomLength) {
            int num = random.nextInt(100) + 1; // 1-100
            uniqueNumbers.add(num);
        }

        List<Integer> sourceContainer = new ArrayList<>(uniqueNumbers);
        Collections.shuffle(sourceContainer);

        System.out.println("=== Source Container Generated ===");
        System.out.println(sourceContainer);
        System.out.println("==================================");

        // 2. User Input for Capacity (CRITICAL VALIDATION ADDED)
        int capacity = -1;
        while (capacity <= 0) {
            System.out.print("\nEnter Shared Queue Capacity (Positive Integer): ");
            if (scanner.hasNextInt()) {
                capacity = scanner.nextInt();
                if (capacity <= 0) {
                    System.out.println(">> Error: Queue cannot be non-existent! Enter 1 or greater.");
                }
            } else {
                System.out.println(">> Error: Invalid input. Enter a positive integer number.");
                scanner.next(); // Clear invalid input
            }
        }

        // 3. Setup Components
        SimpleBlockingQueue<Integer> sharedQueue = new SimpleBlockingQueue<>(capacity);
        List<Integer> destinationContainer = new ArrayList<>();

        Producer producer = new Producer(sharedQueue, sourceContainer);
        Consumer consumer = new Consumer(sharedQueue, destinationContainer);

        Thread pThread = new Thread(producer);
        Thread cThread = new Thread(consumer);

        // 4. Run Simulation
        System.out.println("\n=== Starting Simulation ===");

        pThread.start();
        cThread.start();

        try {
            pThread.join();
            cThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // 5. Final Verification
        System.out.println("\n=== Simulation Complete ===");
        System.out.println("Source List:      " + sourceContainer);
        System.out.println("Destination List: " + destinationContainer);

        // Collections.sort(sourceContainer);
        // Collections.sort(destinationContainer);

        if (sourceContainer.equals(destinationContainer)) {
            System.out.println("SUCCESS: Data transfer perfectly matched!");
        } else {
            System.out.println("FAILURE: Data mismatch.");
        }

        scanner.close();
    }

    public static boolean isValidCapacity(int capacity) {
        return capacity > 0;
    }
}