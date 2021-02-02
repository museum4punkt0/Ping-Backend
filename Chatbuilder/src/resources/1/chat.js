export const chat = `0 Lass mal sehen... -> 1
1 Kostenstelle fünf hat also 300,- Ausgaben. Davon sind Transport 100,- -> 2
2 120,- für den Einkauf -> 3
3 70,- die Fabrik -> 4
4 Das macht in Summe? [5,6,7]
5 290,- -> 8
6 1000,- -> 131
7 Ähh, was bitte?! -> 131
8 Korrekt!! -> 130
9 Du bist ja aufgeweckt! 🤗 [11,12]
10 Rechnen - nicht raten! 😡 [11,12]
11 Was machst du denn da? -> 13
12 Worum geht es eigentlich? -> 13
13 Ich führe Buch. -> 14
14 Ich kontrolliere Einnahmen und Ausgaben -> 15
15 Um sicherzustellen, -> 16
16 dass das Unternehmen profitabel bleibt. 💸 [17,18]
17 Eine Frau als Buchhalterin? -> 20
18 Macht das denn Spaß? -> 19
19 Ja! Der Job ist der Hammer! -> 132
20 Klar. Oder meinst du Rechnen hat was mit dem Geschlecht zu tun? [21,22]
21 Ne, natürlich nicht. -> 23
22 Ich dachte nur - in der Zeit… -> 23
23 Frauenpower ist zeitlos -> 133
24 Ich hab die Sachen halt gerne unter Kontrolle, schön vorausblickend, effizient, das habe ich am liebsten… -> 25
25 Und du.. -> 26
26 Bist du auch eher so der rationale oder eher der Bauch-Entscheidungs-Typ? [27,28]
27 Klar der rationale... -> 134 {a1+1}
28 Ich entscheide eigentlich meistens aus dem Bauch heraus -> 33 {a1-1}
29 Das finde ich ganz bezaubernd! -> 30
30 Ein Lob auf die Ratio. 🤩 -> 31
31 Sie ist das Einzige, was unsere Welt zusammenhält. -> 32
32 Und die Wirtschaft. -> 36
33 Aha, aus dem Bauch also. 🤨 -> 34
34 Das macht mir direkt Bauchschmerzen. 🤢 -> 35
35 Aber gut, auch den Bauch kann man heutzutage ja berechnen -> 36
36 Alles, was man zählen kann, ist echt! -> 37
37 Ich habe gehört, mittlerweile lässt sich fast alles erfassen -> 38
38 Schritte, Schlafminuten, Kalorien ... -> 39
39 Wenn es das schon zu meiner Zeit gegeben hätte - ein Traum -> 40
40 Wie viele Schritte bist du denn heute schon gelaufen? Bist du im Soll? [41,42,43]
41 Die 10.000er-Marke habe ich schon fast geknackt -> 44 {a3+1}
42 Ich tracke mich nicht - neoliberale Selbstoptimierung! -> 44 {a0-1}
43 Bislang habe ich noch keine App, aber mit ihr wäre ich sicherlich fitter. -> 44 
44 Ach, wie interessant. -> 45
45 Ich glaube wir ergänzen uns ideal! 😁 -> 46
46 Ich handele mit Marzipan und liebe Süßes. Auch Genuss kann man zählen. -> 47
47 Lass uns doch später auf einen Kaffee treffen? Oder anderthalb? [48,49]
48 Ja, gerne. -> 51
49 Sorry, bin schon verabredet. -> 50
50 Ok. Kein Problem. Viel Spaß noch in Bonn! -> 136
51 Super. Ich freu mich! -> 136
 
130 ||Image0 -> 9
131 ||Image1 -> 10
132 ||Image2 -> 24
133 ||Image3 -> 24
134 ||Image4 -> 29
135 ||Image5 -> 34
136 ||Image6 -> 150
150 ||Exit`