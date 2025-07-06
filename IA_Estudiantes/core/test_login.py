from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class LoginTests(TestCase):
    

    # CA-01: Ingreso exitoso con credenciales válidas
    def test_login_valido_redirecciona(self):
        response = self.client.post(reverse('login'), {
            'username': 'Pedro',
            'password': 'p3dr0123'
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras login
        self.assertTrue(response.url.startswith('/'))  # Asegura redirección
    
    # CA-02: Mensaje de error con credenciales inválidas
    def test_login_invalido_muestra_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'Pedro',
            'password': 'malacontra'
        })
        self.assertEqual(response.status_code, 200)  # No redirige
        self.assertContains(response, "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.")  # Mensaje estándar de Django

    # CA-03: Validación de campos vacíos
    def test_login_con_campos_vacios(self):
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)


    # CA-04: Acceso restringido según rol
    def test_usuario_redirigido_a_vista_por_rol(self):
        docente = User.objects.create_user(username='profe', password='pass123')
        group = Group.objects.create(name='Docentes')
        docente.groups.add(group)

        self.client.login(username='profe', password='pass123')
        
        response = self.client.get(reverse('rendimiento_usuario'))  # ✅ vista existente

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "rendimiento")  # ajusta si querís un texto más exacto