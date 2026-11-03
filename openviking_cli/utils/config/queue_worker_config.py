# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: AGPL-3.0
"""Queue worker runtime configuration."""

from pydantic import BaseModel, Field


class QueueWorkerConfig(BaseModel):
    """Runtime limits for one queue worker."""

    max_concurrent: int = Field(
        default=4,
        gt=0,
        description="Maximum number of jobs processed concurrently",
    )


class AddResourceQueueWorkerConfig(QueueWorkerConfig):
    """Runtime limits for add-resource queue workers."""

    file_operation_concurrency: int = Field(
        default=16,
        gt=0,
        description="Maximum concurrent file-level commit and comparison operations within one add-resource job",
    )

    file_vectorization_concurrency: int = Field(
        default=8,
        gt=0,
        description="Maximum number of files read, prepared, and enqueued concurrently within one vectors-only job",
    )


class QueueRequeueConfig(BaseModel):
    """Shared re-enqueue limits for QueueFS consumers."""

    max_blocked_requeues: int = Field(
        default=8,
        ge=0,
        description="Maximum re-enqueues when a path-lock handoff is blocked by another holder.",
    )
    max_recovery_requeues: int = Field(
        default=2,
        ge=0,
        description="Maximum re-enqueues for other path-lock handoff recovery failures.",
    )


class QueueWorkersConfig(BaseModel):
    """Runtime limits for QueueFS consumers."""

    external_parse: QueueWorkerConfig = Field(default_factory=QueueWorkerConfig)
    add_resource: AddResourceQueueWorkerConfig = Field(default_factory=AddResourceQueueWorkerConfig)
    reindex: QueueWorkerConfig = Field(default_factory=QueueWorkerConfig)
    session_commit: QueueWorkerConfig = Field(
        default_factory=lambda: QueueWorkerConfig(max_concurrent=8)
    )
    external_task: QueueWorkerConfig = Field(
        default_factory=lambda: QueueWorkerConfig(max_concurrent=10)
    )
    requeue: QueueRequeueConfig = Field(default_factory=QueueRequeueConfig)
