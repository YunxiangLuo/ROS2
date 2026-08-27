# -*- coding: utf-8 -*-
"""包级 conftest：显式加载共享 ROS stubs(避免 rootdir/confcutdir 差异)。"""

import os
import sys

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import _ros_stubs  # noqa: F401,E402
