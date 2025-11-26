package com.assessment.tests;

import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import com.assessment.core.SimpleBlockingQueue;

import com.assessment.app.Main;

public class TestBlockingQueue {

    // Simple class to hold test results for the summary
    static class TestResult {
        String name;
        boolean passed;

        TestResult(String name, boolean passed) {
            this.name = name;
            this.passed = passed;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("==========================================");
        System.out.println("RUNNING COMPREHENSIVE UNIT TESTS");
        System.out.println("==========================================");

        List<TestResult> results = new ArrayList<>();

        // --- TEST 3.1: Input Validation ---
        boolean valPass = testInputValidation();
        results.add(new TestResult("3.1 Input Validation", valPass));

        // --- TEST 3.2 & 3.3: Sync & Concurrency ---
        // We use the Stress Test to prove both synchronization and concurrent execution
        // at once.
        boolean concPass = testConcurrencyAndDataIntegrity();
        results.add(new TestResult("3.2 Thread Synchronization", concPass));
        results.add(new TestResult("3.3 Concurrent Programming", concPass));

        // --- TEST 3.4 & 3.5: Blocking & Wait/Notify ---
        // The "Blocking" behavior physically proves the "Wait/Notify" mechanism works.
        boolean prodBlockPass = testProducerBlocksWhenFull();
        results.add(new TestResult("3.4 Blocking Queues (Full)", prodBlockPass));

        boolean consBlockPass = testConsumerBlocksWhenEmpty();
        results.add(new TestResult("3.5 Blocking Queues (Empty)", consBlockPass));

        // If blocking worked in both directions, the Wait/Notify mechanism is verified
        boolean waitNotifyPass = prodBlockPass && consBlockPass;
        results.add(new TestResult("Mech: Wait/Notify Mechanism", waitNotifyPass));

        // Calculate totals
        long passedCount = results.stream().filter(r -> r.passed).count();
        long failedCount = results.stream().filter(r -> !r.passed).count();

        System.out.println("\n==========================================");
        System.out.println("TEST SUMMARY");
        System.out.println("==========================================");

        for (TestResult result : results) {
            String status = result.passed ? "[PASSED]" : "[FAILED]";
            // Print neatly aligned
            System.out.printf("%-8s %s%n", status, result.name);
        }

        System.out.println("------------------------------------------");
        System.out.println("Total: " + passedCount + " Passed, " + failedCount + " Failed");
        System.out.println("==========================================");

        // Force exit to ensure no lingering threads keep JVM alive
        System.exit(failedCount > 0 ? 1 : 0);
    }

    // --- TEST METHOD 1: Invalid Inputs ---
    public static boolean testInputValidation() {
        System.out.print("[Test 3.1] Input Validation (Capacity > 0)... ");

        boolean result = true;
        // Verify valid inputs pass
        if (!Main.isValidCapacity(5))
            result = false;
        // Verify invalid inputs fail
        if (Main.isValidCapacity(0))
            result = false;
        if (Main.isValidCapacity(-5))
            result = false;

        if (result)
            System.out.println("PASSED");
        else
            System.out.println("FAILED");
        return result;
    }

    // --- TEST METHOD 2 & 3: Concurrency Stress &Sync Test ---
    public static boolean testConcurrencyAndDataIntegrity() throws InterruptedException {
        System.out.print("[Test 3.2 & 3.3] Concurrency & Sync (Stress Test)... ");

        // Setup: Transfer 100 items with a tiny buffer (capacity 2)
        // This forces intense context switching.
        int itemCount = 100;
        SimpleBlockingQueue<Integer> queue = new SimpleBlockingQueue<>(2);
        List<Integer> source = new ArrayList<>();
        for (int i = 0; i < itemCount; i++)
            source.add(i);

        List<Integer> dest = Collections.synchronizedList(new ArrayList<>());

        Thread producer = new Thread(() -> {
            try {
                for (Integer item : source)
                    queue.put(item);
                queue.put(-1); // Poison Pill
            } catch (InterruptedException e) {
            }
        });

        Thread consumer = new Thread(() -> {
            try {
                while (true) {
                    Integer item = queue.take();
                    if (item == -1)
                        break;
                    dest.add(item);
                }
            } catch (InterruptedException e) {
            }
        });

        producer.setDaemon(true);
        consumer.setDaemon(true);

        producer.start();
        consumer.start();

        producer.join(2000);
        consumer.join(2000);

        if (dest.size() == itemCount && dest.containsAll(source)) {
            System.out.println("PASSED (Transferred " + dest.size() + " items)");
            return true;
        } else {
            System.out.println("FAILED (Source: " + itemCount + ", Dest: " + dest.size() + ")");
            return false;
        }
    }

    // --- TEST METHOD 4: Producer Blocking ---
    public static boolean testProducerBlocksWhenFull() throws InterruptedException {
        System.out.print("[Test 3.4] Producer Blocks when Full... ");

        SimpleBlockingQueue<Integer> queue = new SimpleBlockingQueue<>(1);
        queue.put(1); // Fill the queue

        Thread t = new Thread(() -> {
            try {
                queue.put(2); // Should block here
            } catch (InterruptedException e) {
                // Expected interruption during exit
            }
        });
        t.setDaemon(true);
        t.start();

        Thread.sleep(100); // Give it time to try and block

        if (t.getState() == Thread.State.WAITING) {
            System.out.println("PASSED (Thread State: WAITING)");
            return true;
        } else {
            System.out.println("FAILED (Thread State: " + t.getState() + ")");
            return false;
        }
    }

    // --- TEST METHOD 5: Consumer Blocking ---
    public static boolean testConsumerBlocksWhenEmpty() throws InterruptedException {
        System.out.print("[Test 3.5] Consumer Blocks when Empty... ");

        SimpleBlockingQueue<Integer> queue = new SimpleBlockingQueue<>(1); // Empty

        Thread t = new Thread(() -> {
            try {
                queue.take(); // Should block here
            } catch (InterruptedException e) {
                // Expected interruption during exit
            }
        });
        t.setDaemon(true);
        t.start();

        Thread.sleep(100);

        if (t.getState() == Thread.State.WAITING) {
            System.out.println("PASSED (Thread State: WAITING)");
            return true;
        } else {
            System.out.println("FAILED (Thread State: " + t.getState() + ")");
            return false;
        }
    }
}
