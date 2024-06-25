'''
Fonction calculant le rythme cardiaque avec détection de fronts montants d'après le signal fenêtré sur un certain nombre d'échantillons et la fréquence d'échantillonage Fe
'''
def HeartRatePosedge(signal, Fe):
    # Filtrage par moyenne glissante
    smoothening_window_size = 10
    filtered_signal = signal[:smoothening_window_size] #Les premiers termes sont remplacés par le signal car on ne peut pas encore faire de moyenne glissante

    # Calcul de la moyenne glissante
    for i in range(smoothening_window_size, len(signal)):
        filtered_signal.append(sum(signal[i - smoothening_window_size:i]) / smoothening_window_size)

    # Calcul de la moyenne du signal filtré
    average = sum(filtered_signal) / len(filtered_signal)

    '''
    En étudiant plusieurs électrocardiogrammes, nous avons remarqué que le signal d'une onde R
    allait de son minimum à son maximum en au plus 0,1 secondes.
    Donc pour détecter un front montant, on compare la valeur de signal[i] à la moyenne,
    et celle de signal[i + delta] à la moyenne, où:
    i correspond à un échantillon donné
    delta correspond au nombre d'échantillons pendant 0,1 secondes: delta = 0,1*Fe
    '''
    delta = int(round(0.1*Fe))
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

    peak_counter = sum(peak_indices) #Compteur de fronts montants
    #Rythme cardiaque
    return(60*peak_counter*Fe/len(signal))


"""
# POUR TESTER LE FONCTIONNEMENT AVEC LES DONNEES DE TEST CSV
import matplotlib.pyplot as plt
import csv

file = open("files/HeartAcq_mod.csv")
csv_reader = csv.reader(file)
signal = []
#Lecture des données dans la liste rows
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



# Filtrage par moyenne glissante
smoothening_window_size = 10
filtered_signal = signal[:smoothening_window_size] #Les premiers termes sont remplacés par le signal car on ne peut pas encore faire de moyenne glissante

# Calcul de la moyenne glissante
for i in range(smoothening_window_size, len(signal)):
    filtered_signal.append(sum(signal[i - smoothening_window_size:i]) / smoothening_window_size)

# Calcul de la moyenne du signal filtré
average = sum(filtered_signal) / len(filtered_signal)
print("Moyenne : ", average)

# Fréquence d'échantillonnage
Fe = 80

'''
En étudiant plusieurs électrocardiogrammes, nous avons remarqué que le signal d'une onde R
allait de son minimum à son maximum en au plus 0,1 secondes.
Donc pour détecter un front montant, on compare la valeur de signal[i] à la moyenne,
et celle de signal[i + delta] à la moyenne, où:
i correspond à un échantillon donné
delta correspond au nombre d'échantillons pendant 0,1 secondes: delta = 0,1*Fe
'''
delta = int(round(0.1 * Fe))  # delta correspond à 0,1 secondes d'échantillons
peak_indices = delta*[0] #Cette liste va servir à stocker les indices des fronts montants
peak_flag = 0 #Flag servant à éviter les erreurs de comptage

for k in range(delta, len(filtered_signal)):
    if filtered_signal[k - delta] < average < filtered_signal[k] and peak_flag == 0:
        peak_indices.append(1)
        peak_flag = delta  #Pendant delta échantillons, on ne cherche plus de fronts montants
    else:
        if peak_flag > 0:
            peak_flag -= 1
        peak_indices.append(0)

# Compter le nombre de pics détectés
peak_counter = sum(peak_indices) #Compteur de fronts montants
print("Nombre de fronts montants :", peak_counter)

# Calcul de la fréquence cardiaque
bpm = 60 * peak_counter * Fe / len(filtered_signal)
print("Fréquence cardiaque (BPM) :", bpm)

# Tracer le signal filtré
plt.plot(signal, label="Signal original")
plt.plot(filtered_signal, label="Signal filtré")
plt.plot([average]*len(signal), label = "Moyenne")
plt.plot(peak_indices, label = "Fronts montants")
plt.xlabel("Échantillon")
plt.ylabel("Amplitude en unités arbitraires")
plt.title("Détection de fronts montants sur " + str(len(filtered_signal)) + "/" + str(Fe) + " = " + str(len(filtered_signal)/Fe) + " secondes")
plt.legend()
plt.show()
"""
