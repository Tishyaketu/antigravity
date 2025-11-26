Producer-Consumer Simulation (Java 17)
A robust, thread-safe implementation of the classic Producer-Consumer pattern. This project demonstrates core concurrent programming competencies including thread synchronization, blocking queues, and the wait/notify mechanism, built from scratch without high-level concurrent collections.
📂 Project Structure
The project follows a modular package architecture to separate concerns between core logic, workers, application flow, and testing.
src/
└── com/
    └── assessment/
        ├── app/
        │   └── Main.java                 # Entry point, input validation, and simulation driver
        ├── core/
        │   └── SimpleBlockingQueue.java  # Custom thread-safe queue (The Monitor Object)
        ├── workers/
        │   ├── Producer.java             # Runnable task with dynamic processing speed
        │   └── Consumer.java             # Runnable task with dynamic processing speed
        └── tests/
            └── TestBlockingQueue.java    # Comprehensive unit test suite


🎯 What Is Achieved
This solution satisfies all specific testing objectives outlined in the assignment:
1. Thread Synchronization
Achievement: Guaranteed data integrity with zero race conditions.
How: Implemented using Java's intrinsic locks (synchronized blocks) in SimpleBlockingQueue. This ensures that only one thread can access the internal data structure at any given millisecond.
2. Concurrent Programming
Achievement: True parallel execution of data production and consumption.
How: Utilized the Runnable interface to decouple tasks and the Thread class to spawn separate execution stacks.
Dynamic Simulation: Added randomized sleep intervals (context switching) to Producer and Consumer to simulate unpredictable real-world CPU loads.
3. Blocking Queues
Achievement: A finite buffer that halts threads when limits are reached.
How:
Queue Full: The Producer automatically blocks (waits) until space is available.
Queue Empty: The Consumer automatically blocks (waits) until data arrives.
4. Wait/Notify Mechanism
Achievement: Efficient inter-thread communication without busy waiting.
How:
Used Object.wait() to release the lock and suspend threads when the queue state is invalid (Full/Empty).
Used Object.notifyAll() to wake up waiting threads immediately after a state change (Item added/removed).
5. Robustness & Validation
Graceful Shutdown: Implemented the Poison Pill Pattern (Sentinel Value -1) to ensure the Consumer terminates cleanly after processing all data.
Input Validation: The application strictly enforces positive integer input for queue capacity, rejecting invalid or non-numeric inputs to prevent crashes.
🚀 How to Run
Prerequisites: Java Development Kit (JDK) 17 or higher.
Important: Run all commands from the project root folder (producer_consumer_assignment).
Step 1: Compile the Project
Since the project uses a modular structure, compile all packages simultaneously:
javac src/com/assessment/core/*.java src/com/assessment/workers/*.java src/com/assessment/app/*.java src/com/assessment/tests/*.java


Step 2: Run the Simulation
Execute the main application driver. You will be prompted to enter a queue capacity.
java -cp src com.assessment.app.Main


Expected Interaction:
Source Generation: The app generates a random list of unique integers.
User Input: Enter a capacity (e.g., 2).
Observation: Watch the console logs.
See [Queue] FULL messages to verify Producer blocking.
See [Queue] EMPTY messages to verify Consumer blocking.
Completion: The app verifies that Source Data matches Destination Data exactly.
Step 3: Run Unit Tests
Execute the standalone test suite to verify logic requirements.
java -cp src com.assessment.tests.TestBlockingQueue


Test Coverage:
The suite runs 4 specific tests corresponding to the assignment objectives:
✅ 3.1 Input Validation: Verifies rejection of negative/zero inputs.
✅ 3.2/3.3 Concurrency Stress Test: Transfers 100 items through a tiny buffer at max speed to prove data integrity under race conditions.
✅ 3.4 Producer Blocking: Verifies the thread enters WAITING state when the queue is full.
✅ 3.5 Consumer Blocking: Verifies the thread enters WAITING state when the queue is empty.
📊 Sample Output
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


