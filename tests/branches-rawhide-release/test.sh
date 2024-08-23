#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k expandtab sts=4
#
# Inspired by distribution-gpg-keys github workflow
# https://github.com/rpm-software-management/distribution-gpg-keys/blob/main/.github/workflows/fedora-repos.yml
# Bodhi fetching of active branches inspired from github action
# https://github.com/sgallagher/get-fedora-releases-action/blob/main/get_fedora_releases.py
#
# Checks whether active releases point to correct rawhide version
. /usr/share/beakerlib/beakerlib.sh || exit 1


: ${REPOURL:=https://src.fedoraproject.org/rpms/fedora-repos.git}
: ${BODHI_RELEASES_URL:="https://bodhi.fedoraproject.org/releases/"}
: ${CLONEDIR:=fedora-repos}
SPECPATH="${CLONEDIR}.spec"

spec_rawhide_release() {
    local SPEC=$1
    awk '$1 == "%global" && $2 == "rawhide_release" { print $3 } ' $SPEC
}

get_bodhi_branches() {
    local FILE="$1"
    shift
    curl -fL "${BODHI_CURRENT_URL}$*" -o "$FILE"
}

parse_bodhi_branches() {
    jq -r '.releases[] | select(.id_prefix == "FEDORA") | .branch' "$@" | xargs echo
}

rlJournalStart
    rlPhaseStartSetup
        rlRun "tmp=\$(mktemp -d)" 0 "Create tmp directory"
        rlRun "pushd $tmp"
        rlRun "git clone $REPOURL --depth 1 --no-single-branch $CLONEDIR"
        rlRun "curl -fL \"${BODHI_RELEASES_URL}?state=current\" -o releases.current"
        rlRun "curl -fL \"${BODHI_RELEASES_URL}?state=pending\" -o releases.pending"
        rlRun "BODHI_STABLE_BRANCHES=\"$(parse_bodhi_branches releases.current)\"" 0 "Obtain supported stable branches from bodhi"
        rlRun "BODHI_PENDING_BRANCHES=\"$(parse_bodhi_branches releases.pending)\"" 0 "Obtain pending branches from bodhi"
    rlPhaseEnd

    rlPhaseStartTest
        pushd $CLONEDIR
        rlRun "RAWHIDE_RELEASE=$(spec_rawhide_release $SPECPATH)"
        rlAssertGreater "Check we have positive number" "$RAWHIDE_RELEASE" 0
        # If branching is still in development
        for ((R=RAWHIDE_RELEASE-1; R>=RAWHIDE_RELEASE-2; R--)); do
            rlRun "git checkout f${R}" 0 "Test f${R} branch"
            rlRun "RAWHIDE_BRANCH=$(spec_rawhide_release $SPECPATH)"
            rlAssertGreater "Check we have positive number" "$RAWHIDE_BRANCH" 0
            rlAssertEquals "Check rawhide version is correct on f$R" "$RAWHIDE_RELEASE" "$RAWHIDE_BRANCH"
        done
        for BRANCH in ${BODHI_STABLE_BRANCHES} ${BODHI_PENDING_BRANCHES}; do
            if [ "$BRANCH" = eln ]; then
                continue
            fi
            rlRun "git checkout $BRANCH" 0 "Test $BRANCH bodhi branch"
            rlRun "RAWHIDE_BODHI_BRANCH=$(spec_rawhide_release $SPECPATH)"
            rlAssertGreater "Check we have positive number" "$RAWHIDE_BODHI_BRANCH" 0
            rlAssertEquals "Check rawhide version is correct on bodhi $BRANCH" "$RAWHIDE_RELEASE" "$RAWHIDE_BODHI_BRANCH"
        done
        popd
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "rm -rf $CLONEDIR"
        rlRun "popd"
        rlRun "rm -r $tmp" 0 "Remove tmp directory"
    rlPhaseEnd
rlJournalEnd
