NAUD_PARAMETERS = {
    'tonic': {
        'C_m': 200,      # pF - Membrane capacitance
        'g_L': 10,       # nS - Leak conductance
        'E_L': -70,      # mV - Leak reversal potential
        'v_T': -50,      # mV - Spike threshold
        'delta_T': 2,    # mV - Spike slope factor
        'v_reset': -58,  # mV - Reset potential (NOT -70!)
        'v_threshold': 0,  # mV - Detection threshold for spike cutoff
        'tau_w': 30,     # ms - Adaptation time constant
        'a': 2,          # nS - Subthreshold adaptation
        'b': 0,          # pA - Spike-triggered adaptation (none for tonic)
        'I': 500,        # pA - Injected Current
    },
    'adaptation': {
        'C_m': 200,      # pF
        'g_L': 12,       # nS - Slightly higher leak
        'E_L': -70,      # mV
        'v_T': -50,      # mV
        'delta_T': 2,    # mV
        'v_reset': -58,  # mV
        'v_threshold': 0,  # mV
        'tau_w': 300,    # ms - 10x slower adaptation!
        'a': 2,          # nS
        'b': 60,         # pA - Strong spike-triggered adaptation
        'I': 500,        # pA - Injected Current
    },
    'original': {          # Parameters from the 2005 Brette et al. paper
        'C_m': 281,        # pF
        'g_L': 30,         # nS - Slightly higher leak
        'E_L': -70.6,      # mV
        'v_T': -50.4,      # mV
        'delta_T': 2,      # mV
        'v_reset': -70.6,  # mV
        'v_threshold': 20, # mV
        'tau_w': 144,      # ms - 10x slower adaptation!
        'a': 4,            # nS
        'b': 80.5,         # pA - Strong spike-triggered adaptation
        'I': 2500,         # pA - Injected Current
    },
}


DATA = {
    'mCP-dspn-e150917_c6_D1-manimal_1_n24_04102017_cel1/': {
        'IV_499.soma.v': 'expdata/ECBL_IV_ch5_499.dat',
        'IV_499.soma.i': 'expdata/ECBL_IV_ch4_499.dat',
        'IV_502.soma.v': 'expdata/ECBL_IV_ch5_502.dat',
        'IV_502.soma.i': 'expdata/ECBL_IV_ch4_502.dat',
        'IDthresh-sub_541.soma.v': 'expdata/ECBL_IDthresh_ch5_541.dat',
        'IDthresh-sub_541.soma.i': 'expdata/ECBL_IDthresh_ch4_541.dat',
        'IDthresh_543.soma.v': 'expdata/ECBL_IDthresh_ch5_543.dat',
        'IDthresh_543.soma.i': 'expdata/ECBL_IDthresh_ch4_543.dat',
        'IDthresh_544.soma.v': 'expdata/ECBL_IDthresh_ch5_544.dat',
        'IDthresh_544.soma.i': 'expdata/ECBL_IDthresh_ch4_544.dat',
        'IDthresh_553.soma.v': 'expdata/ECBL_IDthresh_ch5_553.dat',
        'IDthresh_553.soma.i': 'expdata/ECBL_IDthresh_ch4_553.dat'
    }
}