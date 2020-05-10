# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import io
import os
import tarfile
import zipfile

import requests

ARCH_NAME = {
    "x68_64": "64",
    "x68": "32",
}

PLATFORM_ARTIFACT = {
    "linux": "nvim-linux{arch}.tar.gz",
    "macos": "nvim-macos.tar.gz",
    "windows": "nvim-win{arch}.zip",
}

VERSION_URL = (
    "https://github.com/neovim/neovim/releases/download"
    "/v{version}/{platform_artifact}"
)

EXTRACT_DIR = os.environ[
    "REZ_BUILD_INSTALL_PATH"
    if os.environ["REZ_BUILD_INSTALL"] == "1" else
    "REZ_BUILD_PATH"
]


def download_url():
    """Create download URL for current environment.

    Returns:
        str: Full URL to the artifact to download.
    """
    version = os.environ["REZ_BUILD_PROJECT_VERSION"].split("+")[0]
    platform_artifact = PLATFORM_ARTIFACT[os.environ["REZ_PLATFORM_VERSION"]]
    platform_artifact.format(arch=ARCH_NAME[os.getenv("REZ_ARCH_VERSION")])
    return VERSION_URL.format(**locals())


def iter_stripped(archive, levels=1, sep="/", verbose=False):
    """Iterate over members with leading paths removed.

    Args:
        archive: Iterable list of archive members.
        levels (int): Custom level of leading folders to strip.
        sep (str): Character to use to identify folder separators.

    Yields:
        zipfile.ZipInfo or tarfile.TarInfo: Archive member with stripped paths.
    """
    for member in archive:
        file_path = None
        if isinstance(member, zipfile.ZipInfo):
            file_path = member.filename
        elif isinstance(member, tarfile.TarInfo):
            file_path = member.name

        if file_path is not None and file_path.count(sep) >= levels:
            stripped_parts = file_path.split(sep)[levels:]
            stripped_path = sep.join(stripped_parts)
            if verbose:
                print(stripped_path)

            if isinstance(member, zipfile.ZipInfo):
                member.filename = stripped_path
            elif isinstance(member, tarfile.TarInfo):
                member.name = stripped_path

        yield member


def install_nix(artifact_url):
    """Extract tar directly from GitHub for Mac/Linux.

    Args:
        artifact_url (str): Full path to release tar artifact.
    """
    print('Extracting from "{}"'.format(artifact_url))
    print('into "{}"'.format(EXTRACT_DIR))
    response = requests.get(artifact_url, stream=True)

    with tarfile.open(fileobj=response.raw, mode="r|gz") as artifact_tar:
        artifact_tar.extractall(
            path=EXTRACT_DIR,
            members=iter_stripped(artifact_tar),
        )


def install_windows(artifact_url):
    """Download and extract zip from GitHub for Windows.

    Args:
        artifact_url (str): Full path to release zip artifact.
    """
    print('Downloading into memory "{}"'.format(artifact_url))
    response = requests.get(artifact_url)
    zip_io = io.BytesIO(response.content)
    print('Extracting into "{}"'.format(EXTRACT_DIR))

    with zipfile.ZipFile(zip_io) as artifact_zip:
        artifact_zip.extractall(
            path=EXTRACT_DIR,
            members=iter_stripped(artifact_zip.infolist()),
        )


if __name__ == "__main__":
    if os.name == "nt":
        install_windows(download_url())
    else:
        install_nix(download_url())
