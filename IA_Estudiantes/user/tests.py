import unittest
from user.metricas import (
    calcular_avance_objetivo,
    calcular_porcentaje_temas,
)

class TestMetricas(unittest.TestCase):

    def test_calcular_avance_objetivo(self):
        notas_simulacros = {"matematicas": 600, "lenguaje": 720}
        notas_objetivos = {"matematicas": 700, "lenguaje": 750}
        esperado = {"matematicas": 0.86, "lenguaje": 0.96}
        resultado = calcular_avance_objetivo(notas_simulacros, notas_objetivos)
        self.assertEqual(resultado, esperado)

    def test_calcular_avance_objetivo_con_faltantes(self):
        notas_simulacros = {"matematicas": 600}
        notas_objetivos = {"matematicas": 700, "lenguaje": 750}
        esperado = {"matematicas": 0.86, "lenguaje": 0.0}
        resultado = calcular_avance_objetivo(notas_simulacros, notas_objetivos)
        self.assertEqual(resultado, esperado)

    def test_calcular_porcentaje_temas(self):
        self.assertEqual(calcular_porcentaje_temas(8, 10), 80.0)
        self.assertEqual(calcular_porcentaje_temas(0, 10), 0.0)
        self.assertEqual(calcular_porcentaje_temas(3, 0), 0)

    def test_estimar_rendimiento(self):
        notas_simulacros = {"matematicas": 600, "lenguaje": 720}
        self.assertEqual(estimar_rendimiento(notas_simulacros), 660.0)
        self.assertEqual(estimar_rendimiento({}), 0)

if __name__ == "__main__":
    unittest.main()

