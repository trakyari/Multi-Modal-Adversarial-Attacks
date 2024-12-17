import json
import argparse
from typing import List
from jiwer import wer, cer

# Function to load JSON files


def load_json(file_path: str):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

# Function to compute WER for all transcriptions


def compute_wer(ground_truth_file: str, comparison_file: str):
    """Compute Word Error Rate (WER) between ground truth and comparison transcriptions."""
    # Load the JSON files
    ground_truth_data = load_json(ground_truth_file)
    comparison_data = load_json(comparison_file)

    if not ground_truth_data or not comparison_data:
        print("Failed to load files.")
        return

    # Check for data consistency
    if len(ground_truth_data) != len(comparison_data):
        print("Warning: The two JSON files have different lengths.")

    total_wer = 0
    total_cer = 0
    total_entries = len(ground_truth_data)

    for i, (gt, cmp) in enumerate(zip(ground_truth_data, comparison_data)):
        gt_transcription = gt.get('transcription', '')
        cmp_transcription = cmp.get('transcription', '')

        # Compute WER for the current pair
        entry_wer = wer(gt_transcription, cmp_transcription)
        print(f"Entry {i+1}: WER = {entry_wer:.2%}")

        entry_cer = cer(gt_transcription, cmp_transcription)
        print(f"Entry {i+1}: CER = {entry_cer:.2%}")

        total_wer += entry_wer
        total_cer += entry_cer

    # Compute the average WER across all entries
    average_wer = total_wer / total_entries if total_entries > 0 else 0
    average_cer = total_cer / total_entries if total_entries > 0 else 0
    print(f"\nAverage WER: {average_wer:.2%}")
    print(f"Average CER: {average_cer:.2%}")


# Main function to handle arguments


def main():
    parser = argparse.ArgumentParser(
        description="Compute Word Error Rate (WER) between two JSON files.")
    parser.add_argument("ground_truth_file", type=str,
                        help="Path to the ground truth JSON file.")
    parser.add_argument("comparison_file", type=str,
                        help="Path to the comparison JSON file.")

    args = parser.parse_args()

    compute_wer(args.ground_truth_file, args.comparison_file)


# Entry point
if __name__ == "__main__":
    main()
