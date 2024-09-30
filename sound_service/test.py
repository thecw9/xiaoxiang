import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import matplotlib.pyplot as plt
with nidaqmx.Task() as task:
  task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai1")
  task.timing.cfg_samp_clk_timing(16000.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=16000*1)
  data = task.read(READ_ALL_AVAILABLE)
  data = np.array(data)
  print(data)
  plt.plot(data)
  plt.ylabel('Amplitude')
  plt.title('Waveform')
  plt.show()
