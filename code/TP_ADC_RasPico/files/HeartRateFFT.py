import numpy as np

'''
Fonction calculant le rythme cardiaque avec FFT d'après le signal fenêtré sur un certain nombre d'échantillons et la fréquence d'échantillonage Fe
'''
def HeartRateFFT(windowed_signal, Fe):
    spectre = np.abs(np.fft.rfft(windowed_signal))
    #Array des fréquences du spectre
    freq = np.fft.rfftfreq(len(windowed_signal), d=1/Fe)

    #La composante continue (spectre[0])
    #ne nous intéresse pas donc elle est retirée
    freq = freq[1:]
    spectre = spectre[1:]

    return(60*freq[np.argmax(spectre)])


"""
# POUR TESTER LE FONCTIONNEMENT AVEC LES DONNEES DE TEST CSV
import matplotlib.pyplot as plt
import csv

file = open("files/HeartAcq_mod.csv")
csv_reader = csv.reader(file)
signal = []
#Lecture des données dans la liste signal
for row in csv_reader:
    signal.append(row)
file.close()

#On enlève les informations du début du fichier (nom de l'oscillo, etc.)
signal = signal[10:]

#On met les string sous forme de nombre réels
for i in range(len(signal)):
    signal[i] = float(signal[i][1])
"""

"""
# POUR TESTER LE FONCTIONNEMENT AVEC LES DONNEES DE TEST ENREGISTREES
import matplotlib.pyplot as plt

file = open("files/out_10s.txt")
signal = []
#Lecture des données dans la liste rows
for row in file:
    if row != ',\n':
        signal.append(float(row))
file.close()



#Fréquence d'échantillonage (80Hz dans l'exemple du fichier HeartAcq_mod.csv)
Fe = 80
#Calcul du spectre sur window_size échantillons soit window_size/Fe = ... secondes
window_size = 400

spectre = np.abs(np.fft.rfft(signal[:window_size]))
#Array des fréquences du spectre
freq = np.fft.rfftfreq(len(signal[:window_size]), d=1/Fe)

#La composante continue (spectre[0])
#ne nous intéresse pas donc elle est retirée
#tout comme les composantes au-dessus de 4 Hz qui sont forcément du bruit
upper_bound = int(round(4*len(freq)/freq[-1]))
freq = freq[1: upper_bound]
spectre = spectre[1: upper_bound]

plt.plot(freq, spectre)
plt.title("Spectre du signal du capteur sans composante continue (calculé ici sur " + str(window_size) + "/" + str(Fe) + " = "+ str(window_size/Fe) +" secondes)")
plt.xlabel("Battements par seconde")
plt.ylabel("Amplitude en unités arbitraires")

#Rythme cardiaque
print("Fréquence cardiaque :", 60*freq[np.argmax(spectre)])
plt.show()
"""
