import pygame
from pygame.locals import *

def loadLevel(lvl):
    # P = Platform
    # Q = Platform (Player Can't change dimension)
    # q Platform (Player Can't jump)
    # D = Platform (Can change side Platform)
    # d = Platform (stop Camera)
    # H = Portal
    # B = Blackholes
    # F = Ghost Platform (1 - 255 Alpha, Changer, Collision)
    # I = Ghost Platform (0 Alpha, no Changer, no Collision)
    # i = Ghost Platform (0 Alpha, no Changer, Collision)
    # E = Enemy
    # (T, t) = Trampolin
    # (|, -) = Laser
    # S = Switch
    # (o, O, 0) = Coins Blue/Red/Gold
    # (M, m) = Platform Color (M - RED, m - BLUE)
    # C = Cannon
    # (^, <, >, v) = Spikes
    # (A, a) = Arrow (Change ORIENTATION)
    # (@, *) = Marks (@ -> Camera / * -> Player)
    # (X, x) = CheckPoint

    if lvl == 1:
        level =['                                       ',
                'P                                      ',
                'PH                                     ',
                'P                       P              ',
                'P                       P              ',
                'P                       P              ',
                '    B  B  B                            ',
                '                                       ',
                '                 PP                    ',
                '                  P                    ',
                '                  P                    ',
                '                E P                    ',
                '                  P                    ',
                '                  P                    ',
                'P                 P                    ',
                'PS                P                    ',
                'P                 P                    ',
                '               * PP                    ',
                '                                       ',
                '                                       ',
                '                         B  B  B  B  B ',
                '                                       ',
                'I                 PPPPPPP             I',
                'I                 P     |             I',
                'I                 P 0   |             I',
                'I                 P     |             I',
                'I                 PPPPPPP             I',
                '                                       ',
                '                         B  B  B  B  B ',
                '                                       ',
                '            O                          ',
                '                                       ',
                '                                       ',
                '                                       ',
                '            o                          ',
                '                                       ',
                '            o                          ',
                '                                       ',
                '            o                          ',
                '                                       ',
                '                                       ',
                '      P           G                    ',
                '      P           G                    ',
                '      Po              *                ',
                '      P                                ',
                '      Po                               ',
                '      P                                ',
                '      PPo                       F      ',
                '      PPP                     O F      ',
                '      PPPPo                     F      ',
                '      PPPP  O                 0 F      ',
                '      PPPPo                     F      ',
                '      PPP                     O F      ',
                '      PPo                       F      ',
                '      P                                ',
                '      Po                               ',
                '      P                                ',
                '      Po                               ',
                '      P                                ',
                '      P                                ',
                '      P                                ',
                '                                       ',
                '                           P           ',
                '                           P           ',
                '                           P           ',
                'I                          P OO       I',
                'I                          P oo       I',
                'I                          P oo       I',
                'I                          P oo       I',
                'I                          P oo       I',
                'I                          P          I',
                'I                          P     0    I',
                'I                          P          I',
                '                           P           ',
                '                           P           ',
                '        P                              ',
                '        P                              ',
                '        P                              ',
                '        P                              ',
                '        P         P                    ',
                '                  P                    ',
                '                  P                    ',
                '         PMMMMMMMMPPPPPPPPP            ',
                '         P        PS      P            ',
                '         P        P       P            ',
                '         P        P       P            ',
                '         P        |       P            ',
                '         P        |       P            ',
                '         P        |       P            ',
                '         P        P       P            ',
                '         P        P       P            ',
                '         P        P       P            ',
                '         PPPPPPPPPP       P            ',
                '                          P            ',
                '                      P   P            ',
                '                      PPPPP            ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '            P                          ',
                '            P              C          P',
                '            P                         P',
                '            P                         P',
                '            P                         P',
                '            P                         P',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                       ',
                '                                       ',
                'P                                      ',
                'P                                      ',
                '                                       ',
                '                                       ',
                '             B                         ',
                'PP                                     ',
                'P            B      P                  ',
                'P                   P                  ',
                'P       PPPPPPP     PPPPPPPP           ',
                'P       P     P>          <P           ',
                'P       P     P>       0 PPP           ',
                'PE      PPPPPPP>          <P           ',
                'P             P>       PPPPP           ',
                'P             P>       PPPPP           ',
                'P             P>          <Q           ',
                'P       P     PPPP        <Q           ',
                'P       P                 <Q           ',
                'P       P                 <P           ',
                'P       P                 <P           ',
                'P       PPPPPPPPPPPPPPPPPPPP           ',
                'P                                      ',
                'PP                                     ',
                '                                       ',
                '                                      P',
                '                                      P',
                '                                  o   P',
                '                                      P',
                '                                  o   P',
                '                                    PPP',
                '                                     PP',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                 k    P']

        settings = [
                     {'class': 'Laser', 'id': [1, 2, 3], 't': '|', 'property': {'color': 'yellow'}},
                     {'class': 'Laser', 'id': [4, 5, 6], 't': '|', 'property': {'color': 'red'}},
                     {'class': 'Switch','id': [1], 't': 'S', 'property': {'dir': 'left', 'color': 'yellow', 'idLaser': [1, 2, 3]}},
                     {'class': 'Switch','id': [2], 't': 'S', 'property': {'dir': 'left', 'color': 'red', 'idLaser': [4, 5, 6]}},
                     {'class': 'GhostPlatform','id': [1, 2, 3, 4, 5, 6, 7], 't': 'F', 'property': {'alpha': 255, 'velAlpha': 23}},
                     {'class': 'Canon','id': [1], 't': 'C', 'property': {'dir': 'top', 'color': 'red', 'power': 12, 'disable': False}},
                     {'class': 'Enemy','id': [1], 't': 'E', 'property': {'collision': True, 'dir': 'left', 'orientation': 'up', 'group': 'enemy01', 'speedY': 2, 'speedX': 5, 'canDie': True, 'damage': False, 'lives': 1, 'stopped': False}},
                     {'class': 'Enemy','id': [2], 't': 'E', 'property': {'collision': True, 'dir': 'right', 'orientation': 'up', 'group': 'enemy01', 'speedY': 2, 'speedX': 5, 'canDie': True, 'damage': False, 'lives': 1, 'stopped': False}},
                     {'class': 'Marker','id': [1], 't': '*', 'property': {'speed': 1}},
                     {'class': 'Marker','id': [2], 't': '*', 'property': {'speed': 2}},
                     {'class': 'Platform','id': [1, 2], 't': 'G', 'property': {'coord': [200, 0, 200, 0], 't1': 'P', 't2': 'G', 'speedX': 0, 'speedY': 2, 'glued': True}}
                     #{'class': 'Switch','id': [1], 't': 'S', 'property': {'color': 'yellow', 'idLaser': [1, 2, 3]}},
            ]

    if lvl == 2:

        level =['                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                '                                      ',
                'P                                     ',
                'PH                                    ',
                'P                                     ',
                'P                                     ',
                'P                                     ',
                'P                                     ',
                'P                                     ',
                'P                                     ',
                'P                                     ',
                'P                                     ',
                'P           <PPPPPPPPPP               ',
                'P           <P>vvvvvvvv               ',
                'P           <P>                       ',
                'P           <P>  a                    ',
                'P           <P>                       ',
                'P           <P> o o o  D              ',
                'P            P> O o o  D              ',
                'PPP>         P> o o o  D              ',
                'P            P> o o O  D           P  ',
                'P           <P> O o o             0P  ',
                'P           <P> O o o              P  ',
                'P           <P> o o o                 ',
                'P           <P> o o O  D              ',
                'P           <P> O o o  D              ',
                'P           <P> o o o  D              ',
                'P      B    <P> o o o  D              ',
                'P>          <P>                       ',
                'P           <P>                       ',
                'P           <P>                       ',
                'P                                     ',
                'P      C                              ',
                'P                            P        ',
                'P                            P        ',
                'P            P>              P        ',
                'P^^^^^^^^^^^^P>              P        ',
                'PPPPPPPPPPPPPP>              P        ',
                '                             P        ',
                '   PPPP                      P        ',
                'I     P                      P        I',
                'I   0 P                      P        I',
                'I     P                      P        I',
                '   PPPP                      P        ',
                '                             P        ',
                '                             P        ',
                '                             P        ',
                '     P                       P o  P   ',
                '     P                            P   ',
                '     P                            P   ',
                '     P0   P a          B          P   ',
                '     P    Po                          ',
                '     PO   P    P                      ',
                '     P    Po   Po      B             P',
                '     Po   P    P                     P',
                '     P    PO   Po                    P',
                '     Po        P                     P',
                '     P A       Po                    P',
                '               P                    oP',
                '                                     P',
                '                                    oP',
                '                                     P',
                '                    PP          C   oP',
                '                    P                P',
                '                    P                P',
                '                    Po                ',
                '                    P       B         ',
                '                    P                 ',
                '                    Po                ',
                '                    P       B         ',
                '                    P           C     ',
                '                    Po                ',
                '                    PE      B         ',
                '                    P                 ',
                '                    P                 ',
                '                    P                 ',
                '                    P                 ',
                '                    PP       P        ',
                '                            oP        ',
                '                             P        ',
                '                            oP        ',
                '                             P        ',
                '                            oP        ',
                '                             P        ',
                'P                            P        ',
                'Po                           P        ',
                'P                           <PP       ',
                'P                            <PP      ',
                '                              <PPP    ',
                '                                 <Pooo ',
                '                                 <Pooo ',
                'P                                <P    ',
                'P                                <PO O ',
                'Po                                P    ',
                'P                0                P 0  ',
                'Po                                P    ',
                'P                                <P    ',
                'Po                               <P A  ',
                'P                                <P    ',
                'P                                <PPPPP',
                'P K                                    ',
                                                        ]
        settings = [
                     {'class': 'Canon','id': [1, 2], 't': 'C', 'property': {'dir': 'bot', 'color': 'blue', 'power': 12, 'disable': False}},
                     {'class': 'Canon','id': [3], 't': 'C', 'property': {'dir': 'top', 'color': 'blue', 'power': 12, 'disable': False}},
                     {'class': 'Enemy','id': [1], 't': 'E', 'property': {'dir': 'left', 'orientation': 'up', 'group': 'enemy01', 'speed': 2, 'canDie': True, 'frames': 8, 'lives': 1}},
                     
                     #{'class': 'Switch','id': [1], 't': 'S', 'property': {'color': 'yellow', 'idLaser': [1, 2, 3]}},
                   ]
    elif lvl == 3:

        level= ['                                       ',
                '                                       ',
                'PPPPP                                  ',
                ' H  P                                  ',
                '    P  o                               ',
                '    P                                  ',
                '    P                                  ',
                '    P                                  ',
                '    P                                  ',
                '    P                                  ',
                '    P                                  ',
                '    P                                  ',
                '    d                                  ',
                '    P                                  ',
                '                                       ',
                '                                       ',
                '                    G                  ',
                '                    G                  ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                    d                  ',
                '                    P                  ',
                '                                 I     ',
                '                                  P    ',
                '                                  P    ',
                '                   <P>          E P    ',
                '                   <P>            P    ',
                '                   <P>            P    ',
                '                   <P>            P    ',
                '                   <P>           I     ',
                '                   <P>                 ',
                '                              PPPPPPPPP',
                '                              P       P',
                '                              P     a P',
                '                    PPPPPPPPPPP        ',
                '                    P        |D        ',
                '                    P        |D        ',
                '                    P        |D        ',
                '                    P         P        ',
                '                    P         P       F',
                '                    P|        P      SF',
                '             P******P|        P       F',
                'P            P      P|        PPPPPPPPP',
                'P            P------P          P       ',
                '             P------P  @              Q',
                '           O P      P                 Q',
                '             P    A P          P      Q',
                '      PPPPPPPP      |          P       ',
                '      PS     P      |          P       ',
                '      P      P      |          P       ',
                '      P      P a    P          P      Q',
                '      P      P------P          P      Q',
                '      P      P      P-----     P       ',
                '      P             P          P       ',
                '      P             P          P       ',
                '      P             P          P o    P',
                '      P      P      P          P       ',
                '      P------P      P          P       ',
                '      d      P      P     -----P       ',
                '      d      P      P A        P       ',
                '      P      P  0   P         SP       ',
                '      P      P  A   PPPPPPPPPPPP       ',
                '      P      P      PP        PP       ',
                'PPPPPPPmmmmmmPPPPPPPPP        PPPPPPPPP',
                '      P                                ',
                '                                       ',
                '              C                        ',
                ' P                                     ',
                ' P                        PPPP         ',
                ' P                                     ',
                '                                       ',
                '                                       ',
                'PPPPPPPPPPPPPPPPPPPPPPPP      PPPPPPPPP',
                '                                       ',
                '                                       ',
                '                                       ',
                '                             C         ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '          C                            ',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                       ',
                '                                       ',
                'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                P      ',
                '                                P      ',
                '                                P   O  ',
                '                                P      ',
                'PPPPPPPPP             PPPPPPPPPPPffffff',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '              PPPPPPPPPPPPPPPPPPPPPPPPP',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                       ',
                '                                E      ',
                '                                       ',
                '                                       ',
                'PPPPPPPPPPPPPPPPPPPPPPPP               ',
                '        p                              ',
                '        p                              ',
                '        p                              ',
                '                                       ',
                '    I                       B          ',
                '     P>                                ',
                'I    P>                               I',
                'I    P>                     B         I',
                'I    P>                               I',
                'I    P>                               I',
                'I    P>                     B       0 I',
                'I   EP>                               I',
                'I    P>                               I',
                'I    P>                     B         I',
                'I    P>                               I',
                'I    P>                               I',
                'I    P>                     B         I',
                'I    P>                             O I',
                'I    P>                               I',
                '    I                       B          ',
                '                                       ',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                      P',
                '                                       ',
                '          <P                           ',
                '          <P                           ',
                '                                       ',
                '                                       ',
                '       <P                              ',
                '       <P                              ',
                '                                       ',
                '                                       ',
                '             <P#                       ',
                '             <P#                       ',
                '                                       ',
                'PPPt                                   ',
                'PPP                                    ',
                'PPP                                    ',
                'Pvv                                    ',
                'P                                      ',
                'P                                      ',
                'Px                                     ',
                'P                                      ',
                'P                                      ',
                'P          B  C       P                ',
                'P     P               P                ',
                'P     P    B          P             PPP',
                'I     P               P            P  I',
                'I     P                            P0 I',
                'II                                 P  I',
                'P                                   PPP',
                'P            I                         ',
                'P           P                       B  ',
                'P           P                          ',
                'P           P E        P            B  ',
                'P           P          P               ',
                'P           P          P            B  ',
                'P           P          P               ',
                'P E         P                       B  ',
                'P           P                          ',
                'P        B  P                       B  ',
                'P           P                          ',
                'P E      B  FI                      B  ',
                'P           F                          ',
                'P        B  Fo       C              B  ',
                ' I          F                          ',
                '         B                          B  ',
                'P                                      ',
                'P        B                          B  ',
                'P                                      ',
                'P                                      ',
                'P                                      ',
                'P                                      ',
                'P  K                                   ',
                'P                                      ',
                'P                                      ',
                'P                                      ',
                'P                                      ',
                'P                                      ',
                'P                                      ',
                'P                                      ',
                                                         ]

        settings = [
                     {'class': 'Canon','id': [2], 't': 'C', 'property': {'dir': 'bot', 'color': 'blue', 'power': 12, 'disable': False}},
                     {'class': 'Canon','id': [1], 't': 'C', 'property': {'dir': 'top', 'color': 'red', 'power': 12, 'disable': False}},
                     {'class': 'Canon','id': [3, 4], 't': 'C', 'property': {'dir': 'top', 'color': 'blue', 'power': 12, 'disable': True}},
                     {'class': 'Canon','id': [5], 't': 'C', 'property': {'dir': 'top', 'color': 'red', 'power': 12, 'disable': True}},
                     {'class': 'GhostPlatform','id': [1, 5], 't': 'F', 'property': {'alpha': 0, 'velAlpha': 26}},
                     {'class': 'GhostPlatform','id': [5, 8], 't': 'F', 'property': {'alpha': 0, 'velAlpha': 10}},
                     {'class': 'Marker','id': [1], 't': '@', 'property': {'speed': 1}},
                     {'class': 'Marker','id': [2, 8], 't': '*', 'property': {'speed': 2}},
                     {'class': 'Enemy','id': [3], 't': 'E', 'property': {'collision': True, 'dir': 'left', 'orientation': 'down', 'group': 'enemy03', 'speedY': 1, 'speedX': 7, 'canDie': True, 'damage': True, 'lives': 1, 'stopped': False, 'hasItem': None}},
                     {'class': 'Enemy','id': [1], 't': 'E', 'property': {'collision': True, 'dir': 'left', 'orientation': 'down', 'group': 'enemy01', 'speedY': 2, 'speedX': 5, 'canDie': True, 'damage': True, 'lives': 1, 'stopped': False, 'hasItem': 'O'}},
                     {'class': 'Enemy','id': [2], 't': 'E', 'property': {'collision': True, 'dir': 'left', 'orientation': 'down', 'group': 'enemy01', 'speedY': 2, 'speedX': 5, 'canDie': True, 'damage': True, 'lives': 1, 'stopped': False, 'hasItem': None}},
                     {'class': 'Enemy','id': [4], 't': 'E', 'property': {'collision': True, 'dir': 'right', 'orientation': 'down', 'group': 'enemy01', 'speedY': 2, 'speedX': 5, 'canDie': True, 'damage': True, 'lives': 1, 'stopped': False, 'hasItem': None}},
                     {'class': 'Enemy','id': [5], 't': 'E', 'property': {'collision': False, 'dir': 'right', 'orientation': 'up', 'group': 'enemy02', 'speedY': 2, 'speedX': 4, 'canDie': False, 'damage': False, 'lives': 1, 'stopped': True, 'hasItem': None}},
                     {'class': 'Enemy','id': [6], 't': 'E', 'property': {'collision': True, 'dir': 'right', 'orientation': 'up', 'group': 'enemy01', 'speedY': 2, 'speedX': 5, 'canDie': True, 'damage': True, 'lives': 1, 'stopped': False, 'hasItem': None}},
                     {'class': 'Laser', 'id': [1, 6], 't': '-', 'property': {'color': 'yellow', 'coord': [120, 120], 'dir': 'up', 'speedUp': 2, 'speedDown': 2, 'random': False, 'timeDelay': 0}},
                     {'class': 'Laser', 'id': [6, 12], 't': '-', 'property': {'color': 'yellow', 'coord': [120, 120], 'speedUp': 3, 'speedDown': 3, 'random': False, 'timeDelay': 20}},
                     {'class': 'Laser', 'id': [12, 17], 't': '-', 'property': {'color': 'yellow', 'coord': [120, 120], 'speedUp': -2, 'speedDown': -2, 'random': False, 'timeDelay': 0}},             
                     {'class': 'Laser', 'id': [17, 23], 't': '-', 'property': {'color': 'yellow', 'coord': [120, 120], 'speedUp': -2, 'speedDown': -2, 'random': False, 'timeDelay': 40}},
                     {'class': 'Laser', 'id': [23, 26], 't': '|', 'property': {'color': 'blue', 'coord': []}},
                     {'class': 'Laser', 'id': [26, 32], 't': '-', 'property': {'color': 'red', 'coord': []}},
                     {'class': 'Laser', 'id': [32, 38], 't': '-', 'property': {'color': 'green', 'coord': []}},
                     {'class': 'Laser', 'id': [38, 41], 't': '|', 'property': {'color': 'yellow', 'coord': [160, 160], 'speedLeft': -2, 'speedRight': -2, 'random': False, 'timeDelay': 0}},
                     {'class': 'Laser', 'id': [41, 44], 't': '|', 'property': {'color': 'yellow', 'coord': [160, 160], 'speedLeft': 2, 'speedRight': 2, 'random': False, 'timeDelay': 0}},
                     {'class': 'Switch', 'id': [1], 'idLaser': [26, 32], 't': 'S', 'property': {'dir': 'right', 'color': 'red'}},
                     {'class': 'Switch', 'id': [2], 'idLaser': [23, 26], 't': 'S', 'property': {'dir': 'left', 'color': 'blue'}},
                     {'class': 'Switch', 'id': [3], 'idLaser': [32, 38], 't': 'S', 'property': {'dir': 'right', 'color': 'green'}},
                     {'class': 'Platform','id': [1, 2, 3], 't': 'p', 'property': {'id': 1}}, 
                     {'class': 'Platform','id': [4, 5], 't': 'G', 'property': {'coord': [0, 320, 0, 320], 't1': 'D', 't2': 'G', 'speedX': -2, 'speedY': 0, 'glued': True}},
                     {'class': 'Trap','id': [1, 3], 't': '#', 'property': {'dir': 'left', 'time': 50}}]

    return level, settings
