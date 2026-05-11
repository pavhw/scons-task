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
from scons_task.dyn_var import DynVar

from task_cmd import TaskCmd


#==============================================================================
class Task:
    #--------------------------------------------------------------------------
    def __init__(self, *, env, name, **kwargs):
        self.env = env.Clone()
        self.name = name

        self.full_name = self.__get_full_name()

        self.vars = {}
        self.cmds = []
        self.cmd_idx = 0
        self.target_nodes = []

        self.__update_vars(kwargs.get('vars', {}))

        self.silent = kwargs.get('silent', False)
        self.internal = kwargs.get('internal', False)

        cmds = kwargs.get('cmds')

        if not cmds:
            self.__fatal('No command is defined')

        for cmd_item in cmds:
            self.__process_cmd(cmd_item)

        if name not in env.get('TASK_EXCLUDES', []):
            env['TASKS'][name] = self

        alias_prefix = f"_task_" if self.internal else ""
        env.Alias(f"{alias_prefix}{self.full_name}", self.target_nodes)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __update_vars(self, vars):
        for key, value in vars.items():
            if type(value) is DynVar:
                self.vars[key] = value.execute(self)
            else:
                self.vars[key] = value

        self.vars.update(ARGUMENTS)
        self.env.Replace(**self.vars)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __process_cmd(self, cmd_item):
        if type(cmd_item) is str:
            self.__add_cmd(cmd=cmd_item)
        elif type(cmd_item) is dict:
            if 'cmd' in cmd_item and 'task' in cmd_item:
                # FIXME: message
                self.__fatal('cmd or task is defined')

            if 'cmd' in cmd_item:
                self.__add_cmd(**cmd_item)
            elif 'task' in cmd_item:
                self.__add_task(**cmd_item)
            else:
                # FIXME: message
                self.__fatal('cmd or task is defined')
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __get_full_name(self):
        namespace = self.env.get('TASK_PREFIX', '').strip()
        return f"{namespace}:{self.name}" if namespace else self.name
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __new_fake_target(self):
        target = f"_task_{self.full_name}_{self.cmd_idx}_"
        self.cmd_idx += 1

        return target
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __add_cmd(self, **kwargs):
        cmd_str = kwargs['cmd']

        cmd_args = {
            'silent': kwargs.get('silent', False),
            'ignore_errors': kwargs.get('ignore_errors', False),
        }

        cmd = TaskCmd(
            task=self, cmd_str=cmd_str,
            target=self.__new_fake_target(), **cmd_args
        )

        self.cmds.append(cmd)
        self.target_nodes.extend(cmd.target_nodes)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __add_task(self, **kwargs):
        task_name = kwargs['task']

        task_args = {
            'silent': kwargs.get('silent', False),
            'vars': kwargs.get('vars', {}),
        }

        task_ref = TaskRef(
            parent=self, task_name=task_name,
            target_prefix=self.__new_fake_target(), **task_args
        )

        self.cmds.extend(task_ref.cmds)
        self.target_nodes.extend(task_ref.target_nodes)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __error(self, msg):
        log.error(msg, task_name=self.full_name)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __warn(self, msg):
        log.warn(msg, task_name=self.full_name)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __info(self, msg):
        log.info(msg, task_name=self.full_name)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def __fatal(self, msg, *, exit_code=1):
        log.fatal(msg, task_name=self.full_name, exit_code=exit_code)
    #--------------------------------------------------------------------------

# class Task
#==============================================================================
