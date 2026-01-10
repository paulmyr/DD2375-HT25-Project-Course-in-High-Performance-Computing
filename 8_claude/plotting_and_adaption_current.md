❯ The python script jaxley_test_adex.py produces python plots adex_comparison_adaptation.png
  adex_comparison_tonic.png and adex_comparison_original.png. I want to use the figures in my report, but I can't
  have that many individual figures. Therefore I want to combine them into one, without loosing too much visual
  clarity. Do you have any suggestions how to do this? Maybe write a plotting function that I can include in
  jaxley_test_adex.py

⏺ Let me first look at the current plotting code to understand what's being generated.

⏺ Read(5_evaluation/jaxley_test_adex.py)
  ⎿  Read 864 lines

⏺ Let me also check the plot_comparison function in plotting_scripts.py to understand the current plot structure.

⏺ Read(5_evaluation/plotting_scripts.py)
  ⎿  Read 100 lines

⏺ Now I understand the structure. Each figure is a 3×2 grid (6 subplots), showing Brian2 vs Jaxley comparison. You have 3 such figures, which is 18 subplots total.

  Here are a few options to combine them:

  Option 1: Compact overlay-only (3×1 or 1×3)
  Show only the voltage overlay comparison for each condition. This is the most informative single plot from each figure.

  Option 2: Two-row combined (3×2)
  Show voltage overlay + spike raster for each condition. Preserves key information in 6 subplots total.

  Option 3: Single-row with shared legend (1×3)
  Just the overlays in a horizontal strip, good for wide figures in papers.

  I'd recommend Option 2 as it balances compactness with completeness. Here's a function you can add to plotting_scripts.py:

⏺ Update(5_evaluation/plotting_scripts.py)
  ⎿  Added 107 lines
        1   import matplotlib.pyplot as plt
        2
        3
        4 + def plot_combined_comparison(results_dict, params_dict, figsize=(14, 6)):
        5 +     """
        6 +     Combined figure showing multiple AdEx comparisons in a compact layout.
        7 +
        8 +     Shows voltage overlay and spike raster for each condition.
        9 +
       10 +     Args:
       11 +         results_dict: Dict mapping condition name -> (brian2_results, jaxley_results)
       12 +                       where each result tuple is (time, voltage, w, spike_times)
       13 +         params_dict: Dict mapping condition name -> params dict
       14 +         figsize: Figure size (width, height)
       15 +
       16 +     Returns:
       17 +         fig: matplotlib figure
       18 +
       19 +     Example:
       20 +         results = {
       21 +             'Tonic': (brian2_tonic, jaxley_tonic),
       22 +             'Adaptation': (brian2_adapt, jaxley_adapt),
       23 +             'Original': (brian2_orig, jaxley_orig),
       24 +         }
       25 +         params = {
       26 +             'Tonic': NAUD_PARAMETERS['tonic'],
       27 +             'Adaptation': NAUD_PARAMETERS['adaptation'],
       28 +             'Original': NAUD_PARAMETERS['original'],
       29 +         }
       30 +         fig = plot_combined_comparison(results, params)
       31 +     """
       32 +     n_conditions = len(results_dict)
       33 +     fig, axes = plt.subplots(2, n_conditions, figsize=figsize)
       34 +
       35 +     # Handle single condition case
       36 +     if n_conditions == 1:
       37 +         axes = axes.reshape(2, 1)
       38 +
       39 +     for col, (name, (brian2_res, jaxley_res)) in enumerate(results_dict.items()):
       40 +         t_brian, v_brian, w_brian, spikes_brian = brian2_res
       41 +         t_jaxley, v_jaxley, w_jaxley, spikes_jaxley = jaxley_res
       42 +         params = params_dict[name]
       43 +
       44 +         # Top row: Voltage overlay
       45 +         ax_v = axes[0, col]
       46 +         ax_v.plot(t_brian, v_brian, 'b-', linewidth=1.2, label='Brian2', alpha=0.8)
       47 +         ax_v.plot(t_jaxley, v_jaxley, 'g--', linewidth=1.2, label='Jaxley', alpha=0.8)
       48 +         ax_v.axhline(params['v_threshold'], color='r', linestyle=':', alpha=0.4, label='Threshold')
       49 +         ax_v.set_title(name, fontsize=11)
       50 +         ax_v.set_ylabel('Voltage (mV)')
       51 +         ax_v.grid(True, alpha=0.3)
       52 +         if col == 0:
       53 +             ax_v.legend(loc='upper right', fontsize=8)
       54 +
       55 +         # Bottom row: Spike raster
       56 +         ax_s = axes[1, col]
       57 +         if len(spikes_brian) > 0:
       58 +             ax_s.eventplot([spikes_brian], colors='b', lineoffsets=1.5,
       59 +                           linelengths=0.8, linewidths=1.5, label='Brian2')
       60 +         if len(spikes_jaxley) > 0:
       61 +             ax_s.eventplot([spikes_jaxley], colors='g', lineoffsets=0.5,
       62 +                           linelengths=0.8, linewidths=1.5, label='Jaxley')
       63 +         ax_s.set_ylim(0, 2.5)
       64 +         ax_s.set_yticks([0.5, 1.5])
       65 +         ax_s.set_yticklabels(['Jaxley', 'Brian2'], fontsize=8)
       66 +         ax_s.set_xlabel('Time (ms)')
       67 +         ax_s.grid(True, alpha=0.3, axis='x')
       68 +
       69 +     plt.tight_layout()
       70 +     return fig
       71 +
       72 +
       73 + def plot_combined_overlay_only(results_dict, params_dict, figsize=(12, 3)):
       74 +     """
       75 +     Minimal combined figure showing only voltage overlays for each condition.
       76 +
       77 +     Args:
       78 +         results_dict: Dict mapping condition name -> (brian2_results, jaxley_results)
       79 +         params_dict: Dict mapping condition name -> params dict
       80 +         figsize: Figure size (width, height)
       81 +
       82 +     Returns:
       83 +         fig: matplotlib figure
       84 +     """
       85 +     n_conditions = len(results_dict)
       86 +     fig, axes = plt.subplots(1, n_conditions, figsize=figsize, sharey=True)
       87 +
       88 +     if n_conditions == 1:
       89 +         axes = [axes]
       90 +
       91 +     for col, (name, (brian2_res, jaxley_res)) in enumerate(results_dict.items()):
       92 +         t_brian, v_brian, _, _ = brian2_res
       93 +         t_jaxley, v_jaxley, _, _ = jaxley_res
       94 +         params = params_dict[name]
       95 +
       96 +         ax = axes[col]
       97 +         ax.plot(t_brian, v_brian, 'b-', linewidth=1.0, label='Brian2', alpha=0.8)
       98 +         ax.plot(t_jaxley, v_jaxley, 'g--', linewidth=1.0, label='Jaxley', alpha=0.8)
       99 +         ax.axhline(params['v_threshold'], color='r', linestyle=':', alpha=0.3)
      100 +         ax.set_title(name, fontsize=10)
      101 +         ax.set_xlabel('Time (ms)')
      102 +         ax.grid(True, alpha=0.3)
      103 +         if col == 0:
      104 +             ax.set_ylabel('Voltage (mV)')
      105 +             ax.legend(loc='upper right', fontsize=8)
      106 +
      107 +     plt.tight_layout()
      108 +     return fig
      109 +
      110 +
      111   def plot_comparison(brian2_results, jaxley_results, params, title="AdEx Comparison"):
      112       """
      113       Verification Plot.

⏺ Now let me update jaxley_test_adex.py to use the combined plotting. I'll add a helper function and modify the script to collect results and produce a single combined figure:

⏺ Update(5_evaluation/jaxley_test_adex.py)
  ⎿  Added 1 line, removed 1 line
      15   import time
      16
      17   from parameters import NAUD_PARAMETERS
      18 -from plotting_scripts import plot_comparison, plot_responses
      18 +from plotting_scripts import plot_comparison, plot_responses
         +, plot_combined_comparison, plot_combined_overlay_only
      19
      20
      21
  ⎿  Found 5 new diagnostic issues in 1 file (ctrl+o to expand)

⏺ Update(5_evaluation/jaxley_test_adex.py)
  ⎿  Added 51 lines, removed 8 lines
      199
      200
      201
      202 - plot_and_run('tonic')
      203 - plot_and_run('tonic', duration=400.)
      202 + def run_all_comparisons(modules=['tonic', 'adaptation', 'original'], duration=400., t_max=600.,
          +dt=0.01):
      203 +     """
      204 +     Run all module comparisons and return collected results for combined plotting.
      205
      206 - """## Adaptation"""
      206 +     Args:
      207 +         modules: List of module names to run
      208 +         duration: Stimulus duration in ms
      209 +         t_max: Total simulation time in ms
      210 +         dt: Time step in ms
      211
      212 - #plot_and_run('adaptation')
      213 - plot_and_run('adaptation', duration=400.)
      212 +     Returns:
      213 +         results_dict: Dict mapping module name -> (brian2_results, jaxley_results)
      214 +         params_dict: Dict mapping module name -> parameters
      215 +     """
      216 +     results_dict = {}
      217 +     params_dict = {}
      218
      219 - """## Original"""
      219 +     for module in modules:
      220 +         parameters = NAUD_PARAMETERS[module]
      221
      222 - #plot_and_run('original')
      223 - plot_and_run('original', duration=400.)
      222 +         t_brian, v_brian, w_brian, spikes_brian = run_brian2_adex(
      223 +             parameters, dt_ms=dt, duration_ms=duration, t_max_ms=t_max
      224 +         )
      225
      226 +         t_jaxley, v_jaxley, w_jaxley, s_jaxley = run_jaxley_adex(
      227 +             parameters, dt_ms=dt, duration_ms=duration, t_max_ms=t_max
      228 +         )
      229
      230 +         # Capitalize module name for display
      231 +         display_name = module.capitalize()
      232 +         results_dict[display_name] = (
      233 +             (t_brian, v_brian, w_brian, spikes_brian),
      234 +             (t_jaxley, v_jaxley, w_jaxley, s_jaxley)
      235 +         )
      236 +         params_dict[display_name] = parameters
      237 +
      238 +     return results_dict, params_dict
      239 +
      240 +
      241 + # Run individual comparisons (uncomment if needed)
      242 + # plot_and_run('tonic', duration=400.)
      243 + # plot_and_run('adaptation', duration=400.)
      244 + # plot_and_run('original', duration=400.)
      245 +
      246 + # Run combined comparison
      247 + results, params = run_all_comparisons()
      248 +
      249 + # Option 1: Combined figure with voltage overlay and spike raster (2 rows x 3 cols)
      250 + fig = plot_combined_comparison(results, params, figsize=(14, 5))
      251 + plt.savefig('adex_comparison_combined.pdf', dpi=150, bbox_inches='tight')
      252 + plt.show()
      253 +
      254 + # Option 2: Minimal figure with only voltage overlays (1 row x 3 cols)
      255 + # fig = plot_combined_overlay_only(results, params, figsize=(12, 3))
      256 + # plt.savefig('adex_comparison_combined_minimal.pdf', dpi=150, bbox_inches='tight')
      257 +
      258 +
      259   #--------------------------------
      260   # Training on bio-physical data
      261   #--------------------------------
  ⎿  Found 10 new diagnostic issues in 1 file (ctrl+o to expand)

⏺ Let me also fix the numpy import issue in plotting_scripts.py:

⏺ Update(5_evaluation/plotting_scripts.py)
  ⎿  Added 1 line
      1   import matplotlib.pyplot as plt
      2 + import numpy as np
      3
      4
      5   def plot_combined_comparison(results_dict, params_dict, figsize=(14, 6)):
  ⎿  Found 10 new diagnostic issues in 1 file (ctrl+o to expand)

⏺ I've added two new plotting functions to plotting_scripts.py and updated jaxley_test_adex.py to use them. Here's a summary:

  New functions in plotting_scripts.py:

  1. plot_combined_comparison(results_dict, params_dict, figsize) - Creates a 2×N grid showing voltage overlays (top row) and spike rasters (bottom row) for N conditions. This is the recommended option.
  2. plot_combined_overlay_only(results_dict, params_dict, figsize) - Creates a minimal 1×N strip showing only voltage overlays. Even more compact if space is very limited.

  Changes in jaxley_test_adex.py:

  - Added run_all_comparisons() function that collects results from all three modules
  - The script now produces a single combined figure adex_comparison_combined.pdf

  Output comparison:
  ┌──────────────────────────────────────────┬──────────────────────────────┐
  │                  Before                  │            After             │
  ├──────────────────────────────────────────┼──────────────────────────────┤
  │ 3 separate 6-panel figures (18 subplots) │ 1 combined 6-panel figure    │
  ├──────────────────────────────────────────┼──────────────────────────────┤
  │ adex_comparison_tonic.png                │ adex_comparison_combined.pdf │
  ├──────────────────────────────────────────┼──────────────────────────────┤
  │ adex_comparison_adaptation.png           │                              │
  ├──────────────────────────────────────────┼──────────────────────────────┤
  │ adex_comparison_original.png             │                              │
  └──────────────────────────────────────────┴──────────────────────────────┘
  You can switch to the minimal version by uncommenting lines 254-256 and commenting out lines 249-252. The figsize can be adjusted to fit your report's column width.

✻ Crunched for 1m 13s

❯ The code comment of the exponential euler function is written as
  \verb|exp_term = save_exp(-dt / x_tau)|\\
  \verb|return x * exp_term +|\\
  \verb|       x_inf * (1.0 - exp_term)|

  Can you please explain to me, how and why this is applicable to my adaption current w?
  I'm finishing currently writing the \subsubsection{Numerical Integration}, but I struggle to understand this.
  ⎿  Found 14 new diagnostic issues in 2 files (ctrl+o to expand)

⏺ Let me find the actual AdEx channel implementation to give you a precise answer.

⏺ Search(pattern: "dw/dt|tau_w|exponential.*euler|exp_term", path: "~/Projects/university/35_project_course")
  ⎿  Found 20 files (ctrl+o to expand)

⏺ Read(3_jaxley/jaxley/channels/non_capacitive/adex.py)
  ⎿  Read 401 lines

⏺ Read(3_jaxley/jaxley/solver_gate.py)
  ⎿  Read 68 lines

⏺ Now I can explain this clearly.

  The Adaptation Current Equation

  The AdEx adaptation current follows:

  $$\tau_w \frac{dw}{dt} = a(V - E_L) - w$$

  Rearranging into standard form:

  $$\frac{dw}{dt} = \frac{a(V - E_L) - w}{\tau_w} = \frac{w_\infty - w}{\tau_w}$$

  where $w_\infty = a(V - E_L)$ is the steady-state value that $w$ would approach if $V$ remained constant.

  Why Exponential Euler Works

  This is a linear first-order ODE of the form:

  $$\frac{dx}{dt} = \frac{x_\infty - x}{\tau}$$

  This has an exact analytical solution over a time step $dt$ (assuming $x_\infty$ is constant during $dt$):

  $$x(t + dt) = x_\infty + (x(t) - x_\infty) \cdot e^{-dt/\tau}$$

  Expanding this:

  $$x(t + dt) = x(t) \cdot e^{-dt/\tau} + x_\infty \cdot (1 - e^{-dt/\tau})$$

  Which matches exactly the code at solver_gate.py:43-44:
  exp_term = save_exp(-dt / x_tau)
  return x * exp_term + x_inf * (1.0 - exp_term)

  Application to w in adex.py:135

  w = exponential_euler(w, dt, a * (v - E_L), tau_w)

  Maps to:
  - x → w (current adaptation value)
  - x_inf → a * (v - E_L) (steady-state target)
  - x_tau → tau_w (time constant)

  Why Use This Instead of Forward Euler?

  1. Exact for linear ODEs: Unlike forward Euler which approximates, this is the analytical solution
  2. Unconditionally stable: Forward Euler can explode if $dt > 2\tau$; exponential Euler never does
  3. Larger time steps: You can use bigger $dt$ without numerical instability

  Note that the voltage equation uses forward Euler (v = v + dt * dv) because it's nonlinear (the exponential spike term). Exponential Euler only works for linear relaxation dynamics.

✻ Cogitated for 36s
