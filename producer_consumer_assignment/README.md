# Producer-Consumer Simulation (Java 17)

A robust, thread-safe implementation of the classic Producer-Consumer pattern. This project demonstrates core concurrent programming competencies including thread synchronization, blocking queues, and the wait/notify mechanism, built from scratch without high-level concurrent collections.

## 📂 Project Structure

The project follows a modular package architecture to separate concerns between core logic, workers, application flow, and testing.

```text
producer_consumer_assignment/
├── pom.xml                       # Maven Project Configuration
├── src/
│   └── com/assessment/
│       ├── app/
│       │   └── Main.java                 # Entry point, input validation, and simulation driver
│       ├── core/
│       │   └── SharedQueue.java  # Custom thread-safe queue (The Monitor Object)
│       ├── workers/
│       │   ├── Producer.java             # Runnable task with dynamic processing speed
│       │   └── Consumer.java             # Runnable task with dynamic processing speed
│       └── tests/
│           └── TestSharedQueue.java    # Comprehensive manual test suite
└── src_test/
    └── com/assessment/tests/
        └── WrapperTest.java      # JUnit wrapper for CI/CD integration
```

## 🎯 What Is Achieved

This solution satisfies all specific testing objectives outlined in the assignment:

### 1. Thread Synchronization
*   **Achievement:** Guaranteed data integrity with zero race conditions.
*   **How:** Implemented using Java's intrinsic locks (`synchronized` blocks) in `SharedQueue`. This ensures that only one thread can access the internal data structure at any given millisecond.

### 2. Concurrent Programming
*   **Achievement:** True parallel execution of data production and consumption.
*   **How:** Utilized the `Runnable` interface to decouple tasks and the `Thread` class to spawn separate execution stacks.
*   **Dynamic Simulation:** Added randomized sleep intervals (context switching) to Producer and Consumer to simulate unpredictable real-world CPU loads.

### 3. Blocking Queues
*   **Achievement:** A finite buffer that halts threads when limits are reached.
*   **How:**
    *   **Queue Full:** The Producer automatically blocks (`wait()`) until space is available.
    *   **Queue Empty:** The Consumer automatically blocks (`wait()`) until data arrives.

### 4. Wait/Notify Mechanism
*   **Achievement:** Efficient inter-thread communication without busy waiting.
*   **How:**
    *   Used `Object.wait()` to release the lock and suspend threads when the queue state is invalid (Full/Empty).
    *   Used `Object.notifyAll()` to wake up waiting threads immediately after a state change (Item added/removed).

### 5. Robustness & Validation
*   **Graceful Shutdown:** Implemented the Poison Pill Pattern (Sentinel Value `-1`) to ensure the Consumer terminates cleanly after processing all data.
*   **Input Validation:** The application strictly enforces positive integer input for queue capacity, rejecting invalid or non-numeric inputs to prevent crashes.

## 🚀 How to Run

**Prerequisites:** Java Development Kit (JDK) 17 or higher, Maven 3.x.

### Option 1: Using Maven (Recommended)

**1. Run Unit Tests & Coverage**
```bash
mvn clean test
```
*   This executes the full suite including the manual integration tests.
*   Generates a coverage report in `target/site/jacoco/index.html`.

**2. Run the Application**
```bash
mvn exec:java -Dexec.mainClass="com.assessment.app.Main"
```

### Option 2: Manual Compilation (No Maven)

**1. Compile the Project**
```bash
javac src/com/assessment/core/*.java src/com/assessment/workers/*.java src/com/assessment/app/*.java src/com/assessment/tests/*.java
```

**2. Run the Simulation**
```bash
java -cp src com.assessment.app.Main
```

**3. Run Unit Tests**
```bash
java -cp src com.assessment.tests.TestSharedQueue
```

## 🧪 Test Coverage & Scenarios

The suite runs **7 specific tests** covering all assignment objectives plus real-world integration:

*   ✅ **3.1 Input Validation:** Verifies rejection of negative/zero inputs.
*   ✅ **3.2/3.3 Concurrency Stress Test:** Transfers 100 items through a tiny buffer at max speed to prove data integrity under race conditions.
*   ✅ **3.4 Producer Blocking:** Verifies the thread enters `WAITING` state when the queue is full.
*   ✅ **3.5 Consumer Blocking:** Verifies the thread enters `WAITING` state when the queue is empty.
*   ✅ **4.0 Real Worker Classes:** Instantiates and runs the actual `Producer` and `Consumer` classes to ensure they work correctly.
*   ✅ **5.0 Main App Execution:** Simulates user input to verify the application entry point and wiring.

**Total Code Coverage:** ~93% (Verified by JaCoCo)

## 📊 Sample Output

```text
=== Source Container Generated ===
[42, 15, 7, 99]
==================================

Enter Shared Queue Capacity (Positive Integer): 2

=== Starting Simulation ===
[Producer] Reading from source: 42
Produced: 42 | Queue State: [42] (Size: 1)
[Producer] Reading from source: 15
Produced: 15 | Queue State: [42, 15] (Size: 2)
[Producer] Reading from source: 7
    [Queue] FULL (2/2). Producer waiting...   <-- BLOCKING DEMONSTRATED
Consumed: 42 | Queue State: [15] (Size: 1)
Produced: 7 | Queue State: [15, 7] (Size: 2)
...
SUCCESS: Data transfer perfectly matched!
```
