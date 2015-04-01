from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from fly.models import Document
from fly.forms import DocumentForm
from gps import runCode



def upload(request):
    # Handle file upload
    velocity = 0
    acceleration = 0
    force = 0
    coordinates = 0
    trajectory = 0
    wrongfiletag = ""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
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
                form = DocumentForm()
                documents = Document.objects.all()
                return render(
                        request,
                        'upload.html',
                        {'documents': documents, 'form': form, 'wrongfile': wrongfiletag},
                        )
            if request.POST.get('velocity', 0) == 'on':
                velocity = 1
            if request.POST.get('acceleration', 0) == 'on':
                acceleration = 1
            if request.POST.get('force', 0) == 'on':
                force = 1
            if request.POST.get('coordinates', 0) == 'on':
                coordinates = 1
            if request.POST.get('trajectory', 0) == 'on':
                trajectory = 5
            if request.POST.get('units', 0) == '1':
                units = 1
            else:
                units = 0
            mass = float(request.POST['mass'])
            input_path = newdoc.docfile.path
            output_path = ""
            fileVar = 1 # Need to write in the autocheck later
            runCode(input_path, output_path, mass, trajectory, velocity, coordinates, acceleration, units, force, fileVar)
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('fly.views.upload'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'upload.html',
        {'documents': documents, 'form': form},
    )