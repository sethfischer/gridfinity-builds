"""Invoke tasks for Europlan brand furniture."""

from invoke import task

from gridfinity_builds.helpers import output


@task
def tab_drawer_spacer(c):
    """Drawer spacer for Europlan TAB pedestal drawers."""
    slug = "drawer-spacer-tab"

    dr_width = 326.5
    dr_depth = 449.5
    chamf_rad = 1.0
    tolerance = 0.25

    from cqgridfinity import GridfinityDrawerSpacer

    spacers = GridfinityDrawerSpacer(
        dr_width,
        dr_depth,
        verbose=True,
        show_arrows=False,
        chamf_rad=chamf_rad,
        tolerance=tolerance,
    )
    spacers.render_half_set()
    spacers.save_step_file(output(slug, length=dr_width, width=dr_depth).as_posix())
