"""
Test module of tools export
"""

###############
### Imports ###
###############

import sys
sys.path.append(".")

from mock import patch

from mcq_maker_tools.tools_export import (
    generate_QCM,
    create_folder_QCM,
    export_QCM_txt,
    export_QCM_docx,
    export_QCM_H5P_text_fill_blanks,
    export_QCM_H5P_text_single_choice,
    export_QCM_moodle,
    launch_export_QCM
)

######################
### Test variables ###
######################

#############
### Tests ###
#############
