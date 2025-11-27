# Testing Strategy & Coverage Report

This document outlines the comprehensive testing strategy implemented for the Producer-Consumer Simulation. The project utilizes a hybrid testing approach, combining a custom-built manual test suite with standard JUnit integration to ensure robust verification of concurrency, data integrity, and application flow.

## 🧪 Testing Architecture

The testing infrastructure is designed to verify both the low-level synchronization primitives and the high-level application behavior.

### 1. The Core Test Suite (`TestSharedQueue.java`)
This is the "brain" of the testing logic. Unlike standard unit tests that mock everything, this suite spins up **real threads** to simulate actual runtime conditions.

*   **Location:** `src/com/assessment/tests/TestSharedQueue.java`
*   **Type:** Integration & System Tests
*   **Mechanism:** It executes a series of scenarios programmatically and returns a boolean success status.

### 2. The CI/CD Wrapper (`WrapperTest.java`)
This acts as the bridge to the Maven build lifecycle.

*   **Location:** `src_test/com/assessment/tests/WrapperTest.java`
*   **Type:** JUnit 4 Wrapper
*   **Mechanism:** It invokes the Core Test Suite and asserts its success. If the custom suite reports a failure, this JUnit test fails, causing the Maven build to fail.

---

## 🎯 What Is Tested?

We have achieved **92.6% Total Code Coverage**, verifying the following critical components:

### ✅ 1. Core Synchronization Logic (`SharedQueue`)
*   **Coverage:** **100%**
*   **Scenarios:**
    *   **Input Validation:** Verifies that the queue rejects invalid capacities (e.g., 0 or negative numbers).
    *   **Blocking (Queue Full):** Proves that a Producer thread enters the `WAITING` state when attempting to write to a full queue.
    *   **Blocking (Queue Empty):** Proves that a Consumer thread enters the `WAITING` state when attempting to read from an empty queue.
    *   **Wait/Notify Mechanism:** Indirectly verified by the successful state transitions of the blocking tests.

### ✅ 2. Concurrency & Data Integrity
*   **Scenarios:**
    *   **Stress Test:** A high-speed transfer of 100 items through a tiny buffer (Capacity: 2).
    *   **Verification:** Ensures that **Order is Preserved** (FIFO) and **No Data is Lost** despite thousands of context switches.

### ✅ 3. Worker Components (`Producer` & `Consumer`)
*   **Coverage:** **~95%**
*   **Scenarios:**
    *   **Real Execution:** Instantiates the actual `Producer.java` and `Consumer.java` classes used in the main app.
    *   **Lifecycle:** Verifies they start, process data, handle the "Poison Pill" shutdown signal, and terminate gracefully.

### ✅ 4. Application Entry Point (`Main`)
*   **Coverage:** **~88%**
*   **Scenarios:**
    *   **End-to-End Simulation:** Simulates user input (injecting "5" into `System.in`) to trigger the full application flow.
    *   **Integration:** Verifies that the `Main` class correctly wires up the Queue, Workers, and Threads.

---

## 🚀 How to Run Tests

### Option 1: Standard Maven Test (Recommended)
This runs the full suite and generates the coverage report.
```bash
mvn clean test
```

### Option 2: Standalone Manual Test
You can run the test suite directly to see the detailed console output without Maven.
```bash
java -cp src:target/classes com.assessment.tests.TestSharedQueue
```

---

## 📊 Coverage Summary (JaCoCo)

| Component | Class | Coverage | Status |
| :--- | :--- | :--- | :--- |
| **Core Logic** | `SharedQueue` | **100%** | ✅ Perfect |
| **Workers** | `Producer` | **95.3%** | ✅ Excellent |
| | `Consumer` | **94.8%** | ✅ Excellent |
| **Application** | `Main` | **88.2%** | ✅ Very High |
| **Test Suite** | `TestSharedQueue` | **85.8%** | ✅ High |

**Total Project Coverage:** **92.6%**
