extensions [csv]

;; pv is used for improved biological algorithm
turtles-own [state pv] ;; one of "active", "inactive", "elected{-conflict}" and "mis"
                       ;; colors: sky,     yellow,    lime,                     red


globals [
  max-degree
  num-broadcasts-sent
  num-messages-sent
  num-bits-sent
  execution-finished

  ;; For biological algorithm
  i
  j
  biology-tick-finished
]

;;;;;;;;;;;;;;;;;;;;;
;; SETUP AND RESET ;;
;;;;;;;;;;;;;;;;;;;;;
to setup
  clear-all
  reset-ticks

  ;; Setup global variables for biological algorithm
  set i 0
  set j 0

  ;; Create vertices
  create-turtles num-vertices [
    set shape "circle"
    setxy (random-xcor * 0.95) (random-ycor * 0.95)
    set color sky
    set state "active"
    set pv 0.5 ;; for improved biological algorithm
  ]

  ;; Create edges
  ask links [ die ]
  while [ count links < num-edges * num-vertices ] [
    ask one-of turtles [
      create-link-with one-of other turtles
    ]
  ]

  ;; Calculate max degree
  set max-degree max [count link-neighbors ] of turtles ;;
end

to reset-graph
  reset-ticks
  set i 0
  set j 0
  set execution-finished 0
  set biology-tick-finished 0
  set num-messages-sent 0
  set num-bits-sent 0
  set num-broadcasts-sent 0

  ask turtles [
    set color sky
    set state "active"
    set pv 0.5
  ]

end

;;;;;;;;;;;;;;;;;;
;; TEST-RUNNING ;;
;;;;;;;;;;;;;;;;;;
to export-data [file-name graphid repeatid]
  file-open file-name

  ifelse file-name = "biology.csv" [
    file-print ( word graphid "," repeatid "," num-vertices "," num-edges "," ticks "," num-messages-sent "," num-bits-sent "," num-broadcasts-sent "," M "," biology-tick-finished)
  ] [
    file-print ( word graphid "," repeatid "," num-vertices "," num-edges "," ticks "," num-messages-sent "," num-bits-sent "," num-broadcasts-sent )
  ]

  file-close
end

to run-and-output-experiments
  foreach ["basic-random.csv" "luby.csv" "biology-imp.csv" "biology.csv"] [file-name ->
    file-open file-name

    ifelse file-name = "biology.csv" [
    file-print ( "graphid,repeatid,vertices, edges, ticks, num-messages-sent,num-bits-sent,num-broadcasts-sent,M,tick-finished" )
  ] [
    file-print ( "graphid,repeatid,vertices, edges, ticks, num-messages-sent,num-bits-sent,num-broadcasts-sent" )
  ]

  file-close
  ]


  let graphid 0
  foreach [100 1000 10000] [ vertices_loop ->
    set num-vertices vertices_loop
    foreach [3 7 15] [ edges_loop ->
      set num-edges edges_loop
      repeat num-graphs [
        setup

        let repeatid 0
        repeat num-graph-repeats [
          while [execution-finished = 0] [basic-random]
          export-data "basic-random.csv" graphid repeatid
          reset-graph
          set repeatid repeatid + 1
        ]

        set repeatid 0
        repeat num-graph-repeats [
          while [execution-finished = 0] [luby]
          export-data "luby.csv" graphid repeatid
          reset-graph
          set repeatid repeatid + 1
        ]

        set repeatid 0
        repeat num-graph-repeats [
          while [execution-finished = 0] [biology-imp]
          export-data "biology-imp.csv" graphid repeatid
          reset-graph
          set repeatid repeatid + 1
        ]

        foreach [3 4 5 6 7 15 34]  [ M-test ->;; test different values for M variable
          set M M-test
          set repeatid 0
          repeat num-graph-repeats [
            while [execution-finished = 0] [biology]
            export-data "biology.csv" graphid repeatid
            reset-graph
            set repeatid repeatid + 1
          ]
        ]
        set graphid graphid + 1
      ]
    ]
  ]
end

;;;;;;;;;;;;;;;;;;;;;;
;; REPORTS AND MORE ;;
;;;;;;;;;;;;;;;;;;;;;;
to edges-update-viewmode
  if edges-viewmode = "all" [
    ask links [set hidden? false]
  ]

  if edges-viewmode = "none" [
    ask links [set hidden? true]
  ]

  if edges-viewmode = "all-mis" [
    ask links [set hidden? true]
    ask links with [[state] of end1  = "mis" OR [state] of end2 = "mis"] [ set hidden? false ]
  ]

  if edges-viewmode = "between-mis" [
    ask links [set hidden? true]
    ask links with [[state] of end1  = "mis" AND [state] of end2 = "mis"] [ set hidden? false ]
  ]
end

to-report max-degree-active-set
  let tmp max [count link-neighbors with [ state != "inactive" ] ] of turtles with [ state != "mis" AND state != "inactive"] ;; max degree of active subgraph
  report max list 1 tmp
end

;;;;;;;;;;;;;;;;;;
;; BASIC RANDOM ;;
;;;;;;;;;;;;;;;;;;
to basic-random
  if not any? turtles with [state = "active" or state = "elected"] [ set execution-finished 1 stop ]

  let step ticks mod 3


  (ifelse step = 0 [ basic-random-step1 ]
  step = 1 [ basic-random-step2 ]
  step = 2 [ basic-random-step3 ])

  tick
end

to basic-random-step1
  ask turtles with [state = "active"] [
    ;;if random-float 1.0 < (1 / max-degree-active-set) [ ;; Extra (not going by theory)
    if random-float 1.0 < (1 / max-degree) [
      set color lime
      set state "elected"

      ;; send one 1-bit message to each neighbor that you are elected
      set num-messages-sent num-messages-sent + count link-neighbors
      set num-bits-sent num-bits-sent + count link-neighbors
      set num-broadcasts-sent num-broadcasts-sent + 1
    ]
  ]
end

to basic-random-step2
  ask turtles with [state = "elected"] [
    if any? link-neighbors with [state = "elected" OR state = "elected-conflict"] [
      ;; change state of myself
      set state "elected-conflict"
      ]
    ]

  ask turtles with [ state = "elected-conflict" ] [
    set color sky
    set state "active"
  ]
end

to basic-random-step3
  ask turtles with [ state = "elected" ] [
    set color red
    set state "mis"

    ;; send one 1-bit message to each neighbor that you've entered mis
    ;; (and they should go inactive)
    set num-messages-sent num-messages-sent + count link-neighbors
    set num-bits-sent num-bits-sent + count link-neighbors
    set num-broadcasts-sent num-broadcasts-sent + 1

    ask link-neighbors with [ state = "active"] [
      set color yellow
      set state "inactive"
    ]
  ]
end

;;;;;;;;;;
;; LUBY ;;
;;;;;;;;;;
to luby
  if not any? turtles with [state = "active" or state = "elected"] [ set execution-finished 1 stop ]

  let step ticks mod 3


  (ifelse step = 0 [ luby-step1 ]
  step = 1 [ luby-step2 ]
  step = 2 [ luby-step3 ])
  tick
end

to luby-step1
  ask turtles with [state = "active"] [
    if random-float 1.0 < (1 / (max list 1 (2 * count link-neighbors))) [
      set color lime
      set state "elected"

      ;; send one 1-bit message to each neighbor that you are elected
      ;; (neighbors that werent elected go inactive by default)
      set num-messages-sent num-messages-sent + count link-neighbors
      set num-bits-sent num-bits-sent + count link-neighbors
      set num-broadcasts-sent num-broadcasts-sent + 1
    ]
  ]
end

to luby-step2
  ask turtles with [state = "elected"] [
    let elected-neighbors link-neighbors with [state = "elected"]

    ;; send one message to each elected neighbor thats log(max_degree) bits
    ;; and contains your degree
    let degree-msg-bits ceiling log max-degree 2
    set num-messages-sent num-messages-sent + count elected-neighbors
    set num-bits-sent num-bits-sent + (count elected-neighbors * degree-msg-bits)
    set num-broadcasts-sent num-broadcasts-sent + 1

    if any? elected-neighbors [ ;; more than one adjacent elected vertices

      let my-degree count link-neighbors with [state = "elected"]
      let max-other-deg max [count link-neighbors with [state != "inactive"]] of link-neighbors with [state = "elected"]

      if my-degree > max-other-deg [ stop ] ;; stay elected

      if my-degree < max-other-deg [
        ;; switch to active
        set color sky
        set state "active"
        stop
      ]

      ;; else multiple with same degree, find biggest id
      ;; send one message to each elected neighbor thats log(count of turtles) bits
      ;; and contains your turtle who number
      let who-msg-bits ceiling log (count turtles) 2
      set num-messages-sent num-messages-sent + count elected-neighbors
      set num-bits-sent num-bits-sent + (count elected-neighbors * who-msg-bits)
      set num-broadcasts-sent num-broadcasts-sent + 1

      if who < max [who] of link-neighbors with [state = "elected"] [
        ;; switch to active
        set color sky
        set state "active"
        stop
      ]

    ]
  ]
end

to luby-step3
  ask turtles with [state = "elected"] [
    set color red
    set state "mis"

    ask link-neighbors with [ state = "active" ] [
      set color yellow
      set state "inactive"
    ]
  ]
end

;;;;;;;;;;;;;
;; BIOLOGY ;;
;;;;;;;;;;;;;
to biology
  let outer ceiling (log max-degree 2) ;; Delta
  let inner floor (M * log num-vertices 2) ;; M * logn
  if i = outer [ set execution-finished 1 stop ]

  let step ticks mod 3

  ;; Lines 1 through 3
  (ifelse step = 0 [ biology-step1 ]
  step = 1 [ biology-step2 ]
  step = 2 [ biology-step3 ])

  if step = 2 [
    ;; next iteration
    set j j + 1
    if j = inner [
      set j  0
      set i  i + 1
    ]
  ]
  tick

  ;; Check if finished (for testing purposes)
  if not any? turtles with [state = "active" or state = "elected"] [
    if biology-tick-finished = 0 [  ;; not already set
      set biology-tick-finished ticks
    ]
  ]
end

to biology-step1
  let outer ceiling (log max-degree 2) ;; Delta
  ask turtles with [ state = "active" ] [
    let probability 1 / (2 ^ outer - i) ;; 2^logD - i

    if random-float 1.0 < probability [
      set state "elected"
      set color lime

      set num-messages-sent num-messages-sent + count link-neighbors
      set num-bits-sent num-bits-sent + count link-neighbors
      set num-broadcasts-sent num-broadcasts-sent + 1
    ]
  ]
end

to biology-step2
  ask turtles with [ state = "elected" ] [
    if any? link-neighbors with [state = "elected" OR state = "elected-conflict" ] [
      set state "elected-conflict"
    ]
  ]

  ask turtles with [ state = "elected-conflict" ] [
    set state "active"
    set color sky
  ]
end

to biology-step3
  ask turtles with [ state = "elected" ] [
    set state "mis"
    set color red

    set num-messages-sent num-messages-sent + count link-neighbors
    set num-bits-sent num-bits-sent + count link-neighbors
    set num-broadcasts-sent num-broadcasts-sent + 1

    ask link-neighbors with [ state = "active" ] [
      set state "inactive"
      set color yellow
    ]
  ]
end

;;;;;;;;;;;;;;;;;;;;;;
;; BIOLOGY IMPROVED ;;
;;;;;;;;;;;;;;;;;;;;;;
to biology-imp
  if not any? turtles with [state = "active" or state = "elected"] [ set execution-finished 1 stop ]

  let step ticks mod 3

  (ifelse step = 0 [ biology-imp-step1 ]
  step = 1 [ biology-imp-step2 ]
  step = 2 [ biology-imp-step3 ])

  tick
end

to biology-imp-step1
  ask turtles with [ state = "active" ] [
    if random-float 1.0 < pv [
      set state "elected"
      set color lime

      set num-messages-sent num-messages-sent + count link-neighbors
      set num-bits-sent num-bits-sent + count link-neighbors
      set num-broadcasts-sent num-broadcasts-sent + 1
    ]
  ]
end

to biology-imp-step2
  ask turtles with [ state = "elected" ] [
    ifelse any? link-neighbors with [ state = "elected" OR state = "elected-conlfict"] [
      set state "elected-conflict"
      set pv (pv / 2)
    ][ ;; else
      set pv (pv * 2)
      set pv (min list 0.5 pv) ;; pv=min(0.5,2*pv)
    ]
  ]

  ask turtles with [ state = "elected-conflict" ] [
    set state "active"
    set color sky
  ]
end

to biology-imp-step3
  ask turtles with [ state = "elected" ] [
    set state "mis"
    set color red

    set num-messages-sent num-messages-sent + count link-neighbors
    set num-bits-sent num-bits-sent + count link-neighbors
    set num-broadcasts-sent num-broadcasts-sent + 1

    ask link-neighbors [
      set state "inactive"
      set color yellow
    ]
  ]
end
@#$#@#$#@
GRAPHICS-WINDOW
508
10
1173
676
-1
-1
19.91
1
10
1
1
1
0
0
0
1
-16
16
-16
16
1
1
1
ticks
30.0

SLIDER
18
52
190
85
num-vertices
num-vertices
0
10000
46.0
1
1
vertices
HORIZONTAL

BUTTON
18
17
81
50
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
16
94
219
127
num-edges
num-edges
1
16
2.0
1
1
times num of vertices
HORIZONTAL

MONITOR
98
285
157
330
min-deg
min [count link-neighbors] of turtles
17
1
11

MONITOR
14
285
95
330
max-degree
max-degree
17
1
11

BUTTON
152
138
284
171
run basic random
basic-random
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
303
67
441
100
update edges viewmodel
edges-update-viewmode
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
13
138
149
171
step basic random
basic-random
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
13
173
96
206
step luby
luby
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
98
173
175
206
run luby
luby
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
114
209
208
242
run biology
biology
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
13
209
113
242
step biology
biology
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
13
243
141
276
step imp. biology
biology-imp\n
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
143
243
266
276
run imp. biology
biology-imp
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
304
197
433
242
biology: tick finished
biology-tick-finished
17
1
11

SLIDER
210
209
302
242
M
M
0
34
2.0
1
1
NIL
HORIZONTAL

BUTTON
83
17
180
50
reset graph
reset-graph\n
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

CHOOSER
303
24
441
69
edges-viewmode
edges-viewmode
"all" "none" "all-mis" "between-mis"
0

MONITOR
14
331
131
376
messages sent
num-messages-sent
17
1
11

MONITOR
134
331
215
376
bits sent
num-bits-sent
17
1
11

MONITOR
218
331
293
376
broadcasts
num-broadcasts-sent
17
1
11

BUTTON
14
378
206
411
NIL
run-and-output-experiments
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
15
413
187
446
num-graphs
num-graphs
1
1000
200.0
1
1
graphs
HORIZONTAL

SLIDER
15
448
317
481
num-graph-repeats
num-graph-repeats
1
100
5.0
1
1
times repeat each graph
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
