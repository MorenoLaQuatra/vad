# VAD - simple voice activity detection in Python

This is a simple voice activity detection (VAD) algorithm in Python. It is based on simple energy-based thresholding and is intended to be used as a simple method for detecting speech in audio files when other methods cannot be used for both privacy, performance, or other reasons.

## Installation

You can install the package using pip:
```bash
pip install vad
```

## Usage

The package can be seamlessly integrated into your Python code. The following example shows how to use the package to detect speech in an audio file:

```python
from vad import EnergyVAD

# load audio file in "audio" variable

vad = EnergyVAD(
    sample_rate: int = 16000,
    frame_length: int = 25,
    frame_shift: int = 20,
    energy_threshold: float = 0.05,
    pre_emphasis: float = 0.5,
) # default values are used here

voice_activity = vad(audio) # returns a boolean array indicating whether a frame is speech or not

# you can also use the following method to get the audio file with only speech
# speech_signal is a numpy array of the same shape as audio
speech_signal = vad.apply_vad(audio)
```

## Audio samples

- `example.wav` is a sample audio file that can be used to test the package.
- `example_vad.wav` is the audio file with only speech after applying the VAD algorithm.
- `example_vad_2.wav` is the audio file with only speech direcly extracted from the original audio file using the `apply_vad` method.
- `vad_output.png` is a plot of the voice activity detected by the VAD algorithm.
- `test_vad.py` is the script that was used to generate the above audio files and plot.

## Known issues

- There is no additional VAD algorithm implemented in this package at the moment. It may be added in the future.

## License

This project is licensed under the CC-BY-NC-SA 4.0 license. See the [LICENSE](LICENSE) file for details.