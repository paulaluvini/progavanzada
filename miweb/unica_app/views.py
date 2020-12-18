from django.shortcuts import render

# Create your views here.
from django_pandas.io import read_frame
from django.http import HttpResponse
from .apps import PredictorConfig
from django.http import JsonResponse
from rest_framework.views import APIView
from django.template import loader
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import json
from .models import EmailHistorico
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmailHistoricoserializer
from rest_framework import generics
from .models import Quota
from .serializers import QuotaSerializer


#Metodo para la prediccion de spam or ham.
#Se tiene en cuenta la consulta de quota disponible.
#Si corresponde se reduce la quota, como asi tambien aumentan los procesados.
#Se guarda el mail consultado para luego poder devolver el historico.
class call_model(APIView):
    serializer = QuotaSerializer
    def post(self,request):
    #Obtengo el id de usuario, para filtrar la quota disponible y los procesados
            user_id = self.request.user
            #Obtengo el reg de quota filtrado por el usuario
            cond = Quota.objects.filter(user_id=user_id)
            if len(cond) == 0:
                disponibles = 0
            else:
                #Obtengo el valor de la quota disponible
                instance = cond.values('disponibles')[0]
                disponibles = instance['disponibles']
                #Obtengo el valor de los procesados
                instance = cond.values('procesados')[0]
                procesados = instance['procesados']
                #Si queda quota disponible
            if disponibles > 0:
                #Obtengo el json completo
                email =  request.data
                #Obtengo el campo text del json
                f = request.data.get("text")
                #Obtengo el id del usuario
                user = request.user
                #Convierto en string el json
                email = str(email)
                # vectorize email
                vector = PredictorConfig.vectorizer.transform([email])
                # predict based on vector
                prediction =int(PredictorConfig.regressor.predict(vector)[0])
                #Defino el valor del output
                if prediction == 0:
                    result = 'HAM'
                else:
                    result = 'SPAM'
                    # build response
                    response = {'result': result}
                    eh = EmailHistorico.objects.create(text = f , user = request.user, result= result)

                #Quito disponibles
                disponibles = disponibles -1
                #Aumento los procesados
                procesados = procesados +1
                #Hago el update del registro de quota
                Quota.objects.filter(user_id=user_id).update(disponibles = disponibles, procesados = procesados)
                #Rama false del if, si no queda quota disponible, arrojo la respuesta de que no le queda quota
            else:
                response = {'status':"fail",'message':'No quota left'}
            return Response(response)

#Metodo para consultar la quota disponible.
class quota_info(generics.ListAPIView):
    serializer_class = QuotaSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
#Obtengo el usuario que esta generando la consulta.
        user = self.request.user
#Devuelvo el objeto Quota filtrado por el usuario que genera la consulta.
#El serializer ya devuelve la informacion en el formato solicitado.
        return Quota.objects.filter(user_id=user)

#Metodo no solicitado. Es auxiliar para poder generar una quota a los usuarios.
#Si no existe en la tabla de quota el id de usuario, se crea un nuevo registro, si no se actualiza el que ya existe.
class quotaagregate(APIView):
    def post(self,request):
#Obtengo la cantidad de quota que se le quiere agregar o crear al usuario
            disponibles = request.data.get("disponibles")
#Obtengo el user_id del usuario al que le quiero agregar o crear la quota
            user_id = request.data.get("user_id")
#Me fijo si el usuario ya tiene un registro en la tabla de quota
            response = Quota.objects.filter(user_id=user_id)
            if len(response) == 0:
#Si no tiene registro, entonces lo creo
                qr = Quota.objects.create(user_id=user_id, disponibles = disponibles)
            else:
#Si tiene registro, entonces lo actualizo
                Quota.objects.filter(user_id=user_id).update(disponibles = disponibles)
            return Response()


#Metodo para visualizar el historico de los mails procesados
class consultList(generics.ListAPIView):
    serializer_class = EmailHistoricoserializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
#Parametro que indica la cantidad de mails que quiero visualizar
        n =int(self.request.GET.get('n'))
#Usuario que esta solicitando el historico
        user = self.request.user
#Obtengo todos los mails procesados por el usuario que hace la peticion
        queryset = EmailHistorico.objects.filter(user_id=user)
#Genero las cotas para luego filtrar los mails que visualizo.
        last = int(len(queryset)+1)
        first = int(last - n - 1)
        queryset_rev = queryset[first:last]
        return queryset_rev

#Agrego esta view para streamlit
class database(generics.ListAPIView):
    serializer_class = EmailHistoricoserializer
    def get_queryset(self):
        queryset = EmailHistorico.objects.filter()
        return queryset


#Test
class test_if_logged(APIView):
    def get(self, request):
        # en request.user tiene el objeto user de quien hizo el pedido
        return Response({'status':'ok!'})
