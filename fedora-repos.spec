Summary:        Fedora package repositories
Name:           fedora-repos
Version:        28
Release:        0.3%{?dist}
License:        MIT
Group:          System Environment/Base
URL:            https://pagure.io/fedora-repos/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.bz2
Provides:       fedora-repos(%{version})
Requires:       system-release(%{version})
Requires:       fedora-repos-rawhide = %{version}-%{release}
Requires:       fedora-gpg-keys = %{version}-%{release}
Obsoletes:      fedora-repos-anaconda < 22-0.3
BuildArch:      noarch
BuildRequires:  fedora-release = %{version}

%description
Fedora package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-repos = %{version}-%{release}
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description rawhide
This package provides the rawhide repo definitions.


%package -n fedora-gpg-keys
Summary:        Fedora RPM keys
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description -n fedora-gpg-keys
This package provides the RPM signature keys.


%prep
%setup -q

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/%{name}-%{version}/archmap) \
        || echo "WARNING: no archmap entry for $key"
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{version}-primary RPM-GPG-KEY-%{version}-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done


%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%files -n fedora-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%changelog
* Mon Sep 25 2017 Matthew Miller <mattdm@fedoraproject.org> - 28-0.3
- add dist tag to align with packaging guidelines (and to solve a problem for MBS)
- added BuildRequires on fedora-release of the same version, to prevent possible
  confusion with the dist-tag not matching the package version.

* Fri Sep 22 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 28-0.2
- Split out GPG keys into fedora-gpg-keys

* Tue Aug 15 2017 Mohan Boddu <mboddu@redhat.com> - 28-0.1
- Setup for rawhide being f28
