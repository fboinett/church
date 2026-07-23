# Dashboard module for Church Platform
# Contains workspace configurations and dashboard APIs

from .workspaces import (
    get_archbishop_workspace,
    get_bishop_workspace,
    get_archdeacon_workspace,
    get_vicar_workspace,
    get_member_workspace,
)
from .analytics import (
    get_engagement_stats,
    get_share_analytics,
    get_event_analytics,
    get_readership_breakdown,
    get_trending_content,
)

__all__ = [
    "get_archbishop_workspace",
    "get_bishop_workspace",
    "get_archdeacon_workspace",
    "get_vicar_workspace",
    "get_member_workspace",
    "get_engagement_stats",
    "get_share_analytics",
    "get_event_analytics",
    "get_readership_breakdown",
    "get_trending_content",
]
