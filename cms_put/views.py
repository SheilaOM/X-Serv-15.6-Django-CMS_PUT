from django.shortcuts import render
from django.http import HttpResponse
from cms_put.models import Pages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def barra(request):
    resp = "Las direcciones disponibles son: "
    lista_pages = Pages.objects.all()
    for page in lista_pages:
        resp += "<br>-/" + page.name + " --> " + page.page
    return HttpResponse(resp)


@csrf_exempt
def process(request, req):
    if request.method == "GET":
        try:
            page = Pages.objects.get(name=req)
            resp = "La página solicitada es /" + page.name + " -> " + page.page
        except Pages.DoesNotExist:
            resp = "La página introducida no está en la base de datos. Créala:"
            resp += "<form action='/" + req + "' method=POST>"
            resp += "Nombre: <input type='text' name='nombre'>"
            resp += "<br>Página: <input type='text' name='page'>"
            resp += "<input type='submit' value='Enviar'></form>"
    elif request.method == "POST":
        nombre = request.POST['nombre']
        page = request.POST['page']
        pagina = Pages(name=nombre, page=page)
        pagina.save()
        resp = "Has creado la página " + nombre
    elif request.method == "PUT":
        try:
            page = Pages.objects.get(name=req)
            resp = "Ya existe una página con ese nombre"
        except Pages.DoesNotExist:
            page = request.body
            pagina = Pages(name=req, page=page)
            pagina.save()
            resp = "Has creado la página " + req
    else:
        resp = "Error. Method not supported."

    return HttpResponse(resp)
