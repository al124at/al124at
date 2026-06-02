# Segmentácia koronálnych štruktúr v sekvencii obrazov slnečnej koróny

This repository contains the practical part of the bachelor thesis **“Segmentácia koronálnych štruktúr v sekvencii obrazov slnečnej koróny”**.

The work compares the reference **SCSS-Net** model with the proposed **ConvLSTM-SCSS-Net** architecture. SCSS-Net is used as a baseline model that processes one image, while ConvLSTM-SCSS-Net processes a short sequence of temporally close solar corona images.

The goal is to evaluate whether temporal context from sequnces of images can improve the segmentation of coronal structures.

## Repository structure

```text
src/                 model definitions and metrics
notebooks/           standard pipeline notebooks
trained_models/      trained SCSS-Net and ConvLSTM-SCSS-Net models
data/                compact prediction datasets
outputs/             generated outputs after running notebooks
requirements.txt     Python dependencies
```

## Models

Two models are included:

* **SCSS-Net** — baseline model working with a single image;
* **ConvLSTM-SCSS-Net** — proposed model working with a sequence of images.

The standard sequence contains three previous frames and the current target frame:

```text
input_1, input_2, input_3, target image
```

The model then predicts the segmentation mask for the target image.

## Data

The full training datasets are not included because of their size.

Instead, the repository contains compact final prediction datasets:

```text
data/CH_predict_2021/
data/AR_predict_2021/
```

These datasets are used to demonstrate the final prediction and post-processing pipeline with already trained models.

## Notebooks

The repository contains two main notebooks:

```text
notebooks/CH_demo.ipynb
notebooks/AR_demo_final.ipynb
```

Both notebooks keep the structure of the full standard pipeline:

1. setup and configuration;
2. data discovery;
3. temporal sequence preparation;
4. preprocessing and generators;
5. model construction;
6. training stage placeholder;
7. loading of trained models;
8. final prediction;
9. post-processing;
10. visual and numerical comparison.

The full training stage is disabled by default because the full training dataset is not included. Instead, the notebooks load trained models from:

```text
trained_models/
```

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Open Jupyter Notebook:

```bash
jupyter notebook
```

Then run one of the notebooks from the `notebooks/` folder.

The notebooks use relative paths, so the repository should keep this structure:

```text
src/
notebooks/
trained_models/
data/
```

During execution, the ZIP files from `data/` are automatically unpacked, trained models are loaded, and predictions are saved to:

```text
outputs/
```

## Output

The notebooks generate:

* predicted binary masks;
* visual comparison images;
* overlay comparison images;
* CSV files with metrics;
* run configuration files.

Overlay colors:

```text
red    = baseline only
cyan   = ConvLSTM only
yellow = both models
```

## Notes

The repository is intended to demonstrate the practical pipeline and final prediction process. Full training from scratch requires the original full datasets, which are not included in this repository.
