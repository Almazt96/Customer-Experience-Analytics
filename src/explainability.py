import shap
import matplotlib.pyplot as plt

def generate_text_shap_explanation(model, vectorizer, sample_text: str):
    """
    Generates SHAP values for TF-IDF + Classifier pipelines or HuggingFace transformers.
    """
    # For TF-IDF + Linear Model / Tree Baseline:
    explainer = shap.LinearExplainer(model, vectorizer.transform([sample_text]))
    shap_values = explainer.shap_values(vectorizer.transform([sample_text]))
    
    # Save force plot / summary plot static images for Streamlit rendering
    plt.figure(figsize=(10, 3))
    shap.summary_plot(shap_values, feature_names=vectorizer.get_feature_names_out(), plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig("assets/shap_summary.png")
    plt.close()