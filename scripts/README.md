# Refinement Scripts with Data Collection

This directory contains scripts for running refinement processes on examples from the documents_train.csv file, with comprehensive data collection and analysis capabilities.

## Files Overview

### Core Scripts
- **`refine_on_x_examples.py`** - Main script to run refinement on any number of examples
- **`csv_loader.py`** - Shared module for loading and selecting examples from CSV
- **`refinement_data_collector.py`** - Data structures and collection logic
- **`enhanced_orchestrator.py`** - Enhanced orchestrator with detailed data collection
- **`refinement_analyzer.py`** - Analysis utilities for the collected data

## Usage

### Running Refinement

```bash
# Run on 1 example (default)
python scripts/refine_on_x_examples.py

# Run on 5 examples
python scripts/refine_on_x_examples.py -n 5

# Run on 10 examples with custom output file
python scripts/refine_on_x_examples.py -n 10 -o my_results.txt

# Run on 3 examples with custom random seed
python scripts/refine_on_x_examples.py -n 3 --seed 123

# Get help
python scripts/refine_on_x_examples.py --help
```

### Command Line Options

- `-n, --num_examples`: Number of examples to process (default: 1)
- `-o, --output`: Output file name (default: refinement_results.txt)
- `--seed`: Random seed for reproducibility (default: 42)

### Output Files

The script generates two output files:

1. **`refinement_results.csv`** - Detailed data in long format with all iterations
2. **`refinement_results.txt`** - Summary report with final results

## CSV Data Structure

The CSV file uses a **long format** where each row represents one iteration of one example:

| Column | Description |
|--------|-------------|
| `example_id` | Unique identifier for the example |
| `title` | Title of the example |
| `profession` | Profession of the author |
| `purpose` | Writing purpose |
| `original_text_length` | Length of input text |
| `iteration_number` | Iteration number (1, 2, 3, ...) |
| `structure_score` | Structure judge score |
| `coverage_score` | Coverage judge score |
| `focus_relevance_score` | Focus/Relevance judge score |
| `redundancy_score` | Redundancy judge score |
| `combined_score` | Weighted combined score |
| `structure_reasoning` | Structure judge reasoning |
| `coverage_reasoning` | Coverage judge reasoning |
| `focus_relevance_reasoning` | Focus/Relevance judge reasoning |
| `redundancy_reasoning` | Redundancy judge reasoning |
| `output` | Generated output for this iteration |
| `refinement_reasoning` | Refiner's reasoning for changes |
| `is_final_iteration` | Whether this is the final iteration |
| `converged_early` | Whether refinement stopped before max iterations |
| `total_iterations` | Total iterations for this example |
| `current_best_score` | Current best score achieved by this example so far |

## Analysis Capabilities

### Using the Analyzer

```bash
# Analyze results and print summary report
python scripts/refinement_analyzer.py refinement_results.csv

# Generate plots
python scripts/refinement_analyzer.py refinement_results.csv --plot

# Show detailed process for specific example
python scripts/refinement_analyzer.py refinement_results.csv --example-id example_001
```

### Query Examples

The long format supports various analytical queries:

#### 1. View entire refinement process of one example:
```python
example_data = df[df['example_id'] == 'example_001'].sort_values('iteration_number')
```

#### 2. Plot average scores across iterations (trend analysis):
```python
avg_scores = df.groupby('iteration_number').agg({
    'combined_score': 'mean',
    'structure_score': 'mean',
    'coverage_score': 'mean'
}).reset_index()
```

#### 3. Compare final scores across examples:
```python
final_scores = df[df['is_final_iteration'] == True][['example_id', 'current_best_score']]
```

#### 4. Find examples that needed most iterations:
```python
iterations_needed = df.groupby('example_id')['iteration_number'].max().sort_values(ascending=False)
```

#### 5. Analyze which judge is most critical:
```python
judge_performance = df[['structure_score', 'coverage_score', 'focus_relevance_score', 'redundancy_score']].mean()
```

#### 6. Find examples that improved most:
```python
improvement = df.groupby('example_id').agg({
    'combined_score': lambda x: x.iloc[-1] - x.iloc[0]
}).sort_values('combined_score', ascending=False)
```

## Benefits of This Structure

- **Scalable**: Works with any number of iterations without changing column structure
- **Analyzable**: Easy to analyze trends across iterations
- **Standard**: Follows database normalization principles
- **Flexible**: Can easily add new judges or metrics
- **Query-friendly**: Supports all common analytical queries
- **Plot-ready**: Perfect for trend analysis and visualization

## Example Workflow

1. **Run refinement on examples:**
   ```bash
   python scripts/refine_on_x_examples.py -n 5
   ```

2. **Analyze the results:**
   ```bash
   python scripts/refinement_analyzer.py refinement_results.csv --plot
   ```

3. **Examine specific examples:**
   ```bash
   python scripts/refinement_analyzer.py refinement_results.csv --example-id example_001
   ```

4. **Load into pandas for custom analysis:**
   ```python
   import pandas as pd
   df = pd.read_csv('refinement_results.csv')
   
   # Custom analysis here...
   ``` 