#!/usr/bin/python36

import os
import sys
import argparse   as ap
import getpass
import requests
from shareplum import Office365

username        = getpass.getuser() + "@wavious.com"
spfile          = ''
sp_base_path    = 'https://wavious.sharepoint.com/'
sp_site_name    = ''
sp_doc_library  = ''


##########################
def get_sp_pass():
  try: 
      p = getpass.getpass(prompt='SharePoint Password:') 
  except Exception as error: 
      print('ERROR with getting password from user', error) 
      sys.exit(1)
  else: 
      return p 


##########################
def upload_it():
  
  password = get_sp_pass()
  site_name = sp_site_name
  base_path = sp_base_path
  doc_library = sp_doc_library
  
  print("Trying to upload File: {} as user: {}".format(spfile, username))


  # Obtain auth cookie
  authcookie = Office365(base_path, username=username, password=password).GetCookies()
  session = requests.Session()
  session.cookies = authcookie
  session.headers.update({'user-agent': 'python_bite/v1'})
  session.headers.update({'accept': 'application/json;odata=verbose'})

  # dirty workaround.... I'm getting the X-RequestDigest from the first failed call
  session.headers.update({'X-RequestDigest': 'FormDigestValue'})
  response = session.post( url=base_path + "/sites/" + site_name + "/_api/web/GetFolderByServerRelativeUrl('" + doc_library + "')/Files/add(url='a.txt',overwrite=true)",
                           data="")
  session.headers.update({'X-RequestDigest': response.headers['X-RequestDigest']})

  # perform the actual upload
  with open( spfile, 'rb') as file_input:
      try: 
          response = session.post( 
              url=base_path + "/sites/" + site_name + "/_api/web/GetFolderByServerRelativeUrl('" + doc_library + "')/Files/add(url='" 
              + spfile + "',overwrite=true)",
              data=file_input)
      except Exception as err: 
          print("Some error occurred: " + str(err))


##########################
def get_args():
  parser = ap.ArgumentParser(description="A tool for uploading a file to Sharepoint. Because sharepoint..")
  parser.add_argument("-f", "-file",        help="(Required) File to upload", type=str)
  parser.add_argument("-u", "-user",        help="(Optional) Username you use to log into sharepoint ($user@wavious.com is default). Your pass word will be asked for but not saved", type=str)
  parser.add_argument("-b", "-base",        help="(Optional) Sharepoint base url (https://wavious.sharepoint.com/ is default)", type=str)
  parser.add_argument("-s", "-site",        help="(Required) Sharepoint site name (i.e. WCL/WPM)", type=str)
  parser.add_argument("-d", "-doclib",      help="(Required) Sharepoint doc library (i.e. Shared%20Documents/Diagrams/)", type=str)
  
  args = parser.parse_args()
  
  if args.f:
    global spfile
    spfile = args.f
  else:
    print("Error: A file to upload was not specified!")
    parser.print_help(sys.stderr)
    sys.exit(1)
  
  if args.u:
    global username
    username = args.u
  
  if args.b:
    global sp_base_path
    sp_base_path = args.b
  
  if args.s:
    global sp_site_name
    sp_site_name = args.s
  else:
    print("Error: A site name was not specified!")
    parser.print_help(sys.stderr)
    sys.exit(1)
    
  if args.d:
    global sp_doc_library
    sp_doc_library = args.d
  else:
    print("Error: A doc library was not specified!")
    parser.print_help(sys.stderr)
    sys.exit(1)
  
############################
# Run
############################
get_args()
upload_it()
