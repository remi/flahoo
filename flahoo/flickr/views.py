from django.template import Context, loader
from django.http import HttpResponse
from flahoo.flickr.models import Flickr

def index(request):
    if (request.GET.has_key('s')) :
        return photos(request)
    else :
        t = loader.get_template('accueil.html')
        c = Context({})
        return HttpResponse(t.render(c))    

def photos(request):
    f = Flickr()
    photos = f.get_photos_by_tag(request.GET['s'])
    newphotos = []
    
    for photo in photos:
        p = {
             'title' : photo('title'),
             'image'   : f.get_photo_image(photo),
             'url' : f.get_photo_url(photo)
        }
        newphotos.append(p)
    
    t = loader.get_template('photos.html')
    c = Context({
        'photos': newphotos,
    })

    return HttpResponse(t.render(c))