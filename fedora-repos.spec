Summary:        Fedora package repositories
Name:           fedora-repos
Version:        27
Release:        5%{?_module_build:%{?dist}}
License:        MIT
URL:            https://fedoraproject.org/

Provides:       fedora-repos(%{version})
Requires:       system-release(%{version})
Requires:       fedora-gpg-keys = %{version}-%{release}
Obsoletes:      fedora-repos-rawhide <= 27-0.4
Obsoletes:      fedora-repos-anaconda < 22-0.3
BuildArch:      noarch

Source1:        archmap
Source2:        fedora.repo
Source3:        fedora-updates.repo
Source4:        fedora-updates-testing.repo
Source5:        fedora-rawhide.repo
Source6:        fedora-cisco-openh264.repo

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

Source100:      RPM-GPG-KEY-fedora-modularity

Source150:      RPM-GPG-KEY-fedora-iot-2019

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
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    arches=$(sed -ne "s/^${key}://p" %{_sourcedir}/archmap) \
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
for file in %{_sourcedir}/fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done


%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo

%files rawhide
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%files -n fedora-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*

%changelog
* Wed Nov 14 2018 Mohan Boddu <mboddu@bhujji.com> - 27-5
- Adding fedora-iot-2019 key

* Wed Aug 22 2018 Mohan Boddu <mboddu@bhujji.com> - 27-4
- Fixing F30 key

* Mon Aug 20 2018 Mohan Boddu <mboddu@bhujji.com> - 27-3
- Bump and build for source merge change
- Add fedora 30 primary key

* Sat Feb 17 2018 Dennis Gilmore <dennis@ausil.us> - 27-2
- add the Fedora 29 gpg key

* Mon Oct 23 2017 Mohan Boddu <mboddu@redhat.com> - 27-1
- Setup for F27 final

* Mon Sep 25 2017 Stephen Gallagher <sgallagh@redhat.com> - 27-0.6
- Add a dist tag when building for modules

* Fri Sep 22 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 27-0.5
- Do not require rawhide, but obsolete it

* Fri Sep 22 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 27-0.4
- Split out GPG keys into fedora-gpg-keys

* Tue Aug 15 2017 Dennis Gilmore <dennis@ausil.us> - 27-0.3
- Disable Rawhide
- Enable fedora, updates, updates-testing
- Add Fedora 28 key

* Tue May 16 2017 Dennis Gilmore <dennis@ausil.us> - 27-0.2
- add the missing Fedora 14 secondary arch key
- add the new modularity key

* Sat Feb 25 2017 Mohan Boddu <mboddu@redhat.com> - 27-0.1
- Setup for rawhide being f27
