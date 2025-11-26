# Testing Strategy & Coverage Report

This project maintains **100% code coverage** through a comprehensive suite of unit and integration tests. We use Python's built-in `unittest` framework for testing and `coverage.py` for coverage analysis.

## 🧪 Test Suite Breakdown

The test suite is modularized to target specific layers of the application architecture:

### 1. Core Logic (`tests/test_stream.py`)
**Target:** `src/sales_analysis/core/stream.py`
- **What is tested:** 
  - All stream operations: `map`, `filter`, `distinct`, `sorted`, `group_by`, `reduce`.
  - Lazy evaluation mechanics (generators).
  - Chained operations (e.g., `filter` -> `map` -> `reduce`).
- **Methodology:** Uses deterministic in-memory data to verify logic without external dependencies.

### 2. Data Ingestion (`tests/test_ingestion.py`)
**Target:** `src/sales_analysis/ingestion/`
- **What is tested:**
  - **Cleaning Logic:** Edge cases for currency parsing, percentage conversion, and dirty data handling (e.g., `clean_currency`, `clean_rating`).
  - **File Loading:** Verifies `csv_reader` handles missing files gracefully and parses valid CSV rows correctly.
- **Methodology:** Uses `unittest.mock` to simulate file system operations (`mock_open`, `os.path.exists`), ensuring tests run fast and don't require real files.

### 3. Data Models (`tests/test_models.py`)
**Target:** `src/sales_analysis/core/models.py`
- **What is tested:**
  - Immutable `Product` data class.
  - Computed properties like `savings` (Actual Price - Discounted Price).
- **Methodology:** Unit tests on object instantiation and property access.

### 4. Application Integration (`tests/test_app.py`)
**Target:** `src/sales_analysis/app.py`
- **What is tested:**
  - The full "End-to-End" flow of the application.
  - Verifies that all reports (Revenue, Categories, Top Discounts) are generated and printed.
- **Methodology:** Mocks the data source (`csv_reader`) to provide a controlled stream of products and captures `sys.stdout` to verify the final report output.

---

## 🚀 How to Run Tests

### Prerequisites
Ensure you have the coverage tool installed:
```bash
pip install coverage
```

### Running the Suite
To run all tests and see a simple pass/fail status:
```bash
python3 -m unittest discover -s tests
```

---

## 📊 Checking Code Coverage

We aim for **100% coverage** to ensure every line of code, including error handling and edge cases, is verified.

### 1. Run Coverage Analysis
Execute the tests while monitoring code usage:
```bash
python3 -m coverage run --source=src -m unittest discover -s tests
```

### 2. View Report
Display the coverage percentage in the terminal:
```bash
python3 -m coverage report -m
```

### Current Status (as of latest run)
| File | Coverage | Status |
| :--- | :--- | :--- |
| `core/stream.py` | **100%** | ✅ Verified |
| `core/models.py` | **100%** | ✅ Verified |
| `ingestion/cleaning.py` | **100%** | ✅ Verified |
| `ingestion/loader.py` | **100%** | ✅ Verified |
| `app.py` | **100%** | ✅ Verified |
