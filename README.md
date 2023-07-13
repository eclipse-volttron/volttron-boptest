# Volttron BopTest Monorepo

This repo hosts both volttron-boptest-agent and volttron-lib-boptest-integration. For more information about mono-repo,
please see [Poetry Monorepo](https://gitlab.com/craig81/poetry-monorepo).
Please refer to [volttron-boptest-agent/README.md](volttron-boptest-agent/README.md)
and [volttron-lib-boptest-integration/README.md](volttron-lib-boptest-integration/README.md) for documentation within
individual sub-repo.

## Usage

(Assuming Poetry is installed at system level,) To create the poetry virtual environments:

```shell
scripts/poetry_install.sh
```

It might update the `poetry.lock` files, which is mainly usefull when running on new architectures.

If a new dependency has been added to any of the poetry file, run the helper script to update all lock files:

```shell
scripts/poetry_update.sh
```

It by design will update all `poetry.lock` files, such that updated transitive dependencies are correct.
It might also update other transitive dependencies to latest versions.

On the build server, one can determine the actual local semver version of the current checkout, and update all version
numbers in the codebase:


```shell
scripts/poetry_build.sh
```

Note that this changes the `pyproject.toml` files with changes that **should not be committed** to git.

Alternatively, to not have to modify `pyproject.toml` files, one can first build the packages.
Then, we need to modify the dependencies in the wheel & tar.gz artifacts.
This is done as follows (without invoking `poetry_build.sh`):

```shell
cd package-b
poetry build
../scripts/replace_path_deps.sh
```

