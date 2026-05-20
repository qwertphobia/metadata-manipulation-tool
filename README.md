**README**:
Metadata Manipulation Tool is a CLI tool that allows viewing, editing, and removing metadata. Metadata is information embedded in a file, basically data about data. It could contain certain information about you that is potentially sensitive. This tool allows the manipulation (including removal) of these embedded data. A file will be backed up called <filename.ext>_original to prevent file corruption and data loss.
*Example: If Alex sends a photo to Bob, Bob can find out Alice's location. Alice might not want to leak her location by accident.*

**Warning**:
Both exiftool and pyexiftool needs to be installed for the program to run. Pyexiftool can be installed using ```pip install PyExifTool``` .
Exiftool can be installed with package managers to 
Linux (apt): ```sudo apt install exiftool```
Linux (dnf): ```sudo dnf install perl-Image-ExifTool```
Linux (pacman): ```sudo pacman -S perl-image-exiftool```
Windows (winget): ```winget install -e --id OliverBetz.ExifTool```
Windows (chocolatey): ```choco install exiftool```
Macos (brew): ```brew install exiftool```
Manual Installation at exiftool.org. Please add exiftool to the environmental variables.

**Usage**:
Default:   <main.py> -f <filepath>
Quiet:     <main.py> -f <filepath> -q
View:      <main.py> -f <filepath> -v 
Edit:      <main.py> -f <filepath> -e 
Overwrite: <main.py> -f <filepath> -o
Help:      <main.py> -q
*Multiple Flags can be used (eg: <main.py> -f sample.jpg -qo).*

**Explanation**: 
-f or --file to declare the filepath for the file (required)
-q or --quiet to mute output
-v or --view to view metadata (no removal)
-e or --edit to edit metadata
-o or --overwrite to overwrite file if removal takes place
-h or --help to show options
*Some flags are incompatible with each other (eg: quiet is incompatible with edit).*


**Notice**:
Use this program at your own risk. Certain file formats (eg: adobe-dng) might have proprietary parts that are necessary for rendering. In the scenario you should not use the -o or --overwrite flag. 

**AI**:
Some AI is used in the production of this program, especially in the gui menu and the editing of the metadata.

```python3 ./main.py -f <filepath>``` for python script or ```./main.py -f <filepath>``` (the shebang/hashbang line only works for linux systems, as only #!/usr/bin/env python3 works there. i implemented that so i can develop easier without doing python3 repetively. this will be fixed.)  
```./main<ext> -f <filepath>``` for executable file
