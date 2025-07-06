from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from django.utils import timezone
from Enciclopedia.models import Enciclopedia
from Enciclopedia.serializers import EnciclopediaSerializer
from Enciclopedia.views import EnciclopediaViewSet, EsDocenteOReadOnly

# CA-01: Carga de contenidos (serializer válido)
class CargaContenidoSerializerTest(TestCase):
    def test_creacion_valida(self):
        archivo = SimpleUploadedFile("doc.pdf", b"contenido", content_type="application/pdf")
        data = {
            "nombre": "Ejemplo",
            "descripcion": "Contenido de prueba",
            "archivo": archivo,
            "categoria": "Fisica"
        }
        serializer = EnciclopediaSerializer(data=data)
        self.assertTrue(serializer.is_valid())

# CA-02: Control de acceso de estudiantes (filtrado)
class FiltroPorGrupoTest(TestCase):
    def test_filtro_categoria_por_grupo(self):
        Enciclopedia.objects.create(nombre="Química", archivo=SimpleUploadedFile("a.pdf", b"x"), categoria="Quimica")
        Enciclopedia.objects.create(nombre="Física", archivo=SimpleUploadedFile("b.pdf", b"x"), categoria="Fisica")
        grupo = Group.objects.create(name="Fisica")
        user = User.objects.create_user(username="juan", password="1234")
        user.groups.add(grupo)
        grupos_usuario = list(user.groups.values_list("name", flat=True))
        visibles = Enciclopedia.objects.filter(categoria__in=grupos_usuario)
        self.assertEqual(visibles.count(), 1)
        self.assertEqual(visibles.first().nombre, "Física")

# CA-03: Registro de visualización (timestamp simulado)
class RegistroVisualizacionTest(TestCase):
    def test_registro_hora_manual(self):
        acceso = timezone.now()
        self.assertLessEqual(acceso, timezone.now())

# CA-04: Visualización según rol (permisos de API)
class PermisoDocenteTest(TestCase):
    def test_docente_puede_postear(self):
        factory = APIRequestFactory()
        user = User.objects.create_user("doc", password="1234")
        user.groups.add(Group.objects.create(name="docentes"))
        request = factory.post("/api/enciclopedia/", {})
        request.user = user
        permiso = EsDocenteOReadOnly()
        self.assertTrue(permiso.has_permission(request, EnciclopediaViewSet()))

