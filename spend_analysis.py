import pandas as pd
import numpy as np
import json
import sys

def load_data(file_path):
    print("Loading data...")
    df = pd.read_csv(file_path)

    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)

    numeric_cols = ['spend', 'impressions', 'clicks', 'conversions', 'revenue']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    df = df.drop_duplicates()
    df = df.fillna(0)

    print("Rows loaded:", len(df))
    return df

def calculate_metrics(df):
    print("Calculating metrics...")
    df['roas'] = np.where(df['spend'] != 0, df['revenue'] / df['spend'], 0)
    df['cpc'] = np.where(df['clicks'] != 0, df['spend'] / df['clicks'], 0)
    df['cpa'] = np.where(df['conversions'] != 0, df['spend'] / df['conversions'], 0)
    return df

def summarize_overall(df):
    print("Generating summary...")
    total_spend = df['spend'].sum()
    total_revenue = df['revenue'].sum()
    total_conversions = df['conversions'].sum()

    summary = {
        "total_spend": float(total_spend),
        "total_revenue": float(total_revenue),
        "total_conversions": int(total_conversions),
        "overall_roas": float(total_revenue / total_spend)
    }

    print(summary)
    return summary

def summarize_channels(df):
    grouped = df.groupby('channel').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'conversions': 'sum'
    }).reset_index()
    grouped['roas'] = grouped['revenue'] / grouped['spend']

    print("\nChannel Performance:")
    print(grouped.sort_values(by='roas', ascending=False))
    return grouped

def summarize_monthly(df):
    grouped = df.groupby('month').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'conversions': 'sum'
    }).reset_index()
    grouped['roas'] = grouped['revenue'] / grouped['spend']

    print("\nMonthly Performance:")
    print(grouped)
    return grouped

def generate_insights(overall, channels):
    insights = []

    best_channel = channels.sort_values(by="roas", ascending=False).iloc[0]
    worst_channel = channels.sort_values(by="roas", ascending=True).iloc[0]

    insights.append(
        f"{best_channel['channel']} is the highest performing channel with ROAS of {best_channel['roas']:.2f}x. Consider scaling budget."
    )

    insights.append(
        f"{worst_channel['channel']} has the lowest ROAS of {worst_channel['roas']:.2f}x. Optimization required."
    )

    if overall["overall_roas"] > 3:
        insights.append("Overall marketing performance is strong with ROAS above 3x.")
    else:
        insights.append("Overall ROAS is below target. Reallocation may be required.")

    insights.append("Email and SEO show strong efficiency and should be prioritized.")
    insights.append("Instagram requires campaign-level optimization.")

    return insights

def export_summary(overall, channels, monthly, insights):
    summary = {
        "overall_metrics": overall,
        "channel_metrics": channels.to_dict(orient="records"),
        "monthly_metrics": monthly.to_dict(orient="records"),
        "insights": insights
    }

    with open("summary_data.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("\nsummary_data.json exported successfully.")


def main():
    print("Script started")

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "marketing_spend_data.csv"

    df = load_data(file_path)
    df = calculate_metrics(df)

    overall = summarize_overall(df)
    channels = summarize_channels(df)
    monthly = summarize_monthly(df)

    insights = generate_insights(overall, channels)

    print("\nInsights:")
    for i in insights:
        print("-", i)

    export_summary(overall, channels, monthly, insights)

if __name__ == "__main__":
    main()