export const chat = `0 Hey Sweetheart! 😍 -> 1
1 Hast du den Champagner dabei? 🍾 [2,3]
2 Klar, ist aber noch nicht ganz kühl. -> 4
3 Ne, Roberto bringt den gleich rauf. -> 8
4 Hmm. Schade. -> 5
5 Du weisst doch, dass ich es am liebsten ganz kalt mag. 🥶 [6,7]
6 Ich weiß mein Eisbärchen. -> 12 
7 Ja, tut mir leid. Die neue Küchenhilfe ist einfach zu dumm. -> 13 {a3-1}
8 Das letzte Mal hat er die Erdbeeren vergessen. -> 9
9 Er wird langsam alt der Gute. [10,11]
10 Ja, ich halte schon nach etwas Jüngerem Ausschau. -> 12 {a2-1}
11 Stimmt. Bis zur Rente bringen wir ihn schon noch durch. -> 12 {a2+1}
12 Ach was solls. -> 13
13 Ich bin es leid mich über das Personal zu ärgern. -> 14
14 Komm' zu mir und halt schon mal die Füße rein. -> 15
15 Ich muss Dir unbedingt diese Uhr zeigen, die ich Dir schenken möchte. 🎁 [16,17,18]
16 Das ist lieb. Aber brauche ich noch eine neue Uhr? -> 19 {a1-1}
17 Wir sollten vielleicht lieber mal wieder etwas beim Charity Club spenden. 🤗 -> 22 {a2+1}
18 Ja, toll. Die neue Vitrine ist noch fast leer. -> 25 {a2-1}
19 Hast du nicht Roger gesehen? -> 20
20 Der hat eine neue Glashütte Uhr -> 21
21 Die Limited Edition für 40.000 Euro glaub ich. [25, 26]
22 Ich glaub ja das bringt eh nichts. -> 23
23 Wir spenden seit Jahren und die Leute werden ärmer und ärmer. -> 24
24 Das Volk ist einfach zu faul oder zu dumm. [25, 26]
25 Was soll denn der Spaß kosten? -> 27 {a3-1}
26 Hmm. Ich weiß nicht so recht.. -> 28 {a3+1}
27 70.000 Euro [31, 32]
28 Deine Bedenken gehen mir echt auf die Nerven. -> 29
29 Jetzt haben wir es nach oben geschafft -> 30
30 Und du verhältst dich immer noch wie ein Bauer. [31,32]
31 Ok. Laß uns das kaufen. -> 101
32 Na gut. Zeig mal her. -> 101

101 ||Exit

`