"""Invoke tasks for Empire brand items."""

from invoke import task

from gridfinity_builds.helpers import output


@task
def rule_stop_emssrs(c):
    """Empire EMSSRS ruler stop 5U×1U×6U."""
    from gridfinity_builds.empire.rule_stop_emssrs import EmpireRuleStopEmssrs

    slug = "empire-emssrs"

    gf_module = EmpireRuleStopEmssrs()
    gf_module.save_step_file(
        output(
            slug,
            length=EmpireRuleStopEmssrs.LENGTH_U,
            width=EmpireRuleStopEmssrs.WIDTH_U,
            height=EmpireRuleStopEmssrs.HEIGHT_U,
        )
    )
