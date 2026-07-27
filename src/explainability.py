import os
import matplotlib.pyplot as plt
import numpy as np
import shap


def generate_text_shap_explanation(
    model, vectorizer, sample_text: str, output_path: str = "assets/shap_summary.png"
) -> str:
    """Generates and saves SHAP feature importance plot for a TF-IDF + Classifier pipeline.

    Args:
        model: Trained linear or tree-based model classifier.
        vectorizer: Fitted TF-IDF / Count vectorizer.
        sample_text (str): Input review text to explain.
        output_path (str): File path to save the generated plot asset.

    Returns:
        str: Path to the saved SHAP figure asset.
    """
    # 1. Ensure output directory exists to avoid FileNotFoundError
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 2. Transform input text to TF-IDF matrix
    X_sample = vectorizer.transform([sample_text])
    feature_names = vectorizer.get_feature_names_out()

    # 3. Create explainer & compute SHAP values
    explainer = shap.LinearExplainer(model, X_sample)
    shap_values = explainer.shap_values(X_sample)

    # Convert sparse matrix to dense array for clear feature mapping
    X_dense = X_sample.toarray()

    # 4. Clear existing matplotlib figures to prevent plot overlaps
    plt.clf()
    plt.close("all")

    # 5. Generate SHAP plot
    # Calling summary_plot directly handles its own figure bounds when show=False
    shap.summary_plot(
        shap_values,
        features=X_dense,
        feature_names=feature_names,
        plot_type="bar",
        show=False,
    )

    # 6. Adjust layout and save figure asset
    fig = plt.gcf()
    fig.set_size_inches(10, 4)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path