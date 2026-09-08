from django.test import TestCase
from django.urls import reverse


class CarritoCantidadTests(TestCase):
    def test_carrito_muestra_botones_de_cantidad(self):
        session = self.client.session
        session['carrito'] = {
            '1': {
                'id': 1,
                'nombre': 'Producto de prueba',
                'precio': 100,
                'cantidad': 2,
            }
        }
        session.save()

        response = self.client.get(reverse('carrito'))

        self.assertContains(response, 'btn-menos')
        self.assertContains(response, 'btn-mas')

    def test_actualizar_cantidad_a_cero_elimina_producto(self):
        session = self.client.session
        session['carrito'] = {
            '1': {
                'id': 1,
                'nombre': 'Producto de prueba',
                'precio': 100,
                'cantidad': 1,
            }
        }
        session.save()

        response = self.client.post(reverse('actualizar_cantidad_carrito', args=[1]), {'cantidad': 0})

        self.assertEqual(response.status_code, 302)
        self.assertNotIn('1', self.client.session.get('carrito', {}))
