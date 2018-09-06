from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
# from django.shortcuts import render

# Create your views here.
@api_view(['POST'])
@parser_classes((FormParser, MultiPartParser, ))
def upload(request):
  # """
  # Currently supports uploading one file
  # """
  # repositoryFullName = request.data['repository'] # Full name means :owner/:repo_name
  # branch = request.data['branch']
  # path = request.data['path']
  # file = request.data['files']
  # username = request.session['username'].split('@')[0]
  # userBasePathStr = os.path.join(settings.MEDIA_ROOT, 'repos', repositoryFullName, branch, username)
  # # TODO
  # uploadedFilePath = pathlib.Path(userBasePathStr) / path / file.name
  # fileContent = file.read()
  # with open(str(uploadedFilePath), 'wb') as fo:
  #   fo.write(fileContent)
  # newFile = {}
  # newFile['path'] = str(uploadedFilePath)
  # newFile['path'] = newFile['path'].replace(userBasePathStr, '')
  # newFile['path'] = newFile['path'][1:] # To remove the leading /
  # newFile['name'] = os.path.basename(newFile['path'])
  # newFile['nodes'] = []
  # newFile['added'] = True
  # newFile['modified'] = False
  # newFile['sha'] = None
  # newFile['url'] = None
  # newFile['type'] = 'blob'
  # newFile['mode'] = '100644'
  # # To match encoding / decoding scheme to blobs through GitHub API
  # newFile['originalContent'] = base64.b64encode(fileContent).decode('utf-8')
  # # The if block below didn't work for uploaded text files
  # #   (worked for existing text, binary, and uploaded binary, though)
  # # if _isBinary((newFile['name'])):
  # #   newFile['originalContent'] = base64.b64encode(fileContent).decode('utf-8')
  # # else:
  # #   newFile['originalContent'] = fileContent.decode('utf-8')
  # newFile['size'] = os.stat(str(uploadedFilePath)).st_size
  # return Response({
  #   'res': uploadedFilePath.exists(),
  #   'createdFiles': [newFile],
  #   'size': newFile['size']
  # })
  return Response({
    'res': 'drf working',
    'data': request.data
  })
