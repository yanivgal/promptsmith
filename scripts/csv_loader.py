#!/usr/bin/env python3
"""
Shared module for loading and selecting examples from CSV files.
Used by refinement scripts to avoid code duplication.
"""

import pandas as pd
import random
from pathlib import Path
from typing import List, Dict, Any

def load_and_select_document_examples(csv_path: Path, num_examples: int = 5, random_seed: int = 42) -> List[Dict[str, Any]]:
    """
    Load the CSV file and select random examples.
    
    Args:
        csv_path: Path to the CSV file
        num_examples: Number of examples to select
        random_seed: Random seed for reproducibility
    
    Returns:
        List of dictionaries containing the selected examples
    """
    
    random.seed(random_seed)
    
    print(f"Loading CSV file: {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Loaded {len(df)} examples")
    print(f"Columns: {list(df.columns)}")
    print(f"Selecting {num_examples} random example(s) (seed={random_seed})...")
    
    selected_indices = random.sample(range(len(df)), min(num_examples, len(df)))
    selected_examples = df.iloc[selected_indices]
    
    examples = []
    for idx, row in selected_examples.iterrows():
        example = {
            'index': idx,
            'original_id': row.get('id', ''),
            'title': row.get('title', 'Untitled'),
            'text': row.get('resource', ''),
            'profession': row.get('user_profession', 'Unknown'),
            'purpose': row.get('user_write_purpose', 'Unknown')
        }
        examples.append(example)
    
    return examples

def get_default_csv_path() -> Path:
    """
    Get the default path to the documents_train.csv file.
    
    Returns:
        Path to the CSV file
    """
    return Path("data/documents_train.csv") 