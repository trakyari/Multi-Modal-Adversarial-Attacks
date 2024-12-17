# Prerequisites

- OpenAI key in `key.txt`
- Conda environment
- OpenAI python package

# Usage

```bash
conda activate
python main.py
```

## Perturb audio

```bash
python .\perturb_audio.py  .\data\commonvoice_subset\ .\data\perturbed_1_255\ --epsilon 1/255
```

# Results

50db distortion - no success
35db distortion - no success
20db distortion - success