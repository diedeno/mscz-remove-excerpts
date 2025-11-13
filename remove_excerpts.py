#!/usr/bin/env python3
"""
Script to remove Excerpts directory from MuseScore .mscz files

Copyright 2025 Diego Denolf <graffesmusic@gmail.com> 
v1.0

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.


"""

import os
import shutil
import zipfile
import tempfile
import sys

def remove_excerpts_from_mscz(mscz_file_path):
    """
    Remove the Excerpts directory from a MuseScore .mscz file
    
    Args:
        mscz_file_path (str): Path to the .mscz file
    """
    
    if not os.path.exists(mscz_file_path):
        print(f"Error: File '{mscz_file_path}' not found.")
        return False
    
    if not mscz_file_path.lower().endswith('.mscz'):
        print(f"Error: '{mscz_file_path}' is not a .mscz file.")
        return False
    
    # Create temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Extract the .mscz file (which is a ZIP archive)
            with zipfile.ZipFile(mscz_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Check if Excerpts directory exists
            excerpts_dir = os.path.join(temp_dir, 'Excerpts')
            if os.path.exists(excerpts_dir):
                print(f"Removing Excerpts directory from {mscz_file_path}")
                shutil.rmtree(excerpts_dir)
            else:
                print(f"No Excerpts directory found in {mscz_file_path}")
                return True
            
            # Create backup of original file
            backup_path = mscz_file_path + '.backup'
            shutil.copy2(mscz_file_path, backup_path)
            print(f"Backup created: {backup_path}")
            
            # Create new .mscz file without Excerpts directory
            with zipfile.ZipFile(mscz_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Create relative path for ZIP archive
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
            
            print(f"Successfully removed Excerpts directory from {mscz_file_path}")
            return True
            
        except Exception as e:
            print(f"Error processing {mscz_file_path}: {str(e)}")
            return False

def main():
    # Get the actual command that was used to run the program
    program_name = os.path.basename(sys.argv[0])
         
    if len(sys.argv) != 2:
        print(f"Usage: {program_name} <path_to_mscz_file>")
        sys.exit(1)
    
    mscz_file = sys.argv[1]
    remove_excerpts_from_mscz(mscz_file)

if __name__ == "__main__":
    main()
