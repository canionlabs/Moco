from django.test import TestCase

class ViewTest(TestCase):
    TEXT = "Sent successfully"

    def test_send_whatsapp(self):
        response = self.client.post('message/whatsapp/',
            {
                'to': '99223783',
                'message': 'testando aplicação'
            }
        )

        self.assertContains(response, TEXT, count=1 , status_code=200)
    
    def test_send_message(self):
        response = self.client.post('message/sms/',
            {
                'to': '99223783',
                'message': 'testando aplicação'
            }
        )

        self.assertContains(response, TEXT, count=1 , status_code=200)