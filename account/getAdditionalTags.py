from .models import UploadedDocuments

def getadditionaltag(addtags, filename):
    updaterec = UploadedDocuments.objects.get(newfilename = filename)
    updaterec.tags = updaterec.tags+","+addtags
    updaterec.save()
