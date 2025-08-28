import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('data/documents.csv')

print("=== COMPREHENSIVE EDA FOR DOCUMENTS DATASET ===\n")

# Basic dataset info
print("1. BASIC DATASET INFO")
print(f"Total rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Columns: {list(df.columns)}")
print()

# Text length analysis
print("2. TEXT LENGTH ANALYSIS")
df['text_length'] = df['resource'].str.len()
df['word_count'] = df['resource'].str.split().str.len()

print(f"Average text length: {df['text_length'].mean():.0f} characters")
print(f"Median text length: {df['text_length'].median():.0f} characters")
print(f"Min text length: {df['text_length'].min():,} characters")
print(f"Max text length: {df['text_length'].max():,} characters")
print(f"Standard deviation: {df['text_length'].std():.0f} characters")
print()

print(f"Average word count: {df['word_count'].mean():.0f} words")
print(f"Median word count: {df['word_count'].median():.0f} words")
print(f"Min word count: {df['word_count'].min()} words")
print(f"Max word count: {df['word_count'].max():,} words")
print()

# Title analysis
print("3. TITLE ANALYSIS")
df['title_length'] = df['title'].str.len()
print(f"Average title length: {df['title_length'].mean():.1f} characters")
print(f"Median title length: {df['title_length'].median():.1f} characters")
print(f"Min title length: {df['title_length'].min()} characters")
print(f"Max title length: {df['title_length'].max()} characters")
print(f"Unique titles: {df['title'].nunique():,}")
print()

# Profession distribution
print("4. PROFESSION DISTRIBUTION")
print("Top 10 user_professions:")
print(df['user_profession'].value_counts().head(10))
print(f"Total unique professions: {df['user_profession'].nunique()}")
print()

# Write purpose distribution
print("5. WRITE PURPOSE DISTRIBUTION")
print(df['user_write_purpose'].value_counts())
print()

# Text length by profession
print("6. TEXT LENGTH BY PROFESSION")
top_professions = df['user_profession'].value_counts().head(8).index
for prof in top_professions:
    subset = df[df['user_profession'] == prof]
    print(f"{prof}: {len(subset):,} docs, avg {subset['text_length'].mean():.0f} chars")
print()

# Text length by write purpose
print("7. TEXT LENGTH BY WRITE PURPOSE")
for purpose in ['work', 'school', 'personal']:
    subset = df[df['user_write_purpose'] == purpose]
    print(f"{purpose}: {len(subset):,} docs, avg {subset['text_length'].mean():.0f} chars")
print()

# Data quality check
print("8. DATA QUALITY CHECK")
print("Missing values per column:")
print(df.isnull().sum())
print()

# Unique values
print("9. UNIQUE VALUES")
print(f"Unique titles: {df['title'].nunique():,}")
print(f"Unique resource_ids: {df['resource_id'].nunique():,}")
print(f"Unique ids: {df['id'].nunique():,}")
print()

# Text length percentiles
print("10. TEXT LENGTH PERCENTILES")
percentiles = [10, 25, 50, 75, 90, 95, 99]
for p in percentiles:
    print(f"{p}th percentile: {df['text_length'].quantile(p/100):.0f} characters")
print()

# Profession vs KYC profession comparison
print("11. PROFESSION COMPARISON")
print(f"Rows where user_profession != user_kyc_profession: {(df['user_profession'] != df['user_kyc_profession']).sum()}")
print(f"Percentage match: {((df['user_profession'] == df['user_kyc_profession']).sum() / len(df)) * 100:.1f}%")
print()

# Sample of very long and very short texts
print("12. TEXT LENGTH EXTREMES")
print("Shortest texts (top 5 by word count):")
shortest = df.nsmallest(5, 'word_count')[['title', 'word_count', 'user_profession']]
for _, row in shortest.iterrows():
    print(f"  '{row['title']}' ({row['word_count']} words) - {row['user_profession']}")

print("\nLongest texts (top 5 by word count):")
longest = df.nlargest(5, 'word_count')[['title', 'word_count', 'user_profession']]
for _, row in longest.iterrows():
    print(f"  '{row['title']}' ({row['word_count']} words) - {row['user_profession']}")
