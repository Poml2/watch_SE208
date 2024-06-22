import numpy as np

'''
Fonction calculant le rythme cardiaque d'après le signal fenêtré sur un certain nombre d'échantillons et la fréquence d'échantillonage Fe
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

''' POUR TESTER LE FONCTIONNEMENT AVEC LES DONNEES DE TEST
import csv
import matplotlib.pyplot as plt
import numpy as np

file = open("   METTRE CHEMIN ADEQUAT ICI    /TP_ADC_RasPico/files/HeartAcq_mod.csv")
csv_reader = csv.reader(file)
rows = []
#Lecture des données dans la liste rows
for row in csv_reader:
    rows.append(row)
file.close()

#On enlève les informations du début du fichier (nom de l'oscillo, etc.)
rows = rows[10:]

#On met les string sous forme de nombre réels
for i in range(len(rows)):
    rows[i] = [float(rows[i][0]), float(rows[i][1])]

#Conversion en array pour des manipulations plus faciles
rows = np.asarray(rows)

N = len(rows)
#Fréquence d'échantillonage (80Hz dans l'exemple du fichier HeartAcq_mod.csv)
Fe = 80
#Calcul du spectre sur window_size échantillons soit window_size/Fe = ... secondes
window_size = 400

spectre = np.abs(np.fft.rfft(rows[:window_size,1]))
#Array des fréquences du spectre
freq = np.fft.rfftfreq(len(rows[:window_size]), d=1/Fe)

#La composante continue (spectre[0])
#ne nous intéresse pas donc elle est retirée
freq = freq[1:]
spectre = spectre[1:]

plt.plot(freq, spectre)
plt.title("Spectre du signal du capteur sans composante continue (calculé ici sur " + str(window_size) + "/" + Fe + " = 5 secondes)")
plt.xlabel("Battements par seconde")
plt.ylabel("Amplitude en unités arbitraires")

#Rythme cardiaque
print(60*freq[np.argmax(spectre)])
plt.show()
'''
