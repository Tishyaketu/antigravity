# 🛠️ Intuit Build Challenge: Combined Solutions

This document combines the technical READMEs for the two required assignments in the Intuit Build Challenge, demonstrating proficiency in **Concurrent Programming (Assignment 1)** and **Functional Programming/Data Analysis (Assignment 2)**.

---

## 💻 Assignment 1: Producer-Consumer Simulation (Java 17)

This project is a robust, thread-safe implementation of the classic Producer-Consumer pattern. It is built in Java 17 and demonstrates core concurrent programming competencies, including thread synchronization and the wait/notify mechanism, built from scratch without high-level concurrent collections.

### 🎯 What Is Achieved

This solution satisfies all specific testing objectives outlined for Assignment 1:

- **Thread Synchronization**: Guaranteed data integrity with zero race conditions. This is implemented using Java's intrinsic locks (`synchronized` blocks) in `SimpleBlockingQueue`.
- **Concurrent Programming**: Achieved true parallel execution of data production and consumption. This utilized the `Runnable` interface to decouple tasks and the `Thread` class to spawn separate execution stacks.
- **Blocking Queues**: Implemented a finite buffer that automatically halts threads when limits are reached. The Producer blocks (`wait()`) when the queue is full, and the Consumer blocks (`wait()`) when the queue is empty.
- **Wait/Notify Mechanism**: Used `Object.wait()` to release the lock and suspend threads when the queue state is invalid (Full/Empty), and `Object.notifyAll()` to wake up waiting threads after a state change (Item added/removed).
- **Robustness**: Implemented the Poison Pill Pattern (Sentinel Value -1) for graceful consumer shutdown and strict input validation for queue capacity.

### 📂 Project Structure (Assignment 1)

```plaintext
producer_consumer_assignment/
├── pom.xml
├── src/
│   └── com/assessment/
│       ├── app/
│       │   └── Main.java                 # Entry point and simulation driver
│       ├── core/
│       │   └── SimpleBlockingQueue.java  # Custom thread-safe queue (The Monitor Object)
│       └── workers/
│           ├── Producer.java             # Runnable task
│           └── Consumer.java             # Runnable task
└── tests/
    └── com/assessment/tests/
        └── TestBlockingQueue.java      # Comprehensive test suite
```

### 🚀 How to Run (Assignment 1)

**Prerequisites**: Java Development Kit (JDK) 17 or higher, Maven 3.x.

#### Run the Application (Recommended):

```bash
mvn exec:java -Dexec.mainClass="com.assessment.app.Main"
```

#### Run Unit Tests & Coverage:

```bash
mvn clean test
```

**Coverage Status**: ~93% (Verified by JaCoCo).

---

## 📊 Assignment 2: Amazon Product Stream Analysis (Python 3)

This project solves the data analysis challenge using Python 3 and demonstrates proficiency with Functional Programming paradigms by implementing a custom, memory-efficient Stream API powered by Python Generators. The goal is to analyze raw, unstructured sales data ("dirty data") without relying on heavy external libraries like Pandas.

### 🎯 What Is Achieved

This solution satisfies all specific testing objectives outlined for Assignment 2:

- **Functional Programming & Stream Operations**: Logic is expressed as declarative stream chains (`.map().filter().reduce()`), using pure functions for all cleaning logic. All data is modeled using immutable `@dataclass` structures.
- **Lazy Evaluation (Memory Efficiency)**: The custom `Stream` class (`core/stream.py`) uses Python's `yield` keyword (Generators). Data is processed one item at a time, resulting in O(1) memory complexity, as the dataset is never fully loaded into memory.
- **Data Aggregation**: Performs various aggregation and grouping operations on sales data. This includes computing Total Revenue, Category Averages, and Top Discounts.
- **Lambda Expressions**: Anonymous functions are used extensively for passing behavior into the stream engine (e.g., as predicates for filtering or functions for mapping).
- **ETL Pipeline**: Includes robust real-time cleaning logic to sanitize "dirty" data (currency symbols, percentage signs) from the `amazon.csv` dataset.

### 📂 Project Structure (Assignment 2)

```plaintext
.
├── run.py                          # Entry point (Bootstraps the application)
├── data/
│   └── amazon.csv                  # Input dataset
├── src/
│   └── sales_analysis/
│       ├── app.py                  # Business Logic (The Analytical Queries)
│       ├── core/                   # Domain Layer
│       │   ├── models.py           # Immutable Data Structures (@dataclass)
│       │   └── stream.py           # The Custom Stream Engine
│       └── ingestion/              # Data Layer (ETL)
│           ├── cleaning.py         # Parsing Utilities (Pure Functions)
│           └── loader.py           # CSV Generator
└── tests/
    ├── test_app.py                 # Integration tests
    └── ...                         # Unit tests
```

### 🚀 How to Run (Assignment 2)

**Prerequisites**: Python 3.8 or higher (Standard Library only).

#### Run the Analysis Report:

```bash
python3 run.py
```

#### Run the Test Suite:

```bash
python3 -m unittest discover -s tests -v
```

#### Check Code Coverage:

```bash
python3 -m coverage run --source=src -m unittest discover -s tests -v
python3 -m coverage report -m
```

**Coverage Status**: 100%.