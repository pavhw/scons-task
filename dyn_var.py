#******************************************************************************
#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2026 Anton Polstyankin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#******************************************************************************

import subprocess
from SCons.Script import *

from scons_task import log


#==============================================================================
# Set dynamic variable
#
class DynVar:
    #--------------------------------------------------------------------------
    def __init__(self, cmd_str, *, convert_fn=None):
        self.cmd_str = cmd_str
        self.convert_fn = convert_fn
        self.task = None
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def execute(self, task):
        self.task = task
        value = self.__run_cmd()

        if self.convert_fn is not None:
            value = self.convert_fn(value)

        return value
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __run_cmd(self):
        result = subprocess.run(
            self.cmd_str, capture_output=True, text=True, shell=True
        )

        if result.returncode != 0:
            log.fatal(
                f"Command '{self.cmd_str}' failed, "
                f"exit code: {result.returncode}",
                task=self.task.full_name
            )

        return result.stdout.strip()
    #--------------------------------------------------------------------------

# class DynVar
#==============================================================================


#------------------------------------------------------------------------------
def sh(cmd_str, *, convert_fn=None):
    return DynVar(cmd_str, convert_fn=convert_fn)
#------------------------------------------------------------------------------
