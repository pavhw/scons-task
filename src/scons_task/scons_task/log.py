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

from SCons.Script import Exit

COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'blue': '\033[94m',

    'err': '\033[91m',
    'error': '\033[91m',
    'warn': '\033[93m',
    'warning': '\033[93m',
    'info': '\033[92m',

    'bold': '\033[1m',
    'end': '\033[0m',
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
    log('error', msg, task_name=task_name)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def warning(msg, *, task_name=''):
    log('warning', msg, task_name=task_name)
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
def default_log_fn(env, task, cmd_str, color='info'):
    color = COLORS.get(color, COLORS['info'])
    end = COLORS['end']
    prefix = f"scons-task: [{task.full_name}] "
    cmd_str = env.subst(cmd_str)

    return f"{color}{prefix}{cmd_str}{end}"
#------------------------------------------------------------------------------
