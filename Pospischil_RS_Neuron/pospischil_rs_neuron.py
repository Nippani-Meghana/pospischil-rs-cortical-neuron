#POSPISCHIL ET AL(2008) RS CORTICAL NEURON MODEL

import matplotlib.pyplot as plt
import numpy as np


#Constant Variables
gNa = 50
gNaP = 0.15
gK = 5
gL = 0.05
gM = 0.07
ENa = 50
EK = -90
EL = -70
Cm = 1
V0 = -65
Iext = 14
t_ref = 2
m = 0.05
h = 0.60
n = 0.318
p = 0.05
dt = 0.01
Vth = -20
V_reset = -65


def mNap_inf(V, theta=-55.0, k=6.0):
    return 1.0 / (1.0 + np.exp(-(V - theta) / k))

def neuron_model(V,t,m,h,n,p, gNa, gNaP):
    alpha_m = (0.1*(V + 40))/(1 - (np.exp(-(V + 40)/10)))
    beta_m = 4*(np.exp(-(V + 65)/18))
    m_inf = alpha_m/(alpha_m+beta_m)
    tau_m = 1/(alpha_m + beta_m)
    alpha_h = 0.07*(np.exp(-(V + 65)/20))
    beta_h = 1/(1 + (np.exp(-(V + 35)/10)))
    h_inf = alpha_h/(alpha_h + beta_h)
    tau_h = 1/(alpha_h + beta_h)
    alpha_n = (0.01*(V + 55))/(1 - np.exp(-(V + 55)/10))
    beta_n = 0.125*(np.exp(-(V+65)/80))
    n_inf = alpha_n/(alpha_n + beta_n)
    tau_n = 1/(alpha_n + beta_n)
    p_inf = 1/(1 + np.exp(-(V + 35)/10))
    tau_p = 100

    if t > 1:
        m += (dt)*((m_inf - m)/tau_m)
        h += (dt)*((h_inf - h)/tau_h)
        n += (dt)*((n_inf - n)/tau_n)
        p += (dt)*((p_inf - p)/tau_p)

    INa = gNa*pow(m,3)*h*(V - ENa)
    IK = gK*pow(n,4)*(V - EK)
    IL = gL*(V - EL)
    INaP = gNaP *mNap_inf(V)*(V - ENa)
    IM = gM*p*(V - EK)
    dVdt = (Iext - (INa + IK + IL + INaP + IM))/Cm
    return dVdt,m,h,n,p


def call_method(gNa, gNaP, T = 100.0):
    V = -65.0
    m = 0.05
    h = 0.60
    n = 0.318
    p = 0.05
    spike_times = []
    V_collections = []
    oldV = V
    refractory_remain = 0.0
    for t in np.arange(0,T,dt):
        if refractory_remain > 0:
            dVdt,m,h,n,p = neuron_model(V_reset,t,m,h,n,p,gNa,gNaP)
            V_collections.append(V)
            refractory_remain -= dt
            oldV = V
            continue

        oldV = V
        dVdt,m,h,n,p = neuron_model(V,t,m,h,n,p,gNa,gNaP)
        V += dt*dVdt

        if oldV<Vth and V>=Vth:
            spike_times.append(t)
            refractory_remain = t_ref
            V = V_reset

        V_collections.append(V)
        

    return spike_times, V_collections
    
def plot_spikes():
    print("Spikes at (ms):", np.round(spike_times, 2))
    t = np.arange(len(V_collections)) * dt
    plt.xlabel("Time (ms)")
    plt.plot(t, V_collections)
    plt.ylabel("membrane Potential (mV)")
    plt.title("RS Cortical Neuron")
    plt.show()

def metrics(spike_times, V_collections):
    num = len(spike_times)
    first = None if num == 0 else spike_times[0]
    finalV = None if len(V_collections) == 0 else V_collections[-1]
    return num, first, finalV

def fmt_ms(x):   return "—" if x is None else f"{x:.2f}"
def fmt_mv(x):   return "—" if x is None else f"{x:.1f}"

def all_cases(cases, T=200.0):
    print("\nSummary (T = %.0f ms, dt = %.2f ms, Iext = %.1f)" % (T, dt, Iext))
    print(f"{'Case':28s} | {'Spikes':6s} | {'First spike (ms)':15s} | {'Final V (mV)':12s}")
    print("-"*28 + "-+-" + "-"*6 + "-+-" + "-"*15 + "-+-" + "-"*12)
    for name, gNa_eff, gNaP_eff in cases:
        spk, Vc = call_method(gNa_eff, gNaP_eff, T=T)
        num, first, finalV = metrics(spk, Vc)
        print(f"{name:28s} | {num:6d} | {fmt_ms(first):15s} | {fmt_mv(finalV):12s}")

cases = [
    ("Normal",                 50.0,                 0.15),
    ("Valproate 100µM",        50.0*(1-0.20),        0.15),
    ("Valproate 200µM",        50.0*(1-0.30),        0.15),
    ("Valproate 300µM",        50.0*(1-0.40),        0.15),
    ("Lamotrigine 100µM",      50.0,                 0.15*(1-0.50)),
    ("Lamotrigine 200µM",      50.0,                 0.15*(1-0.65)),
    ("Lamotrigine 300µM",      50.0,                 0.15*(1-0.75)),
    ("Combo 100+100µM",        50.0*(1-0.20),        0.15*(1-0.50)),
    ("Combo 200+200µM",        50.0*(1-0.30),        0.15*(1-0.65)),
    ("Combo 300+300µM",        50.0*(1-0.40),        0.15*(1-0.75)),
]


while True:
    print("\nWelcome to the Pospischil RS Cortical Neuron Menu :")
    print("1. Normal Spike Neuron Data ")
    print("2. Valpraote Introduced Neuron Data")
    print("3. Lamotrigine Introduced Neuron Data")
    print("4. Valproate + Lamotrigine Introduced Neuron Data")
    print("5. Analytics")
    print("6. Exit")

    choice = input("Please Enter Your Option(1-5) : ")

    if choice == '1':
        gNa = 50
        gNaP = 0.15
        spike_times, V_collections = call_method(gNa, gNaP, T = 100.0)
        plot_spikes()
    
    elif choice == '2':
        gNaP = 0.15
        while True:
            print("\nPlease Select Dosage of Valproate :")
            print("1. 100 micro M")
            print("2. 200 micro M")
            print("3. 300 micro M")
            print("4. Return to Main Menu")
            ch = input("Please Select Your Option(1-4) : ")
            if ch == '1':
                gNa -= 0.20 * gNa
            elif ch == '2':
                gNa -= 0.3 * gNa
            elif ch == '3':
                gNa -= 0.4 * gNa
            elif ch == '4':
                print("You Will Now Return To Main Menu")
                break
            else :
                print("Invalid Choice!")
                continue
            spike_times, V_collections = call_method(gNa, gNaP, T = 100.0)
            plot_spikes()

    elif choice == '3':
        gNa = 50
        while True:
            print("Please Select Dosage of Lamotrigine : ")
            print("1. 100 micro M")
            print("2. 200 micro M")
            print("3. 300 micro M")
            print("4. Return to Main Menu")
            ch = input("Please Select Your Option(1-4) : ")
            if ch == '1':
                gNaP -= 0.50 * gNaP
            elif ch == '2':
                gNaP -= 0.65 * gNaP
            elif ch == '3':
                gNaP -= 0.75 * gNaP
            elif ch == '4':
                print("You Will Now Return To Main Menu")
                break
            else :
                print("Invalid Choice!")
                continue
            spike_times, V_collections = call_method(gNa, gNaP, T = 100.0)
            plot_spikes()

    elif choice == '4':
        while True:
            print("Please Select Dosage of Valproate and Lamotrigine : ")
            print("1. 100 micro M each")
            print("2. 200 micro M each")
            print("3. 300 micro M each")
            print("4. Return to Main Menu")
            ch = input("Please Select Your Option(1-4) : ")
            if ch == '1':
                gNa -= 0.20 * gNa
                gNaP -= 0.50 * gNaP
            elif ch == '2':
                gNa -= 0.3 * gNa
                gNaP -= 0.65 * gNaP
            elif ch == '3':
                gNa -= 0.4 * gNa
                gNaP -= 0.75 * gNaP
            elif ch == '4':
                print("You Will Now Return To Main Menu")
                break
            else :
                print("Invalid Choice!")
                continue
            spike_times, V_collections = call_method(gNa, gNaP, T = 100.0)
            plot_spikes()

    elif choice =='5':
        all_cases(cases, T=100.0)

    elif choice == '6':
        print("Program Terminated Successfully! Have a Great Day!")
        break
    
    else:
        print("Invalid Choice!")
        continue
