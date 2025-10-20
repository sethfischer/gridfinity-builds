import os
from pathlib import Path

from gridfinity_builds.constants import BUILD_DIR


def output(slug: str, length: float, width: float, height: float = None) -> Path:
    """Generate output pathname."""
    filename = f"gf_{slug}_{length}x{width}"

    if height:
        filename += f"x{height}"

    filename += ".step"

    client_id = os.environ.get("BOXES_CLIENT_ID", None)

    if client_id:
        filename = f"{client_id}_{filename}"

    return Path(BUILD_DIR, filename)
