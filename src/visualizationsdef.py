import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set style for professional, scannable charts
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.titlesize"] = 16


def plot_sentiment_distribution(df):
    """Generates a stacked bar chart showing sentiment distribution by bank."""
    plt.figure(figsize=(10, 6))

    # Pivot data to get counts of sentiment per bank
    sentiment_counts = (
        df.groupby(["bank", "sentiment_score"])
        .size()
        .unstack(fill_value=0)
        .apply(lambda x: x / x.sum() * 100, axis=1)
    )

def plot_rating_distribution(df):
    """Generates a boxplot showing customer ratings distribution per bank."""
    plt.figure(figsize=(9, 6))

    sns.boxplot(
        x="bank",
        y="score",
        data=df,
        palette="Set2",
        hue="bank",
        legend=False,
    )


def plot_top_themes(df):
    """Generates a horizontal bar chart of dominant themes/keywords."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True)

    banks = df["bank"].unique()

    for i, bank in enumerate(banks):
        bank_df = df[df["bank"] == bank]
        # Assuming you have a 'theme' or 'keyword' column from Task 2/3
        top_themes = bank_df["assigned_theme"].value_counts().head(5)

        sns.barplot(
            x=top_themes.values,
            y=top_themes.index,
            ax=axes[i],
            palette="Blues_r",
            hue=top_themes.index,
            legend=False,
        )
        axes[i].set_title(f"Top 5 Customer Themes: {bank}")
        axes[i].set_xlabel("Mention Frequency")
