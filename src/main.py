# src/main.py
from load_data import load_csv
from clean_data import clean_sensor_data
from evaluate import WaterQualityEvaluator

def main():
    data_path = "data/sensor_data.csv"

    # Step 1: Load
    df = load_csv(data_path)
    if df is None:
        return

    # Step 2: Clean
    df = clean_sensor_data(df)

    # Step 3: Evaluate
    evaluator = WaterQualityEvaluator(df)
    results = evaluator.evaluate_all()

    # Step 4: Print Results
    for r in results:
        print(f" {r['sensor_id']} : {r['status']}")

if __name__ == "__main__":
    main()
