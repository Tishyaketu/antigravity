# Java Producer-Consumer Simulation

A robust, thread-safe implementation of the Producer-Consumer pattern in Java 17. This project demonstrates concurrent programming concepts including thread synchronization, blocking queues, and the wait/notify mechanism without using high-level concurrent collections.

## Features
* **Custom Blocking Queue:** Implemented from scratch using `synchronized`, `wait()`, and `notifyAll()` to demonstrate low-level thread management.
* **Dynamic/Randomized Concurrency:** Simulation uses random processing times for Producer and Consumer to guarantee race conditions are tested and both "Queue Full" and "Queue Empty" states are reached naturally.
* **Robust Input Validation:** Ensures user cannot input invalid, negative, or non-numeric queue capacities.
* **Data Integrity Verification:** Uses a "Poison Pill" (Sentinel Value `-1`) pattern to gracefully shut down consumers and validates that Source Data exactly matches Destination Data.
* **Real-time Visualization:** Console logs detail the exact state of the Queue (size/contents), Producer, and Destination List at every step.

## Project Structure
```text
src/
└── com/
    └── assessment/
        ├── SimpleBlockingQueue.java  (The shared monitor with wait/notify)
        ├── Producer.java             (Runnable task with dynamic speed)
        ├── Consumer.java             (Runnable task with dynamic speed)
        ├── Main.java                 (Entry point, validation, and summary)
        └── TestBlockingQueue.java    (Unit tests for blocking logic)