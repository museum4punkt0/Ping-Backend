export const chat = `0 Jetzt liege ich hier am Boden... 😢 -> 1
1 Abgestürzt, gefallen, erniedrigt. 😖 -> 2
2 Was war das für ein Höhenflug. Mein Traum, ich ganz oben! -> 3
3 Einmal "bei den Göttern". Dafür hat es sich gelohnt. Auch das Fallen. -> 4
4 Sind Sie schon mal geflogen? [5,6]
5 Ja, natürlich - mit dem Flugzeug. -> 8
6 Nein, noch nie... -> 7 {a1+1}
7 Ungewöhnlich. Sie sollten es mal versuchen! -> 12
8 Fliegen Sie viel? [9,10,11]
9 Nein, nur sehr selten. -> 12 {a1+1}
10 1-3 mal im Jahr. -> 12 {a1+0}
11 Mehr als 3 mal im Jahr. -> 12 {a1-1}
12 Fliegen ist doch eine tolle Sache! -> 13
13 Schauen Sie, ich rapple mich schon wieder auf. 🙂 -> 14
14 Nicht, dass Sie einen falschen Eindruck bekommen. 😉 -> 15
15 Es schmerzt doch ziemlich... Doch nur wer alles gibt, die richtige Einstellung hat... -> 16
16 ... -> 17
17 Man kann alles schaffen, wenn man nur fest genug daran glaubt! [18,19,20]
18 Da hast du völlig Recht! -> 22 {a0-1}
19 Ja, und nur die Stärksten setzen sich durch. -> 23 {a0-1}
20 Ich bin anderer Meinung. -> 21 {a0+1}
21 Ach wirklich? Gut, die Diskussion hatte ich schon öfter... darauf lasse ich mich gar nicht ein... ich möchte Ihre und meine Zeit nicht weiter verschwenden... -> 22
22 Lassen Sie uns das Gespräch beenden. -> 25
23 Sie also auch? Die Gewinner-Typen ziehen sich wie magisch an. 🙂 -> 24
24 Aber jetzt will ich es erneut versuchen. -> 25
25 Ich heb' dann mal wieder ab! -> 26
26 * Über den Wolken ... * -> 101

101 ||Exit
`