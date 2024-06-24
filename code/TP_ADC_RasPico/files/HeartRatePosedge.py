import numpy as np

'''
Fonction calculant le rythme cardiaque avec détection de fronts montants d'après le signal fenêtré sur un certain nombre d'échantillons et la fréquence d'échantillonage Fe
'''
def HeartRatePosedge(signal, Fe):
    #Calcul de la moyenne du signal sur cette fenêtre
    average = np.average(signal)

    '''
    En étudiant plusieurs électrocardiogrammes, nous avons remarqué que le signal d'une onde R
    allait de son minimum à son maximum en au plus 0,1 secondes.
    Donc pour détecter un front montant, on compare la valeur de signal[i] à la moyenne,
    et celle de signal[i + delta] à la moyenne, où:
    i correspond à un échantillon donné
    delta correspond au nombre d'échantillons pendant 0,1 secondes: delta = 0,1*Fe
    '''
    delta = int(np.round(0.1*Fe))
    peak_indices = delta*[0] #Cette liste va servir à stocker les indices des fronts montants
    peak_flag = 0 #Flag servant à éviter les erreurs de comptage
    for k in range(delta, len(signal)):
        if (signal[k-delta] < average) and (signal[k] > average) and (peak_flag == 0):
            peak_indices.append(1)
            peak_flag = delta #Pendant delta échantillons, on ne cherche plus de fronts montants
        else:
            if (peak_flag > 0):
                peak_flag -= 1
            peak_indices.append(0)

    peak_counter = np.sum(peak_indices) #Compteur de fronts montants
    #Rythme cardiaque
    return(60*peak_counter*Fe/len(signal))

# POUR TESTER LE FONCTIONNEMENT AVEC LES DONNEES DE TEST
import csv
import matplotlib.pyplot as plt
import numpy as np

file = open("HeartAcq_mod.csv")
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


x = rows[:,1] #Signal du capteur

# Filtrage par moyenne glissante
filter_signal = [0] * len(x)
window_size = 20

# Calcul de la moyenne glissante
for i in range(1, len(x) - window_size + 1):
    filter_signal[i] = sum(x[i:i + window_size]) / window_size

# Tracer le signal filtré
plt.plot(x, label='Original Signal')
plt.plot(filter_signal, label='Filtered Signal')
plt.legend()
plt.show()

# Fréquence d'échantillonnage
Fe = 80

# Signal après filtrage (en retirant les premiers échantillons incomplets)
signal = filter_signal[window_size - 1:]

# Calcul de la moyenne du signal filtré
average = sum(signal) / len(signal)
print("Average:", average)

# Détection des fronts montants
delta = int(round(0.1 * Fe))  # delta correspond à 0,1 secondes d'échantillons
peak_indices = []
peak_flag = 0

for k in range(delta, len(signal)):
    if signal[k - delta] < average < signal[k] and peak_flag == 0:
        peak_indices.append(k)
        peak_flag = delta  # Empêche la détection de multiples pics dans un court intervalle
    else:
        if peak_flag > 0:
            peak_flag -= 1

# Compter le nombre de pics détectés
peak_counter = len(peak_indices)
print("Number of Peaks:", peak_counter)

# Calcul du rythme cardiaque (BPM)
bpm = 60 * peak_counter * Fe / len(signal)
print("BPM:", bpm)

plt.plot(signal) #Signal
plt.plot(len(signal)*[average]) #Moyenne du signal
plt.plot(peak_indices) #Fronts montants
plt.title("Signal du capteur, sa moyenne et ses fronts montants, fenêtré sur " + str(window_size) +"/"+ str(Fe) +" = "+ str(window_size/Fe) + " secondes")
plt.xlabel("Échantillon")
plt.ylabel("Amplitude en unités arbitraires")
plt.legend(["Signal", "Moyenne", "Fronts montants"])
plt.show()
