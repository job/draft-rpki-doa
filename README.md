# draft-ietf-sidrops-rpki-rsc

## Artifacts

The `artifacts` branch provides in-tree storage for built artifacts.

Each commit in the `artifacts` branch should have exactly two parents:

- The previous head of the `artifacts` branch; and
- The commit containing the source tree from which the artifacts were built.

Thus, the commit containing the artifacts built from a given commit can be
identified by identifying a commit object that is:

- Reachable from the head of the `artifacts` branch; and
- Not reachable from the head of the `main` branch; and
- Has the source commit of interest as a parent

For example:

``` bash
f() {
    src_ref="$(git rev-parse ${1:-HEAD})"
    git rev-list main..artifacts --parents \
        | grep "${src_ref}" \
        | cut -d" " -f1
}
```

Only the last commit in a sequence pushed to github will have its artifacts
built and added to the `artifacts` branch automatically.

To find the most recent commit on `artifacts` that is a descendent of a source
commit:

``` bash
g() {
    src_ref="$(git rev-parse ${1:-HEAD})"
    for ref in $(git rev-list main..artifacts --reverse ); do
        git rev-list "${ref}" "^${src_ref}^" \
            | grep "^${src_ref}" >/dev/null \
            && art_ref="${ref}" \
            && break
    done
    echo "${art_ref}"
}
```
