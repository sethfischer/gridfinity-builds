"""Invoke tasks for Wiha brand items."""

from invoke import task

from gridfinity_builds.helpers import output


@task
def magnetizer_400_10(c):
    """Wiha 400 10 magnetizer 2U×2U×6U.

    Manufacturer: Wiha
    Model: 40010
    Product page: https://www.wihatools.com/products/magnetizer-and-demagnetizer
    """
    from gridfinity_builds.wiha.magnetizer_40010 import Wiha40010Horizontal

    slug = "wiha-400-10"

    gf_module = Wiha40010Horizontal()
    gf_module.save_step_file(
        output(
            slug,
            length=Wiha40010Horizontal.LENGTH_U,
            width=Wiha40010Horizontal.WIDTH_U,
            height=Wiha40010Horizontal.HEIGHT_U,
        )
    )
