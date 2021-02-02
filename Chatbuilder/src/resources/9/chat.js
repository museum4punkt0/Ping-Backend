export const chat = `0 Wow! -> 1
1 Das ist unfassbar!!! -> 2
2 Ich bin hier gerade bei der Eröffnung des neuen Media Markts!!! 🤩🤩🤩 -> 3
3 Die Leute rennen die Bude ein - sind total im Kaufrausch!!! 🤑🤑🤑 -> 4
4 Es gibt ein paar richtig geile Schnäppchen! 💗💗💗 [5,6,7]
5 Cool, ich wäre gern mitgekommen. -> 8 {a1-1}
6 Für mich wäre das nichts, ich shoppe lieber online... -> 9 {a1-1}
7 Ich shoppe generell nicht soooo gern 😃 -> 9 {a1+1}
8 Hahaha, ok, next time! 😒 -> 10
9 Hahaha, ok 😒 -> 10
10 ….Ein bisschen macht es aber auch Angst. Ich bin hier mittendrin. Diese Menschenmassen... -> 11
11 Egal. Soll ich dir was mitbringen? Alles super günstig!!! 😛😛😛 [12,13,14]
12 Ja, sehr gerne einfach irgendwas!!! -> 15 {a1-1}
13 Ja, einen neuen Flachbildschirm 😏  -> 15 {a1-1}
14 Hmm... eigentlich brauche ich nichts... -> 15 {a1+1}
15 Haha, ich glaube ich kaufe für alle, die ich lieb habe, erstmal diese günstigen USB-Sticks hier … Alles kostet weniger als 1 Euro. Unfassbar geil hier. Unfassbar günstig. Für dich auch? 🤗 [16,17,18]
16 Ja, mega gern! -> 19 {a1-1}
17 Wenn es fast nichts kostet! -> 19 {a1-1}
18 Das brauche ich alles eigentlich nicht. -> 19 {a1+1}
19 Ok, so oder so - hab jetzt gegriffen, was ich konnte. -> 20
20 Ich kämpfe mich mal weiter durch die Massen hier.  -> 21
21 Boah, das musst du gesehen haben. Die Menschen rasten alle aus. 🤪🤪🤪 -> 22
22 Morgen ist hier auch noch alles heruntergesetzt... [23,24,25]
23 Super, mega gut zu wissen... 🙄 -> 26 {a1-1}
24 Ok, online ist es trotzdem bestimmt noch billiger 🤔 -> 26 {a1-1}
25 Gut, ich kaufe lieber gebraucht. 🤓 -> 26 {a1-0}
26 Ok, ich kämpfe mich hier jetzt weiter!!! -> 101

101 ||Exit
`