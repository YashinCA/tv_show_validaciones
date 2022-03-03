from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .models import Tvshow, Network
from datetime import datetime, timedelta
from django.contrib import messages


def redirigir(request):
    return redirect('/shows')


def index(request):
    context = {
        'alltvshows': Tvshow.objects.all(),
        'allnetworks': Network.objects.all(),
    }
    return render(request, 'app/index.html', context)


def newtvshow(request):
    time_delta = datetime.today()-timedelta(1)
    date_yesterday = time_delta.strftime('%Y-%m-%d')
    contexto = {
        'networks': Network.objects.all(),
        "date_today": date_yesterday
    }
    return render(request, 'app/formulario_new.html', contexto)


def createtvshow(request):
    print(request.POST)
    if request.method == 'POST':
        error = Tvshow.objects.basic_validator(request.POST)
        if len(error) > 0:
            request.session['title'] = request.POST['title']
            time_delta = datetime.today()-timedelta(1)
            date_yesterday = time_delta.strftime('%Y-%m-%d')
            contexto = {
                'networks': Network.objects.all(),
                "date_today": date_yesterday
            }
            for valor in error.values():
                messages.error(request, valor)
            return render(request, 'app/formulario_new.html', contexto)

        else:
            print(request.POST)
            if (request.POST['network'] != 'otro'):
                if Network.objects.get(id=request.POST['network']):
                    this_network = Network.objects.get(
                        id=request.POST['network'])
                    tv_show = Tvshow.objects.create(title=request.POST['title'], network=this_network,
                                                    releasedate=request.POST['releasedate'], description=request.POST['description'])
                    showid = tv_show.id
                    return redirect(f"/shows/{showid}")
                else:
                    return render(request, 'app/formulario_new.html')
            else:
                create = Tvshow.objects.create(title=request.POST['title'], network=Network.objects.create(
                    name=request.POST['network-new']), releasedate=request.POST['releasedate'], description=request.POST['description'])
                showid = create.id
                return redirect(f"/shows/{showid}")


def details(request, id):
    detalle = Tvshow.objects.get(id=id)
    context = {
        "detailstvshow": detalle,
    }
    return render(request, 'app/detalle.html', context)


def edit(request, id):
    if request.method == 'GET':
        editar = Tvshow.objects.get(id=id)
        network_defect_name = editar.network.name
        network_defect_id = editar.network.id
        networks = Network.objects.all().exclude(name=network_defect_name)
        release_date = editar.releasedate
        release_date = release_date.strftime('%Y-%m-%d')
        time_delta = datetime.today()-timedelta(1)
        date_yesterday = time_delta.strftime('%Y-%m-%d')

        print(release_date)
        context = {
            "edit": editar,
            "release_date": release_date,
            "network_default_name": network_defect_name,
            "network_default_id": network_defect_id,
            "networks": networks,
            "date_today": date_yesterday
        }
    return render(request, 'app/formulario_edit.html', context)


def update(request, id):
    print(request.POST)

    if request.method == 'POST':
        editar = Tvshow.objects.get(id=id)
        network_defect_name = editar.network.name
        network_defect_id = editar.network.id
        networks = Network.objects.all().exclude(name=network_defect_name)
        release_date = editar.releasedate
        release_date = release_date.strftime('%Y-%m-%d')
        time_delta = datetime.today()-timedelta(1)
        date_yesterday = time_delta.strftime('%Y-%m-%d')
        error = Tvshow.objects.basic_validator(request.POST)
        if len(error) > 0:

            for valor in error.values():
                messages.error(request, valor)

            # editar = Tvshow.objects.get(id=id)
            # network_defect_name = editar.network.name
            # network_defect_id = editar.network.id
            # networks = Network.objects.all().exclude(name=network_defect_name)
            # release_date = editar.releasedate
            # release_date = release_date.strftime('%Y-%m-%d')
            # time_delta = datetime.today()-timedelta(1)
            # date_yesterday = time_delta.strftime('%Y-%m-%d')
            context = {
                "edit": editar,
                "release_date": release_date,
                "network_default_name": network_defect_name,
                "network_default_id": network_defect_id,
                "networks": networks,
                "date_today": date_yesterday
            }
            return render(request, 'app/formulario_edit.html', context)
        else:
            es_unico = Tvshow.objects.filter(title=request.POST['title'])
            if es_unico.count() < 1:
                update_tvshow = Tvshow.objects.get(id=id)
                network_default = Network.objects.get(
                    id=update_tvshow.network.id)
                network_post = Network.objects.get(id=request.POST['network'])
                if update_tvshow.network.id == network_post:
                    update_tvshow.title = request.POST['title']
                    update_tvshow.description = request.POST['description']
                    update_tvshow.releasedate = request.POST['releasedate']
                    update_tvshow.save()
                    print(network_default)
                else:
                    network_post.tvshows.add(update_tvshow)
                    update_tvshow.title = request.POST['title']
                    update_tvshow.description = request.POST['description']
                    update_tvshow.releasedate = request.POST['releasedate']
                    update_tvshow.save()
                    return redirect(f"/shows/{id}")
            else:
                newtitle = request.POST['title']
                context = {
                    "edit": editar,
                    "release_date": release_date,
                    "network_default_name": network_defect_name,
                    "network_default_id": network_defect_id,
                    "networks": networks,
                    "date_today": date_yesterday
                }
                messages.error(request, f'El TvShow {newtitle} ya existe')
                return render(request, 'app/formulario_edit.html', context)


def destroy(request, id):
    print(request.POST)
    deleteshow = Tvshow.objects.get(id=id)
    deleteshow.delete()
    return redirect("/shows")
