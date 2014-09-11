# ArcGIS Online Thumbnail Builder Server Backend
## An Esri SE Prototype

See the live demo: http://nwdemo1.esri.com/ThumbnailBuilder.

Here is a sample of the actually Geoprocessing Service:
http://nwdemo1.esri.com/arcgis/rest/services/GP/GenerateThumb2/GPServer

This is a python script that is published as a Geoprocessing Service to an Esri ArcGIS Server 10.2+.  This is the backend that performs the merging of images and text to create a new thumbnail for ArcGIS Online users.

### Basic Usage

TODO

### Front End UI Component

The front end web application that will work with this backend service can be found here:
https://github.com/sirws/ThumbnailBuilder

### Installing Locally

You will need to install PILLOW on your server (and ArcGIS Desktop) if you want to run this component from ArcMap.
PILLOW can be downloaded here:
https://pypi.python.org/pypi/Pillow/2.5.3

Specifically, you will want the correct build for your server.

For ArcGIS Server on Windows, you will want 2.5.3 for Python 2.7 64-bit
https://pypi.python.org/packages/2.7/P/Pillow/Pillow-2.5.3.win-amd64-py2.7.exe#md5=33c3a581ff1538b4f79b4651084090c8

### Software Required

ArcGIS Server 10.2+
ArcMap 10.2+
