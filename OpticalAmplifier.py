# -*- coding: utf-8 -*-
# describe optical amplidfier

NAME = 'amp_1'
OPTICAL_AMPLIFIER_TYPE = 'EDFA'
GAIN_RANGE = 'LOW_GAIN_RANGE'
OPTICAL_AMPLIFIER_MODE = 'CONSTANT_POWER'
TARGET_GAIN = 20
MIN_GAIN = 15
MAX_GAIn = 25
ENABLED = True
FIBER_TYPE_PROFILE = 'SSMF'

class OpticalAmplifier:
    def __init__(self, name=None, amp_type=None, gain_range=None, amp_pwr_mode=None, fiber_type=None, ):
        self.name = name
        self.amp_type = amp_type
        self.amp_pwr_mode = amp_pwr_mode
        self.fiber_type = fiber_type
        self.gain_range = gain_range
        self.target_gain = None
        self.min_gain = None
        self.max_gain = None
        self.enabled = bool


if __name__ == "__main__":
    pass
    
