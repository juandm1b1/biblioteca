import datetime
from datetime import timedelta
from apps.libro.models import Reserva


""" Middleware personalizado para validar las Reservas de los libros que ha hecho cada Usuario
    así como validar si está ya se venció para quitar la reserva"""

class ValidarReservasMiddleware:    
    def __init__(self, get_response):        
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):        
        if request.user.is_authenticated:
            fecha_actual = datetime.date.today() # Si en el modelo es 'DateField', aca debe ser 'date', si es 'DateTimeField', acá es 'datetime'"
            reservas = Reserva.objects.filter(estado = True, usuario = request.user)
            for reserva in reservas:                
                fecha_vencimiento = reserva.fecha_creacion + timedelta(days=reserva.cantidad_dias)                
                if fecha_actual >= fecha_vencimiento:
                    reserva.estado = False
                    reserva.save()

            # Activa los libros cuyas reservas           
            # for reserva in reservas:                
            #     if (datetime.date.today().day - reserva.fecha_creacion.day) >= reserva.cantidad_dias:
            #         reserva.estado = False
            #         reserva.save()
            #         libro = reserva.libro
            #         libro.estado = True
            #         libro.cantidad += 1
            #         libro.save()
                     
            

        