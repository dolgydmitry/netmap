# -*- coding: utf-8 -*-
# test handler
import ConnectorDb 
import OpticalAmplifier

NAME = 'amp_1'
OPTICAL_AMPLIFIER_TYPE = 'EDFA'
GAIN_RANGE = 'LOW_GAIN_RANGE'
OPTICAL_AMPLIFIER_MODE = 'CONSTANT_POWER'
TARGET_GAIN = 20
MIN_GAIN = 15
MAX_GAIn = 25
ENABLED = True
FIBER_TYPE_PROFILE = 'SSMF'

FILE_PATH_PARAMETRS = '/home/dvdolgy/netmap/db_param.json'

 



if __name__ == "__main__":
    amp_1 = OpticalAmplifier.OpticalAmplifier(
    name=NAME,
    amp_type=OPTICAL_AMPLIFIER_TYPE,
    amp_pwr_mode=OPTICAL_AMPLIFIER_MODE,
    gain_range=GAIN_RANGE,
    fiber_type=FIBER_TYPE_PROFILE
    )

    
    conn = ConnectorDb.ConnectorDb(FILE_PATH_PARAMETRS)
    conn.collection_name = 'kras_500'
    conn.start_connect_db()
    conn.connect_to_coll()
    print(conn.collection)