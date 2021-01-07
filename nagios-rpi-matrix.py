#######
# V.1.0 - gen 2021
# nagios and sense hat matrix integration
# G Augiero

from sense_hat import SenseHat
import subprocess
import argparse
import re

#Init
ledr=0
ledg=0
leda=0
ledb=0
#HTML File
webfile='/var/www/matrice.html'
#Nagios Server
nagiossvr="user@ip"
#Matrix 8 x 8
maxled = 64
#Leds for rule
riga=8
#LEDs that can be used for alarms, I leave the last line free for other information
disponibili = (maxled - riga)
#Cursor
cursoreriga=0

matrice=['-', '-', '-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-', '-', '-'],['-', '-', '-', '-', '-', '-', '-', '-']

#Colors
rosso=(255, 0, 0)
verde=(0,255,0)
giallo=(255,255,0)
celeste=(0,0,255)
magenta=(128,0,128)
arancione=(128,128,0)
spento=(0, 0, 0)

#Inizializz la matrice luminosa
sense = SenseHat()
sense.clear()
#Half Light
sense.low_light =  True 


def matriceupdate(led,colore):
  global cursoreriga
  global disponibili
  if (disponibili < led):
           led = disponibili
  if (led > 0):
     righeintere,parzialeriga= (divmod(led,riga))
     for j in range(cursoreriga,cursoreriga+righeintere):
         for k in range (0,riga):
              matrice[j][k]= colore 
     for i in range(0,parzialeriga): 
        matrice[cursoreriga+righeintere][i]= colore
     cursoreriga=cursoreriga+righeintere + 1 
     disponibili = ((maxled - riga) - (riga * cursoreriga))

def luce():
    for x in range (0,riga):
       for y in range (0,riga):
           colore=coloreled(matrice[x][y])
           sense.set_pixel(y,x,colore)

def coloreled(x):
    return {
        'R': rosso,
        'V': verde,
        'G': giallo,
        'A': arancione,
        'B': celeste,
        'M': magenta,
        '-': spento
    }[x]


#Matrix
def matrixinit():
    global matrice
    for x in range (0,riga):
        for y in range (0,riga):
            matrice[x][y]='-'

#Print matrix status
def matrixprint():
    for x in range (0,riga):
        print (matrice[x])

def web():
    webheader = '''
<html>
    <body>
'''
    webfooter = '''
    </body>
</html>
'''
    webbody='<H2> Stato Matrice <p><table style="width:100%">'
    for j in range (0,riga):
        webbody= webbody + " <tr>"
        for k in range (0,riga):
            webbody= webbody + '<th> <p style="color:rgb' + str(coloreled(matrice[j][k])) + ';">' + matrice[j][k]+'</p></th>'
        webbody= webbody + " </tr>"
    webbody= webbody + "</table>"
    file = open(webfile,"w")
    file.write(webheader)
    file.write(webbody)
    file.write(webfooter)
    file.close()




def main():


    states = subprocess.check_output("ssh " + nagiossvr + " nagios4stats > nagios.txt ", shell=True)

    #nagios stat
    pattern = re.compile("Crit")

    for line in open("nagios.txt"):
     for match in re.finditer(pattern, line):
            ledr = int (line.split(" ")[21])
            ledg = int (line.split(" ")[17])
            leda = int (line.split(" ") [19])
    
    #Critical
    matriceupdate(ledr,"R")

    #Warning
    if (cursoreriga<7):
       matriceupdate(ledg,"G")

    #Unknown
    if (cursoreriga<7):
       matriceupdate(leda, "A")


    #Host DOWN
    if (cursoreriga<7): 
        pattern = re.compile("Hosts Up")
        for line in open("nagios.txt"):
         for match in re.finditer(pattern, line):
            ledb = int(line.split(" ")[21])
        matriceupdate(ledb, "B")



    #All is OK
    if (ledr==0) and (ledg==0) and (leda==0):
        matriceupdate(8, "V")    


    #View
    if (args.view == True):
        matrixprint()
    luce()
    #Web
    if (args.web == True):
        web()


if __name__ == "__main__":
    #Parameters
    parser = argparse.ArgumentParser(prog='nagios-matrix.py',description="Nagios and Sense Hat integration")
    parser.add_argument('--view', action='store_true',  help='Print matrix on screen ')
    parser.add_argument('--web',  action='store_true', help='Create html file')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    main()

