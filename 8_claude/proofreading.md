Pretend you are my course professor.
  I am currently working on a project report.
  I tried to answer a research question: 'Can gradient based optimisation be succesfully adapted to optimise simplified neuron models, namely AdEx.
  In this folder you find my implementation. It extended Jaxkely, bio-physical neuron simulator (folder 3_jaxley), and evaluation files (folder 5_evaluation). The report is in the folder 2_paper.

  The submission criteria is listed as follows:
  This assignment aims to finalize the scientific paper on the topic you selected. You will build on the work you’ve already completed (Background, Related Work, and Methodology sections) to produce a complete and cohesive
  research paper.

  Task Description
  You are required to write the remaining sections of your paper, including:

  Abstract. Summarize the paper’s objectives, methodology, results, and contributions concisely and quantitatively. Check for guidelines: 2.1 - Writing the Paper Abstract
  1 Introduction. Establish the importance of the topic. Present the motivation for your work. Please make sure to clearly outline the specific contributions of your paper in bullet points. Check: 2.2 - Writing the
  "Introduction" Section
  2. Background. Provide foundational knowledge, including terminologies, principles, equations, and system architectures essential for understanding your research. Incorporate visual aids (e.g., diagrams) where
  appropriate. Rely on the previous Background section you wrote. Check for guidelines: 2.3 - Writing the "Background" Section
  3. Related Work. Review and analyze prior research related to your topic. Identify gaps in the literature that your work addresses. Rely on the previous Related Work section you wrote. Check for guidelines: 2.4 - Writing
  the "Related Work" Section
  4. Methodology. Explain the methods and techniques developed or applied in your study, focusing on their novelty and rigor. Use diagrams, equations, or pseudo-codes to illustrate key methods. Rely on the previous Methods
  section you wrote. Check for guidelines: 2.5 - Writing the "Methodology" Section
  5. Experimental Setup. Describe the hardware, software, and configurations used for your experiments. Include details such as compiler versions, flags, libraries, and datasets to ensure reproducibility. Check: 2.6 -
  Writing the "Experimental Setup" Section
  6. Results. Present the findings of your experiments using clear tables, plots, and quantitative analysis. Describe the data without interpreting it. Check: 2.7 - Writing the "Results" Section
  7. Discussion and Conclusion. Summarize the key findings and their implications. Discuss the limitations of your work and propose potential future improvements. Check: 2.8 - Writing the "Discussion and Conclusion" Section
  Formatting and Submission
  - Length: The final paper must not exceed ten pages, including all figures, tables, and references.
  - Format: Use either the IEEE or ACM LaTeX template in a double-column layout.
  - Quality: Include high-quality plots, diagrams, and properly formatted citations with bibtex. Ensure the paper is technically rigorous, clearly written, and logically structured.

  Evaluation
  Your submission will be graded based on the following:
  - Completeness and Technical Rigor: Clarity and thoroughness of the presented research.
  - Adherence to Guidelines: Correct use of templates, citation styles, and overall formatting.
  - Writing Quality: Organization, coherence, and adherence to scientific writing best practices.

  Use of generative AI is allowed with disclosure.
  You may use generative‑AI tools (e.g., ChatGPT, GitHub Copilot, Claude, Gemini, ...) for brainstorming, refactoring, coding assistance, plotting, or editing.

  This is allowed with disclosure. Add an AI assistance disclosure as the last section of your submission, containing:

  Tools/models used (names and versions, if known).

  Per‑task usage: for each Task, a brief note of what the tool was used for.

  Prompts/transcripts: main prompts or a summary of interactions (a link or screenshot is acceptable if long).

  Validation: how you checked and adapted outputs (tests run, docs consulted, comparisons, plots).

  All the students must understand the submitted work and be able to explain it to the mentors and the course responsible. Do not paste secrets (API tokens, private data) into third‑party tools

  Please critique my report. You can annotate the .tex file.
  Use \mtodo[color]{your critisizm} where you think it is appropriate. Be concise and direct.

⏺ I'll read your report and provide critique as annotations. Let me start by examining the paper.

⏺ Read(2_paper/differentiable_adex.tex)
  ⎿  Read 742 lines

⏺ Now I'll add my critique annotations to the document.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      38     \textbf{Gap:} Surrogate gradients (from SNNs) enable differentiation through spikes, but were developed for network weight training, not biophysical parameter estimation.\\
      39     \textbf{Contribution:} We bridge these worlds by implementing surrogate gradient-enabled AdEx in Jaxley and investigating what loss functions enable successful parameter fitting.\\
      40     \textbf{Finding:} MSE loss fails due to spike timing sensitivity; feature-based losses (Guarino et al.) enable optimization of bulk firing properties.\\
      41 -  \textbf{Implication:} Loss function design is critical when adapting SNN techniques for biophysical parameter estimation.}
      41 +  \textbf{Implication:} Loss function design is critical when adapting SNN techniques for biophysical parameter estimation.}
         +\mtodo[red]{CRITICAL: Abstract is missing entirely. This is unacceptable for submission. Write a proper 150-200 word abstract with quantitative results.}
      42   \end{abstract}
      43
      44   \begin{IEEEkeywords}

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      46   \end{IEEEkeywords}
      47
      48   \section{Introduction}\label{sec:intro}
      49 -In the last century, studying and modelling neurons has been seen as the gateway of understanding the brain in its entirety.
      49 +In the last century, studying and modelling neurons has been seen as the gateway of understanding the brain in its entirety.
         +\mtodo[orange]{Vague opening. "Last century" spans 1900-2000. Be more specific about the timeline.}
      50   What first started with very simple \ac{LIF}-models, quickly became proving ground for more complex and more sophisticated ideas.
      51   Lack of computational resources has been a primary driver why simplified neuron models were still developed, because they promised to be the only way to really model parts of the brain on super computers 20
          years ago.
      52   With the steady increase in computing power, the research community shifted focus from those models in favour of more sophisticated \ac{HH}-type models, which require more computational resources to simulate
          and to fit parameters to.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      48   \section{Introduction}\label{sec:intro}
      49   In the last century, studying and modelling neurons has been seen as the gateway of understanding the brain in its entirety.\mtodo[orange]{Vague opening. "Last century" spans 1900-2000. Be more specific about
          the timeline.}
      50   What first started with very simple \ac{LIF}-models, quickly became proving ground for more complex and more sophisticated ideas.
      51 -Lack of computational resources has been a primary driver why simplified neuron models were still developed, because they promised to be the only way to really model parts of the brain on super computers 20
         -years ago.
      51 +Lack of computational resources has been a primary driver why simplified neuron models were still developed, because they promised to be the only way to really model parts of the brain on super computers 20
         +years ago.\mtodo[yellow]{Grammar: "primary driver why" should be "primary driver for why" or rephrase entirely.}
      52   With the steady increase in computing power, the research community shifted focus from those models in favour of more sophisticated \ac{HH}-type models, which require more computational resources to simulate
          and to fit parameters to.
      53   However, the idea of simulating the brain as whole has remained an unreachable goal for many decades.
      54

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      52   With the steady increase in computing power, the research community shifted focus from those models in favour of more sophisticated \ac{HH}-type models, which require more computational resources to simulate
          and to fit parameters to.
      53   However, the idea of simulating the brain as whole has remained an unreachable goal for many decades.
      54
      55 - This could change soon.
      55 + This could change soon.\mtodo[yellow]{Too informal for academic writing. Avoid speculative statements without evidence.}
      56   Computational power has reached whole new levels, and using computationally less intensive simplified models might be the key step to perform whole brain simulations.
      57   Adaptive models like \ac{AdEx} can faithfully capture the firing behaviour of diverse neuron types and therefore promise to be a prime candidate for realistic large-scale simulations.
      58   However, this needs very fast and efficient, reliable, and effective optimization methods to fit neuron models to experimental data.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      56   Computational power has reached whole new levels, and using computationally less intensive simplified models might be the key step to perform whole brain simulations.
      57   Adaptive models like \ac{AdEx} can faithfully capture the firing behaviour of diverse neuron types and therefore promise to be a prime candidate for realistic large-scale simulations.
      58   However, this needs very fast and efficient, reliable, and effective optimization methods to fit neuron models to experimental data.
      59 -Due to the non differentiable nature of simplified models, optimization methods like grid search or evolutionary algorithms are used compared to gradient methods.
      59 +Due to the non differentiable nature of simplified models, optimization methods like grid search or evolutionary algorithms are used compared to gradient methods.
         +\mtodo[yellow]{Awkward phrasing: "used compared to" should be "used instead of".}
      60
      61   In this work, we investigate whether surrogate gradient techniques can enable gradient-based parameter estimation for simplified neuron models.
      62   Specifically, we ask:

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      68   \begin{enumerate}
      69     \item We implement a surrogate gradient-enabled \ac{AdEx} model within the Jaxley framework, enabling gradient-based parameter optimization.
      70     \item We investigate loss function requirements and compare voltage-based \ac{MSE} loss against feature-based losses.
      71 -  \item We find that \ac{MSE}-based optimization fails to recover correct spiking behavior, while feature-based losses show more promise, though significant challenges remain.
      71 +  \item We find that \ac{MSE}-based optimization fails to recover correct spiking behavior, while feature-based losses show more promise, though significant challenges remain.
         +\mtodo[orange]{This contribution is weak --- "show more promise" and "challenges remain" are vague. Quantify: what $\Gamma$ values did you achieve?}
      72   \end{enumerate}
      73
      74   We start giving a brief background introduction in Section~\ref{sec:background} and an overview over the related work in~\ref{sec:relwork}.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
       96     \text{if } V > 0 \text{ mV}\; \text{ then} &= \begin{cases}
       97       V \rightarrow V_r,\\
       98       w \rightarrow w_r = w + b.
       99 -   \end{cases}\label{eq:adex3}
       99 +   \end{cases}\label{eq:adex3}\mtodo[red]{Malformed equation --- the LHS is incomplete. Should be a conditional statement, not an equation with "=".}
      100   \end{align}
      101
      102   It describes the membrane potential over time $V(t)$ given an injected current $I(t)$.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      102   It describes the membrane potential over time $V(t)$ given an injected current $I(t)$.
      103   Equation (\ref{eq:adex1}) describes the change of potential.
      104   $C$ is the membrane capacitance, $g_L$ the leak conductance and $E_L$ the effective resting potential.
      105 -We can understand $-g_L (V - E_L)$ as the leak current that slowly pulls the membrane potential towards it's resting potential.
      105 +We can understand $-g_L (V - E_L)$ as the leak current that slowly pulls the membrane potential towards it's resting potential.\mtodo[yellow]{Grammar: "it's" should be "its" (possessive).}
      106   $g_L \Delta_T \exp(\frac{V - V_T}{\Delta_T})$ models the depolarisation initialised by the fast reacting sodium channels using and exponential function,
      107   modelled using a driving force based on an effective threshold potential $V_T$ and an slope factor $\Delta_T$.
      108   $I$ is the injected current, and $w$ is the adaptation current, which is described in equation \ref{eq:adex2}.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      103   Equation (\ref{eq:adex1}) describes the change of potential.
      104   $C$ is the membrane capacitance, $g_L$ the leak conductance and $E_L$ the effective resting potential.
      105   We can understand $-g_L (V - E_L)$ as the leak current that slowly pulls the membrane potential towards it's resting potential.\mtodo[yellow]{Grammar: "it's" should be "its" (possessive).}
      106 -$g_L \Delta_T \exp(\frac{V - V_T}{\Delta_T})$ models the depolarisation initialised by the fast reacting sodium channels using and exponential function,
      107 -modelled using a driving force based on an effective threshold potential $V_T$ and an slope factor $\Delta_T$.
      106 +$g_L \Delta_T \exp(\frac{V - V_T}{\Delta_T})$ models the depolarisation initialised by the fast reacting sodium channels using and exponential function,
          +\mtodo[yellow]{Typo: "using and" $\rightarrow$ "using an".}
      107 +modelled using a driving force based on an effective threshold potential $V_T$ and an slope factor $\Delta_T$.\mtodo[yellow]{"an slope" $\rightarrow$ "a slope".}
      108   $I$ is the injected current, and $w$ is the adaptation current, which is described in equation \ref{eq:adex2}.
      109
      110   The adaptation mechanism is controlled via an adaptation current which opposes depolarisation.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      122   To perform parameter optimisation, \texttt{Jaxley} uses automatic differentiation (via \texttt{Jax}).
      123   It shows very promising results, matching or outperforming other state-of-the-art (e.g. genetic algorithms) in performance for small and large neuron models respectively.
      124   However, as previously stated, in many circumstances it still remains unfeasible to use \ac{HH}-type models for large-scale simulations.
      125 -\texttt{Jaxley} fails to support simplified models to perform parameter tuning.
      125 +\texttt{Jaxley} fails to support simplified models to perform parameter tuning.\mtodo[orange]{Citation needed. Did Deistler et al. explicitly state this limitation?}
      126   The fundamental limitation is that simplified models are not by default automatically differentiable.
      127   This is a result of the reset condition in equation~\ref{eq:adex3}.
      128   Addressing this issues requires special treatment: surrogate gradients.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      134   To overcome this issue, prior work replaced the discontinues (heavyside-) functions derivative with a (e.g. sigmoid) surrogate, but only for the backward pass \cite{Neftci2019}.
      135   For training weights in \acp{SNN}, this performed sufficiently well.
      136
      137 -In this work we will bridge these two worlds: combine gradient optimisation using Jaxley for using simplified models in bio-physical neuron simulations.
      137 +In this work we will bridge these two worlds: combine gradient optimisation using Jaxley for using simplified models in bio-physical neuron simulations.
          +\mtodo[orange]{This sentence is awkward and belongs in Introduction, not Background.}
      138
      139   \section{Related Work}\label{sec:relwork}
      140   Simplified Neuron Models historically were a necessary evil to deal with the fact that computing resources were too limited to perform large scale brain simulations with sophisticated ion-channel based
           models.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      137   In this work we will bridge these two worlds: combine gradient optimisation using Jaxley for using simplified models in bio-physical neuron simulations.\mtodo[orange]{This sentence is awkward and belongs in
           Introduction, not Background.}
      138
      139   \section{Related Work}\label{sec:relwork}
      140 -Simplified Neuron Models historically were a necessary evil to deal with the fact that computing resources were too limited to perform large scale brain simulations with sophisticated ion-channel based models.
      140 +Simplified Neuron Models historically were a necessary evil to deal with the fact that computing resources were too limited to perform large scale brain simulations with sophisticated ion-channel based models.
          +\mtodo[yellow]{"necessary evil" is informal. Use more academic phrasing.}
      141   With the rise of cheap and widely available supercomputing, focus shifted back to more detailed \ac{HH}-type model.
      142   In recent years however, interest in simplified models resurged, driven by mainly two reasons: researchers wanting to progress \acp{ANN} to use more detailed spiking neurons and computational neuroscientists
           getting closer to feasibly simulating whole mammal brains.
      143   \subsection{Parameter Estimation for AdEx Model}

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      151
      152   Hertag et al. \cite{Hertag2011} developed an analytical approximation to the AdEx model to speed up computations.
      153   Using automatic differentiation could also address this issue.
      154 -Jones et al. \cite{Jones2024} and Deistler2025 et al. \cite{Deistler2025} demonstrated that gradient-based methods can effectively parametrize HH-type models.
      154 +Jones et al. \cite{Jones2024} and Deistler2025 et al. \cite{Deistler2025} demonstrated that gradient-based methods can effectively parametrize HH-type models.
          +\mtodo[red]{Typo: "Deistler2025 et al." should be "Deistler et al.~\cite{Deistler2025}"}
      155   However, they require the inherently differentiable nature of HH-type models.
      156   Simplified models require additional treatment to benefit from this technique.
      157

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      174   Neuron models are highly specialised and are fit to very specific data.
      175   Therefore it proves to be difficult to compare models systematically.
      176   Jolivet et al. \cite{Jolivet2008} introduce a coincidence factor, which allows to evaluate neuron models.
      177 -We use the concept to evaluate the quality of trained parameters
      177 +We use the concept to evaluate the quality of trained parameters.\mtodo[yellow]{Incomplete sentence --- missing period.}
      178
      179 -This work will try to replicate the model behaviour given by existing implementations \cite{Stimberg2019} using the parameters given by \cite{Naud2008}.
      179 +This work will try to replicate the model behaviour given by existing implementations \cite{Stimberg2019} using the parameters given by \cite{Naud2008}.
          +\mtodo[orange]{This paragraph is confusingly placed. What exactly is being replicated vs. evaluated?}
      180   For benchmarking the optimisation behaviour, we will fit the model use voltage traces of \acp{SPN} gained from experiments by Johansson et al. \cite{Johansson2020}.
      181
      182   \section{Methodology}\label{sec:method}

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      427   Initial parameters are given in Table \ref{tab:initial-params}.
      428
      429   We evaluated two different loss functions: \ac{MSE} and a differentiable version of a feature based loss developed by Guarino et al.\cite{Guarino2025}, which we will name Guarino loss for the remaining
           report.
      430 -Detailed hyperparameters can be found in Table \ref{tab:training-params}, however, most parameters are chosen arbitrary.
      431 - Due to time reasons no extensive hyperparameter tuning was conducted.
      430 +Detailed hyperparameters can be found in Table \ref{tab:training-params}, however, most parameters are chosen arbitrary.
          +\mtodo[orange]{"arbitrary" is concerning. Even a small ablation study would strengthen this work.}
      431 + Due to time reasons no extensive hyperparameter tuning was conducted.\mtodo[yellow]{Avoid "due to time reasons" --- this undermines your work. Simply state what you did.}
      432   We plan on revising this in future work.
      433
      434   \begin{table}[t]

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 4 lines, removed 4 lines
      550   We use this to compare our fitted parameters.
      551
      552   \section{Experimental Setup}\label{sec:expsetup}
      553 -All experiments were conducted on a 2020 Apple Silicon Mac.
      554 -Software is written in python and executed using python version 3.14.2.
      553 +All experiments were conducted on a 2020 Apple Silicon Mac.\mtodo[orange]{Specify: M1, M2? RAM? This affects reproducibility.}
      554 +Software is written in python and executed using python version 3.14.2.\mtodo[red]{Python 3.14.2 does not exist as of Jan 2026. Verify version number.}
      555   The implementation is built on Jaxley version 0.12.0.
      556 -Comparison were performed using the Brian2 simulator 2.10.1.
      557 -Full list of software versions is found in the \href{https://github.com/paulmyr/DD2375-HT25-Project-Course-in-High-Performance-Computing/blob/master/requirements.txt}{requirements.txt}
      556 +Comparison were performed using the Brian2 simulator 2.10.1.\mtodo[yellow]{Typo: "Comparison" $\rightarrow$ "Comparisons"}
      557 +Full list of software versions is found in the \href{https://github.com/paulmyr/DD2375-HT25-Project-Course-in-High-Performance-Computing/blob/master/requirements.txt}{requirements.txt}
          +\mtodo[orange]{This section is too brief. Add runtime information and number of training runs.}
      558
      559   \section{Results}\label{sec:results}
      560   \subsection{AdEx verification}

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      618   The gradient at any point reflects primarily the instantaneous voltage mismatch rather than structural similarity of the spike trains.
      619   Consequently, gradient descent steps often move parameters in directions that reduce voltage error at specific time points while disrupting the overall firing pattern.
      620
      621 -Additionally, perfekt spike time matchings are punished.
      621 +Additionally, perfekt spike time matchings are punished.\mtodo[yellow]{Typo: "perfekt" $\rightarrow$ "perfect"}
      622   This is because \ac{AdEx} values are reset before the jaxley simulator records the voltage trace --- if experimental data and simulation data would spike at the exact same time,
      623   the loss would be huge (AdEx is at $V_{r}$, experiment is at $V_{\text{peak}}$).
      624   This enforces a mismatch between spike timing and simulation.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      667     \caption{
      668   }\label{fig:coincidence_evaluation}
      669   \end{figure*}
      670 - \itodo[red]{Write caption for this Figure \ref{fig:coincidence_evaluation}}
      670 + \itodo[red]{Write caption for this Figure \ref{fig:coincidence_evaluation}}\mtodo[red]{CRITICAL: Empty caption is unacceptable. This figure needs a full descriptive caption before submission.}
      671
      672   We attribute this to the following reasons:
      673   \begin{itemize}

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      657   \subsection{Coincidence Factor}
      658   To evaluate the performance of the two loss functions, we measured spike timing prediction quality using the coincidence factor $\Gamma$ from Jolivet et al.~\cite{Jolivet2008},
      659   with a coincidence window $\Delta = 2$\,ms.
      660 -We found that for both training approaches (\ac{MSE}-based and guarino-based) could not produce meaningful parameter sets,
      661 -both produced parameter sets having a measured spike timing prediction quality of $\Gamma \approx 0$.
      660 +We found that for both training approaches (\ac{MSE}-based and guarino-based) could not produce meaningful parameter sets,\mtodo[yellow]{Grammar: "for both ... could not" is awkward. Rephrase.}
      661 +both produced parameter sets having a measured spike timing prediction quality of $\Gamma \approx 0$.
          +\mtodo[orange]{This is a significant negative result. Be explicit: both methods essentially perform at chance level.}
      662
      663   \begin{figure*}
      664     \begin{center}

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      685   Future work could address these limitations by carefully adjusting spike-timing-aware loss functions, training on multiple stimulus conditions or changing the recording behaviour of the simulation.
      686
      687   \section{Discussion and Conclusion}\label{sec:discussion}
      688 - We successfully implemented the \ac{AdEx} model in Jaxley and enable automatic differentiation through surrogate gradients.
      688 + We successfully implemented the \ac{AdEx} model in Jaxley and enable automatic differentiation through surrogate gradients.\mtodo[orange]{Given $\Gamma \approx 0$ results, "successfully" only applies to
          +implementation, not to the optimization goal. Be clearer about what worked and what didn't.}
      689   We discovered that \ac{MSE} is fundamentally unsuitable for training spiking behaviour.
      690   Feature-based losses show more promising optimization results, however, differentiability of the loss function as a fundamental requirement makes this a non-trivial problem to tackle.
      691   First evaluation showed that spike timing precision remains challenging, however it is a crucial requirement for useful bio-physical neuron simulations.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      703
      704   We bridged two worlds: Gradient optimization methods using surrogate gradients and parameter fitting for simplified biophysical models.
      705   We discovered that loss function design matters more than the optimization algorithm and were able to produce a testing framework that showed exactly this.
      706 -The main contribution was to implement a differentiable AdEx model Jaxley.
      707 -We gained an understanding of loss requirements, and will iterate on this in the future.
      706 +The main contribution was to implement a differentiable AdEx model Jaxley.\mtodo[yellow]{Missing "in" --- "model in Jaxley".}
      707 +We gained an understanding of loss requirements, and will iterate on this in the future.\mtodo[yellow]{"will iterate on this in the future" is informal and weak for a conclusion.}
      708
      709   \section*{Acknowledgment}\label{sec:ack}
      710   I want to thank Alexander Kozlov for suggesting this topic and providing valuable insight and resources.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      707   We gained an understanding of loss requirements, and will iterate on this in the future.\mtodo[yellow]{"will iterate on this in the future" is informal and weak for a conclusion.}
      708
      709   \section*{Acknowledgment}\label{sec:ack}
      710 -I want to thank Alexander Kozlov for suggesting this topic and providing valuable insight and resources.
      711 - I also want to thank Johan Eklund for my supervision.
      710 +I want to thank Alexander Kozlov for suggesting this topic and providing valuable insight and resources.\mtodo[yellow]{Standard form: "The author thanks..." rather than "I want to thank..."}
      711 + I also want to thank Johan Eklund for my supervision.\mtodo[yellow]{"for my supervision" $\rightarrow$ "for his supervision" or "for supervising this work".}
      712
      713   \section*{AI assistance disclosure}\label{sec:ai}
      714   AI assistance was used for this project.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      491   To capture the essential characteristics of a neuron, they identified:
      492   \begin{itemize}
      493       \item \textbf{Spike timing:} time to first ($t_1$), second ($t_2$), third ($t_3$), and last spike ($t_{\text{last}}$)
      494 -    \item \textbf{Interspike intervals:} inverse of first ISI ($1/\text{ISI}1$) and last ISI ($1/\text{ISI}{\text{last}}$)\mtodo{format this nicer}
      494 +    \item \textbf{Interspike intervals:} inverse of first ISI ($1/\text{ISI}1$) and last ISI ($1/\text{ISI}{\text{last}}$)\mtodo[red]{Fix LaTeX formatting: should be $1/\text{ISI}
          +_1$ and $1/\text{ISI}_{\text{last}}$. Also remove your own TODO before submission.}
      495       \item \textbf{Firing rate:} mean firing frequency over the stimulus duration
      496       \item \textbf{Subthreshold behaviour:} membrane voltage at stimulus end ($V_{\text{stimend}}$)
      497   \end{itemize}

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      537   The \textbf{Coincidence Factor for Spike Train Evaluation $\Gamma$} measures spike timing prediction quality, normalized by chance level.
      538   It is given by
      539   \begin{equation}
      540 -   \Gamma = \frac{N_{coinc} - \langle N_{coinc} \rangle}{0.5(N_{data} + N_{model})} \cdot \frac{1}{1 - 2f\Delta}
      540 +   \Gamma = \frac{N_{coinc} - \langle N_{coinc} \rangle}{0.5(N_{data} + N_{model})} \cdot \frac{1}{1 - 2f\Delta}
      541     \label{eq:coincidence-factor}
      542 - \end{equation}\mtodo{verify formula}
      542 + \end{equation}\mtodo[red]{Your own TODO "verify formula" is still here. Verify and remove before submission.}
      543   where $N_{coinc}$ describe coincidences within $\pm\Delta$ (default 2ms)
      544   and $f$ is the model firing rate.
      545

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 2 lines, removed 2 lines
      416   \subsubsection{Dataset}\label{sec:data-set}
      417   We use intracellular recordings from striatal projection neurons provided by Johansson and Silberberg \cite{Johansson2020}.
      418   The dataset contains voltage traces from four distinct striatal neuron types, recorded under current-clamp conditions.
      419 -However, we only used a single trace\footnote{Files can be found
          -\href{https://github.com/a1eko/humanspn/tree/df6ec55178c81e64fdcf4ae79aaa1872458c621f/models/optimisations/mCP-dspn-e150917_c6_D1-manimal_1_n24_04102017_cel1/expdata}{here}.
      419 +However, we only used a single trace\footnote{Files can be found
          +\href{https://github.com/a1eko/humanspn/tree/df6ec55178c81e64fdcf4ae79aaa1872458c621f/models/optimisations/mCP-dspn-e150917_c6_D1-manimal_1_n24_04102017_cel1/expdata}{here}.
      420   Voltage file: \texttt{ECBL\_IDthresh\_ch5\_553.dat}
      421 -Current file: \texttt{ECBL\_IDthresh\_ch4\_553.dat}}, mainly due to time constraint.
      421 +Current file: \texttt{ECBL\_IDthresh\_ch4\_553.dat}}, mainly due to time constraint.\mtodo[orange]{Using a single trace severely limits generalizability. Acknowledge this as a major limitation.}
      422
      423   \subsubsection{Optimisation Setup}\label{sec:optimization-setup}
      424

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      422
      423   \subsubsection{Optimisation Setup}\label{sec:optimization-setup}
      424
      425 -We optimise the following subset of \ac{AdEx} parameters: $\{g_L, E_L, V_T, a, b, \tau_w, V_T, v_{\text{reset}}\}$.
      425 +We optimise the following subset of \ac{AdEx} parameters: $\{g_L, E_L, V_T, a, b, \tau_w, V_T, v_{\text{reset}}\}$.\mtodo[red]{$V_T$ appears twice in this set. Remove duplicate.}
      426   Parameters $\{C_m, \Delta_T, v_threshold\}$ were fixed.
      427   Initial parameters are given in Table \ref{tab:initial-params}.
      428

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      423   \subsubsection{Optimisation Setup}\label{sec:optimization-setup}
      424
      425   We optimise the following subset of \ac{AdEx} parameters: $\{g_L, E_L, V_T, a, b, \tau_w, V_T, v_{\text{reset}}\}$.\mtodo[red]{$V_T$ appears twice in this set. Remove duplicate.}
      426 - Parameters $\{C_m, \Delta_T, v_threshold\}$ were fixed.
      426 + Parameters $\{C_m, \Delta_T, v_threshold\}$ were fixed.\mtodo[yellow]{Inconsistent notation: $v\_threshold$ should be $v_{\text{threshold}}$ to match earlier usage.}
      427   Initial parameters are given in Table \ref{tab:initial-params}.
      428
      429   We evaluated two different loss functions: \ac{MSE} and a differentiable version of a feature based loss developed by Guarino et al.\cite{Guarino2025}, which we will name Guarino loss for the remaining
           report.

⏺ Update(2_paper/differentiable_adex.tex)
  ⎿  Added 1 line, removed 1 line
      712
      713   \section*{AI assistance disclosure}\label{sec:ai}
      714   AI assistance was used for this project.
      715 - I used Anthropics Opus 4.5 via Claude Code.
      715 + I used Anthropics Opus 4.5 via Claude Code.\mtodo[yellow]{"Anthropics" $\rightarrow$ "Anthropic's" (possessive).}
      716   Usage mainly included writing feedback, code refactoring, documentation of code and plotting scripts.
      717   For example, I used claude to rewrite my evaluation files into a coherent python module (see
           \href{https://github.com/paulmyr/DD2375-HT25-Project-Course-in-High-Performance-Computing/blob/master/8_claude/evaluation_code_refactoring.md}{this prompt}).
      718   It also included transcribing lists of values into tables (e.g. Table \ref{tab:adex_params}) from code or text files.

⏺ I have annotated your report with \mtodo[color]{...} comments. Here is a summary of my critique:

  Critical Issues (Red)

  1. Abstract is missing - This is unacceptable. You have only a TODO placeholder.
  2. Empty figure caption (Figure 4) - Must be filled before submission.
  3. Malformed equation (Eq. 3) - The reset condition syntax is broken.
  4. Typos in text - "Deistler2025 et al." instead of "Deistler et al.", Python version 3.14.2 doesn't exist.
  5. Unresolved TODOs - You left your own TODOs in the submission ("verify formula", "format this nicer").
  6. Duplicate parameter - $V_T$ appears twice in the trainable parameters set.

  Significant Issues (Orange)

  1. Weak third contribution - "$\Gamma \approx 0$" means both methods failed. State this clearly rather than saying "challenges remain."
  2. Arbitrary hyperparameters - No ablation study undermines credibility.
  3. Single training trace - This severely limits generalizability.
  4. Brief experimental setup - Missing hardware specs, runtime, number of runs.
  5. Claims vs. results mismatch - You claim "success" but achieved chance-level performance.

  Writing Issues (Yellow)

  - Multiple grammar errors ("it's" vs "its", "perfekt", "an slope")
  - Informal language ("necessary evil", "This could change soon")
  - Awkward phrasing throughout
  - Inconsistent notation ($vthreshold$ vs $v_{\text{threshold}}$)

  Structural Concerns

  - Background section ends with a sentence that belongs in Introduction
  - Related Work subsection on benchmarks is confusingly placed
  - Discussion doesn't clearly separate what worked from what didn't

  Before Submission

  1. Write the abstract immediately
  2. Fix all red-flagged issues
  3. Proofread for typos and grammar
  4. Remove all internal TODOs
  5. Be honest about negative results - $\Gamma \approx 0$ is a meaningful finding about the difficulty of this problem

  The implementation work appears solid, but the writing and presentation need significant polish. The negative results are publishable if framed correctly as insights into loss function requirements.

✻ Baked for 3m 54s
