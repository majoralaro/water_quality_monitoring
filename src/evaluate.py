# src/evaluate.py
import pandas as pd
class WaterQualityEvaluator:
    """Evaluates if water samples meet safe thresholds."""

    def __init__(self, df):
        self.df = df
        self.safe_ph_range = (6.5, 8.5)
        self.max_turbidity = 1.0

    def evaluate_row(self, row):
        """Evaluates a single sensor reading."""
        issues = []

        if pd.isna(row['pH']):
            issues.append("missing pH")
        elif not (self.safe_ph_range[0] <= row['pH'] <= self.safe_ph_range[1]):
            issues.append("pH too high" if row['pH'] > self.safe_ph_range[1] else "pH too low")

        if pd.isna(row['turbidity']):
            issues.append("missing turbidity")
        elif row['turbidity'] > self.max_turbidity:
            issues.append("turbidity too high")

        if issues:
            return f"❌ Unsafe ({', '.join(issues)})"
        else:
            return "✅ Safe"

    def evaluate_all(self):
        """Evaluates all rows and returns results."""
        results = []
        for _, row in self.df.iterrows():
            status = self.evaluate_row(row)
            results.append({
                'sensor_id': row['sensor_id'],
                #'location': row['location'],
                'status': status
            })
        return results
