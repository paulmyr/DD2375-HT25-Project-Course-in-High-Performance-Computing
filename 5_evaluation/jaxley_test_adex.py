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

import jax
from jax import config
from jax import grad, value_and_grad
import jax.numpy as jnp
import numpy as np
import optax

import jaxley as jx
from jaxley.channels import AdEx, AdExSurrogate

import matplotlib.pyplot as plt
import time


def plot_responses(responses, expdata=[], junction_potential=0, figsize=None, fig=None, ax=None):
    if not ax:
        fig, axes = plt.subplots(len(responses), figsize=figsize)
    for index, (name, response) in enumerate(sorted(responses.items())):
        axis = axes[index] if not ax else ax
        if name in expdata:
            data = np.loadtxt(expdata[name])
            time = data[:,0]
            voltage = data[:,1] - junction_potential
            axis.plot(time, voltage, color='lightgrey')
        axis.plot(response['time'], response['voltage'])
        if not ax:
            axis.set_title(name, size='small')
    fig.tight_layout()

def geometry_for_capacitance(C_pF, specific_capacitance=1.0):
    """
    Calculate cylindrical cell geometry to achieve target total capacitance.
    I'm not exaclty sure where exactly jaxley uses cell radius and length
    but if this is not adjusted, everything brakes...
    """
    C_uF = C_pF * 1e-6
    area_cm2 = C_uF / specific_capacitance
    radius_cm = jnp.sqrt(area_cm2 / (6.28 * jnp.pi))
    radius_um = radius_cm * 1e4
    length_um = 3.14 * radius_um
    return radius_um, length_um, area_cm2

def run_jaxley_adex(params, dt_ms=0.025, duration_ms=400.0, t_max_ms=600.0):
    """
    AdEx simulation in Jaxley.

    Args:
        params: AdEx parameters
        dt_ms: time step in milliseconds
        duration_ms: total time in ms

    Returns:
        time_array, voltage_array, w_array, s_array
    """

    radius_um, length_um, area_cm2 = geometry_for_capacitance(params['C_m'])

    # Create cell with proper geometry
    cell = jx.Cell()
    cell.set('radius', radius_um)
    cell.set('length', length_um)

    # Insert AdEx channel
    cell.insert(AdEx())

    # Set AdEx parameters (convert to density units)
    cell.set("capacitance", params['C_m'])  # μF/cm² (standard)
    cell.set("AdEx_C_m", params['C_m'])  # μF/cm² (standard)
    cell.set("AdEx_g_L", params['g_L'])
    cell.set("AdEx_E_L", params['E_L'])
    cell.set("AdEx_v_T", params['v_T'])
    cell.set("AdEx_delta_T", params['delta_T'])
    cell.set("AdEx_v_threshold", params['v_threshold'])
    cell.set("AdEx_v_reset", params['v_reset'])
    cell.set("AdEx_tau_w", params['tau_w'])
    cell.set("AdEx_a", params['a'])
    cell.set("AdEx_b", params['b'])

    # Set initial conditions
    cell.set("v", params['v_reset'])

    cell.record("v")
    cell.record("AdEx_w")
    cell.record("AdEx_spikes")

    # jx.step_current expects nA
    I_nA = params['I'] * params['C_m'] / 1000.0  # pA -> nA

    # Inject current
    cell.stimulate(jx.step_current(0.0, duration_ms, I_nA, dt_ms, t_max=t_max_ms))

    # Run simulation
    results = jx.integrate(cell, delta_t=dt_ms)

    # Extract results
    voltage_array = np.array(results[0]).flatten()
    w_array = np.array(results[1]).flatten()
    spikes_array = np.array(results[2]).flatten()

    # Create time array with same length as voltage
    time_array = np.arange(len(voltage_array)) * dt_ms

    # Extract spike times
    spike_indices = np.where(spikes_array > 0.5)[0]
    spike_times = time_array[spike_indices] if len(spike_indices) > 0 else np.array([])

    return time_array, voltage_array, w_array, spike_times



def plot_responses(responses, expdata=[], junction_potential=0, figsize=None, fig=None, ax=None):
    if not ax:
        fig, axes = plt.subplots(len(responses), figsize=figsize)
    for index, (name, response) in enumerate(sorted(responses.items())):
        axis = axes[index] if not ax else ax
        if name in expdata:
            data = np.loadtxt(expdata[name])
            time = data[:,0]
            voltage = data[:,1] - junction_potential
            axis.plot(time, voltage, color='lightgrey')
        axis.plot(response['time'], response['voltage'])
        if not ax:
            axis.set_title(name, size='small')
    fig.tight_layout()


def read_data(path, expdata, junction_potential=0):
    basepath = "../4_data/models/optimisations/"
    fig, axes = plt.subplots(len(expdata), figsize=None)
    for index, expname in enumerate(expdata.keys()):
        print(expname)
        print(basepath + path)
        print(basepath + path + expdata[expname])
        data = np.loadtxt(basepath + path + expdata[expname])
        time = data[:,0]
        voltage = data[:,1] - junction_potential
        axes[index].plot(time, voltage, color='lightgrey')
    plt.show()



def plot_and_run(module, duration=600, t_max=600):
    dt = 0.025

    parameters = NAUD_PARAMETERS[module]

    t_jaxley, v_jaxley, w_jaxley, s_jaxley = run_jaxley_adex(
        parameters, dt_ms=dt, duration_ms=duration, t_max_ms=t_max
    )

    # plt.savefig(f'adex_comparison_{module}.png', dpi=150, bbox_inches='tight')
    # plt.show()

"""## Tonic"""

#plot_and_run('tonic')

"""## Adaptation"""

#plot_and_run('adaptation')

"""## Original"""

#plot_and_run('original')

#plot_and_run('original', duration=400.0)


data = {
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


#for path in data.keys():
#    read_data(path, data[path])


# =============================================================================
# Training Infrastructure for AdEx Parameter Optimization
# =============================================================================

# Parameter bounds for biophysically realistic constraints
PARAM_BOUNDS = {
    'C_m': (50.0, 500.0),       # pF
    'g_L': (1.0, 50.0),         # nS
    'E_L': (-90.0, -50.0),      # mV
    'v_T': (-60.0, -40.0),      # mV
    'delta_T': (0.5, 5.0),      # mV
    'v_reset': (-80.0, -50.0),  # mV
    'v_threshold': (-20.0, 30.0), # mV
    'tau_w': (10.0, 500.0),     # ms
    'a': (0.0, 10.0),           # nS
    'b': (0.0, 200.0),          # pA
}

# Default initial parameters (starting point for optimization)
DEFAULT_PARAMS = {
    'C_m': 200.0,
    'g_L': 10.0,
    'E_L': -70.0,
    'v_T': -50.0,
    'delta_T': 2.0,
    'v_reset': -58.0,
    'v_threshold': 0.0,
    'tau_w': 30.0,
    'a': 2.0,
    'b': 0.0,
}


def detect_spikes(voltage, threshold_mv=0.0, min_interval_ms=2.0, dt_ms=0.025):
    """Detect spike times from voltage trace using threshold crossing.

    Args:
        voltage: Voltage trace array (mV)
        threshold_mv: Spike detection threshold (mV)
        min_interval_ms: Minimum interval between spikes (ms) to avoid double-counting
        dt_ms: Time step (ms)

    Returns:
        Array of spike times (ms)
    """
    # Find threshold crossings (rising edge)
    above_threshold = voltage > threshold_mv
    crossings = np.diff(above_threshold.astype(int)) > 0
    spike_indices = np.where(crossings)[0] + 1  # +1 because diff shifts by 1

    # Filter out spikes that are too close together
    if len(spike_indices) > 1:
        min_interval_samples = int(min_interval_ms / dt_ms)
        filtered_indices = [spike_indices[0]]
        for idx in spike_indices[1:]:
            if idx - filtered_indices[-1] >= min_interval_samples:
                filtered_indices.append(idx)
        spike_indices = np.array(filtered_indices)

    spike_times = spike_indices * dt_ms
    return spike_times


def load_experimental_data(voltage_path, current_path, junction_potential=0.0,
                          current_scale_factor=200.0):
    """Load matched voltage and current traces from experimental files.

    Args:
        voltage_path: Path to voltage data file (format: [time, voltage])
        current_path: Path to current data file (format: [time, current])
        junction_potential: Liquid junction potential correction (mV)
        current_scale_factor: Scaling factor for current (typically C_m value).
                              The Jaxley model needs current scaled by this factor
                              due to how geometry affects current density.

    Returns:
        dict with 'time', 'voltage', 'current', 'current_nA', 'spike_times', 'dt_ms'
    """
    # Load voltage data
    v_data = np.loadtxt(voltage_path)
    time = v_data[:, 0]
    voltage = v_data[:, 1] - junction_potential  # Apply junction potential correction

    # Load current data
    i_data = np.loadtxt(current_path)
    current_pA = i_data[:, 1]  # Assume pA

    # Calculate timestep from data
    dt_ms = np.mean(np.diff(time))

    # Convert current from pA to nA with scaling
    # The model geometry requires current to be scaled by C_m factor
    # Formula: I_nA = I_pA * scale_factor / 1000
    current_nA = current_pA * current_scale_factor / 1000.0

    # Detect spikes from experimental voltage trace
    spike_times = detect_spikes(voltage, threshold_mv=0.0, dt_ms=dt_ms)

    return {
        'time': jnp.array(time),
        'voltage': jnp.array(voltage),
        'current_pA': jnp.array(current_pA),
        'current_nA': jnp.array(current_nA),
        'spike_times': jnp.array(spike_times),
        'dt_ms': dt_ms,
        'n_timesteps': len(time),
        'current_scale_factor': current_scale_factor,
    }


def create_soft_spike_target(spike_times, n_timesteps, dt_ms, sigma_ms=2.0):
    """Convert spike times to a soft target trace with Gaussian bumps.

    Args:
        spike_times: Array of spike times (ms)
        n_timesteps: Number of timesteps in the trace
        dt_ms: Time step (ms)
        sigma_ms: Gaussian kernel width (ms) - spike timing tolerance

    Returns:
        Soft target trace (shape: [n_timesteps])
    """
    time_array = jnp.arange(n_timesteps) * dt_ms
    sigma_steps = sigma_ms / dt_ms

    soft_target = jnp.zeros(n_timesteps)
    for spike_t in spike_times:
        # Gaussian bump centered at spike time
        gaussian = jnp.exp(-((time_array - spike_t) ** 2) / (2 * sigma_ms ** 2))
        soft_target = soft_target + gaussian

    # Clip to [0, 1] range
    soft_target = jnp.clip(soft_target, 0.0, 1.0)
    return soft_target


def spike_timing_loss(sim_spikes, target_soft_spikes):
    """Compute spike timing loss between simulated and target spike traces.

    This is a differentiable loss that compares soft spike indicators.

    Args:
        sim_spikes: Simulated spike trace from AdExSurrogate (shape: [T])
        target_soft_spikes: Soft target trace with Gaussian bumps (shape: [T])

    Returns:
        Scalar loss value (lower = better spike timing match)
    """
    # MSE between soft spike traces
    mse = jnp.mean((sim_spikes - target_soft_spikes) ** 2)

    # Add penalty for spike count mismatch
    sim_count = jnp.sum(sim_spikes)
    target_count = jnp.sum(target_soft_spikes)
    count_penalty = ((sim_count - target_count) / (target_count + 1.0)) ** 2

    return mse + 0.1 * count_penalty


def create_cell_with_params(params, use_surrogate=True, surrogate_type="exponential",
                            surrogate_slope=10.0):
    """Create a Jaxley cell with AdEx channel and set parameters.

    Args:
        params: Dictionary of AdEx parameters
        use_surrogate: If True, use AdExSurrogate for differentiable spikes
        surrogate_type: Type of surrogate gradient ('sigmoid', 'exponential', 'superspike')
        surrogate_slope: Steepness of surrogate gradient

    Returns:
        Configured Jaxley Cell object
    """
    radius_um, length_um, _ = geometry_for_capacitance(params['C_m'])

    cell = jx.Cell()
    cell.set('radius', radius_um)
    cell.set('length', length_um)

    # Insert AdEx channel (with or without surrogate gradients)
    if use_surrogate:
        cell.insert(AdExSurrogate(surrogate_type=surrogate_type,
                                   surrogate_slope=surrogate_slope))
    else:
        cell.insert(AdEx())

    # Set all AdEx parameters
    cell.set("capacitance", params['C_m'])
    cell.set("AdEx_C_m", params['C_m'])
    cell.set("AdEx_g_L", params['g_L'])
    cell.set("AdEx_E_L", params['E_L'])
    cell.set("AdEx_v_T", params['v_T'])
    cell.set("AdEx_delta_T", params['delta_T'])
    cell.set("AdEx_v_threshold", params['v_threshold'])
    cell.set("AdEx_v_reset", params['v_reset'])
    cell.set("AdEx_tau_w", params['tau_w'])
    cell.set("AdEx_a", params['a'])
    cell.set("AdEx_b", params['b'])

    # Set initial voltage to reset potential
    cell.set("v", params['E_L'])

    # Setup recording
    cell.record("v")
    cell.record("AdEx_w")
    cell.record("AdEx_spikes")

    return cell


def run_simulation_with_data(cell, current_trace, dt_ms):
    """Run simulation with experimental current trace using data_stimulate.

    Args:
        cell: Configured Jaxley Cell
        current_trace: Current trace in nA (shape: [T])
        dt_ms: Time step (ms)

    Returns:
        Tuple of (voltage, w, spikes) arrays
    """
    # Apply current via data_stimulate for JIT compatibility
    data_stimuli = cell.comp(0).data_stimulate(current_trace, None)

    # Calculate t_max from trace length
    t_max = len(current_trace) * dt_ms

    # Run simulation
    results = jx.integrate(cell, data_stimuli=data_stimuli, delta_t=dt_ms, t_max=t_max)

    voltage = results[0].flatten()
    w = results[1].flatten()
    spikes = results[2].flatten()

    return voltage, w, spikes


def setup_trainable_cell(initial_params, current_trace, dt_ms,
                         surrogate_type="exponential", surrogate_slope=10.0):
    """Create a Jaxley cell with trainable AdEx parameters.

    This sets up the cell once with make_trainable() so parameters can be
    optimized via jx.integrate(cell, params=params).

    Args:
        initial_params: Dictionary of initial AdEx parameters
        current_trace: Current trace in nA for data_stimulate
        dt_ms: Time step (ms)
        surrogate_type: Type of surrogate gradient
        surrogate_slope: Steepness of surrogate gradient

    Returns:
        Tuple of (cell, data_stimuli, t_max, trainable_params)
    """
    radius_um, length_um, _ = geometry_for_capacitance(initial_params['C_m'])

    cell = jx.Cell()
    cell.set('radius', radius_um)
    cell.set('length', length_um)

    # Insert AdExSurrogate for differentiable spikes
    cell.insert(AdExSurrogate(surrogate_type=surrogate_type,
                               surrogate_slope=surrogate_slope))

    # Set initial parameter values
    cell.set("capacitance", initial_params['C_m'])
    cell.set("AdEx_C_m", initial_params['C_m'])
    cell.set("AdEx_g_L", initial_params['g_L'])
    cell.set("AdEx_E_L", initial_params['E_L'])
    cell.set("AdEx_v_T", initial_params['v_T'])
    cell.set("AdEx_delta_T", initial_params['delta_T'])
    cell.set("AdEx_v_threshold", initial_params['v_threshold'])
    cell.set("AdEx_v_reset", initial_params['v_reset'])
    cell.set("AdEx_tau_w", initial_params['tau_w'])
    cell.set("AdEx_a", initial_params['a'])
    cell.set("AdEx_b", initial_params['b'])

    # Set initial voltage
    cell.set("v", initial_params['E_L'])

    # Make all AdEx parameters trainable
    cell.make_trainable("length")
    cell.make_trainable("radius")
    cell.make_trainable("AdEx_C_m")
    cell.make_trainable("AdEx_g_L")
    cell.make_trainable("AdEx_E_L")
    cell.make_trainable("AdEx_v_T")
    cell.make_trainable("AdEx_delta_T")
    cell.make_trainable("AdEx_v_threshold")
    cell.make_trainable("AdEx_v_reset")
    cell.make_trainable("AdEx_tau_w")
    cell.make_trainable("AdEx_a")
    cell.make_trainable("AdEx_b")

    # Setup recording
    cell.record("v")
    cell.record("AdEx_w")
    cell.record("AdEx_spikes")

    # Setup data stimulation
    data_stimuli = cell.comp(0).data_stimulate(current_trace, None)
    t_max = len(current_trace) * dt_ms

    # Get trainable parameters
    trainable_params = cell.get_parameters()

    return cell, data_stimuli, t_max, trainable_params


def make_loss_fn(cell, data_stimuli, t_max, dt_ms, target_soft_spikes):
    """Create a loss function for the given cell and target.

    Args:
        cell: Jaxley Cell with trainable parameters
        data_stimuli: Data stimuli tuple from data_stimulate()
        t_max: Maximum simulation time
        dt_ms: Time step (ms)
        target_soft_spikes: Pre-computed soft target spike trace

    Returns:
        Loss function that takes trainable params and returns scalar loss
    """
    def loss_fn(params):
        # Run simulation with current parameters
        results = jx.integrate(
            cell,
            params=params,
            data_stimuli=data_stimuli,
            delta_t=dt_ms,
            t_max=t_max
        )

        # Extract spike trace (index 2 = AdEx_spikes)
        sim_spikes = results[2].flatten()

        # Ensure same length (truncate or pad if needed)
        min_len = min(len(sim_spikes), len(target_soft_spikes))
        sim_spikes = sim_spikes[:min_len]
        target = target_soft_spikes[:min_len]

        # Compute loss
        loss = spike_timing_loss(sim_spikes, target)
        return loss

    return loss_fn


def extract_param_values(trainable_params):
    """Extract current parameter values from trainable params list.

    Args:
        trainable_params: List of parameter dicts from cell.get_parameters()
                         Format: [{'AdEx_C_m': Array}, {'AdEx_g_L': Array}, ...]

    Returns:
        Dictionary mapping parameter names to values
    """
    result = {}
    for param_dict in trainable_params:
        for name, value in param_dict.items():
            result[name] = float(value[0])
    return result


def clip_trainable_params(params):
    """Clip trainable parameters to biophysically valid bounds.

    Args:
        params: List of parameter dicts from cell.get_parameters()
                Format: [{'AdEx_C_m': Array}, {'AdEx_g_L': Array}, ...]

    Returns:
        List of clipped parameter dicts
    """
    clipped = []
    for param_dict in params:
        clipped_dict = {}
        for name, value in param_dict.items():
            # Strip AdEx_ prefix for bounds lookup
            bounds_key = name.replace('AdEx_', '')
            if bounds_key in PARAM_BOUNDS:
                bounds = PARAM_BOUNDS[bounds_key]
                clipped_dict[name] = jnp.clip(value, bounds[0], bounds[1])
            else:
                clipped_dict[name] = value
        clipped.append(clipped_dict)
    return clipped


def train_adex(exp_data, initial_params=None, n_epochs=100, lr=1e-3,
               sigma_ms=2.0, surrogate_type="exponential", surrogate_slope=10.0,
               print_every=10):
    """Train AdEx parameters to match experimental data.

    Args:
        exp_data: Dictionary from load_experimental_data()
        initial_params: Starting parameters (dict). Uses DEFAULT_PARAMS if None.
        n_epochs: Number of optimization steps
        lr: Learning rate for Adam optimizer
        sigma_ms: Spike timing tolerance (ms)
        surrogate_type: Type of surrogate gradient
        surrogate_slope: Steepness of surrogate gradient
        print_every: Print progress every N epochs

    Returns:
        Dictionary with 'params' (fitted parameters), 'loss_history', 'initial_params'
    """
    if initial_params is None:
        initial_params = DEFAULT_PARAMS.copy()

    # Pre-compute soft target spikes
    target_soft_spikes = create_soft_spike_target(
        exp_data['spike_times'],
        exp_data['n_timesteps'],
        exp_data['dt_ms'],
        sigma_ms=sigma_ms
    )

    # Setup cell with trainable parameters
    cell, data_stimuli, t_max, trainable_params = setup_trainable_cell(
        initial_params,
        exp_data['current_nA'],
        exp_data['dt_ms'],
        surrogate_type=surrogate_type,
        surrogate_slope=surrogate_slope
    )

    # Create loss function
    loss_fn = make_loss_fn(cell, data_stimuli, t_max, exp_data['dt_ms'], target_soft_spikes)

    # Setup optimizer
    optimizer = optax.adam(lr)
    opt_state = optimizer.init(trainable_params)

    # Training loop
    loss_history = []

    print(f"Starting training with {n_epochs} epochs...")
    print(f"Initial parameters: {initial_params}")
    print(f"Target spike times: {exp_data['spike_times']}")
    print(f"Number of trainable parameter groups: {len(trainable_params)}")

    time_total = 0.

    for epoch in range(n_epochs):
        t0 = time.time()
        # Compute loss and gradients
        loss, grads = jax.value_and_grad(loss_fn)(trainable_params)

        # Update parameters
        updates, opt_state = optimizer.update(grads, opt_state)
        trainable_params = optax.apply_updates(trainable_params, updates)

        # Apply constraints
        trainable_params = clip_trainable_params(trainable_params)

        loss_history.append(float(loss))
        t1 = time.time()
        time_total += t1 - t0

        if epoch % print_every == 0:
            print(f"Epoch {epoch:4d}: loss = {loss:.6f},\t Time per Epoch: {time_total / (epoch + 1)}")

    # Extract final parameters
    final_params = extract_param_values(trainable_params)
    print(f"\nTraining complete!")
    print(f"Final loss: {loss_history[-1]:.6f}")
    print(f"Final parameters: {final_params}")

    return {
        'params': final_params,
        'loss_history': loss_history,
        'initial_params': initial_params,
    }


def convert_fitted_to_params(fitted_params):
    """Convert fitted parameter dict (with AdEx_ prefix) to standard format.

    Args:
        fitted_params: Dict with 'AdEx_*' keys from training

    Returns:
        Dict with standard keys (C_m, g_L, etc.) for create_cell_with_params
    """
    return {

        'length': fitted_params.get('length', fitted_params.get('length', 0)),
        'radius': fitted_params.get('radius', fitted_params.get('radius', 0)),
        'C_m': fitted_params.get('AdEx_C_m', fitted_params.get('C_m', 200.0)),
        'g_L': fitted_params.get('AdEx_g_L', fitted_params.get('g_L', 10.0)),
        'E_L': fitted_params.get('AdEx_E_L', fitted_params.get('E_L', -70.0)),
        'v_T': fitted_params.get('AdEx_v_T', fitted_params.get('v_T', -50.0)),
        'delta_T': fitted_params.get('AdEx_delta_T', fitted_params.get('delta_T', 2.0)),
        'v_reset': fitted_params.get('AdEx_v_reset', fitted_params.get('v_reset', -58.0)),
        'v_threshold': fitted_params.get('AdEx_v_threshold', fitted_params.get('v_threshold', 0.0)),
        'tau_w': fitted_params.get('AdEx_tau_w', fitted_params.get('tau_w', 30.0)),
        'a': fitted_params.get('AdEx_a', fitted_params.get('a', 2.0)),
        'b': fitted_params.get('AdEx_b', fitted_params.get('b', 0.0)),
    }


def plot_fit_results(exp_data, fitted_params, initial_params=None):
    """Visualize the fit results comparing experimental vs simulated traces.

    Args:
        exp_data: Dictionary from load_experimental_data()
        fitted_params: Fitted AdEx parameters (can have AdEx_ prefix or not)
        initial_params: Optional initial parameters for comparison
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # Convert parameter format if needed
    params_for_cell = convert_fitted_to_params(fitted_params)

    # Run simulation with fitted parameters
    cell = create_cell_with_params(params_for_cell, use_surrogate=False)
    v_fitted, w_fitted, s_fitted = run_simulation_with_data(
        cell, exp_data['current_nA'], exp_data['dt_ms']
    )
    time = np.arange(len(v_fitted)) * exp_data['dt_ms']

    # Plot 1: Voltage comparison
    ax1 = axes[0]
    ax1.plot(exp_data['time'], exp_data['voltage'], 'gray', alpha=0.7,
             label='Experimental', linewidth=1)
    ax1.plot(time, v_fitted, 'b-', label='Fitted model', linewidth=1)

    # Mark experimental spikes
    for st in exp_data['spike_times']:
        ax1.axvline(st, color='gray', linestyle=':', alpha=0.5)

    # Mark simulated spikes
    sim_spike_times = time[np.array(s_fitted) > 0.5]
    for st in sim_spike_times:
        ax1.axvline(st, color='blue', linestyle='--', alpha=0.5)

    ax1.set_ylabel('Membrane potential (mV)')
    ax1.set_title('Voltage trace comparison')
    ax1.legend()

    # Plot 2: Current stimulus
    ax2 = axes[1]
    ax2.plot(exp_data['time'], exp_data['current_pA'], 'k-', linewidth=1)
    ax2.set_ylabel('Current (pA)')
    ax2.set_title('Stimulus current')

    # Plot 3: Spike raster / comparison
    ax3 = axes[2]
    ax3.eventplot([exp_data['spike_times']], lineoffsets=1, colors='gray',
                   label='Experimental')
    ax3.eventplot([sim_spike_times], lineoffsets=0, colors='blue',
                   label='Simulated')
    ax3.set_yticks([0, 1])
    ax3.set_yticklabels(['Simulated', 'Experimental'])
    ax3.set_xlabel('Time (ms)')
    ax3.set_title(f'Spike times - Exp: {len(exp_data["spike_times"])}, Sim: {len(sim_spike_times)}')
    ax3.legend()

    plt.tight_layout()

    # Print parameter comparison
    print("\nFitted parameters:")
    for key, val in sorted(fitted_params.items()):
        # Strip AdEx_ prefix for bounds lookup
        bounds_key = key.replace('AdEx_', '')
        bounds = PARAM_BOUNDS.get(bounds_key, (None, None))
        print(f"  {key:20s}: {val:10.3f}  (bounds: {bounds})")

    return fig


# =============================================================================
# Example usage
# =============================================================================

def run_training_example():
    """Example of how to run the training pipeline."""
    basepath = "../4_data/models/optimisations/"

    # Load example data with appropriate current scaling
    # Scale factor of 190 provides non-zero gradients while not over-saturating
    exp_data = load_experimental_data(
        voltage_path=basepath + "hPu-dspn-e150917_c6_D1-mAB5_porta76_cel5/expdata/ECBL_IDthresh_ch5_543.dat",
        current_path=basepath + "hPu-dspn-e150917_c6_D1-mAB5_porta76_cel5/expdata/ECBL_IDthresh_ch4_543.dat",
        junction_potential=0.0,
        current_scale_factor=190.0
    )

    print(f"Loaded data: {exp_data['n_timesteps']} timesteps, dt={exp_data['dt_ms']:.4f} ms")
    print(f"Detected {len(exp_data['spike_times'])} spikes in experimental trace")

    # Use initial parameters that produce non-zero gradients
    # Higher g_L values move toward the transition zone where gradients flow
    initial_params = DEFAULT_PARAMS.copy()
    initial_params['g_L'] = 12.0  # Start in region with non-zero gradients

    # Train model
    results = train_adex(
        exp_data,
        initial_params=initial_params,
        n_epochs=500,
        lr=0.01,  # Higher learning rate since gradients can be small
        sigma_ms=5.0,  # Wider spike timing tolerance
        surrogate_type="exponential",
        surrogate_slope=10.0,
        print_every=10
    )

    # Visualize results
    fig = plot_fit_results(exp_data, results['params'], results['initial_params'])
    plt.show()

    return results


# Uncomment to run:
config.update("jax_platform_name", "cpu")
results = run_training_example()

