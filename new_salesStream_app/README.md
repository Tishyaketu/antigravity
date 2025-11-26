# Amazon Product Stream Analysis

A high-performance, memory-efficient data processing pipeline built in Python 3. This application demonstrates **Functional Programming** paradigms to analyze Amazon sales data, implementing a custom Stream API powered by Python Generators.

## 📌 Project Overview

This project solves the challenge of analyzing raw, unstructured sales data ("dirty data") without relying on heavy external libraries like Pandas. Instead, it implements a custom **ETL (Extract, Transform, Load)** engine that processes data lazily.

### Key Capabilities:
- **Ingestion**: Reads raw CSV data containing currency symbols, percentage signs, and formatting errors.
- **Cleaning**: Real-time sanitization of prices and ratings using pure functions.
- **Analysis**: Computes complex aggregations (Revenue, Category Averages, Top Discounts) using declarative stream chains.

---

## 🚀 Technical Architecture (The "How")

This solution adheres to strict software engineering principles:

### 1. Functional Programming (FP)
- **Immutability**: All data is modeled using frozen `@dataclass` structures (`src/sales_analysis/core/models.py`). Once a Product is created, it cannot be altered.
- **Pure Functions**: All cleaning logic (`ingestion/cleaning.py`) is deterministic and side-effect-free.
- **Declarative Style**: Logic is expressed as chains (`.map().filter().reduce()`) rather than imperative loops.

### 2. Stream Operations & Lazy Evaluation
- **Generators**: The core `Stream` class (`core/stream.py`) uses Python's `yield` keyword. Data flows through the pipeline one item at a time.
- **Memory Efficiency**: The memory complexity is **O(1)**. Whether the input file is 1MB or 100GB, the RAM usage remains constant because the dataset is never fully loaded into memory (except for specific sorting operations).

### 3. Lambda Expressions
- Anonymous functions are used extensively for passing behavior into the stream engine (e.g., `lambda p: p.discounted_price`).

---

## 📂 Project Structure

The project follows a modular, enterprise-grade directory structure:

```
.
├── run.py                          # Entry point (Bootstraps the application)
├── data/
│   └── amazon.csv                  # Input dataset
├── src/
│   └── sales_analysis/
│       ├── app.py                  # Business Logic (The Analytical Queries)
│       ├── core/                   # Domain Layer (Reusable Code)
│       │   ├── models.py           # Immutable Data Structures
│       │   └── stream.py           # The Custom Stream Engine
│       └── ingestion/              # Data Layer (ETL)
│           ├── cleaning.py         # Parsing Utilities
│           └── loader.py           # CSV Generator
└── tests/
    ├── test_app.py                 # Integration tests for the main application
    ├── test_ingestion.py           # Tests for data cleaning and loading
    ├── test_models.py              # Tests for data models
    └── test_stream.py              # Core Stream engine tests
```

---

## 🛠️ Setup & Prerequisites

### Prerequisites
- Python 3.8 or higher.
- No external dependencies (Standard Library only).
- Optional: `coverage` for running test coverage reports (`pip install coverage`).

### Installation
1. Clone/Download the repository.
2. **Verify Data**: Ensure `amazon.csv` is located inside the `data/` folder.
   > *Note: I selected this dataset because it contains realistic "dirty" data (e.g., "£1,099", "64%"), requiring robust preprocessing logic.*

---

## 💻 How to Run

### 1. Run the Analysis Report
Execute the entry script from the root directory. This will trigger the full ETL pipeline and print the report to the console.

```bash
python3 run.py
```

**Expected Output:**
You will see a structured report containing:
- **Key Financial Metrics**: Total Revenue and Customer Savings.
- **Category Analysis**: Average ratings grouped by category.
- **Top Discounts**: A sorted list of the unique top 5 deals (deduplicated).
- **Verified Hits**: High-quality products (Rating > 4.5) with high review counts.

### 2. Run the Test Suite
Verify the integrity of the stream engine, cleaning logic, and data models using the automated test suite.

```bash
python3 -m unittest discover -s tests -v
```

---

## 🧪 Testing Strategy & Coverage

This project maintains **100% code coverage** through a comprehensive suite of unit and integration tests.

### Test Suite Breakdown

| Component | Test File | Description |
| :--- | :--- | :--- |
| **Core Logic** | `tests/test_stream.py` | Tests all stream operations (`map`, `filter`, `reduce`, etc.) using deterministic in-memory data. |
| **Ingestion** | `tests/test_ingestion.py` | Tests cleaning logic edge cases and mocks file loading to ensure robustness against missing/bad files. |
| **Models** | `tests/test_models.py` | Verifies data model integrity and computed properties. |
| **Integration** | `tests/test_app.py` | Mocks the data source to test the full end-to-end application flow and reporting. |

### Checking Code Coverage

To verify the 100% coverage claim:

1. **Run Analysis**:
   ```bash
   python3 -m coverage run --source=src -m unittest discover -s tests -v
   ```

2. **View Report**:
   ```bash
   python3 -m coverage report -m
   ```

**Current Status:**
- `core/stream.py`: **100%**
- `core/models.py`: **100%**
- `ingestion/cleaning.py`: **100%**
- `ingestion/loader.py`: **100%**
- `app.py`: **100%**
