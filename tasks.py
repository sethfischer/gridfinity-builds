"""Main Invoke task file."""

from invoke import Collection, task

import gridfinity_builds.empire.tasks as empire_tasks
import gridfinity_builds.europlan.tasks as europlan_tasks
import gridfinity_builds.generic.tasks as generic_tasks
import gridfinity_builds.gridfinity.tasks as gridfinity_tasks
import gridfinity_builds.mueller.tasks as mueller_tasks
import gridfinity_builds.wiha.tasks as wiha_tasks
from gridfinity_builds.constants import BUILD_DIR


@task
def mkdir_build(c):
    """Create build directory."""
    c.run(f"mkdir -p {BUILD_DIR}")


@task
def clean(c):
    """Clean build directory."""
    c.run(f"rm -rf {BUILD_DIR}/*.step")


ns = Collection()
ns.add_task(mkdir_build)
ns.add_task(clean)

ns.add_collection(Collection.from_module(empire_tasks), "empire")
ns.add_collection(Collection.from_module(europlan_tasks), "europlan")
ns.add_collection(Collection.from_module(generic_tasks), "generic")
ns.add_collection(Collection.from_module(gridfinity_tasks), "gridfinity")
ns.add_collection(Collection.from_module(mueller_tasks), "mueller")
ns.add_collection(Collection.from_module(wiha_tasks), "wiha")
