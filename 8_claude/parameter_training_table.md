please extract all interesting training parameters from train_adex_mse and train_adex_guarino and write them as a latex table so I can include them in my methodology. You may want to reread those two files, they might
  have changed.

⏺ Read(train_adex_mse.py)
  ⎿  Read 279 lines

⏺ Read(train_adex_guarino.py)
  ⎿  Read 328 lines

⏺ Here's a LaTeX table with the training parameters from both files:

  \begin{table}[htbp]
  \centering
  \caption{Training hyperparameters for AdEx optimization}
  \label{tab:training-params}
  \begin{tabular}{lcc}
  \toprule
  \textbf{Parameter} & \textbf{MSE} & \textbf{Guarino} \\
  \midrule
  \multicolumn{3}{l}{\textit{Optimization}} \\
  Optimizer & Adam & Adam \\
  Learning rate & 0.1 & 0.1 \\
  Gradient clipping (global norm) & 2.0 & 2.0 \\
  Number of epochs & 500 & 500 \\
  \midrule
  \multicolumn{3}{l}{\textit{Surrogate Gradient}} \\
  Surrogate type & sigmoid & sigmoid \\
  Surrogate slope & 25.0 & 25.0 \\
  \midrule
  \multicolumn{3}{l}{\textit{Loss-Specific Parameters}} \\
  Normalize & False & --- \\
  Temperature ($\tau$) & --- & 0.3 \\
  Beta ($\beta$) & --- & 10.0 \\
  Missing feature penalty & --- & 3.0 \\
  \midrule
  \multicolumn{3}{l}{\textit{Guarino Feature Weights}} \\
  $w_{t_\text{first}}$ & --- & 5.0 \\
  $w_{t_\text{second}}$ & --- & 3.0 \\
  $w_{t_\text{third}}$ & --- & 2.0 \\
  $w_{t_\text{last}}$ & --- & 1.0 \\
  $w_{\text{inv\_first\_ISI}}$ & --- & 2.0 \\
  $w_{\text{inv\_last\_ISI}}$ & --- & 1.0 \\
  $w_{\text{firing\_freq}}$ & --- & 1.0 \\
  $w_{V_\text{stim\_end}}$ & --- & 0.5 \\
  \midrule
  \multicolumn{3}{l}{\textit{Simulation}} \\
  Max stimulus duration & \multicolumn{2}{c}{500\,ms} \\
  Spike threshold & \multicolumn{2}{c}{$-20$\,mV} \\
  \bottomrule
  \end{tabular}
  \end{table}

  \begin{table}[htbp]
  \centering
  \caption{Initial AdEx model parameters and trainability}
  \label{tab:adex-params}
  \begin{tabular}{lccc}
  \toprule
  \textbf{Parameter} & \textbf{Symbol} & \textbf{Initial Value} & \textbf{Trainable} \\
  \midrule
  Membrane capacitance & $C_m$ & 200.0\,pF & No \\
  Leak conductance & $g_L$ & 10.0\,nS & Yes \\
  Leak reversal potential & $E_L$ & $-68.0$\,mV & Yes \\
  Spike threshold & $V_T$ & $-45.0$\,mV & Yes \\
  Slope factor & $\Delta_T$ & 2.0\,mV & No \\
  Spike detection threshold & $V_\text{threshold}$ & $-20.0$\,mV & No \\
  Reset potential & $V_\text{reset}$ & $-55.0$\,mV & Yes \\
  Adaptation time constant & $\tau_w$ & 100.0\,ms & Yes \\
  Subthreshold adaptation & $a$ & 2.0\,nS & Yes \\
  Spike-triggered adaptation & $b$ & 1.0\,pA & Yes \\
  \bottomrule
  \end{tabular}
  \end{table}

  This provides two tables:
  1. Training hyperparameters comparing MSE and Guarino loss configurations
  2. Initial AdEx parameters with their values and trainability status

✻ Worked for 34s
