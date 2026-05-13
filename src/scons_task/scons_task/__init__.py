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

from pathlib import Path

from SCons.Script import SConscript

from scons_task import log
from scons_task.task import Task

#------------------------------------------------------------------------------
def include(env, namespace, args):
    if type(args) is str:
        args = {'file': args}

    sconscript = Path(args['file'])

    if not sconscript.exists() or not sconscript.is_file():
        if args.get('optional'):
            return
        else:
            log.fatal(f"The included script is not found: '{sconscript}'")

    this_ns = env.get('TASK_NAMESPACE', '').strip()

    if args.get('flatten'):
        file_ns = this_ns
    else:
        file_ns = f"{this_ns}:{namespace}" if this_ns else namespace

    exclude = args.get('exclude', [])

    if type(exclude) is str:
        exclude = [exclude]

    file_env = env.Clone(
        TASK_NAMESPACE=namespace,
        TASK_PREFIX=file_ns,
        TASK_EXCLUDE=exclude,
        TASK_INTERNAL=args.get('internal', False)
    )

    SConscript(sconscript, exports={'env': file_env})
    env['TASKS'].update(file_env['TASKS'])
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def task(env, name, args):
    if type(args) is str:
        args = {'cmds': [args]}
    elif type(args) is list or type(args) is tuple:
        args = {'cmds': args}
    elif type(args) is not dict:
        log.fatal("Incorrect type of arguments.", task_name=name)

    return Task(env, name, args).target_nodes
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def generate(env):
    env['TASKS'] = {}
    env['TASK_NAMESPACE'] = ''

    env.AddMethod(include, 'Include')
    env.AddMethod(task, 'Task')
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def exists(env):
    return True
#------------------------------------------------------------------------------
