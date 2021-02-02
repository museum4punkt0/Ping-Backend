export const chat = `0 Meine Güte, meine Güte... -> 1
1 Mensch, was sollen wir denn nur machen? 😵 -> 2
2 Ich kann nicht mehr. 😪 -> 3
3 Ständig dieser Zeitdruck, diese Angst. ⏰ -> 4
4 Dieser Job frisst mich auf!!! -> 5 
5 Nun sitz' ich hier und jammere herum... -> 6
6 ... aber seien wir mal ehrlich, vielen geht es doch so wie mir... [7,8,9]
7 Ich kann dich sehr gut verstehen. -> 10 {a2+0}
8 Wie kann ich dir helfen? -> 11 {a2+2}
9 Jeder ist seines eigenen Glückes Schmied. -> 12 {a2-3}
10 Ach, das ist gut zu hören. Wenigstens bin ich nicht alleine. -> 13
11 Naja, das bringt doch alles nichts... Du kannst hier nichts ändern. -> 13
12 Ach danke, den Spruch habe ich auch schon öfter gehört. -> 13
13 Wir schuften hier, machen unbezahlte Überstunden. ⏳ -> 14
14 Das ist echt der Wahnsinn. -> 15
15 Wir machen alles und am Ende reicht es kaum zum Monatsende. 😭 -> 16
16 Und da haben wir noch keine großen Sprünge gemacht – von einem Urlaub ganz zu schweigen. -> 17
17 Mich macht das wütend, aber vor allem auch traurig. -> 18
18 Aber wie geht es dir denn? Bist du denn wenigstens zufrieden mit deiner Arbeit, mit dem Leben? [19,20,21]
19 Ja, ich bin schon zufrieden. -> 22 {a4+3}
20 Ach, es kommt immer darauf an. -> 23 {a4+0}
21 Nein, ich bin ehrlich gesagt auch sehr unzufrieden... -> 24 {a4-3}
22 Wenigstens einer hier. 😅 -> 25
23 Das ist gut gesagt. 🤔 -> 25
24 Wir sitzen alle im selben Boot. 🚣‍♀ -> 25
25 Wir müssen weitermachen. Machs gut, du. Es geht immer so weiter... 👋 [26,27]
26 👋 -> 101
27 🤘 -> 101
101 ||Exit
`