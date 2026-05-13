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

from scons_task import log
from scons_task.task_cmd import TaskCmd

#==============================================================================
class TaskRef:
    #--------------------------------------------------------------------------
    def __init__(self, *, parent, name, target_prefix, **kwargs):
        task = parent.env['TASKS'].get(name)

        if not task:
            log.fatal(f"The task '{name}' does not exist.")

        self.env = parent.env.Clone()
        self.parent = parent
        self.name = name
        self.target_prefix = target_prefix
        self.kwargs = kwargs

        self.cmds = []
        self.cmd_idx = 0
        self.target_nodes = []

        self.vars = kwargs.get('vars', {})
        self.env.Replace(**self.vars)

        for ref_cmd in task.cmds:
            cmd_args = {
                'silent': kwargs.get('silent', False) or ref_cmd.silent
            }

            cmd = TaskCmd(
                env=self.env, task=task, cmd_str=ref_cmd.cmd_str,
                target=self.__new_fake_target(), **cmd_args
            )

            self.cmds.append(cmd)
            self.target_nodes.extend(cmd.target_nodes)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __new_fake_target(self):
        target = f"{self.target_prefix}{self.name}_{self.cmd_idx}_"
        self.cmd_idx += 1

        return target
    #--------------------------------------------------------------------------

# class TaskRef
#==============================================================================
