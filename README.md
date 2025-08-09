# Pospischil et al. (2008) RS Cortical Neuron — Drug Effects Simulator (Python)

A compact, single‑file **Hodgkin–Huxley–type** simulator of a regular‑spiking (RS) cortical neuron, adapted for teaching and exploratory analysis. The model includes transient sodium (Na⁺), delayed‑rectifier potassium (K⁺), leak, persistent sodium (NaP), and M‑type K⁺ currents. It demonstrates how heuristic conductance scalings—used here as stand‑ins for **valproate** (reducing `gNa`) and **lamotrigine** (reducing `gNaP`)—shift excitability, spike timing, and steady‑state membrane potential under tonic input.

> **Caution — Educational use only.** The “drug” manipulations below are heuristic conductance scalings, not pharmacological models. They do not encode dosing guidance or clinical efficacy. Results are qualitative and unvalidated. Do not use this repository to make medical or laboratory decisions.

---

## Background / Author Bio

I built this repository as a concise learning artifact while studying computational models of neuronal excitability. I am an undergraduate in computer science with interests in **computational neuroscience**, **computational psychiatry**, **machine learning**, and **systems modeling**. My goal is to translate primary‑literature models into readable Python that others can study, modify, and extend without heavy dependencies.

This project focuses on the RS neuron archetype popularized by **Pospischil et al. (2008)**. Rather than reproducing a specific parameter table verbatim, I prioritize clarity and reproducibility. The drug conditions are **didactic proxies** implemented as fixed conductance scalings; they illustrate qualitative shifts in excitability but are not intended as biophysical or clinical models. Feedback and suggested extensions are welcome.

---

## Features

* Minimal HH‑type RS neuron with `I_Na`, `I_K`, `I_L`, `I_NaP`, `I_M`
* Persistent‑sodium activation via a Boltzmann `mNap_inf(V)`
* Spike detection by upward threshold crossing with absolute refractory period
* Command‑line menu for baseline, valproate‑proxy, lamotrigine‑proxy, and combo conditions
* “Analytics” mode printing spike count, first‑spike latency, and final membrane potential for all scenarios

---

## Model overview

**Membrane equation**

```
C_m dV/dt = I_ext − (I_Na + I_K + I_L + I_NaP + I_M)
```

**Currents**

```
I_Na  = g_Na  * m^3 * h           * (V − E_Na)
I_K   = g_K   * n^4                * (V − E_K)
I_L   = g_L                        * (V − E_L)
I_NaP = g_NaP * mNap_inf(V)        * (V − E_Na)
I_M   = g_M   * p                  * (V − E_K)
```

**Gates** use HH‑style kinetics for `(m,h,n)` and a slow first‑order gate for `p` (M‑current). Integration uses forward Euler (fixed `dt`), which keeps the code short and readable.

---

## Installation

**Requirements:** Python 3.9+, NumPy, Matplotlib

```bash
python pospischil_rs_neuron.py
```

Menu options:

1. Normal neuron
2. Valproate series (reduces `gNa`)
3. Lamotrigine series (reduces `gNaP`)
4. Combo (valproate + lamotrigine)
5. Analytics (batch‑run all cases)
6. Exit

---

## Scenarios (heuristic scalings)

| Case               | `gNa` scale | `gNaP` scale | Notes                          |
| ------------------ | ----------- | ------------ | ------------------------------ |
| Baseline           | 1.00        | 1.00         | RS under constant drive        |
| Valproate 100 μM   | 0.80        | 1.00         | Reduced fast Na⁺ availability  |
| Valproate 200 μM   | 0.70        | 1.00         | Stronger Na⁺ reduction         |
| Valproate 300 μM   | 0.60        | 1.00         | Strongest Na⁺ reduction in set |
| Lamotrigine 100 μM | 1.00        | 0.50         | Partial NaP block              |
| Lamotrigine 200 μM | 1.00        | 0.35         | Deeper NaP block               |
| Lamotrigine 300 μM | 1.00        | 0.25         | Strongest NaP block in set     |
| Combo 100+100 μM   | 0.80        | 0.50         | Joint Na and NaP reduction     |
| Combo 200+200 μM   | 0.70        | 0.35         | Mid‑range joint reduction      |
| Combo 300+300 μM   | 0.60        | 0.25         | Highest joint reduction        |

---

## Output

* **Trace plot:** membrane potential vs time
* **Spike times:** printed to console
* **Analytics table:** spike count, first‑spike latency, final voltage for all scenarios

Example header (illustrative):

```
Summary (T = 100 ms, dt = 0.01 ms, Iext = 14.0)
Case                         | Spikes | First spike (ms) | Final V (mV)
...
```

---

## Key parameters (defaults)

`Cm=1 μF/cm²`, `ENa=50 mV`, `EK=−90 mV`, `EL=−70 mV`, `gNa=50 mS/cm²`, `gK=5 mS/cm²`, `gL=0.05 mS/cm²`, `gNaP=0.15 mS/cm²`, `gM=0.07 mS/cm²`, `Iext=14 μA/cm²`, `dt=0.01 ms`, `Vth=−20 mV`, `V_reset=−65 mV`, `t_ref=2 ms`.

---

## Design assumptions

* Single, isopotential compartment; no dendrites/axons
* Deterministic dynamics; no channel or synaptic noise
* Heuristic drug mapping via fixed conductance scalings
* Fixed‑step Euler for simplicity (consider RK/adaptive for research use)


---

## References

* Pospischil M., Toledo‑Rodriguez M., Monier C., et al. (2008). Minimal Hodgkin–Huxley type models for different classes of cortical and thalamic neurons. *Biological Cybernetics*.

---

## Citation

If you use this repository for teaching or demos, please cite the original paper and this implementation, for example:

> Pospischil RS Cortical Neuron — Drug Effects Simulator (Python), year of access. Based on Pospischil et al. (2008), *Biol. Cybern.*

---

## Acknowledgments

Thanks to prior RS formulations in the literature, especially Pospischil et al., and to the open‑source community for NumPy and Matplotlib.
