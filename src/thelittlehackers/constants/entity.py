# MIT License
#
# Copyright (C) 2024 The Little Hackers.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from enum import StrEnum
from enum import auto

class EntityState(StrEnum):
    """
    Define the standard lifecycle states of a persistent entity stored in
    the primary data store.

    These states are used internally to control entity behavior and to
    synchronize data with external systems (e.g., mobile client
    applications).
    """
    # Why "State" instead of "Status"?
    #
    # We intentionally use the term "state" rather than "status" to
    # emphasize that these values represent internal lifecycle conditions
    # that may change over time as part of an entity’s workflow.
    #
    # - **State**: Represent the internal condition or lifecycle phase of
    #   an entity.  A state directly influences behavior and business logic,
    #   and typically transitions over time.
    #
    #   Use "state" when:
    #   - Tracking internal workflow progression (e.g., draft → pending →
    #     approved).
    #   - Representing dynamic lifecycle phases.
    #   - Controlling system behavior based on entity condition.
    #
    # - **Status**: Represent a higher-level or externally communicated
    #   condition, often reflecting the outcome of an action or the overall
    #   health of an entity.
    #
    #   Use "status" when:
    #   - Reporting the result of an operation (e.g., success, failure).
    #   - Communicating a summarized condition to external systems.
    #   - Exposing health or outcome information in APIs or UI.
    #
    # In short:
    # - **State** = internal lifecycle and behavioral control.
    # - **Status** = external outcome or summary condition.
    APPROVED = auto()
    DELETED = auto()
    DISABLED = auto()
    DRAFT = auto()
    ENABLED = auto()
    FAILED = auto()
    PENDING = auto()  # Also used for `In Review`
    REJECTED = auto()
    SUCCEEDED = auto()
