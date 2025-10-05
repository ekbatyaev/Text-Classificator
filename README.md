# 🧠 Text-Classificator

A **Siamese-based multi-text classification system** that leverages **sentence embeddings** to perform **semantic comparison and classification of text pairs**.

This project provides an efficient and powerful framework for comparing the meaning of two text inputs and classifying their relationship (e.g., duplicate, entailment, contradiction, or simple classification).

-----

## ✨ Key Features

  * **Siamese Network Architecture:** Utilizes a Siamese neural network, which is ideal for learning a similarity metric between text inputs rather than relying on fixed classification categories.
  * **Sentence Embeddings:** Employs state-of-the-art techniques for generating dense sentence embeddings (vectors) to capture the semantic meaning of the text.
  * **Multi-Text Classification:** Designed specifically for tasks that require the classification of *pairs* of texts, such as:
      * Paraphrase Identification
      * Natural Language Inference (NLI)
      * Duplicate Question Detection
  * **Containerization:** Includes a `Dockerfile` for easy deployment and reproducible environments.
  * **Extensive Training Notebook:** Provides a `training.ipynb` Jupyter Notebook for model development, experimentation, and fine-tuning.

-----

## 🛠️ Installation and Setup

Follow these steps to get a local copy of the project running.

### Prerequisites

  * Python 3.8+
  * `pip` (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ekbatyaev/Text-Classificator.git
cd Text-Classificator
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# .\venv\Scripts\activate # On Windows (PowerShell)
```

### Step 3: Install Dependencies

All necessary Python packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

-----

## 🚀 Usage

The project is split into two main components: training/experimentation and the classification application.

### 1\. Model Training and Experimentation

The `training.ipynb` notebook contains the full pipeline for:

  * Loading and preprocessing your paired-text dataset.
  * Defining and configuring the Siamese network model.
  * Training the model using sentence embeddings.

To run the notebook, ensure you have Jupyter installed (it is likely included in `requirements.txt`) and run:

```bash
jupyter notebook training.ipynb
```

### 2\. Running the Classification Application

The `app.py` script is the main entry point for using the trained model to classify new text pairs.

Assuming you have a trained model saved, you can run the application (details will depend on the implementation inside `app.py`):

```bash
python app.py --text1 "The quick brown fox." --text2 "A swift reddish-brown animal."
```

*(Note: Consult the `app.py` file for exact command-line arguments and required inputs.)*

-----

## 🐳 Containerization (Docker)

The project includes a `Dockerfile` to create a portable environment, ensuring consistent performance across different machines.

### Build the Docker Image

```bash
docker build -t text-classificator-image .
```

### Run the Container

You can run the application inside the container:

```bash
docker run text-classificator-image
```

*(Note: You may need to add volume mounts (`-v`) to provide input data or load a trained model depending on the application's needs.)*

-----

## ⚖️ License

This project is licensed under the **MIT License**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
