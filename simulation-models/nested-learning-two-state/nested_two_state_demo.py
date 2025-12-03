import numpy as np
import matplotlib.pyplot as plt

# --- KONFIGURATION (Beibehalten der stabilen Rate) ---
NUM_STEPS = 5000         
LEARNING_RATE = 0.001    # Niedrige Rate für Stabilität
P_CHANGE = 0.2           

# --- AGENT B: DER WECHSLER (Der Beobachter) ---
M = np.random.rand(2, 2)
M = M / M.sum(axis=1, keepdims=True) 

error_history = []
m_history = [M.copy()]

# --- AGENT A: DAS SYSTEM ---
system_state = 0 # Zustand 0 oder 1
M_TRUE = np.array([[1 - P_CHANGE, P_CHANGE], [P_CHANGE, 1 - P_CHANGE]])

print(f"Simulation gestartet. Wahrer P(wechsel) = {P_CHANGE}. NEUE KORRIGIERTE LERNREGEL.")

# --- SIMULATIONS-LOOP ---
for t in range(NUM_STEPS):
    # Aktueller Zustand (Index)
    current_state_index = system_state
    
    # 1. VORHERSAGE (Der Vorhersagevektor $\hat{O}_{t+1}$ ist die entsprechende Zeile in M)
    prediction = M[current_state_index, :] # <- Das ist der Vektor der Vorhersagewahrscheinlichkeiten

    # System-Schritt: Nächsten Zustand bestimmen
    if np.random.rand() < P_CHANGE:
        system_state = 1 - system_state
    
    # Nächste Beobachtung (Tatsächliche Realität: O_{t+1}) als Vektor
    next_obs = np.array([1.0, 0.0] if system_state == 0 else [0.0, 1.0])

    # 2. LERNSCHLEIFE (Update der Matrix)
    error = next_obs - prediction # Fehler ist der Unterschied zwischen Realität und Vorhersage
    
    # WICHTIG: Korrigierte Regel: Passe NUR die Zeile des aktuellen Zustands an!
    # Die Anpassung erfolgt entlang des Fehlervektors.
    M[current_state_index, :] += LEARNING_RATE * error

    # 3. NORMALISIERUNG und CLIPPING (Absicherung gegen Instabilität)
    M = np.clip(M, 0.0001, 1.0)
    M = M / M.sum(axis=1, keepdims=True) 

    step_error = np.sum(error**2)
    error_history.append(step_error)
    m_history.append(M.copy())


# --- VISUALISIERUNG (unverändert) ---
window_size = 50 
smoothed_error = np.convolve(error_history, np.ones(window_size)/window_size, mode='valid')
m_history = np.array(m_history)
learned_transition_prob = m_history[:, 0, 1] 

print("\n--- ERGEBNIS ---")
print(f"Wahre Übergangsmatrix (P_TRUE):\n {M_TRUE.round(4)}")
print(f"Gelernte Übergangsmatrix (M_FINAL):\n {M.round(4)}")
print(f"Durchschn. Fehler (Start): {np.mean(error_history[:500]):.4f}")
print(f"Durchschn. Fehler (Ende): {np.mean(error_history[-500:]):.4f}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(smoothed_error)
plt.title('Emergentes Verhalten: Reduktion des Vorhersagefehlers (Surprise)')
plt.xlabel('Zeit (Simulationsschritte)')
plt.ylabel('Geglätteter Quadratfehler')
plt.grid(True, alpha=0.5)

plt.subplot(1, 2, 2)
plt.plot(learned_transition_prob, label=r'Gelerntes $P(S_2 | S_1)$')
plt.axhline(P_CHANGE, color='red', linestyle='--', label=r'Wahres $P(S_2 | S_1)$')
plt.title('Agent lernt die System-Regel (Konvergenz)')
plt.xlabel('Zeit (Simulationsschritte)')
plt.ylabel('Wahrscheinlichkeitswert')
plt.legend()
plt.grid(True, alpha=0.5)

plt.tight_layout()
plt.show()
