from django.http import HttpResponse
from django.views import View
from .models import NumberData as Db
import pika


class HomeView(View):

    @staticmethod
    def get(self):
        message = "Hi from test API"
        return HttpResponse(message)


class NumberView(View):

    def get(self, request, number1, number2):
        data = Db(number_one=number1, number_two=number2)
        data.save()
        pk = data.id
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        try:
            channel = connection.channel()
        except Exception as e:
            connection.close()
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
        channel.queue_declare(queue='q')
        data = [pk, number1, number2]
        channel.basic_publish(exchange='', routing_key='q', body=str(data))
        connection.close()

        return HttpResponse(pk)


class ReadView(View):

    def get(self, request, pk):

        content = {}
        try:
            value = Db.objects.get(id=pk)
            content['first'] = getattr(value, 'number_one')
            content['second'] = getattr(value, 'number_two')
            content['total'] = getattr(value, 'total')

        except Exception as e:
            if str(e) =="NumberData matching query does not exist.":
                response = HttpResponse("Invalid Identifier")
                response.status_code = 404
                return response
            else:
                return HttpResponse("something went wrong")
        if not content.get('total', None):
            response = HttpResponse("Please wait")
            response.status_code = 200
            return response

        response = HttpResponse(content.get('total', None))
        response.status_code = 200
        return response


