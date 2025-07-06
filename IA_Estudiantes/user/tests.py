import unittest
from user.models import Pregunta, TemaFavorito
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



def agregar_favorito(lista, tema):
    if tema not in lista:
        lista.append(tema)

def eliminar_favorito(lista, tema):
    if tema in lista:
        lista.remove(tema)

def listar_favoritos(lista):
    return lista.copy()

def filtrar_favoritos(lista, filtro):
    return [tema for tema in lista if filtro.lower() in tema.lower()]


class AgregarFavoritoTest(unittest.TestCase):
    def test_agrega_tema_si_no_existe(self):
        favoritos = []
        agregar_favorito(favoritos, "Matemáticas")
        self.assertIn("Matemáticas", favoritos)

    def test_no_agrega_tema_repetido(self):
        favoritos = ["Lenguaje"]
        agregar_favorito(favoritos, "Lenguaje")
        self.assertEqual(favoritos.count("Lenguaje"), 1)


class EliminarFavoritoTest(unittest.TestCase):
    def test_elimina_tema_si_existe(self):
        favoritos = ["Historia", "Física"]
        eliminar_favorito(favoritos, "Física")
        self.assertNotIn("Física", favoritos)

    def test_no_falla_si_tema_no_existe(self):
        favoritos = ["Química"]
        eliminar_favorito(favoritos, "Lenguaje")
        self.assertEqual(favoritos, ["Química"])


class ListarFavoritosTest(unittest.TestCase):
    def test_lista_igual_a_original(self):
        favoritos = ["Historia", "Lenguaje"]
        copia = listar_favoritos(favoritos)
        self.assertEqual(copia, favoritos)
        self.assertIsNot(copia, favoritos)  # debe ser una copia, no la misma lista


class FiltrarFavoritosTest(unittest.TestCase):
    def test_filtra_por_texto(self):
        favoritos = ["Matemáticas", "Lenguaje", "Biología"]
        resultado = filtrar_favoritos(favoritos, "bio")
        self.assertEqual(resultado, ["Biología"])

    def test_filtrado_sensible_a_mayusculas(self):
        favoritos = ["Química", "Historia"]
        resultado = filtrar_favoritos(favoritos, "HIS")
        self.assertEqual(resultado, ["Historia"])

    def test_filtrado_sin_resultados(self):
        favoritos = ["Física", "Arte"]
        resultado = filtrar_favoritos(favoritos, "geo")
        self.assertEqual(resultado, [])