lsystem_presets = {
    "Arvore clássica": {
        "axiom": "F",
        "rules": {
            "F": "F[+F]F[-F]F"
        },
        "angle": 25,
        "length": 5,
        "iterations": 5
    },
    "Árvore de Natal estilizada": {
        "axiom": "X",
        "rules": {
            "X": "F[+X]F[-X]+X",
            "F": "FF"
        },
        "angle": 25,
        "length": 5,
        "iterations": 6
    },
    "Árvore densa (estilo selvagem)": {
        "axiom": "F",
        "rules": {
            "F": "FF-[-F+F+F]+[+F-F-F]"
        },
        "angle": 22.5,
        "length": 5,
        "iterations": 4
    },
    "Samambaia (Fractal Fern)": {
        "axiom": "X",
        "rules": {
            "X": "F-[[X]+X]+F[+FX]-X",
            "F": "FF"
        },
        "angle": 25,
        "length": 5,
        "iterations": 5
    },
    "Samambaia 2 (Fractal Fern)": {
        "axiom": "X",
        "rules": {
            "X": "F-[[X]+X]+F[+FX]-X",
            "F": "FF"
        },
        "angle": 15 ,
        "length": 2,
        "iterations": 8
    },
    "Koch Curve": {
        "axiom": "F",
        "rules": {
            "F": "F+F−F−F+F"
        },
        "angle": 90,
        "length": 5,
        "iterations": 4
    },
    "Dragon Curve (Heighway)": {
        "axiom": "FX",
        "rules": {
            "X": "X+YF+",
            "Y": "-FX-Y"
        },
        "angle": 90,
        "length": 5,
        "iterations": 10
    },
    "Sierpinski Triangle": {
        "axiom": "F-G-G",
        "rules": {
            "F": "F-G+F+G-F",
            "G": "GG"
        },
        "angle": 120,
        "length": 5,
        "iterations": 5
    }
}

def get_lsystem(name):
    return lsystem_presets.get(name, None)