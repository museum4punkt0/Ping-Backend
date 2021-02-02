export const chat = `0 Oh! -> 1 
1 Welche Überraschung! -> 2
2 Einen wunderschönen exquisiten guten Tag wünsche ich. 😌 -> 3
3 Sie sehen aber entzückend aus! -> 4
4 Haben Sie sich für den Kapitalismus extra zurecht gemacht? 🤭 [5,6,7]
5 Ich sehe immer so aus -> 8 {a0+1}
6 Äh, nein? -> 8 {a1+0}
7 Ja, heute habe ich mich hübsch herausgeputzt -> 8 {a1-1}
8 Das macht mir gleich Lust, mit Ihnen zu plaudern! 🤩 -> 9
9 Lassen Sie mal hören. Wie finden Sie mein Antlitz? 🙂 [10,11]
10 Stilvoll -> 12 {a1-1}
11 Protzig -> 13 {a1+1}
12 Das will ich doch meinen. -> 14
13 Was? Sie Crétin! Sie gehören wohl nicht hierher! Ich sollte die Konversation abbrechen! Na, vielleicht liegt's am Maler... -> 14
14 Zu meiner Zeit ist das mit den Porträts noch etwas schwierig. 🖼 -> 15
15 Hat ganz schön lange gedauert. -> 16
16 So zu wirken, als würde ich zufällig und entspannt hier sitzen -> 17
17 Mir tut noch der Nacken weh. -> 18
18 Das geht ja heute schneller mit den Porträts, habe ich gehört. -> 19
19 Haben Sie schon mal ein Selfie gemacht? 🤳 [20,21,22]
20 Sicher! Mein Instagram-Feed ist voll davon. -> 23 {a2-1}
21 Nein, sowas liegt mir nicht -> 24 {a2+0}
22 Selten mal, um anderen eine Freude zu machen -> 25 {a2+1}
23 Dann sind Sie wohl sehr berühmt. Gratulation! Gratulation! 🤗 -> 26
24 Ach, dann kennt Sie wohl auch niemand. Wie bedauerlich... 😒 -> 26
25 Wie edel, welche Freude! Lieber Geben als Nehmen... -> 26
26 Nun, wissen Sie, Stil ist für mich alles. 😌 -> 27
27 Wenn ich und mein exquisiter Geschmack gesehen werden, kann die Welt ein besserer Ort werden. -> 28
28 Denn Ästhetik ist doch schlussendlich der höchste kulturelle Wert. Oder? [29,30,31]
29 Ohne Ästhetik keine Kultur -> 32 {a2-1}
30 Es gibt Wichtigeres -> 33 {a2+0}
31 Schönheit ist vergänglich -> 34 {a2+1}
32 In der Tat! Ich zeige meine grazile Erscheinung für die Kultur! -> 35
33 Wie wahr! Ich sollte mich vor anderer Kulisse portraitieren lassen! -> 35
34 Sie haben Recht! Umso wichtiger ist, dass Bilder von meiner Perfektion bleiben! -> 35
35 Sind Sie wohlhabend? [36,37,38]
36 Ich lebe gut -> 39 {a4-1}
37 Es ist häufig knapp -> 39 {a4+1}
38 Was ist denn das für eine Frage? -> 39 {a4+0}
39 Stil und Geld, wissen Sie, die beiden haben schon eine intime Beziehung 🤓 -> 40
40 Stil muss man sich leisten können, sonst wird er zur Farce, zum Kitsch, zur Plumpheit -> 41
41 Die Leichtigkeit auf meinem Porträt, die Eleganz, wissen Sie, die entsteht erst auf Basis des Besitzes -> 42
42 Geld ist ja so profan -> 43
43 Aber auch so beruhigend -> 44
44 Und welche Schönheiten es entwickelt! -> 45
45 Zum Beispiel mich... -> 46
46 Was meinen Sie, wollen Sie nicht ein Selfie mit mir machen? -> 47
47 Dann kommen wir beide gut zur Geltung [48,49]
48 Ja gerne -> 50
49 Nein danke -> 51
50 Wunderbar, Stil muss gesehen werden. Bitte recht freundlich! 😌 -> 52
51 Ich verstehe. Kein Freund der Selbstdarstellung. Ob sich dieser Stil je durchsetzt? -> 52
52 Es war schön mit dir! Ich verweile noch ein wenig... [53]
53 Adé -> 100

100 ||Exit
`