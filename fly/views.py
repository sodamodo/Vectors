from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import os
from fly.models import Document
from fly.forms import DocumentForm
from gps import runCode
from Vectors.settings import BASE_DIR
from zipfile import ZipFile
from django.core.servers.basehttp import FileWrapper

def upload(request):
    # Handle file upload
    velocity = 0
    acceleration = 0
    force = 0
    coordinates = 0
    trajectory = 0
    wrongfiletag = ""
    print request.POST
    if request.method == 'POST':
        print("Valid!")
        newdoc = Document(docfile=request.FILES['docfile'])
        newdoc.save()
        filetype = newdoc.docfile.name.split(".")[-1]
        print filetype
        if filetype == "txt":
            fileVar = 1
        elif filetype == "xlsx":
            fileVar = 3
        else:
            wrongfiletag = "Sorry you can only upload Excel files or Text files"
            return render(request, 'upload.html', {'wrongfile': wrongfiletag})


        listo = request.POST.getlist('checkboxes', 0)


        if 'velocity' in listo:
            velocity = 1
        if 'acceleration' in listo:
            acceleration = 1
        if 'force' in listo:
            force = 1
        if 'coordinates' in listo:
            coordinates = 1
        if 'trajectory' in listo:
            trajectory = 5
        #radios is the POST key for units
        if 'radios' in listo:
            units = 1
        else:
            units = 0
        mass = float(request.POST['mass'])
        input_path = newdoc.docfile.path
        output_path = ""
        runCode(input_path, output_path, mass, trajectory, velocity, coordinates, acceleration, units, force, fileVar)



        # kml_data = open(os.path.join(BASE_DIR, 'GoogleEarth.kml'), "rb")
        zf = ZipFile('processed.zip', mode='w')

        print 'adding files'
        zf.write('GoogleEarth.kml')
        if coordinates == 1:
            zf.write('Coordinates.txt')
        # zf.write('GoogleEarth.kml')


        zf.close()

        downloadfile = open('processed.zip', 'rb')


        response = HttpResponse(FileWrapper(downloadfile), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=processed.zip'  # make custom download name
        return response
            # return HttpResponseRedirect(reverse('fly.views.upload'))
    else:
        return render(request, 'upload.html', {'wrongfile': wrongfiletag})

