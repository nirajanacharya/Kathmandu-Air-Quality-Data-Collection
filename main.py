import os
from src.fetch_data import fetch_all_parameters
from src.preprocess import clean_and_pivot

def main():
    print("\n" + "="*60)
    print("  Kathmandu Air Quality Data Collection")
    print("="*60 + "\n")
    
    print("Fetching data from OpenAQ...\n")
    raw_df = fetch_all_parameters()

    if raw_df.empty:
        print("\nERROR: No data fetched. Please check your configuration.")
        return

    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    raw_df.to_csv("data/raw/raw_pollutant_data.csv", index=False)

    print("\nProcessing data...\n")
    processed_df = clean_and_pivot(raw_df)

    processed_df.to_csv("data/processed/final_timeseries_data.csv")


    print("\nSUCCESS! Data saved:")
    print(f"  Raw: data/raw/raw_pollutant_data.csv ({len(raw_df)} records)")
    print(f"  Processed: data/processed/final_timeseries_data.csv ({len(processed_df)} records)")
   
if __name__ == "__main__":
    main()