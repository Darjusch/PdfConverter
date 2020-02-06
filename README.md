# PdfConverter

### SetUp:

    Go into the folder where you want to store the project.
    
    cd ../your/desired/location
    
    Clone the Repository:
    
    git clone https://bitbucket.org/bonialgroup/pdfconverter-2.0/src/master/
    
    Open the Project in your desired ide.
    
    Install virtual environment:
    
    pip3 install virtualenv
    
    Create a virtual environment:
    
    venv env
    
    Install the requirements: 
    
    pip install -r requirements.txt
    
    right click on main.py and press "Run 'main'"

### Functionality:


##### Load Pdf(s):

    Click on the FileIcon to load one or multiple Pdf's.    
    Or click on the Folder Icon to load a folder that contains Pdf's.

##### Pdf manipulation:


    -> SplitPage(s)
    
    Select one or multiple of the displayed pages and click the splitButton to cut the selected pages in half.
    
    -> SwapTwoPages
    
    Select two of the displayed pages and click the swapButton to switch the position of the selected pages.
    
    -> RotatePage(s)
    
    Select one or multiple of the displayed pages and click either the right or left rotationButton to rotated the pages for 90 degrees.
    
    -> CropAPage
    
    Select one of the displayed pages and click the cropButton, a new window will open which displays the selected page bigger.
    You can then select the area you want to crop.
    
    -> DeletePage(s)
    
    Select one or multiple of the displayed pages and click the deleteButton the pages will be deleted.
    
    -> Reset
    
    Click the reset button and all the pdfPages will be deleted.

