import os
import torch
import torchaudio
import argparse
from fractions import Fraction

def load_wav(file_path: str) -> torch.Tensor:
    """
    Load a WAV file with error handling.

    Args:
        file_path (str): Path to the input WAV file.

    Returns:
        tuple: Tuple containing the waveform tensor and sample rate.
    """
    try:
        waveform, sample_rate = torchaudio.load(file_path)
        print(f"Loaded {file_path} successfully.")
        return waveform, sample_rate
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        raise
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        raise

def add_perturbation(waveform: torch.Tensor, epsilon: float) -> torch.Tensor:
    """
    Add adjustable perturbation to the audio data.

    Args:
        waveform (torch.Tensor): Original audio waveform.
        epsilon (float): Perturbation magnitude.

    Returns:
        torch.Tensor: Perturbed audio waveform.
    """
    perturbation = epsilon * torch.randn_like(waveform)
    perturbed_waveform = waveform + perturbation
    return perturbed_waveform

def save_wav(waveform: torch.Tensor, sample_rate: int, output_path: str) -> None:
    """
    Save the perturbed waveform to a WAV file with error handling.

    Args:
        waveform (torch.Tensor): Perturbed audio waveform.
        sample_rate (int): Sample rate of the audio.
        output_path (str): Path to save the perturbed WAV file.
    """
    try:
        torchaudio.save(output_path, waveform, sample_rate)
        print(f"Saved perturbed audio to {output_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        raise

def perturb_audio(input_path: str, output_path: str, epsilon: float) -> None:
    """
    Complete pipeline to load, perturb, and save audio.

    Args:
        input_path (str): Path to the input WAV file or directory.
        output_path (str): Path to save the perturbed WAV file or directory.
        epsilon (float): Perturbation magnitude.
    """
    if os.path.isfile(input_path):
        try:
            waveform, sample_rate = load_wav(input_path)
            perturbed_waveform = add_perturbation(waveform, epsilon)
            save_wav(perturbed_waveform, sample_rate, output_path)
        except Exception as e:
            print(f"Failed to process {input_path}: {e}")
    elif os.path.isdir(input_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Created output directory: {output_path}")
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith('.wav'):
                    input_file = os.path.join(root, file)
                    relative_path = os.path.relpath(root, input_path)
                    output_dir = os.path.join(output_path, relative_path)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    output_file = os.path.join(output_dir, f"perturbed_{file}")
                    try:
                        waveform, sample_rate = load_wav(input_file)
                        perturbed_waveform = add_perturbation(waveform, epsilon)
                        save_wav(perturbed_waveform, sample_rate, output_file)
                    except Exception as e:
                        print(f"Failed to process {input_file}: {e}")
    else:
        print(f"Error: {input_path} is neither a file nor a directory.")
        raise ValueError("Invalid input path.")

def parse_epsilon(value: str) -> float:
    """
    Parse the epsilon argument to handle both fractional and float inputs.

    Args:
        value (str): Epsilon value as a string (e.g., '4/255' or '0.01').

    Returns:
        float: Parsed epsilon value.

    Raises:
        argparse.ArgumentTypeError: If the input is not a valid number or fraction.
    """
    try:
        # Attempt to parse as a fraction first
        return float(Fraction(value))
    except ValueError:
        try:
            # If fraction parsing fails, try converting directly to float
            return float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid epsilon value: '{value}'. Must be a float or a fraction like '4/255'.")

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Add perturbation to WAV files.")
    parser.add_argument("input_path", type=str, help="Path to the input WAV file or directory.")
    parser.add_argument("output_path", type=str, help="Path to save the perturbed WAV file or directory.")
    parser.add_argument("--epsilon", type=parse_epsilon, default=0.01, help="Perturbation magnitude (e.g., '4/255' or '0.01'). Default is 0.01.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    perturb_audio(args.input_path, args.output_path, args.epsilon)
