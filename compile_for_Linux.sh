### Script to create a Windows executable version for MCQMaker ###

# Remove the export directory
rm -r MCQMaker_Linux

# Create a new one
mkdir MCQMaker_Linux

# Create the .exe
python -m PyInstaller ./pyinstaller_config/linux.spec --noconfirm
mv dist/MCQMaker MCQMaker_Linux

# Create the auto update script
python -m PyInstaller ./pyinstaller_config/auto_update.spec --noconfirm
mv dist/Update MCQMaker_Linux

# Copy the files to the directory
cp -r Templates MCQMaker_Linux/Templates
cp -r resources MCQMaker_Linux/resources
cp LICENSE MCQMaker_Linux/LICENSE
cp NOTICE MCQMaker_Linux/NOTICE
cp MCQMaker.kv MCQMaker_Linux/MCQMaker.kv
cp version.toml MCQMaker_Linux/version.toml
cp README.md MCQMaker_Linux/README.md

# Create the empty folders
cd MCQMaker_Linux
mkdir Classes
mkdir Export
mkdir "Question Database"
