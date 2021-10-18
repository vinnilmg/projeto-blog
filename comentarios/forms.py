from django.forms import ModelForm
from .models import Comentario
import requests


class FormComentario(ModelForm):
    def clean(self):
        raw_data = self.data
        recaptcha = raw_data.get('g-recaptcha-response')

        # verificação do captcha
        captcha_req_json = {
                'secret': '6Len_dgcAAAAAOuXg9gxChlQB-ZVeYdVcuBdb8_y',
                'response': recaptcha
            }
        recaptcha_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_req_json).json()
        # print(recaptcha_response)

        if not recaptcha_response.get('success'):
            self.add_error(
                'comentario',
                'Desculpe Mr. Robot, ocorreu um erro no captcha.'
            )

        # pegando valors do form
        cleaned_data = self.cleaned_data

        nome = cleaned_data.get('nome_comentario')
        email = cleaned_data.get('email_comentario')
        comentario = cleaned_data.get('comentario')

        if len(nome) < 5:
            self.add_error(
                'nome_comentario',
                'Nome precisa ter mais que 5 caracteres.'
            )

    class Meta:
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')
