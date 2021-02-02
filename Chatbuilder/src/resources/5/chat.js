export const chat = `0 HILFE!!! HILFE!!! -> 1
1 So hilf mir doch jemand. -> 2
2 Bemerkt mich denn keiner, hört keiner meinen stillen Schrei? [3]
3 Doch, ich höre dir jetzt zu. -> 4 {a2+0}
4 Oh Gott, endlich. Schau mich an, wie ich hier liege! -> 5
5 Wo bin ich? Siehst du nicht, was mit mir passiert? -> 6
6 Siehst du, wie sie mir die Nägel segen? [7]
7 Ja, ich sehe es. -> 8
8 Siehst du, wie sie mir die Rückenhaare rupfen? [9]
9 Ja, ich sehe es. -> 10
10 Siehst du, wie sich meinen Mund besiedeln? Meine letzten Tränen fangen? [11]
11 Ja, ich sehe es. -> 12
12 Wann hat das begonnen und wann hört es wieder auf? -> 13
13 Kannst du mir nicht helfen? -> 14
14 Und: Kannst du mir sagen, wer ich bin? [15,16,17]
15 Du bist ich und ich bin du. -> 18 {a3+2}
16 Ein Monster, ein Affe, ein Mensch. -> 18
17 Du stehst für unseren Planeten. -> 18
18 Das kann sein, ich selbst habe es schon längst vergessen. -> 19
19 Ich bin gerade vorallem eins - eine Ressource... -> 20
20 Die Frage ist, was machen sie dann - die mich bearbeiten - mit Schorf und Schuppen. -> 21
21 ... -> 22
22 Ich kann dich nicht sehen - bist du einer von ihnen? [23,24,25]
23 Ja, ich bin einer von ihnen. -> 26 {a3-2}
24 Das kann sein, aber ich bin gleichzeitig auch du. -> 26 {a3+0}
25 Nein, ich bin hier nur zu Gast. -> 26
26 Du bist dir gegenüber sehr ehrlich. -> 27
27 Ja, wir alle. -> 28
28 Ich bin müde, ich kann nicht mehr. -> 29
29 Was glaubst du, wie geht es mit mir weiter? [30, 31, 32]
30 Du wirst immer müder und irgendwann schläfst du einfach ein... -> 101 {a0+0}
31 Du bäumst dich auf und entledigst dich der Parasiten! -> 101 {a0+1}
32 Die dich bearbeiten stellen ihre Wirtschaften um. -> 101 {a0+1}

101 ||Exit
`