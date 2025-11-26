# Sales Stream Processor

A functional programming-based stream processing engine built in Python 3. This application ingests, cleans, and analyzes sales data using memory-efficient generators.

## Project Structure
* `src/stream_processor.py`: Custom `Stream` class implementing Map/Filter/Reduce.
* `src/data_loader.py`: Generator-based CSV ingestion.
* `main.py`: Execution entry point for analytical queries.
* `tests/`: Unit tests for the stream logic.

## Dataset Choice & Assumptions
**Selected Dataset:** Amazon Sales Data (`amazon.csv`)
**Reasoning:** I selected this dataset because it represents real-world "dirty" data. The currency fields (e.g., `₹1,099`) and ratings contain non-numeric characters. This provided an opportunity to demonstrate the power of Stream `map` operations for real-time data transformation and cleaning, simulating a realistic ETL pipeline where raw data is never perfect.

## How to Run
1. Navigate to the project root.
2. Run the analysis:
   ```bash
   python3 main.py
3. Run the test suite:
   ```bash
   python3 tests/test_stream.py -v