"""OpenEnv environment package for AI Business Growth simulation."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from env.business_env import BusinessEnv

__all__ = ["BusinessEnv"]


def __getattr__(name: str):
	if name == "BusinessEnv":
		from env.business_env import BusinessEnv

		return BusinessEnv
	raise AttributeError(f"module 'env' has no attribute {name!r}")
