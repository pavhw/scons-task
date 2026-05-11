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

from SCons.Script import *


COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'end': '\033[0m',
    'bold': '\033[1m',
    'err': '\033[91m',
    'warn': '\033[93m',
    'info': '\033[92m'
}

#------------------------------------------------------------------------------
def log(color, msg, *, task_name=''):
    color = COLORS.get(color, COLORS['info'])
    end = COLORS['end']
    tag = f"[{task_name}] " if task_name else ""
    prefix = f"scons-task: {tag}"
    print(f"{color}{prefix}{msg}{end}")
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def error(msg, *, task_name=''):
    log('err', msg, task_name=task_name)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def warn(msg, *, task_name=''):
    log('warn', msg, task_name=task_name)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def info(msg, *, task_name=''):
    log('info', msg, task_name=task_name)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def fatal(msg, *, task_name='', exit_code=1):
    error(msg, task_name=task_name)
    Exit(exit_code)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def default_log_fn(task, cmd_str, color):
    color = COLORS.get(color, COLORS['info'])
    end = COLORS['end']
    prefix = f"scons-task: [{task.full_name}]"
    cmd_str = task.env.subst(cmd_str)

    return f"{color}{prefix}{cmd_str}{end}"
#------------------------------------------------------------------------------
