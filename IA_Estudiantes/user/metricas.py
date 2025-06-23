def calcular_avance_objetivo(notas_simulacros, notas_objetivos):
    avance = {}
    for asignatura, objetivo in notas_objetivos.items():
        nota = notas_simulacros.get(asignatura)
        if nota is not None and objetivo > 0:
            avance[asignatura] = round(min(nota / objetivo, 1.0), 2)
        else:
            avance[asignatura] = 0.0
    return avance

def calcular_porcentaje_temas(topicos_cubiertos, total_topicos):
    if total_topicos == 0:
        return 0
    return round((topicos_cubiertos / total_topicos) * 100, 2)
