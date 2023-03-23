import numpy as np

class EnergyVAD:
    '''
    This class implements a simple VAD algorithm based on the energy of the signal.
    '''

    def __init__(
        self,
        sample_rate: int = 16000,
        frame_length: int = 25,
        frame_shift: int = 20,
        energy_threshold: float = 0.05,
        pre_emphasis: float = 0.95,
    ):
        self.sample_rate = sample_rate
        self.frame_length = frame_length
        self.frame_shift = frame_shift
        self.energy_threshold = energy_threshold
        self.pre_emphasis = pre_emphasis

    def __call__(self, waveform: np.ndarray) -> np.ndarray:
        '''
        Args:
            waveform (np.ndarray): input waveform of shape (num_samples,)

        Returns:
            np.ndarray: VAD output of shape (num_frames,)
        '''

        new_waveform, is_stereo = self._convert_to_mono_if_needed(waveform)

        # Pre-emphasis
        new_waveform = np.append(new_waveform[0], new_waveform[1:] - self.pre_emphasis * new_waveform[:-1])

        # Compute energy
        energy = self.compute_energy(new_waveform)

        # Compute VAD
        vad = self.compute_vad(energy)

        return vad

    def compute_energy(self, waveform: np.ndarray) -> np.ndarray:
        '''
        Args:
            waveform (np.ndarray): input waveform of shape (num_samples,)

        Returns:
            np.ndarray: energy of shape (num_frames,)
        '''
        # Compute frame length and frame shift in number of samples (not milliseconds)
        frame_length = self.frame_length * self.sample_rate // 1000
        frame_shift = self.frame_shift * self.sample_rate // 1000

        # Compute energy
        energy = np.zeros((waveform.shape[0] - frame_length + frame_shift) // frame_shift)
        for i in range(energy.shape[0]):
            energy[i] = np.sum(waveform[i * frame_shift : i * frame_shift + frame_length] ** 2)

        return energy

    def compute_vad(self, energy: np.ndarray) -> np.ndarray:
        '''
        Args:
            energy (np.ndarray): energy of shape (num_frames,)

        Returns:
            np.ndarray: VAD output of shape (num_frames,)
        '''
        # Compute VAD
        vad = np.zeros(energy.shape)
        vad[energy > self.energy_threshold] = 1

        return vad

    def apply_vad(self, waveform: np.ndarray) -> np.ndarray:
        '''
        Args:
            waveform (np.ndarray): input waveform of shape (num_samples,)

        Returns:
            np.ndarray: waveform with VAD applied of shape (num_samples,)
        '''
        processed_waveform, is_stereo = self._convert_to_mono_if_needed(waveform)

        vad = self(processed_waveform)

        shift = self.frame_shift * self.sample_rate // 1000
        new_waveform = []
        for channel in range(waveform.shape[0]):
            channel_waveform = []
            for i in range(len(vad)):
                if vad[i] == 1:
                    channel_waveform.extend(waveform[channel, i * shift : i * shift + shift])
            new_waveform.append(channel_waveform)

        new_waveform = np.array(new_waveform)

        return new_waveform
        
    def _convert_to_mono_if_needed(self, waveform: np.ndarray) -> np.ndarray:
        '''
        Args:
            waveform (np.ndarray): input waveform of shape (num_samples,)

        Returns:
            np.ndarray: waveform with dimension adjusted to (1, num_samples)
            bool: True if the signal was stereo, False otherwise
        '''
        if waveform.ndim == 2 and waveform.shape[0] == 2:
            is_stereo = True
            print("Warning: stereo audio detected, using only the first channel")
            waveform = waveform[0]
            waveform = waveform[np.newaxis, :]
        else:
            is_stereo = False

        return waveform, is_stereo