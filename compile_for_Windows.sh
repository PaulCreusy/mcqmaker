### Script to create a Windows executable version for MCQMaker ###

# Remove the export directory
rm -r MCQMaker_Windows

# Create a new one
mkdir MCQMaker_Windows

# Create the .exe
./venv/Scripts/pyinstaller.exe ./pyinstaller_config/windows.spec --noconfirm
mv dist/MCQMaker.exe MCQMaker_Windows

# Create the auto update script
./venv/Scripts/pyinstaller.exe ./pyinstaller_config/auto_update.spec --noconfirm
mv dist/Update.exe MCQMaker_Windows

# Copy the files to the directory
cp -r Templates MCQMaker_Windows/Templates
cp -r Instructions MCQMaker_Windows/Instructions
cp -r resources MCQMaker_Windows/resources
cp LICENSE MCQMaker_Windows/LICENSE
cp NOTICE MCQMaker_Windows/NOTICE
cp version.toml MCQMaker_Windows/version.toml
cp README.md MCQMaker_Windows/README.md

# Create the empty folders
cd MCQMaker_Windows
mkdir Classes
mkdir Export
mkdir "Question Database"
