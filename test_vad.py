from vad.energy_vad import EnergyVAD
import torch
import torchaudio
import numpy as np
import matplotlib.pyplot as plt

import sys 

filename = sys.argv[1]
clean_filename = filename.split("/")[-1].split(".")[0]

# Load audio
waveform, sample_rate = torchaudio.load(filename)

# Compute VAD
vad = EnergyVAD()
vad_output = vad(waveform.numpy())

# print vad output 10 per line
print(len(vad_output))

# Plot VAD output and waveform
plt.figure(figsize=(20, 10))
plt.plot(waveform.numpy()[0, :])
# each frame is 20ms
plt.plot(np.arange(0, waveform.shape[1], 320)[: len(vad_output)], vad_output * 0.5)
plt.savefig("vad_output.png")

# re-stich the audio to remove the silence
# this is just an example, you can do whatever you want with the VAD output
new_waveform = []
for i in range(len(vad_output)):
    if vad_output[i] == 1:
        new_waveform.append(waveform.numpy()[0, i * 320 : (i + 1) * 320])
new_waveform = np.concatenate(new_waveform)
# convert to tensor
new_waveform = torch.from_numpy(new_waveform)
new_waveform = new_waveform.unsqueeze(0)

# save the new audio
torchaudio.save(f"{clean_filename}_vad.wav", new_waveform, sample_rate)

# test apply_vad
new_waveform = vad.apply_vad(waveform.numpy())
print ("New waveform shape: ", new_waveform.shape)
new_waveform = torch.from_numpy(new_waveform)
torchaudio.save(f"{clean_filename}_vad_2.wav", new_waveform, sample_rate)