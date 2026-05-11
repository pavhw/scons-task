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

#------------------------------------------------------------------------------
def include(env, namespace, sconscript, **kwargs):
    f = Path(sconscript)

    if not kwargs.get('optional') and (not f.exists() or not f.is_file()):
        #TODO
        log.fatal()

    this_ns = env.get('TASK_NAMESPACE', '').strip()

    if kwargs.get('flatten'):
        file_ns = this_ns
    else:
        file_ns = f"{this_ns}:{namespace}" if this_ns else namespace

    excludes = [f"{this_ns}:{name}" for name in kwargs.get('exclude', [])]

    file_env = env.Clone(
        TASK_NAMESPACE=namespace,
        TASK_PREFIX=file_ns,
        TASK_EXCLUDE=excludes,
        #TASK_INTERNAL=kw.get('internal')
    )

    SConscript(sconscript, exports={'env': file_env})

    new_tasks = {f"{namespace}:{k}": v for k, v in file_env['TASKS'].items()}
    env['TASKS'].update(new_tasks)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def task(env, name, **kwargs):
    task_fn = lambda env, **kwargs: Task(env, name, **kwargs).target_nodes
    env.AddMethod(task_fn, name)

    return task_fn(env, **kwargs)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def generate(env):
    env['TASKS'] = {}
    env['TASK_NAMESPACE'] = ''

    env.AddMethod(include, 'Include')
    env.AddMethod(task, 'Task')
#------------------------------------------------------------------------------
