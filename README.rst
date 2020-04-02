upload_file_sharepoint
========================
Uploads a file to Sharepoint from Linux. Because why would you want to actually use sharepoint?

Requires shareplum install

This will upload a file to SharePoint/OneDrive authenticating using your username and password. The Password prompt will hide your password typing. 

.. warning ::
  
  I'm not a security expert, I cannot say this is secure because I just don't know.

  
Required arguments:
-------------------

``-f, -file``
  File to upload. There is one requirement that the file you are uploading needs to be in the directory you run this script from. E.g. you want to upload ``test.txt``. You need to make sure you run this from the directory that ``test.txt`` is in. Don't pass ``some/dir/test.txt``. 
  
``-u, -user``
  User name you use for Sharepoint login. Pass word is asked for during upload

``-b, -base``
  Sharepoint Base URL. This is usually something like ``https://<companyname>.sharepoint.com/``

``-s, -site``
  Sharepoint site name. Usually the project you are working on

``-d, -doclib``
  Sharepoint doclibrary. This is usually ``Shared%20Documents/Datasheets`` or something along those lines. If you go to the desired directory in a web browser, you can deduce this from the url. The web browser will put in some extra characters, but they are not required for the upload.
  
**This tool can only upload a file to an existing directory in SharePoint**

