# Find Rpi's ports : ls /dev/tty*

#   sudo apt-get install minicom
#   sudo minicom -b 230400 -o -D /dev/ttyAMA0 or
#   Or '/dev/ttyprintk' '/dev/ttyS0' '/dev/ttyS8'



#
#
#Ce code permet d'utiliser un capteur lidar connecté à un port série pour récupérer les données de distance et d'angle des points détectés. 
#Les données sont ensuite affichées sur un graphique polar en temps réel à l'aide de la bibliothèque matplotlib.

#Le code commence par importer les bibliothèques nécessaires, notamment serial, binascii, matplotlib et math.

#Ensuite, il configure le port série en utilisant les paramètres appropriés pour le capteur lidar, notamment le taux de baud, 
#la taille des octets, la parité, les bits d'arrêt et le délai d'attente.

#Une fois le port série configuré, le code entre dans une boucle while infinie qui lit les données à partir du port série 
#et les analyse pour extraire les données de distance et d'angle. Les données sont stockées dans des listes d'angles et de distances, 
#qui sont ensuite tracées sur le graphique polar en temps réel.

#Le code contient également une fonction de sortie qui permet de quitter la boucle while en appuyant sur la touche "e".

#Enfin, une fois que la boucle while est terminée, le code ferme le port série et s'arrête.
#
#
import serial
import binascii
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='polar')
ax.set_title('lidar (exit: Key E)',fontsize=18)

plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

#Je dois juste trouver le port approprier
ser = serial.Serial("/dev/ttyAMA0",
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)
#I TESTED ALLL PORTS IT S NOT WORKING

tmpString = ""
lines = list()
angles = list()
distances = list()

i = 0
while True:
    loopFlag = True
    flag2c = False

    if(i % 40 == 39):
        if('line' in locals()):
            line.remove()
        line = ax.scatter(angles, distances, c="pink", s=5)
        

        ax.set_theta_offset(math.pi / 2)
        plt.pause(0.01)
        angles.clear()
        distances.clear()
        i = 0
        

    while loopFlag:
        b = ser.read()
        tmpInt = int.from_bytes(b, 'big')
        
        if (tmpInt == 0x54):
            tmpString +=  b.hex()+" "
            flag2c = True
            continue
        
        elif(tmpInt == 0x2c and flag2c):
            tmpString += b.hex()

            if(not len(tmpString[0:-5].replace(' ','')) == 90 ):
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue

            lidarData = CalcLidarData(tmpString[0:-5])
            angles.extend(lidarData.Angle_i)
            distances.extend(lidarData.Distance_i)
                
            tmpString = ""
            loopFlag = False
        else:
            tmpString += b.hex()+" "
        
        flag2c = False
    
    i +=1

ser.close()