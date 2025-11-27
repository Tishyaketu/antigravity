package com.assessment.tests;

import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import com.assessment.core.SharedQueue;

import com.assessment.app.Main;
import java.io.InputStream;

// Custom test harness to verify the Producer-Consumer implementation.
// We use this manual approach to have fine-grained control over thread states and assertions
// which can be tricky with standard unit testing frameworks alone.
public class TestSharedQueue {

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
        runTests();
    }

    // Orchestrates the execution of all unit and integration tests.
    // Returns true only if ALL tests pass.
    public static boolean runTests() throws InterruptedException {
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

        // --- TEST 4.0: Real Workers ---
        boolean workersPass = testRealWorkerClasses();
        results.add(new TestResult("4.0 Real Worker Classes", workersPass));

        // --- TEST 5.0: Main App ---
        boolean mainPass = testMainApp();
        results.add(new TestResult("5.0 Main App Entry", mainPass));

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

        return failedCount == 0;
    }

    // --- TEST METHOD 1: Invalid Inputs ---
    // Verifies that the application correctly rejects invalid configuration (e.g.,
    // negative capacity).
    public static boolean testInputValidation() {
        System.out.print("[Test 3.1] Input Validation (Capacity > 0)... ");

        boolean result = true;
        // Verify valid inputs pass
        if (!Main.isValidCapacity(5))
            result = false;
        // Verify invalid inputs fail (0 and negative numbers)
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

    // --- TEST METHOD 2 & 3: Concurrency Stress & Sync Test ---
    // This is the most critical test. It uses a small buffer (capacity 2) to force
    // frequent context switching between Producer and Consumer.
    // If synchronization is broken, items will be lost or duplicated.
    public static boolean testConcurrencyAndDataIntegrity() throws InterruptedException {
        System.out.print("[Test 3.2 & 3.3] Concurrency & Sync (Stress Test)... ");

        // Setup: Transfer 100 items with a tiny buffer (capacity 2)
        // This forces intense context switching.
        int itemCount = 100;
        SharedQueue<Integer> queue = new SharedQueue<>(2);
        List<Integer> source = new ArrayList<>();
        for (int i = 0; i < itemCount; i++)
            source.add(i);

        // Destination list must be thread-safe for verification
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

        // Verify that every single item was transferred correctly
        if (dest.size() == itemCount && dest.containsAll(source)) {
            System.out.println("PASSED (Transferred " + dest.size() + " items)");
            return true;
        } else {
            System.out.println("FAILED (Source: " + itemCount + ", Dest: " + dest.size() + ")");
            return false;
        }
    }

    // --- TEST METHOD 4: Producer Blocking ---
    // Verifies that the Producer correctly enters the WAITING state when the queue
    // is full.
    // This confirms that `lock.wait()` is being called.
    public static boolean testProducerBlocksWhenFull() throws InterruptedException {
        System.out.print("[Test 3.4] Producer Blocks when Full... ");

        SharedQueue<Integer> queue = new SharedQueue<>(1);
        queue.put(1); // Fill the queue

        Thread t = new Thread(() -> {
            try {
                queue.put(2); // Should block here because capacity is 1
            } catch (InterruptedException e) {
                // Expected interruption during exit
            }
        });
        t.setDaemon(true);
        t.start();

        Thread.sleep(100); // Give it time to try and block

        // Assert that the thread is physically waiting
        if (t.getState() == Thread.State.WAITING) {
            System.out.println("PASSED (Thread State: WAITING)");
            return true;
        } else {
            System.out.println("FAILED (Thread State: " + t.getState() + ")");
            return false;
        }
    }

    // --- TEST METHOD 5: Consumer Blocking ---
    // Verifies that the Consumer correctly enters the WAITING state when the queue
    // is empty.
    public static boolean testConsumerBlocksWhenEmpty() throws InterruptedException {
        System.out.print("[Test 3.5] Consumer Blocks when Empty... ");

        SharedQueue<Integer> queue = new SharedQueue<>(1); // Empty

        Thread t = new Thread(() -> {
            try {
                queue.take(); // Should block here because queue is empty
            } catch (InterruptedException e) {
                // Expected interruption during exit
            }
        });
        t.setDaemon(true);
        t.start();

        Thread.sleep(100);

        // Assert that the thread is physically waiting
        if (t.getState() == Thread.State.WAITING) {
            System.out.println("PASSED (Thread State: WAITING)");
            return true;
        } else {
            System.out.println("FAILED (Thread State: " + t.getState() + ")");
            return false;
        }
    }

    // --- TEST METHOD 6: Real Worker Classes ---
    // Integration test using the actual Producer and Consumer classes to ensure
    // they work together.
    public static boolean testRealWorkerClasses() throws InterruptedException {
        System.out.print("[Test 4.0] Real Producer/Consumer Classes... ");

        List<Integer> source = new ArrayList<>();
        source.add(100);
        source.add(200);
        source.add(300);

        List<Integer> dest = Collections.synchronizedList(new ArrayList<>());
        SharedQueue<Integer> queue = new SharedQueue<>(2);

        com.assessment.workers.Producer producer = new com.assessment.workers.Producer(queue, source);
        com.assessment.workers.Consumer consumer = new com.assessment.workers.Consumer(queue, dest);

        Thread pThread = new Thread(producer);
        Thread cThread = new Thread(consumer);

        pThread.start();
        cThread.start();

        pThread.join(5000);
        cThread.join(5000);

        if (dest.equals(source)) {
            System.out.println("PASSED");
            return true;
        } else {
            System.out.println("FAILED (Dest: " + dest + ")");
            return false;
        }
    }

    // --- TEST METHOD 7: Main Application Entry Point ---
    // Simulates user input to verify the entire application flow via the Main
    // class.
    public static boolean testMainApp() {
        System.out.print("[Test 5.0] Main App Execution... ");

        InputStream originalIn = System.in;
        try {
            // Simulate user typing "5" for capacity
            String input = "5\n";
            System.setIn(new java.io.ByteArrayInputStream(input.getBytes()));

            // Run Main
            Main.main(new String[] {});

            System.out.println("PASSED");
            return true;
        } catch (Exception e) {
            System.out.println("FAILED (" + e.getMessage() + ")");
            e.printStackTrace();
            return false;
        } finally {
            System.setIn(originalIn);
        }
    }
}
