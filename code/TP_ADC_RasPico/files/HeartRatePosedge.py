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

#Fréquence d'échantillonage (80Hz dans l'exemple du fichier HeartAcq_mod.csv)
Fe = 80
#Calcul de la fréquence cardiaque sur window_size échantillons soit window_size/Fe = ... secondes
window_size = 400
signal = rows[:window_size, 1]

# Calcul de la moyenne du signal sur cette fenêtre
average = sum(signal) / len(signal)

'''
En étudiant plusieurs électrocardiogrammes, nous avons remarqué que le signal d'une onde R
allait de son minimum à son maximum en au plus 0,1 secondes.
Donc pour détecter un front montant, on compare la valeur de signal[i] à la moyenne,
et celle de signal[i + delta] à la moyenne, où:
i correspond à un échantillon donné
delta correspond au nombre d'échantillons pendant 0,1 secondes: delta = 0,1*Fe
'''
delta = int(round(0.25 * Fe))
peak_indices = [0] * delta  # Cette liste va servir à stocker les indices des fronts montants
peak_flag = 0  # Flag servant à éviter les erreurs de comptage

for k in range(delta, len(signal)):
    if (signal[k - delta] < average) and (signal[k] > average) and (peak_flag == 0):
        peak_indices.append(1)
        peak_flag = delta  # Pendant delta échantillons, on ne cherche plus de fronts montants
    else:
        if peak_flag > 0:
            peak_flag -= 1
        peak_indices.append(0)

peak_counter = sum(peak_indices)  # Compteur de fronts montants
# Rythme cardiaque
print(60 * peak_counter * Fe / len(signal))

plt.plot(signal) #Signal
plt.plot(len(signal)*[average]) #Moyenne du signal
plt.plot(peak_indices) #Fronts montants
plt.title("Signal du capteur, sa moyenne et ses fronts montants, fenêtré sur " + str(window_size) +"/"+ str(Fe) +" = "+ str(window_size/Fe) + " secondes")
plt.xlabel("Échantillon")
plt.ylabel("Amplitude en unités arbitraires")
plt.legend(["Signal", "Moyenne", "Fronts montants"])
plt.show()
