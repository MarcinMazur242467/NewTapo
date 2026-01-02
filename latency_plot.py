import matplotlib.pyplot as plt
import numpy as np

# Dane
measurements = np.arange(1, 12)
latency = [780, 720, 730, 740, 710, 810, 700, 610, 790, 750, 750]
avg_latency = np.mean(latency)

# Tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.plot(measurements, latency, marker='o', linestyle='-', label='Opóźnienie chwilowe')

# Dodanie linii średniej (trendu)
plt.axhline(y=avg_latency, color='r', linestyle='--', label=f'Średnia: {avg_latency:.1f} ms')

# Ustawienia osi i tytułów
plt.title('Opóźnienie transmisji obrazu z kamery')
plt.xlabel('Numer pomiaru')
plt.ylabel('Opóźnienie (ms)')
plt.xticks(measurements)
plt.ylim(400, 1000) # Skala do 1000 ms
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

# Zapisanie wykresu
plt.savefig('latency_plot_updated.png')
plt.show()

print(f"Wykres wygenerowany. Średnie opóźnienie wynosi: {avg_latency:.1f} ms")