import unittest
from user.models import Pregunta
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

class TestPregunta(unittest.TestCase):
    def setUp(self):
        self.pregunta = Pregunta(
            enunciado="¿Cuál es la función principal de un conector causal en un texto?",
            opcionA="Introducir un ejemplo para reforzar una idea",
            opcionB="Contraponer dos ideas en conflicto",
            opcionC="Indicar la relación de causa entre dos enunciados",
            opcionD="Repetir una información relevante previamente dicha",
            respuestaCorrecta="c",
            retroPregunta="Un conector causal indica relación de causa entre ideas.",
            retroIA="Revisa los conectores de causa como 'porque', 'ya que', 'por tanto'."
        )

    def test_respuesta_correcta(self):
        self.assertFalse(self.pregunta.detectar_respuesta_incorrecta("c"))

    def test_respuesta_incorrecta(self):
        self.assertTrue(self.pregunta.detectar_respuesta_incorrecta("a"))
        self.assertTrue(self.pregunta.detectar_respuesta_incorrecta("b"))
        self.assertTrue(self.pregunta.detectar_respuesta_incorrecta("d"))

if __name__ == "__main__":
    unittest.main()