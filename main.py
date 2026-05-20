#!/usr/bin/env python3
import json
from pathlib import Path
import exiftool # needs to be installed
import argparse
import mimetypes
import time

# Initialization
mimetypes.init([]) # This guarantees interoperability because the Windows Registry's MIME type mappings are different (imcomplete), leading to incomplete results. 
parser = argparse.ArgumentParser(description="Metadata Manipulation Program (mmt). It can show and remove metadata from a file or a directory.")
parser.add_argument("-f", "--file", required=True, help="filepath to the target file")
parser.add_argument("-q", "--quiet", action='store_true', help="remove file metadata (without showing)")
parser.add_argument("-v", "--view", action='store_true', help="view image metadata")
parser.add_argument("-e", "--edit", action='store_true', help="metadata editing mode")
parser.add_argument("-o", "--overwrite", action='store_true', help="overwrites file (without backup) if there is a change in file metadata")
args = parser.parse_args()  

# Check if exiftool is installed and in system PATH
try: 
    with exiftool.ExifToolHelper() as et:
        pass
except:
    print("Exiftool is not installed, or not in PATH.\nDetailed instructions in README.")
# Functions 
def obtain_mimetype_from_file(filepath):
    p = Path(filepath)
    if not p.exists():
        print("The file doesn't exist or is not found")
        exit()
    mime_type, _ = mimetypes.guess_type(str(p))
    return mime_type or "application/octet-stream"
        
def getmeta(printmeta=False):
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(files)       
        metadata_pretty = json.dumps(metadata[0], indent=4, ensure_ascii=False)
        if printmeta == True:
            print(metadata_pretty)
def removemeta(): # AI is used in this function to replace my original failing design of a list comprehension
    with exiftool.ExifToolHelper() as et:
        # Start with the core command
        cmd = ["-all="]

        # Add the overwrite flag only if the user requested it
        if args.overwrite:
            cmd.append("-overwrite_original")

        # Finally add the file path
        cmd.append(str(filepath))

        # Execute the command – unpack the list so each item is a separate argument
        et.execute(*cmd)
# Gather mimetype and configure modes to show metadata or remove metadata in the format in [show, remove]. 1 for true, 0 for false.
mime = obtain_mimetype_from_file(args.file) 
# default is show and remove, so if that is required then no additional flags should be used.
if args.edit:
    flags = [0,0]
elif args.view:
    flags = [1,0]
elif args.quiet:
    flags = [0,1] # edit mode doesn't have show or remove
elif (not args.quiet) and (not args.view) and (not args.edit): # Redunant, but it works, so I have no need to optimize it for now
    flags = [1,1] # Default setting
else:
    print("Only one option can be chosen between quiet, view, and edit.")

filepath = Path(args.file).resolve()

files = [str(filepath)]
if flags == [1,1]: # default (removal)
    removemeta()
    print(f"File: {filepath}    Mime: {mime}")  
    print("File metadata successfully removed!")
elif flags == [1,0]: # view
    getmeta(True)
    #mime.split('/')[0] to get type
elif flags == [0,1]: # quiet
    # Removal
    removemeta()
else: # AI used to enhance my original design here
    # Edit Mode
    import tkinter as tk
    from metagui import Menu
    import subprocess

    root = tk.Tk()
    root.geometry("800x800")
    
    # Fetch initial metadata
    with exiftool.ExifToolHelper() as et:
        initial_metadata = et.get_metadata(files)[0]
    
    # Pass the JSON string to the GUI
    editmenu = Menu(root, json.dumps(initial_metadata, indent=4, ensure_ascii=False)) 
    
    root.mainloop()
    
    # Check if data was saved
    if editmenu.result_data:
        print("Processing metadata changes...")
        
        with exiftool.ExifToolHelper() as et:
            cmd_args = []
            
            # Add overwrite flag if requested
            if args.overwrite:
                cmd_args.append("-overwrite_original")

            changes_made = False
            
            # Iterate through the user's edited data
            for key, value in editmenu.result_data.items():
                # 1. SKIP System/Protected Keys
                protected_keys = [
                    'SourceFile', 'FileName', 'Directory', 'FileSize', 'FileType', 
                    'MIMEType', 'ExifToolVersion', 'FileModifyDate', 'FileCreateDate',
                    'ImageWidth', 'ImageHeight', 'PixelXDimension', 'PixelYDimension'
                ]
                if key in protected_keys or key.startswith('SourceFile'):
                    continue

                # 2. SKIP Complex Structures
                if isinstance(value, (dict, list)):
                    print(f"SKIPPED (Complex Structure): {key}")
                    continue

                # 3. Handle Deletion
                if value is None:
                    cmd_args.append(f"-{key}=")
                    changes_made = True
                else:
                    # 4. Safe String Conversion
                    if not isinstance(value, (str, int, float, bool)):
                        print(f"SKIPPED (Invalid Type): {key}")
                        continue
                    
                    str_value = str(value)
                    cmd_args.append(f"-{key}={str_value}")
                    changes_made = True
            cmd_args.append(str(filepath))
          
            # Execute only if there are changes
            if changes_made and len(cmd_args) > 1:
                
                try:
                    result = subprocess.run(
                        ['exiftool'] + cmd_args,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        print(f"EXIFTOOL ERROR (Exit Code {result.returncode}):")
                        print(result.stderr) # Print the specific error message
                        print("File NOT modified.")
                    else:
                        print("Metadata update successful.")
                        # Verify
                        new_meta = et.get_metadata(files)[0]
                        print(f"Verification: File updated. Total tags: {len(new_meta)}")
                        
                except FileNotFoundError:
                    print("ERROR: 'exiftool' command not found. Is it installed and in PATH?")
                except Exception as e:
                    print(f"Unexpected error during execution: {e}")
            else:
                print("No valid changes to apply.")
    else:
        print("No changes were saved or JSON was invalid.")
