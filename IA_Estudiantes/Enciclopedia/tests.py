from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from Enciclopedia.models import Enciclopedia
from django.core.files.uploadedfile import SimpleUploadedFile

#PRUEBAS DE INTEGRACIÓN PARA LA APLICACIÓN ENCICLOPEDIA

# TC-001 ASOCIADO A TAREA: Verificar que los estudiantes puedan ver contenidos de la enciclopedia
class EnciclopediaVistaTests(TestCase):

    def setUp(self):
        # Crear grupos
        self.docentes = Group.objects.create(name="docentes")
        self.estudiantes = Group.objects.create(name="estudiantes")
        self.matematica = Group.objects.create(name="Matematica")  # 💡 importante

        # Crear usuarios
        self.user_estudiante = User.objects.create_user(username="estudiante", password="1234")
        self.user_estudiante.groups.add(self.estudiantes, self.matematica)

        self.user_docente = User.objects.create_user(username="docente", password="1234")
        self.user_docente.groups.add(self.docentes, self.matematica)

        # Crear contenido de enciclopedia
        Enciclopedia.objects.create(
            nombre="Álgebra",
            descripcion="Contenido de prueba",
            categoria="Matematica"
        )

        self.client = Client()
        self.url = reverse("lista_enciclopedia")


    def test_lista_enciclopedia_estudiante(self):
        self.client.login(username="estudiante", password="1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Álgebra")
        self.assertNotContains(response, "Editar")
        self.assertNotContains(response, "Eliminar")

    def test_lista_enciclopedia_docente(self):
        self.client.login(username="docente", password="1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Álgebra")
        self.assertContains(response, "Editar")
        self.assertContains(response, "Eliminar")

#TC-002 ASOCIADO A TAREA: Permitir que el docente modifique contenidos
class EnciclopediaEdicionTests(TestCase):

    def setUp(self):
        # Crear grupo y usuario docente
        docentes = Group.objects.create(name="docentes")
        self.docente = User.objects.create_user(username="docente", password="1234")
        self.docente.groups.add(docentes)

        # Crear contenido
        self.contenido = Enciclopedia.objects.create(nombre="Física", descripcion="Contenido inicial")

        self.client = Client()
        self.client.login(username="docente", password="1234")

    def test_edicion_de_contenido(self):
        url_editar = reverse("editar_enciclopedia", args=[self.contenido.id])

        archivo_simulado = SimpleUploadedFile("documento.pdf", b"contenido del archivo", content_type="application/pdf")

        response = self.client.post(url_editar, {
            "nombre": "Física Cuántica",
            "descripcion": "Contenido actualizado",
            "archivo": archivo_simulado,
        })

        self.assertEqual(response.status_code, 302)

        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.nombre, "Física Cuántica")
        self.assertEqual(self.contenido.descripcion, "Contenido actualizado")


    def test_eliminacion_de_contenido(self):
        url_eliminar = reverse("eliminar_enciclopedia", args=[self.contenido.id])
        response = self.client.post(url_eliminar)
        self.assertEqual(response.status_code, 302)  # Redirige tras eliminar
        self.assertFalse(Enciclopedia.objects.filter(id=self.contenido.id).exists())

#TC-003 ASOCIADO A TAREA: Controlar acceso de estudiantes
class FiltradoEnciclopediaPorCategoriaTest(TestCase):

    def setUp(self):
        # Crear grupo 'Fisica' y 'Quimica'
        grupo_fisica = Group.objects.create(name="Fisica")
        grupo_quimica = Group.objects.create(name="Quimica")

        # Crear usuario estudiante del grupo 'Fisica'
        self.user_fisico = User.objects.create_user(username="est_fisica", password="1234")
        self.user_fisico.groups.add(grupo_fisica)

        # Crear contenidos
        Enciclopedia.objects.create(
            nombre="Óptica",
            descripcion="Contenido de Física",
            categoria="Fisica"
        )

        Enciclopedia.objects.create(
            nombre="Moléculas",
            descripcion="Contenido de Química",
            categoria="Quimica"
        )

        self.client = Client()
        self.url = reverse("lista_enciclopedia")

    def test_estudiante_ve_solo_contenidos_de_su_categoria(self):
        self.client.login(username="est_fisica", password="1234")
        response = self.client.get(self.url)

        # Debe ver contenido de Física
        self.assertContains(response, "Óptica")

        # No debe ver contenido de Química
        self.assertNotContains(response, "Moléculas")

#TC-004: Crear formulario para subir contenidos

class SubidaContenidoTests(TestCase):

    def setUp(self):
        # Crear grupo docente y otro cualquiera
        grupo_matematica = Group.objects.create(name="Matematica")
        grupo_docente = Group.objects.create(name="docentes")

        # Crear usuario y agregarlo a ambos grupos
        self.user = User.objects.create_user(username="esteban", password="1234")
        self.user.groups.add(grupo_matematica, grupo_docente)

        # Loguear y preparar cliente
        self.client = Client()
        self.client.login(username="esteban", password="1234")

        # Ruta al formulario de subida
        self.url = reverse("subir_enciclopedia")

    def test_acceso_a_formulario(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subir nuevo archivo")

    def test_envio_formulario_valido(self):
        archivo_simulado = SimpleUploadedFile("archivo.pdf", b"contenido PDF", content_type="application/pdf")

        response = self.client.post(self.url, {
            "nombre": "Contenido de ejemplo",
            "descripcion": "Descripción del contenido",
            "archivo": archivo_simulado,
            "categoria": "Matematica"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enciclopedia.objects.filter(nombre="Contenido de ejemplo").exists())

#PRUEBAS UNITARIAS DEL MODELO ENCICLOPEDIA

class EnciclopediaModelTests(TestCase):

    def setUp(self):
        # Archivo simulado para campos obligatorios
        self.archivo_dummy = ContentFile(b"contenido", name="archivo.pdf")

    def test_nombre_es_unico(self):
        Enciclopedia.objects.create(nombre="Física", archivo=self.archivo_dummy)
        with self.assertRaises(IntegrityError):
            Enciclopedia.objects.create(nombre="Física", archivo=self.archivo_dummy)

    def test_descripcion_puede_ser_nula(self):
        obj = Enciclopedia.objects.create(nombre="Química", archivo=self.archivo_dummy)
        self.assertIsNone(obj.descripcion)

    def test_categoria_debe_ser_valida(self):
        obj = Enciclopedia(nombre="Biología", categoria="Invalida", archivo=self.archivo_dummy)
        with self.assertRaises(ValidationError):
            obj.full_clean()  # Valida los constraints declarados en el modelo

    def test_fecha_creacion_se_asigna_automaticamente(self):
        obj = Enciclopedia.objects.create(nombre="Álgebra", archivo=self.archivo_dummy)
        self.assertIsNotNone(obj.fecha_creacion)
        self.assertLessEqual(obj.fecha_creacion, timezone.now())