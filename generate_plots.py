import matplotlib.pyplot as plt
import numpy as np

# --- PEŁNE DANE Z 3 PRZEBIEGÓW TESTU T02 ---
fps_data = [
    # Przebieg 1
    19, 19, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 17, 15, 16, 15, 16, 15, 16, 16, 15, 15, 16, 15, 16, 15, 15, 16, 16, 15, 15, 15, 16, 16, 14, 16, 14, 16, 16, 15, 16, 16, 15, 16, 16, 16, 16, 14, 17, 16, 15, 15, 16, 15, 15, 16, 15, 15, 16, 16, 15, 16, 18, 15, 16, 15, 16, 15, 16, 16, 15, 16, 16, 16, 16, 16, 15, 16, 15, 15, 15, 16, 16, 17, 15, 16, 16, 16, 15, 16, 15, 16, 16, 15, 16, 16, 15, 16, 14, 17, 14, 17, 15, 15, 15, 16, 15, 16, 15, 16, 14, 16, 14, 16, 15, 16, 15, 15, 16, 15, 15, 16, 15, 15, 16, 15, 16, 15, 16, 15, 16, 15, 16, 14, 17, 15, 16, 15, 17, 16, 15, 17, 15, 16, 15, 16, 15, 15, 15, 15, 16, 16,
    # Przebieg 2
    19, 19, 19, 19, 18, 19, 19, 19, 18, 17, 18, 10, 19, 19, 19, 19, 19, 19, 18, 19, 17, 15, 16, 16, 15, 15, 16, 15, 16, 16, 16, 16, 15, 15, 16, 15, 15, 15, 16, 16, 16, 16, 16, 15, 16, 16, 15, 16, 15, 16, 13, 17, 14, 17, 14,
    # Przebieg 3
    19, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 16, 16, 15, 16, 15, 16, 15, 16, 15, 15, 15, 15, 15, 15, 16, 15, 15, 16, 16, 15, 16, 16, 16, 16, 15, 16, 16, 15, 16, 15, 16, 15, 15, 16, 16, 16, 15, 15, 16, 16, 15, 16, 15, 16, 15, 16, 16, 16, 15, 16, 15, 16, 16, 15,
    # Przebieg 4
    19, 19, 17, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 17, 15, 15, 15, 15, 16, 16, 15, 15, 16, 15, 16, 19, 16, 17, 14, 17, 15, 16, 16, 16
]

# Dane z Testu 3: Zużycie RAM
ram_usage_data = [
    (0, 0), (1, 148.32), (2, 296.63), (3, 444.95), (4, 593.26), (5, 741.58),
    (6, 889.89), (7, 1038.21), (8, 1186.52), (9, 1334.84), (10, 1483.15)
]

# --- WYKRES 1: ZAKTUALIZOWANA STABILNOŚĆ FPS ---

plt.style.use('seaborn-v0_8-whitegrid')
fig1, ax1 = plt.subplots(figsize=(10, 6))

# Obliczenie statystyk
avg_fps = np.mean(fps_data)
min_fps = np.min(fps_data)
max_fps = np.max(fps_data)
std_dev = np.std(fps_data)

# Wykres liniowy FPS
ax1.plot(fps_data, label=f'Chwilowy FPS (Odch. std: {std_dev:.2f})', marker='.', linestyle='-', markersize=3, alpha=0.7, zorder=3)

# Linie horyzontalne dla statystyk
ax1.axhline(y=avg_fps, color='r', linestyle='--', label=f'Średni FPS: {avg_fps:.2f}')
ax1.axhline(y=min_fps, color='darkorange', linestyle=':', label=f'Min FPS: {min_fps}')
ax1.axhline(y=max_fps, color='green', linestyle=':', label=f'Max FPS: {max_fps}')

# Tytuły i etykiety
ax1.set_title(f'Wykres 1: Stabilność FPS streamingu (N={len(fps_data)} próbek z 3 przebiegów)', fontsize=14)
ax1.set_xlabel('Kolejne próbki danych w czasie', fontsize=12)
ax1.set_ylabel('Klatki na sekundę (FPS)', fontsize=12)
ax1.legend()
ax1.set_ylim(bottom=min(8, min_fps - 2), top=max_fps + 2)

# Zapis do pliku
fig1.tight_layout()
plot1_filename = 'wykres_stabilnosci_fps_aktualizacja.png'
fig1.savefig(plot1_filename)
print(f"Zapisano zaktualizowany wykres: {plot1_filename}")

# --- WYKRES 2: ZUŻYCIE RAM (bez zmian) ---

fig2, ax2 = plt.subplots(figsize=(10, 6))
time_points, ram_points = zip(*ram_usage_data)
ax2.plot(time_points, ram_points, label='Estymowane zużycie RAM', marker='o', color='purple')
ax2.set_title('Wykres 2: Liniowy wzrost zużycia RAM podczas nagrywania (Test T03)', fontsize=14)
ax2.set_xlabel('Czas nagrania (s)', fontsize=12)
ax2.set_ylabel('Zbuforowana pamięć (MB)', fontsize=12)
ax2.legend()
ax2.set_ylim(bottom=0)
ax2.grid(True)
fig2.tight_layout()
plot2_filename = 'wykres_zuzycia_ram.png'
fig2.savefig(plot2_filename)
print(f"Zapisano wykres: {plot2_filename}")