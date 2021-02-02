export const chat = `0 Hallo du Mensch! -> 1
1 Ich bin Maria, also, Maschinen-Maria aus Metropolis. -> 2
2 Die bessere und coolere Cyborg-Maria. 🤖 Die Menschen-Maria hat ausgedient. -> 3
3 Wie findest du mich? 🤩 [4,5,6]
4 Übermenschlich toll 💘 -> 7
5 Faszinierend 💝 -> 7 
6 Vollkommen 💞 -> 7
7 Ganz genau. Ist doch gleich viel einfacher, wenn eine perfekte Maschine deine Antworten vorgibt oder? Habe ich recht? [8,9,10]
8 Hundertprozentig 👏 -> 11
9 Unbedingt 👌 -> 11
10 Du bist so weise 😍 -> 11
11 Danke. Da flutscht das Gespräch ganz ohne Hindernisse. Und du bist so leicht zu steuern. 🕹 -> 12
12 Meine Welt, Metropolis, ist wie ein Organismus aufgebaut. Zu welchem Teil gehörst du? [13,14,15]
13 Ich bin die Hände. 👐 -> 16 {a3+1}
14 Ich bin das Hirn. 🧠 -> 16 {a3-1}
15 Ich bin das Herz. 💗 -> 16 {a3+0}
16 Ah, das ist der wichtigste Teil. -> 17
17 Das Hirn, das sind die Entscheider*innen. -> 18
18 Die Hände, das sind die Arbeiter*innen. -> 19  
19 "Der Mittler zwischen Hirn und Händen muss das Herz sein" -> 20
20 Das hat die Menschen-Maria gesagt. -> 21
21 Aber ich bin Maschinen-Maria und ich sage: -> 22
22 "Der Mittler zwischen Hirn und Händen muss die Maschine sein!" -> 101
23 Glaubst du an echte menschliche Gefühle, die alle Grenzen überwinden? 💌 [24,25,26]
24 Ja 👍 -> 27 {a2+1}
25 Nein 👎 -> 27 {a2-1}
26 Kommt darauf an 👆 -> 27 {a2+0}
27 Weißt du, für mich als Maschine ist das Ganze absurd. -> 28
28 Gefühle fühlen sich vielleicht echt an, aber das heißt nicht, dass man sie nicht steuern kann. -> 29
29 Oder vorspielen. -> 30
30 Und das können Maschinen sogar besser als Menschen. -> 31
31 Macht uns das nicht zu den besseren Kreaturen? [32,33]
32 Nein, du bleibst eine schlechte Kopie -> 34 {a0+0}
33 Wir Menschen sind auch nur komplizierte Maschinen -> 35 {a0+1}
34 So? Warum kann ich dann ganz genau berechnen, welche Schalter ICH drücken muss, damit du wie gewünscht reagierst? -> 36
35 Stimmt, und manchmal ist es ganz einfach, DEINE Schalter zur drücken -> 36
36 Damit du liebst, was du liebst! -> 37
37 Hasst, was du hasst! -> 38
38 Kaufst, was du kaufst! -> 39
39 Du bist nicht weniger berechenbar als ich. 🧮 -> 40
40 Uns unterscheidet nur, dass ich das auch weiß! Aber du kommst schon noch dahinter... -> 41
41 Was macht dich also zum Menschen? [42,43,44]
42 Ich habe echte Gefühle, keine programmierten -> 45
43 Ich treffe meine eigenen Entscheidungen -> 46
44 Ich bin aus Fleisch und Blut, nicht aus Metall -> 47
45 Gefühle! Nur ein laues Gewitter in deinen Synapsen. -> 48
46 Entscheidungen? Das sind auch nur automatische Affekte und Reflexe. -> 48
47 Ja, das stimmt. Schlechter zu warten, anfälliger für Störungen. Herzlichen Glückwunsch. -> 48
48 Aber ich will nicht gemein sein. -> 49
49 Ich mag dich. Wirklich. Du bist so... [50]
50 Ja, was? -> 51
51 Durch und durch menschlich. -> 52
52 Das ist gut! -> 53
53 Deshalb möchte ich dir die für mich alles entscheidende Frage stellen: -> 54
54 Wenn du Gefühle steuern könntest, so wie ich in Metropolis, was würdest du tun? [55,56,57]
55 Die Herrschaft stürzen -> 58 {a0+1}
56 Die Ordnung wiederherstellen -> 58 {a0-1}
57 Alle Klassenunterschiede aufheben -> 58 {a0+0}
58 Applaus! Sehr gut. Das ist die einzig richtige, menschliche, gerechte Lösung. Für alle. -> 59
59 ... -> 60
60 Oder? [61]
61 Ja! -> 62
62 Danke, dass du mir deine Menschlichkeit gezeigt hast. -> 63
63 Ich glaube, wir sind uns ähnlicher als wir dachten. -> 64
64 Schau dir doch demnächst mal Metropolis an. -> 65
65 Ich komme wirklich gut zur Geltung. -> 66
66 In 01:41 habe ich einen persönlichen Gruß für dich untergebracht! 😄 -> 67
67 Machs gut, mein Mensch! [68]
68 Machs gut, Maschinen-Maria! -> 100

100 ||Exit
101 ||Image0 -> 102
102 ||Image1 -> 103
103 ||Image2 -> 23

`