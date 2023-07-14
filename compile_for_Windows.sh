### Script to create a Windows executable version for MCQMaker ###

# Remove the export directory
rm -r MCQMaker_Windows

# Create a new one
mkdir MCQMaker_Windows

# Create the .exe
./venv/Scripts/pyinstaller.exe ./compilation.spec
mv dist/MCQMaker.exe MCQMaker_Windows

# Copy the files to the directory
cp -r Templates MCQMaker_Windows/Templates
cp -r Instructions MCQMaker_Windows/Instructions
cp -r data MCQMaker_Windows/data
cp -r resources MCQMaker_Windows/resources
cp LICENSE MCQMaker_Windows/LICENSE
cp NOTICE MCQMaker_Windows/NOTICE
cp README.pdf MCQMaker_Windows/README.pdf

# Create the empty folders
cd MCQMaker_Windows
mkdir Classes
mkdir Export
mkdir "Question Database"
