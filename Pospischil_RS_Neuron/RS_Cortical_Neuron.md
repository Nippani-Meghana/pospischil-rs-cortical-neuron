# A Minimal RS Cortical Neuron With Heuristic Drug Blocks (Python Implementation)

**Author:** Nippani Meghana
**Affiliation:** Independent student project
**Date:** 08 August 2025
**Keywords:** Hodgkin–Huxley, cortical neuron, Pospischil model, persistent sodium, M‑current, valproate, lamotrigine

---

## Abstract

This short report documents a didactic Python implementation of a regular‑spiking (RS) cortical neuron inspired by the model family of Pospischil et al. (2008). The aim is to provide a readable, single‑file simulator that demonstrates how reducing fast transient sodium conductance ($g_{Na}$) and persistent sodium conductance ($g_{NaP}$), used here as heuristic proxies for valproate and lamotrigine, respectively shifts neuronal excitability under constant current injection. I summarize the equations, numerical methods, parameter choices, and a small set of experiments that report spike count, first‑spike latency, and final membrane potential across baseline and drug‑scaled conditions. The emphasis is clarity and reproducibility rather than parameter‑identical replication of a particular cell.

> **Cautionary statement — Educational use only.** This project is a simplified, student‑oriented implementation of an HH‑type RS cortical neuron. The “drug” manipulations are heuristic conductance scalings; they are not pharmacological models and they do not encode dosing guidance, safety information, or clinical efficacy. Results are qualitative and unvalidated. Do not use this code or its outputs to diagnose, treat, or guide any medical decision, laboratory protocol, or device design. For research or clinical applications, consult the primary literature, use validated models and datasets, and obtain appropriate ethics and regulatory approvals.

---

## 1. Introduction

Minimal Hodgkin–Huxley–type models are useful for teaching because they preserve the core nonlinear mechanisms behind spike initiation and adaptation without requiring heavy toolchains. The RS phenotype is a common cortical firing class. In this project, I translated a compact RS formulation into a single Python script that depends only on NumPy and Matplotlib and added a command‑line menu to explore conductance scalings as simple stand‑ins for two antiepileptic drugs.

---

## 2. Methods

### 2.1 State and currents

The model is a single, isopotential compartment with state variables $V$ (mV) and four gating variables: $m, h$ for fast sodium, $n$ for delayed rectifier potassium, and $p$ for the M‑type potassium current (slow adaptation).

The membrane equation is

```
C_m dV/dt = I_ext − (I_Na + I_K + I_L + I_NaP + I_M)
```

Currents:

```
I_Na  = g_Na  * m^3 * h           * (V − E_Na)
I_K   = g_K   * n^4                * (V − E_K)
I_L   = g_L                        * (V − E_L)
I_NaP = g_NaP * mNap_inf(V)        * (V − E_Na)
I_M   = g_M   * p                  * (V − E_K)
```

### 2.2 Gating kinetics

Transient Na and K gates use classical HH‑style rate functions. For readability I keep the original forms commonly seen in textbooks; steady‑states and time constants are derived as

```
m_inf = α_m / (α_m + β_m),   τ_m = 1 / (α_m + β_m)
... similarly for h and n
```

The M‑current gate $p$ is first‑order with a sigmoidal steady‑state and a long time constant (here, τ\_p = 100 ms):

```
p_inf(V) = 1 / (1 + exp(-(V + 35)/10))
```

Persistent sodium activation is a simple Boltzmann function:

```
mNap_inf(V) = 1 / (1 + exp(-(V − θ)/k))  with θ = −55 mV, k = 6 mV
```

### 2.3 Spike bookkeeping and numerics

Threshold‑and‑reset is used only for counting spikes and enforcing an absolute refractory period:

* Spike detected when V crosses V\_th upward (default −20 mV).
* After a spike, V is reset to V\_reset (−65 mV) and held for t\_ref = 2 ms.

Integration uses forward Euler with a fixed step (dt = 0.01 ms). This is sufficient for classroom exploration; for research use I would switch to an adaptive method and event‑based spike detection without a hard reset.

### 2.4 Baseline parameter set

```
E_Na =  50 mV,  E_K = −90 mV,  E_L = −70 mV
C_m  =   1 μF/cm²
g_Na = 50 mS/cm², g_K = 5 mS/cm², g_L = 0.05 mS/cm²
g_NaP = 0.15 mS/cm², g_M = 0.07 mS/cm²
I_ext = 14 μA/cm² (constant drive in examples)
```

---

## 3. Heuristic drug mapping

I treat drug application as a fixed scaling of the relevant maximal conductance:

* **Valproate proxy:** reduce `g_Na` by a chosen fraction.
* **Lamotrigine proxy:** reduce `g_NaP` by a chosen fraction.

This is intentionally simple and does not model binding kinetics or channel‑state specificity. The menu exposes three nominal “doses” for each drug and combinations thereof. For example:

| Condition          | g\_Na scale | g\_NaP scale |
| ------------------ | ----------- | ------------ |
| Baseline           | 1.00        | 1.00         |
| Valproate 100 μM   | 0.80        | 1.00         |
| Valproate 200 μM   | 0.70        | 1.00         |
| Valproate 300 μM   | 0.60        | 1.00         |
| Lamotrigine 100 μM | 1.00        | 0.50         |
| Lamotrigine 200 μM | 1.00        | 0.35         |
| Lamotrigine 300 μM | 1.00        | 0.25         |
| Combo 100+100 μM   | 0.80        | 0.50         |
| Combo 200+200 μM   | 0.70        | 0.35         |
| Combo 300+300 μM   | 0.60        | 0.25         |

These values are placeholders to demonstrate qualitative effects on excitability.

---

## 4. Simulation protocol and metrics

All experiments below use T = 100 ms, dt = 0.01 ms, I\_ext = 14 μA/cm² unless stated otherwise. For each condition I record:

1. **Spike count** (number of detected threshold crossings)
2. **First‑spike latency** (ms)
3. **Final membrane potential** at t = T (mV)

A convenience function batch‑runs all menu conditions and prints a compact summary table.

---

## 5. Results (qualitative summary)

Baseline parameters produce tonic spiking under constant drive. As `g_Na` is reduced (valproate proxy), spike initiation weakens: first‑spike latency increases and total spike count drops. Reducing `g_NaP` (lamotrigine proxy) primarily shifts the depolarizing bias and therefore increases the effective rheobase; at fixed input, this also reduces spike count and can abolish spiking at stronger reductions. The combined condition predictably compounds both effects.

Because the model includes an M‑current, interspike intervals typically lengthen modestly over time (spike‑frequency adaptation), which can become more apparent when spiking is just above threshold.

I emphasize that these are qualitative behaviors; the project is not a pharmacodynamic study and does not attempt dose‑response fitting.

---

## 6. Discussion

This compact implementation is meant to lower the barrier to interacting with HH‑type dynamics. It shows how a few conductance scalings already generate the expected shifts in excitability. It also makes it clear where simplicity enters: a single compartment, fixed time step, and hard threshold for spike counting. These choices make the code approachable for students while leaving room for principled extensions.

Two observations stood out in practice:

1. Small changes to `g_NaP` can have outsized effects on firing at near‑threshold inputs because the persistent current effectively biases the voltage nullcline.
2. The M‑current provides a gentle adaptation without dramatically reshaping the action potential, which helps keep the focus on Na/NaP manipulations.

---

## 7. Limitations

* Single compartment; no dendritic processing or axial currents.
* Deterministic; no channel noise or synaptic noise.
* Heuristic drug mapping via fixed conductance scaling; no binding kinetics or state‑dependent block.
* Forward Euler integration; acceptable for small dt but not optimal.
* Parameter values are pedagogical; they are not tuned to a specific cell recording.

---

## 8. Reproducibility and usage

Environment:

```
Python 3.9+
pip install numpy matplotlib
```

Run:

```
python pospischil_rs_neuron.py
```

Use the menu to select baseline or drug conditions, plot traces, and print the analytics table. All key parameters are defined at the top of the script and can be edited directly.


---

## 9. References

Pospischil M., Toledo‑Rodriguez M., Monier C., et al. (2008). Minimal Hodgkin–Huxley type models for different classes of cortical and thalamic neurons. *Biological Cybernetics*.

*Note:* This project is a teaching‑oriented reimplementation that follows the RS phenomenology rather than reproducing a parameter table verbatim. Please consult the original paper for canonical formulations and comparative validation across neuron classes.
