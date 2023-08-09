### Script to create a Windows executable version for MCQMaker ###

# Remove the export directory
rm -r MCQMaker_Linux

# Create a new one
mkdir MCQMaker_Linux

# Create the .exe
python -m PyInstaller ./linux.spec --noconfirm
mv dist/MCQMaker MCQMaker_Linux

# Copy the files to the directory
cp -r Templates MCQMaker_Linux/Templates
cp -r Instructions MCQMaker_Linux/Instructions
cp -r data MCQMaker_Linux/data
cp -r resources MCQMaker_Linux/resources
cp LICENSE MCQMaker_Linux/LICENSE
cp NOTICE MCQMaker_Linux/NOTICE
cp version.toml MCQMaker_Linux/version.toml
cp README.md MCQMaker_Linux/README.md

# Create the empty folders
cd MCQMaker_Linux
mkdir Classes
mkdir Export
mkdir "Question Database"
