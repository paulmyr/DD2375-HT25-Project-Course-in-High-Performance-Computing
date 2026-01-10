❯ I'm currently writing the experimental setup section. Provide me with bullet points for the following things:

  - Dataset description (striatal neurons)
  - Simulation parameters (dt, duration)
  - Training setup (Adam, learning rate, epochs, gradient clipping)
  - Which parameters are trainable vs fixed

⏺ I'll look through your code files to extract the experimental setup details.

⏺ Read(5_evaluation/parameters.py)
  ⎿  Read 59 lines

⏺ Read(5_evaluation/train_adex_guarino.py)
  ⎿  Read 324 lines

⏺ Based on your code, here are the bullet points for your experimental setup:

  Dataset Description (Striatal Neurons)

  - D1-type medium spiny neurons (dSPNs) from mouse striatum
  - Cell: mCP-dspn-e150917_c6_D1-manimal_1_n24_04102017_cel1
  - Electrophysiological recordings with paired voltage/current traces
  - IDthresh protocol traces (e.g., ECBL_IDthresh_ch5_553.dat)
  - Spike threshold detection at -20 mV

  Simulation Parameters

  - Time step (dt): inferred from experimental data (~0.1 ms typical for such recordings)
  - Maximum training window: 500 ms (max_duration_ms = 500.0)
  - Total simulation duration: stim_duration_ms + 100 ms (includes post-stimulus period)
  - Surrogate gradient: sigmoid with slope = 25.0

  Training Setup

  - Optimizer: Adam (via Optax)
  - Learning rate: 0.1
  - Epochs: 500
  - Gradient clipping: global norm clipping with max norm = 2.0
  - Early stopping: best parameters checkpointed based on lowest loss
  - NaN handling: gradient updates skipped when NaN detected

  Trainable vs Fixed Parameters
  ┌──────────────────────────────────┬───────────────────────────────────┐
  │            Trainable             │               Fixed               │
  ├──────────────────────────────────┼───────────────────────────────────┤
  │ g_L (leak conductance)           │ C_m (membrane capacitance)        │
  ├──────────────────────────────────┼───────────────────────────────────┤
  │ E_L (leak reversal)              │ delta_T (spike slope factor)      │
  ├──────────────────────────────────┼───────────────────────────────────┤
  │ v_T (spike threshold)            │ v_threshold (detection threshold) │
  ├──────────────────────────────────┼───────────────────────────────────┤
  │ v_reset (reset potential)        │ radius, length (geometry)         │
  ├──────────────────────────────────┼───────────────────────────────────┤
  │ tau_w (adaptation time constant) │                                   │
  ├──────────────────────────────────┼───────────────────────────────────┤
  │ a (subthreshold adaptation)      │                                   │
  ├──────────────────────────────────┼───────────────────────────────────┤
  │ b (spike-triggered adaptation)   │                                   │
  └──────────────────────────────────┴───────────────────────────────────┘
