# Prerequisites

- OpenAI key in `key.txt`
- Conda environment
- OpenAI python package

# Usage

```bash
conda activate
```

## Perturb audio

```bash
python .\perturb_audio.py  .\data\commonvoice_subset\ .\data\perturbed_1_255\ --epsilon 1/255
```

## Run audio transcription

```bash
python main.py
```

## Compute statistics

```bash
python .\compute_wer.py ground_truth.json predictions.json
```
