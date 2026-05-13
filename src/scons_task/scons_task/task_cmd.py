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

from SCons.Script import Action

from scons_task import log

#==============================================================================
class TaskCmd:
    def __init__(self, *, env, task, cmd_str, target, **kwargs):
        self.env = env
        self.task = task
        self.cmd_str = cmd_str
        self.target = target
        self.kwargs = kwargs

        self.silent = kwargs.get('silent', False)
        self.ignore_errors = kwargs.get('ignore_errors', False)

        log_fn = env.get('TASK_LOG_FN', log.default_log_fn)
        log_str = log_fn(env, task, cmd_str)

        def no_log_fn(*args, **kwargs):
            return None

        def cmd_log_fn(target, source, env):
            return f"{log_str}"

        str_fn = no_log_fn if self.silent else cmd_log_fn

        if self.ignore_errors:
            cmd_str = f"-{cmd_str}"

        self.action = Action(cmd_str, strfunction=str_fn)
        self.target_nodes = self.env.Command(target, None, self.action)

        self.env.AlwaysBuild(self.target_nodes)

# class TaskCmd
#==============================================================================
