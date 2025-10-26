# Contributing

NOT looking for contributors for the foreseeable future!

## Commit Messages

All commits should follow the following convention:

```
<type>(scope - optional): <description>

<body - optional>

<footer - optional>
```

### Commit Types

Below are the currently accepted commit types:

- ``feat`` - a new feature is introduced
- ``fix`` - a bug is fixed
- ``refactor`` - code is refactored (unrelated to features or fixes)
- ``docs`` - documentation is updated
- ``test`` - including, fixing, removing tests
- ``build`` - changes that affect build system
- ``chore`` - changes that don't modify src or test files (unrelated to features or fixes)
- ``revert`` - reverts to a previous commit

If you belive a commit type should be included in the list above, feel free to create an Issue and/or open a PR.

## Branches

- ``master`` - protected branch; accepts PRs only from the ``*/dev`` branches; must be functional and play-tested
- ``<developer_name>/dev`` - staging branches for each developer; ideally follows ``master`` closely to minimize conflicts;
- ``<developer_name>/<branch_name>`` - branches for fixes, features and more; branches from a ``/dev`` and should be merged back into ``/dev``;
