import matplotlib.pyplot as plt
import numpy as np


def plot_combined_comparison(results_dict, params_dict, figsize=(14, 9)):
    """
    Combined figure showing multiple AdEx comparisons in a compact layout.

    Shows voltage overlay and spike raster for each condition.

    Args:
        results_dict: Dict mapping condition name -> (brian2_results, jaxley_results)
                      where each result tuple is (time, voltage, w, spike_times)
        params_dict: Dict mapping condition name -> params dict
        figsize: Figure size (width, height)

    Returns:
        fig: matplotlib figure

    Example:
        results = {
            'Tonic': (brian2_tonic, jaxley_tonic),
            'Adaptation': (brian2_adapt, jaxley_adapt),
            'Original': (brian2_orig, jaxley_orig),
        }
        params = {
            'Tonic': NAUD_PARAMETERS['tonic'],
            'Adaptation': NAUD_PARAMETERS['adaptation'],
            'Original': NAUD_PARAMETERS['original'],
        }
        fig = plot_combined_comparison(results, params)
    """
    n_conditions = len(results_dict)
    fig, axes = plt.subplots(3, n_conditions, figsize=figsize)

    # Handle single condition case
    if n_conditions == 1:
        axes = axes.reshape(2, 1)

    for col, (name, (brian2_res, jaxley_res)) in enumerate(results_dict.items()):
        t_brian, v_brian, w_brian, spikes_brian = brian2_res
        t_jaxley, v_jaxley, w_jaxley, spikes_jaxley = jaxley_res
        params = params_dict[name]

        # Top row: Voltage overlay
        ax_v = axes[0, col]
        ax_v.plot(t_brian, v_brian, 'b-', linewidth=1.2, label='Brian2', alpha=0.8)
        ax_v.plot(t_jaxley, v_jaxley, 'g--', linewidth=1.2, label='Jaxley', alpha=0.8)
        ax_v.axhline(params['v_threshold'], color='r', linestyle=':', alpha=0.4, label='Threshold')
        ax_v.set_title(name, fontsize=11)
        ax_v.set_ylabel('Voltage (mV)')
        ax_v.grid(True, alpha=0.3)
        if col == 0:
            ax_v.legend(loc='upper right', fontsize=8)

        # Middle row adaption current
        ax_w = axes[1, col]
        ax_w.plot(t_brian, w_brian, 'b-', linewidth=1.2, label='Brian2', alpha=0.8)
        ax_w.plot(t_jaxley, w_jaxley, 'g--', linewidth=1.2, label='Jaxley', alpha=0.8)
        ax_w.set_ylabel('Adaption current w (pA)')
        ax_w.grid(True, alpha=0.3)
        if col == 0:
            ax_w.legend(loc='upper right', fontsize=8)

        # Bottom row: Spike raster
        ax_s = axes[2, col]
        if len(spikes_brian) > 0:
            ax_s.eventplot([spikes_brian], colors='b', lineoffsets=1.5,
                          linelengths=0.8, linewidths=1.5, label='Brian2')
        if len(spikes_jaxley) > 0:
            ax_s.eventplot([spikes_jaxley], colors='g', lineoffsets=0.5,
                          linelengths=0.8, linewidths=1.5, label='Jaxley')
        ax_s.set_ylim(0, 2.5)
        ax_s.set_yticks([0.5, 1.5])
        ax_s.set_yticklabels(['Jaxley', 'Brian2'], fontsize=8)
        ax_s.set_xlabel('Time (ms)')
        ax_s.set_xlim(t_jaxley[0], t_jaxley[-1])
        ax_s.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    return fig


def plot_combined_overlay_only(results_dict, params_dict, figsize=(12, 3)):
    """
    Minimal combined figure showing only voltage overlays for each condition.

    Args:
        results_dict: Dict mapping condition name -> (brian2_results, jaxley_results)
        params_dict: Dict mapping condition name -> params dict
        figsize: Figure size (width, height)

    Returns:
        fig: matplotlib figure
    """
    n_conditions = len(results_dict)
    fig, axes = plt.subplots(1, n_conditions, figsize=figsize, sharey=True)

    if n_conditions == 1:
        axes = [axes]

    for col, (name, (brian2_res, jaxley_res)) in enumerate(results_dict.items()):
        t_brian, v_brian, _, _ = brian2_res
        t_jaxley, v_jaxley, _, _ = jaxley_res
        params = params_dict[name]

        ax = axes[col]
        ax.plot(t_brian, v_brian, 'b-', linewidth=1.0, label='Brian2', alpha=0.8)
        ax.plot(t_jaxley, v_jaxley, 'g--', linewidth=1.0, label='Jaxley', alpha=0.8)
        ax.axhline(params['v_threshold'], color='r', linestyle=':', alpha=0.3)
        ax.set_title(name, fontsize=10)
        ax.set_xlabel('Time (ms)')
        ax.grid(True, alpha=0.3)
        if col == 0:
            ax.set_ylabel('Voltage (mV)')
            ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    return fig


def plot_comparison(brian2_results, jaxley_results, params, title="AdEx Comparison"):
    """
    Verification Plot.

    Args:
        brian2_results: (time, voltage, w, spike_times)
        jaxley_results: (time, voltage, w, spike_times)
        params: AdEx parameters (same as in simulation)
    """
    t_brian, v_brian, w_brian, spikes_brian = brian2_results
    t_jaxley, v_jaxley, w_jaxley, s_jaxley = jaxley_results

    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=16)

    # Voltage traces
    axes[0, 0].plot(t_brian, v_brian, 'b-', linewidth=1.5, label='Brian2')
    axes[0, 0].axhline(params['v_threshold'], color='r', linestyle='--', alpha=0.5, label='Threshold')
    axes[0, 0].set_ylabel('Voltage (mV)')
    axes[0, 0].set_title('Brian2: Membrane Potential')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].plot(t_jaxley, v_jaxley, 'g-', linewidth=1.5, label='Jaxley')
    axes[0, 1].axhline(params['v_threshold'], color='r', linestyle='--', alpha=0.5, label='Threshold')
    axes[0, 1].set_ylabel('Voltage (mV)')
    axes[0, 1].set_title('Jaxley: Membrane Potential')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Adaptation currents
    if w_brian is not None:
        axes[1, 0].plot(t_brian, w_brian, 'b-', linewidth=1.5)
        axes[1, 0].set_ylabel('w (pA)')
        axes[1, 0].set_title('Brian2: Adaptation Current')
        axes[1, 0].grid(True, alpha=0.3)
    else:
        axes[1, 0].text(0.5, 0.5, 'No data', ha='center', va='center', transform=axes[1, 0].transAxes)

    if w_jaxley is not None:
        axes[1, 1].plot(t_jaxley, w_jaxley, 'g-', linewidth=1.5)
        axes[1, 1].set_ylabel('w (pA)')
        axes[1, 1].set_title('Jaxley: Adaptation Current')
        axes[1, 1].grid(True, alpha=0.3)
    else:
        axes[1, 1].text(0.5, 0.5, 'Not recorded', ha='center', va='center', transform=axes[1, 1].transAxes)

    # Overlay comparison
    axes[2, 0].plot(t_brian, v_brian, 'b-', linewidth=1.5, label='Brian2', alpha=0.7)
    axes[2, 0].plot(t_jaxley, v_jaxley, 'g--', linewidth=1.5, label='Jaxley', alpha=0.7)
    axes[2, 0].axhline(params['v_threshold'], color='r', linestyle='--', alpha=0.5, label='Threshold')
    axes[2, 0].set_xlabel('Time (ms)')
    axes[2, 0].set_ylabel('Voltage (mV)')
    axes[2, 0].set_title('Overlay Comparison')
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)

    # Spike raster / difference plot
    if len(spikes_brian) > 0:
        axes[2, 1].eventplot([spikes_brian], colors='b', lineoffsets=1, linelengths=0.1, label='Brian2 spikes')
        axes[2, 1].set_ylabel('Spikes')
        axes[2, 1].set_xlabel('Time (ms)')
        axes[2, 1].set_title('Spike Times')
        axes[2, 1].set_ylim(0, 2)
        axes[2, 1].grid(True, alpha=0.3)
    else:
        axes[2, 1].text(0.5, 0.5, 'No spikes detected brian', ha='center', va='center', transform=axes[2, 1].transAxes)

    if len(s_jaxley) > 0:
        axes[2, 1].eventplot([s_jaxley], colors='r', lineoffsets=1, linelengths=0.5, label='Jaxley spikes')
        axes[2, 1].set_ylabel('Spikes')
        axes[2, 1].set_xlabel('Time (ms)')
        axes[2, 1].set_title('Spike Times')
        axes[2, 1].set_ylim(0, 2)
        axes[2, 1].grid(True, alpha=0.3)
    else:
        axes[2, 1].text(0.5, 0.5, 'No spikes detected jaxley', ha='center', va='center', transform=axes[2, 1].transAxes)

    plt.tight_layout()
    return fig


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
