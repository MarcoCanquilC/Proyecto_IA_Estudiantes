from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from Enciclopedia.models import Enciclopedia
from django.core.files.uploadedfile import SimpleUploadedFile

# TC-001 ASOCIADO A TAREA: Verificar que los estudiantes puedan ver contenidos de la enciclopedia
class EnciclopediaVistaTests(TestCase):

    def setUp(self):
        # Crear grupos
        self.docentes = Group.objects.create(name="docentes")
        self.estudiantes = Group.objects.create(name="estudiantes")

        # Crear usuarios
        self.user_estudiante = User.objects.create_user(username="estudiante", password="1234")
        self.user_estudiante.groups.add(self.estudiantes)

        self.user_docente = User.objects.create_user(username="docente", password="1234")
        self.user_docente.groups.add(self.docentes)

        # Crear contenido de enciclopedia
        Enciclopedia.objects.create(nombre="Álgebra", descripcion="Contenido de prueba")

        self.client = Client()
        self.url = reverse("lista_enciclopedia")  # Asegúrate que esta sea tu URL correcta

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

    from django.core.files.uploadedfile import SimpleUploadedFile

    from django.core.files.uploadedfile import SimpleUploadedFile

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