%global rawhide_release 34

Summary:        Fedora package repositories
Name:           fedora-repos
Version:        32
Release:        12%{?_module_build:%{?dist}}
License:        MIT
URL:            https://fedoraproject.org/

Provides:       fedora-repos(%{version}) = %{release}
Requires:       system-release(%{version})
Requires:       fedora-gpg-keys >= %{version}-%{release}
Obsoletes:      fedora-repos-anaconda < 22-0.3
Obsoletes:      fedora-repos-modular < 29-0.6
Provides:       fedora-repos-modular = %{version}-%{release}
BuildArch:      noarch
# Required by %%check
BuildRequires:  gnupg

Source1:        archmap
Source2:        fedora.repo
Source3:        fedora-updates.repo
Source4:        fedora-updates-testing.repo
Source5:        fedora-rawhide.repo
Source6:        fedora-cisco-openh264.repo
Source7:        fedora-updates-archive.repo
Source8:        fedora-eln.repo


Source10:       RPM-GPG-KEY-fedora-7-primary
Source11:       RPM-GPG-KEY-fedora-8-primary
Source12:       RPM-GPG-KEY-fedora-8-primary-original
Source13:       RPM-GPG-KEY-fedora-9-primary
Source14:       RPM-GPG-KEY-fedora-9-primary-original
Source15:       RPM-GPG-KEY-fedora-9-secondary
Source16:       RPM-GPG-KEY-fedora-10-primary
Source17:       RPM-GPG-KEY-fedora-11-primary
Source18:       RPM-GPG-KEY-fedora-12-primary
Source19:       RPM-GPG-KEY-fedora-13-primary
Source20:       RPM-GPG-KEY-fedora-13-secondary
Source21:       RPM-GPG-KEY-fedora-14-primary
Source22:       RPM-GPG-KEY-fedora-14-secondary
Source23:       RPM-GPG-KEY-fedora-15-primary
Source24:       RPM-GPG-KEY-fedora-15-secondary
Source25:       RPM-GPG-KEY-fedora-16-primary
Source26:       RPM-GPG-KEY-fedora-16-secondary
Source27:       RPM-GPG-KEY-fedora-17-primary
Source28:       RPM-GPG-KEY-fedora-17-secondary
Source29:       RPM-GPG-KEY-fedora-18-primary
Source30:       RPM-GPG-KEY-fedora-18-secondary
Source31:       RPM-GPG-KEY-fedora-19-primary
Source32:       RPM-GPG-KEY-fedora-19-secondary
Source33:       RPM-GPG-KEY-fedora-20-primary
Source34:       RPM-GPG-KEY-fedora-20-secondary
Source35:       RPM-GPG-KEY-fedora-21-primary
Source36:       RPM-GPG-KEY-fedora-21-secondary
Source37:       RPM-GPG-KEY-fedora-22-primary
Source38:       RPM-GPG-KEY-fedora-22-secondary
Source39:       RPM-GPG-KEY-fedora-23-primary
Source40:       RPM-GPG-KEY-fedora-23-secondary
Source41:       RPM-GPG-KEY-fedora-24-primary
Source42:       RPM-GPG-KEY-fedora-24-secondary
Source43:       RPM-GPG-KEY-fedora-25-primary
Source44:       RPM-GPG-KEY-fedora-25-secondary
Source45:       RPM-GPG-KEY-fedora-26-primary
Source46:       RPM-GPG-KEY-fedora-26-secondary
Source47:       RPM-GPG-KEY-fedora-27-primary
Source48:       RPM-GPG-KEY-fedora-28-primary
Source49:       RPM-GPG-KEY-fedora-29-primary
Source50:       RPM-GPG-KEY-fedora-30-primary
Source51:       RPM-GPG-KEY-fedora-31-primary
Source52:       RPM-GPG-KEY-fedora-32-primary
Source53:       RPM-GPG-KEY-fedora-33-primary
Source54:       RPM-GPG-KEY-fedora-34-primary
Source55:       RPM-GPG-KEY-fedora-35-primary

Source100:      fedora-modular.repo
Source101:      fedora-updates-modular.repo
Source102:      fedora-updates-testing-modular.repo
Source103:      fedora-rawhide-modular.repo
Source104:      RPM-GPG-KEY-fedora-modularity

Source150:      RPM-GPG-KEY-fedora-iot-2019
Source151:      fedora.conf
Source152:      fedora-compose.conf

%description
Fedora package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-repos = %{version}-%{release}
Obsoletes:      fedora-release-rawhide <= 22-0.3
Obsoletes:      fedora-repos-rawhide-modular < 29-0.6
Provides:       fedora-repos-rawhide-modular = %{version}-%{release}

%package archive
Summary:        Fedora updates archive package repository
Requires:       fedora-repos = %{version}-%{release}

%description archive
This package provides the repo definition for the updates archive repo.
It is a package repository that contains any RPM that has made it to
stable in Bodhi and been available in the Fedora updates repo in the past.

%description rawhide
This package provides the rawhide repo definitions.


%package -n fedora-gpg-keys
Summary:        Fedora RPM keys
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description -n fedora-gpg-keys
This package provides the RPM signature keys.


%package ostree
Summary:        OSTree specific files

%description ostree
This package provides ostree specfic files like remote config from
where client's system will pull OSTree updates.


%package eln
Summary: ELN repo definitions
Requires: fedora-repos-rawhide = %{version}-%{release}
Requires: fedora-repos-rawhide-modular = %{version}-%{release}

%description eln
This package provides repository files for ELN (Enterprise Linux Next)
packages that can be installed atop Rawhide. Note that these packages are
experimental and should not be used in a production environment.


%prep

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
# Also add a symlink for ELN keys
ln -s RPM-GPG-KEY-fedora-%{rawhide_release}-primary RPM-GPG-KEY-fedora-eln-primary
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    if ! grep -q "^${key}:" %{_sourcedir}/archmap; then
        echo "ERROR: no archmap entry for $key"
        exit 1
    fi
    arches=$(sed -ne "s/^${key}://p" %{_sourcedir}/archmap)
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{version}-primary RPM-GPG-KEY-%{version}-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in %{_sourcedir}/fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# Install ostree remote config
install -d -m 755 $RPM_BUILD_ROOT/etc/ostree/remotes.d/
install -m 644 %{_sourcedir}/fedora.conf $RPM_BUILD_ROOT/etc/ostree/remotes.d/
install -m 644 %{_sourcedir}/fedora-compose.conf $RPM_BUILD_ROOT/etc/ostree/remotes.d/

# Check the builder is on supported architectures
TMPRING=$(mktemp)
for VER in %{version} %{rawhide_release}; do
  gpg --no-default-keyring --keyring="$TMPRING" \
    --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-${VER}-$(arch)
done
rm -f "$TMPRING"
%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing.repo
%config(noreplace) /etc/yum.repos.d/fedora-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing-modular.repo

%files archive
%config(noreplace) /etc/yum.repos.d/fedora-updates-archive.repo

%files rawhide
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo
%config(noreplace) /etc/yum.repos.d/fedora-rawhide-modular.repo


%files -n fedora-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*


%files ostree
%dir /etc/ostree/remotes.d/
/etc/ostree/remotes.d/fedora.conf
/etc/ostree/remotes.d/fedora-compose.conf

%files eln
%config(noreplace) /etc/yum.repos.d/fedora-eln.repo


%changelog
* Tue Feb 09 2021 Mohan Boddu <mboddu@bhujji.com> - 32-12
- Fixing archmap for F35

* Thu Feb 04 2021 Mohan Boddu <mboddu@bhujji.com> - 32-11
- Adding F35 key

* Tue Oct 13 2020 Mohan Boddu <mboddu@bhujji.com> - 32-10
- Disable eln repos on non rawhide release (sgallagh)

* Tue Oct 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 32-9
- Ensure that the ELN GPG key always points at the Rawhide key

* Tue Oct 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 32-8
- Update the ELN repos for the BaseOS and AppStream split

* Mon Oct 05 2020 Dusty Mabe <dusty@dustymabe.com> - 32-7
- Add the fedora-repos-archive subpackage.

* Tue Aug 25 2020 Adam Williamson <awilliam@redhat.com> - 32-6
- Add missing per-arch symlinks for F34 key

* Thu Aug 06 2020 Mohan Boddu <mboddu@bhujji.com> - 32-5
- Adding F34 key

* Tue Jun 30 2020 Stephen Gallagher <sgallagh@redhat.com> - 32-4
- Add optional repositories for ELN

* Mon Jun 01 2020 Dusty Mabe <dusty@dustymabe.com> - 32-3
- Add fedora compose ostree repo to fedora-repos-ostree

* Mon Apr 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 32-2
- Add the release to the fedora-repos(NN) Provides:

* Thu Apr 09 2020 Mohan Boddu <mboddu@bhujji.com> - 32-1
- Setup for F32 Final
- Disable testing repos

* Thu Apr 09 2020 Kalev Lember <klember@redhat.com> - 32-0.8
- Switch to metalink for fedora-cisco-openh264 and disable repo gpgcheck
  (#1768206)
- Use the same metadata_expire time for fedora-cisco-openh264 and -debuginfo
- Remove enabled_metadata key for fedora-cisco-openh264

* Sat Feb 22 2020 Neal Gompa <ngompa13@gmail.com> - 32-0.7
- Enable fedora-cisco-openh264 repo by default
- Dont pull in fedora-repos-rawhide (mohanboddu)

* Wed Feb 19 2020 Adam Williamson <awilliam@redhat.com> - 32-0.6
- Restore baseurl lines, but with example domain

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.5
- Disable rawhide repos
- Enable fedora, updates, updates-testing repos

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.4
- Remove baseurl download.fp.o (puiterwijk)
- Enabling dnf countme

* Tue Jan 28 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.3
- Adding F33 key

* Mon Aug 19 2019 Kevin Fenzi <kevin@scrye.com> - 32-0.2
- Fix f32 key having extra spaces.

* Tue Aug 13 2019 Mohan Boddu <mboddu@bhujji.com> - 32-0.1
- Adding F32 key
- Setup for rawhide being f32

* Tue Mar 12 2019 Vít Ondruch <vondruch@redhat.com> - 31-0.3
- Allow to use newer GPG keys, so Rawhide can be updated after branch.

* Thu Mar 07 2019 Sinny Kumari <skumari@redhat.com> - 31-0.2
- Create fedora-repos-ostree sub-package

* Tue Feb 19 2019 Tomas Hrcka <thrcka@redhat.com> - 31-0.1
- Setup for rawhide being f31

* Mon Feb 18 2019 Mohan Boddu <mboddu@bhujji.com> - 30-0.4
- Adding F31 key

* Sat Jan 05 2019 Kevin Fenzi <kevin@scrye.com> - 30-0.3
- Add fedora-7-primary to archmap. Fixes bug #1531957
- Remove failovermethod option in repos (augenauf(Florian H))

* Tue Nov 13 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.2
- Adding fedora-iot-2019 key
- Enable skip_if_unavailable for cisco-openh264 repo

* Tue Aug 14 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.1
- Setup for rawhide being f30
