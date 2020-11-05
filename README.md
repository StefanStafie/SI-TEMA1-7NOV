# SI-TEMA1-7NOV

Pasi pentru testare:
  1. Se deschid, in ordinea urmatoare, procesele: main, clientA, clientB (cel mai bine folosind:  click_dreapta -> Run file in python console)
  2. In consola de la clientA se alege modul de lucru (se scrie 1 sau 2) pentru ECB sau CBC
  3. In consola de la main se pot observa request-urile pentru K1 sau K2
  4. In consola de la clientB se poate observa textul transmis de clientA
 
Altele:
  In CryptoService se pot folosi 
    - test_ecb()
    - test_cbc()
  pentru testarea criptarilor (separat de comunicare prin network)
  
Programul, ca intreg, functioneaza, dar se pot intalni comportamente nedeterministe in functie de procesorul pe care este rulat si multe alte lucruri. 
Am atasat si un demo ca sa demonstrez ca merge.
