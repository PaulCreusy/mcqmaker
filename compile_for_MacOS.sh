### Script to create a Windows executable version for MCQMaker ###

# Remove the export directory
rm -r MCQMaker_MacOS

# Create a new one
mkdir MCQMaker_MacOS

# Create the .exe
python3.11 -m PyInstaller ./pyinstaller_config/macos.spec --noconfirm
mv dist/MCQMaker.app MCQMaker_MacOS

# Create the auto update script
python3.11 -m PyInstaller ./pyinstaller_config/auto_update.spec --noconfirm
mv dist/Update MCQMaker_MacOS/Update.app

# Copy the files to the directory
cp -r Templates MCQMaker_MacOS/Templates
cp -r resources MCQMaker_MacOS/resources
cp LICENSE MCQMaker_MacOS/LICENSE
cp NOTICE MCQMaker_MacOS/NOTICE
cp MCQMaker.kv MCQMaker_MacOS/MCQMaker.kv
cp version.toml MCQMaker_MacOS/version.toml
cp README.md MCQMaker_MacOS/README.md

# Create the empty folders
cd MCQMaker_MacOS
mkdir Classes
mkdir Export
mkdir "Question Database"
