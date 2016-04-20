#!/bin/python
"""
Installs COSSAN-X (and its required pre-requisites).

Note: quick and dirty script - use with caution!
      Tested briefly on CentOS 6.7 using base OS installed Python 2.6.6

1) First, edit 'Config' section (if required).
2) To run script call:
        python install_cossan.py
"""
from __future__ import print_function, with_statement
import errno
import os
import shlex
import subprocess
import urllib

################################################################################
# Config:
#########

# Root path (absolute) to install to.  Default is users home.
ROOT_INSTALL_DIR = os.path.expanduser('~')

# License server config.
SMARX_SERVER = 'hostname.or.ip.to.smarx.server'
SMARX_PORT = '8765'  # Default port is 8765.


################################################################################
# Script:
############

def download_file(url, destination_file):
    """Downloads a file from a URL to the specified destination."""
    if not os.path.isfile(destination_file):
        print("Downloading: " + url + " to: " + destination_file + " ...")
        urllib.urlretrieve(url, destination_file)
    else:
        print("Destination: " + destination_file + " already exists.")


def unzip(source_archive, destination_dir):
    """Unzips an archive to the specified destination directory."""
    if not os.path.isdir(destination_dir):
        print("Extracting: {src} to: {dest} ...".format(src=source_archive,
                                                        dest=destination_dir))
        unzip_command = 'unzip {src} -d {dest}'.format(src=source_archive,
                                                       dest=destination_dir)
        subprocess.call(shlex.split(unzip_command))
    else:
        print("Extracted archive: " + destination_dir + " already exists")


def main():
    """Main function to download and install prerequisites and COSSAN-X."""
    # Install prerequisite WebKitGTK.
    print("Installing WebKitGTK using yum...")
    command = 'sudo yum install webkitgtk --assumeyes'
    subprocess.check_call(shlex.split(command))

    # Create build dir if it doesn't already exist.
    build_dir = os.path.join(ROOT_INSTALL_DIR, 'build')
    try:
        os.makedirs(build_dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(build_dir):
            pass
        else:
            raise

    # Download and extract of MCR runtime installer.
    mcr_url = 'http://uk.mathworks.com/supportfiles/downloads/R2014a/deployment_files/R2014a/installers/glnxa64/MCR_R2014a_glnxa64_installer.zip'
    mcr_archive_file = os.path.join(build_dir, 'MCR_R2014a_glnxa64_installer.zip')
    download_file(mcr_url, mcr_archive_file)
    mcr_extract_dir = os.path.join(build_dir, 'mcr_extracted_archive')
    unzip(mcr_archive_file, mcr_extract_dir)

    # Prepare MCR install configuration.
    mcr_install_dir = os.path.join(ROOT_INSTALL_DIR, 'mcr')
    mcr_log_file = os.path.join(mcr_install_dir, 'mcr_install_log')
    mcr_install_config = '''\
    destinationFolder={mcr_root}
    agreeToLicense=yes
    outputFile={mcr_log}
    mode=automated
    automatedModeTimeout=3000
    '''.format(mcr_root=mcr_install_dir, mcr_log=mcr_log_file)

    # Write MCR install configuration to file.
    mcr_config_file = os.path.join(mcr_extract_dir, 'mcr_config')
    with open(mcr_config_file, 'w') as f:
        f.write(mcr_install_config)

    # Install MCR.
    if not os.path.isdir(mcr_install_dir):
        mcr_installer = os.path.join(mcr_extract_dir, 'install')
        command = (
            '"{installer}" -inputFile "{config_file}"'
            .format(installer=mcr_installer, config_file=mcr_config_file)
        )
        subprocess.check_call(shlex.split(command))

    # Download and extract COSSAN-X installer.
    cossanx_archive_file = os.path.join(build_dir, 'COSSANX_Linux_R2014a.zip')
    cossanx_url = 'https://www.dropbox.com/s/o5x6rv7ycxdhfd1/COSSANX_Linux_R2014a.zip?dl=1&pv=1'
    download_file(cossanx_url, cossanx_archive_file)
    cossanx_install_dir = os.path.join(ROOT_INSTALL_DIR, 'cossanx')
    unzip(cossanx_archive_file, cossanx_install_dir)

    # Read contents of original start_cossan script.
    cossanx_install_dir = os.path.join(cossanx_install_dir, 'COSSANX_Linux_R2014a')
    start_cossan_script = os.path.join(cossanx_install_dir, 'start_cossan.sh')
    with open(start_cossan_script, 'r') as f:
        lines = f.readlines()

    # Delete last line, and replace with configured line.
    lines = lines[:-1]
    new_start_cossan_command = '''\
$WorkDir/cossanx \\
    -smarxserver {smarx_server} \\
    -smarxport {smarx_port} \\
    -data /home/$USER \\
    -consoleLog /eclipse \\
    -loggingEnabled \\
    -vmargs
    '''.format(smarx_server=SMARX_SERVER, smarx_port=SMARX_PORT)
    lines.append(new_start_cossan_command)

    # Re-write edited lines (new script) back.
    with open(start_cossan_script, 'w') as f:
        f.writelines(lines)

    # Configure COSSAN-X mcr.ini file with mcr install directory.
    mcr_ini_file = os.path.join(cossanx_install_dir, 'mcr.ini')
    with open(mcr_ini_file, 'w') as f:
        f.write(mcr_install_dir)

if __name__ == '__main__':
    main()
