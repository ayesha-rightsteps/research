## Collision-type check (evaluation pass)

| Stage                            | Method                     |   Collision episodes |   Drone–obstacle |   Drone–drone |   Both |   % obstacle |   % near goal |
|:---------------------------------|:---------------------------|---------------------:|-----------------:|--------------:|-------:|-------------:|--------------:|
| Stage 2 (5 drones, 5 obstacles)  | Fixed-weight MAPPO         |                  108 |              107 |             1 |      0 |         99.1 |          20.4 |
| Stage 2 (5 drones, 5 obstacles)  | Hand-coded τ-rule MAPPO    |                  125 |              124 |             1 |      0 |         99.2 |          20.8 |
| Stage 2 (5 drones, 5 obstacles)  | MAPPO + PAH                |                  105 |              104 |             1 |      0 |         99   |          21.9 |
| Stage 3 (8 drones, 10 obstacles) | Fixed-weight MAPPO         |                   53 |               50 |             3 |      0 |         94.3 |          30.2 |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH                |                   56 |               56 |             0 |      0 |        100   |          39.3 |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH, Hungarian off |                   97 |               78 |            19 |      0 |         80.4 |          19.6 |

## IGAT-MARL metrics check (evaluation pass)

| Stage                            | Method                     | Loss-of-separation pair-steps per episode   | Active conflict edges per step   |
|:---------------------------------|:---------------------------|:--------------------------------------------|:---------------------------------|
| Stage 2 (5 drones, 5 obstacles)  | Fixed-weight MAPPO         | 0.098 ± 0.038                               | 0.0016 ± 0.0007                  |
| Stage 2 (5 drones, 5 obstacles)  | Hand-coded τ-rule MAPPO    | 0.064 ± 0.030                               | 0.0010 ± 0.0003                  |
| Stage 2 (5 drones, 5 obstacles)  | MAPPO + PAH                | 0.100 ± 0.049                               | 0.0014 ± 0.0007                  |
| Stage 3 (8 drones, 10 obstacles) | Fixed-weight MAPPO         | 0.215 ± 0.166                               | 0.0039 ± 0.0028                  |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH                | 0.185 ± 0.163                               | 0.0030 ± 0.0026                  |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH, Hungarian off | 0.870 ± 0.243                               | 0.0514 ± 0.0182                  |

## Safety-reward frequency and α spread (training-like replay; Stage 2 = mean ± std over 5 seeds)

| Stage                            | Method                     | Safety reward on, % drone-steps (range over training)   | final: drone within 9   | final: obstacle within 9   | Conflict flagged, % (final)   | α median (final)   | α 10th pct (final)   | % steps α < 0.5 (final)   |
|:---------------------------------|:---------------------------|:--------------------------------------------------------|:------------------------|:---------------------------|:------------------------------|:-------------------|:---------------------|:--------------------------|
| Stage 2 (5 drones, 5 obstacles)  | Fixed-weight MAPPO         | 0.18–0.55                                               | 0.01 ± 0.02             | 0.36 ± 0.08                | 0.04 ± 0.02                   | 0.50 ± 0.00        | 0.50 ± 0.00          | 0.00 ± 0.00               |
| Stage 2 (5 drones, 5 obstacles)  | Hand-coded τ-rule MAPPO    | 0.19–0.57                                               | 0.01 ± 0.02             | 0.37 ± 0.09                | 0.03 ± 0.02                   | 0.90 ± 0.00        | 0.90 ± 0.00          | 0.00 ± 0.01               |
| Stage 2 (5 drones, 5 obstacles)  | MAPPO + PAH                | 0.17–0.62                                               | 0.00 ± 0.01             | 0.32 ± 0.04                | 0.02 ± 0.01                   | 0.88 ± 0.05        | 0.71 ± 0.02          | 0.01 ± 0.01               |
| Stage 3 (8 drones, 10 obstacles) | Fixed-weight MAPPO         | 0.81–1.31                                               | 0.41                    | 0.86                       | 0.20                          | 0.50               | 0.50                 | 0.00                      |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH                | 0.85–1.26                                               | 0.10                    | 0.97                       | 0.10                          | 0.87               | 0.70                 | 0.03                      |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH, Hungarian off | 1.20–1.71                                               | 0.61                    | 0.74                       | 1.06                          | 0.90               | 0.70                 | 0.70                      |

## Advantage-correlation check (final checkpoints; Stage 2 = mean ± std over 5 seeds)

| Stage                            | Method                     | α mean      | corr(mission adv., safety adv.)   | raw std mission adv.   | raw std safety adv.   | cosine(own-α signal, α=0.5 signal)   | magnitude own / α=0.5   | corr(own-α signal, plain combined advantage)   |
|:---------------------------------|:---------------------------|:------------|:----------------------------------|:-----------------------|:----------------------|:-------------------------------------|:------------------------|:-----------------------------------------------|
| Stage 2 (5 drones, 5 obstacles)  | Fixed-weight MAPPO         | 0.50 ± 0.00 | -0.52 ± 0.03                      | 3.22 ± 0.10            | 2.32 ± 0.04           | 1.00 ± 0.00                          | 1.00 ± 0.00             | 0.96 ± 0.01                                    |
| Stage 2 (5 drones, 5 obstacles)  | Hand-coded τ-rule MAPPO    | 0.90 ± 0.00 | 0.00 ± 0.06                       | 2.59 ± 0.39            | 4.09 ± 0.08           | 0.78 ± 0.02                          | 1.29 ± 0.03             | 0.99 ± 0.00                                    |
| Stage 2 (5 drones, 5 obstacles)  | MAPPO + PAH                | 0.85 ± 0.02 | -0.03 ± 0.12                      | 2.66 ± 0.13            | 3.97 ± 0.31           | 0.79 ± 0.04                          | 1.28 ± 0.07             | 0.98 ± 0.01                                    |
| Stage 3 (8 drones, 10 obstacles) | Fixed-weight MAPPO         | 0.50        | -0.27                             | 3.75                   | 2.27                  | 1.00                                 | 1.00                    | 0.95                                           |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH                | 0.84        | 0.22                              | 3.57                   | 4.28                  | 0.85                                 | 1.15                    | 0.99                                           |
| Stage 3 (8 drones, 10 obstacles) | MAPPO + PAH, Hungarian off | 0.87        | 0.51                              | 4.22                   | 4.43                  | 0.91                                 | 1.09                    | 1.00                                           |

## Advantage-correlation check across Stage 3 training

|                             |   ('alpha_mean', 'mean') |   ('alpha_mean', 'std') |   ('corr_m_s', 'mean') |   ('corr_m_s', 'std') |   ('cos_own_05', 'mean') |   ('cos_own_05', 'std') |   ('norm_own_over_05', 'mean') |   ('norm_own_over_05', 'std') |   ('corr_own_comb', 'mean') |   ('corr_own_comb', 'std') |
|:----------------------------|-------------------------:|------------------------:|-----------------------:|----------------------:|-------------------------:|------------------------:|-------------------------------:|------------------------------:|----------------------------:|---------------------------:|
| ('B4', 'ep507')             |                    0.5   |                   0     |                 -0.147 |                 0.256 |                    1     |                   0     |                          1     |                         0     |                       0.969 |                      0.009 |
| ('B4', 'ep4064')            |                    0.5   |                   0     |                 -0.217 |                 0.165 |                    1     |                   0     |                          1     |                         0     |                       0.969 |                      0.006 |
| ('B4', 'ep7607')            |                    0.5   |                   0     |                 -0.178 |                 0.144 |                    1     |                   0     |                          1     |                         0     |                       0.985 |                      0.01  |
| ('B4', 'final')             |                    0.5   |                   0     |                 -0.271 |                 0.158 |                    1     |                   0     |                          1     |                         0     |                       0.952 |                      0.011 |
| ('M', 'ep507')              |                    0.897 |                   0     |                  0.318 |                 0.159 |                    0.865 |                   0.038 |                          1.156 |                         0.051 |                       0.998 |                      0.005 |
| ('M', 'ep4044')             |                    0.886 |                   0.003 |                  0.271 |                 0.104 |                    0.856 |                   0.027 |                          1.167 |                         0.036 |                       0.998 |                      0.001 |
| ('M', 'ep7572')             |                    0.876 |                   0.002 |                  0.274 |                 0.096 |                    0.859 |                   0.024 |                          1.158 |                         0.034 |                       0.997 |                      0.001 |
| ('M', 'final')              |                    0.845 |                   0.002 |                  0.219 |                 0.171 |                    0.85  |                   0.046 |                          1.145 |                         0.055 |                       0.992 |                      0.004 |
| ('M-noHungarian', 'ep506')  |                    0.877 |                   0.002 |                  0.481 |                 0.139 |                    0.905 |                   0.029 |                          1.099 |                         0.034 |                       0.999 |                      0.001 |
| ('M-noHungarian', 'ep4030') |                    0.819 |                   0.005 |                  0.482 |                 0.103 |                    0.907 |                   0.022 |                          1.069 |                         0.027 |                       0.991 |                      0.004 |
| ('M-noHungarian', 'ep7565') |                    0.858 |                   0.006 |                  0.595 |                 0.065 |                    0.928 |                   0.013 |                          1.07  |                         0.014 |                       0.997 |                      0.001 |
| ('M-noHungarian', 'final')  |                    0.868 |                   0.003 |                  0.514 |                 0.074 |                    0.912 |                   0.017 |                          1.088 |                         0.018 |                       0.997 |                      0.001 |
