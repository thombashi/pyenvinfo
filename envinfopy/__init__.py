"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import platform
from typing import Dict, List, Mapping, Optional, Sequence, Tuple, Union, cast

import pkg_resources

from .__version__ import __author__, __copyright__, __email__, __license__, __version__


class Key:
    UNAME = "uname"
    PYTHON_IMPLEMENTATION = "python_implementation"
    PYTHON_VERSION = "python_version"


def get_envinfo(packages: Optional[Sequence[str]] = None) -> Dict[str, str]:
    uname = platform.uname()
    envinfo = {
        Key.UNAME: "{} {} {} {}".format(uname.system, uname.node, uname.release, uname.machine),
        Key.PYTHON_IMPLEMENTATION: platform.python_implementation(),
        Key.PYTHON_VERSION: platform.python_version(),
    }

    if not packages:
        return envinfo

    for pkg in packages:
        if not pkg:
            continue

        try:
            envinfo[pkg] = pkg_resources.get_distribution(pkg).version
        except pkg_resources.DistributionNotFound:
            envinfo[pkg] = "not installed"

    return envinfo


def dumps(packages: Optional[Sequence[str]] = None, format: Optional[str] = None) -> str:
    envinfo = get_envinfo(packages)
    uname = envinfo.pop(Key.UNAME)
    implementation = envinfo.pop(Key.PYTHON_IMPLEMENTATION)
    version = envinfo.pop(Key.PYTHON_VERSION)

    lines = ["uname: {}".format(uname), "{} version: {}".format(implementation, version)]
    lines.extend(["{} version: {}".format(key, value) for key, value in envinfo.items()])

    if format and format.strip().lower() == "markdown":
        lines = ["- {}".format(line) for line in lines]

    return "\n".join(lines)
