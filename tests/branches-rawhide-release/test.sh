#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
#
# Inspired by distribution-gpg-keys github workflow
# https://github.com/rpm-software-management/distribution-gpg-keys/blob/main/.github/workflows/fedora-repos.yml
#
# Checks whether active releases point to correct rawhide version
. /usr/share/beakerlib/beakerlib.sh || exit 1


REPOURL=https://src.fedoraproject.org/rpms/fedora-repos.git
CLONEDIR=fedora-repos
SPECPATH="${CLONEDIR}.spec"

spec_rawhide_release() {
	local SPEC=$1
	awk '$1 == "%global" && $2 == "rawhide_release" { print $3 } ' $SPEC
}

rlJournalStart
    rlPhaseStartSetup
        rlRun "tmp=\$(mktemp -d)" 0 "Create tmp directory"
        rlRun "pushd $tmp"
        rlRun "git clone $REPOURL --depth 1 --no-single-branch $CLONEDIR"
    rlPhaseEnd

    rlPhaseStartTest
        pushd $CLONEDIR
        rlRun "RAWHIDE_RELEASE=$(spec_rawhide_release $SPECPATH)"
        for ((R=RAWHIDE_RELEASE-1; R>=RAWHIDE_RELEASE-2; R--)); do
            rlRun "git checkout f${R}"
            rlRun "RAWHIDE_BRANCH=$(spec_rawhide_release $SPECPATH)"
            rlAssertEquals "Check rawhide version is correct on f$R" "$RAWHIDE_RELEASE" "$RAWHIDE_BRANCH"
        done
        # Just informative check for maybe finalized branch
        # TODO: find reliable way to know, when branch is not supported anymore
        R=((RAWHIDE_RELEASE-3))
        rlRun "git checkout f${R}"
        rlRun "RAWHIDE_BRANCH=$(spec_rawhide_release $SPECPATH)"
        popd
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "rm -rf $CLONEDIR"
        rlRun "popd"
        rlRun "rm -r $tmp" 0 "Remove tmp directory"
    rlPhaseEnd
rlJournalEnd
