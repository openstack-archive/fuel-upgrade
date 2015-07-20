%define name fuel-upgrade
%{!?version: %define version 7.0.0}
%{!?release: %define release 1}

Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
Summary: Fuel-upgrade package
URL:     http://mirantis.com
License: Apache
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Prefix: %{_prefix}
BuildRequires:  git
BuildRequires: python-setuptools
BuildArch: noarch

Requires:    python
Requires:    python-argparse
Requires:    PyYAML
Requires:    python-mako
Requires:    python-requests
Requires:    python-six
Requires:    python-docker-py

%description
Fuel-upgrade package

%prep
%setup -cq -n %{name}-%{version}

%build
cd %{_builddir}/%{name}-%{version} && python setup.py build

%install
cd %{_builddir}/%{name}-%{version} && python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=%{_builddir}/%{name}-%{version}/INSTALLED_FILES
install -d -m 755 %{buildroot}%{_sysconfdir}/fuel-upgrade
install -p -D -m 755 %{_builddir}/%{name}-%{version}/upgrade.sh %{buildroot}%{_bindir}/upgrade.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{_builddir}/%{name}-%{version}/INSTALLED_FILES
%defattr(-,root,root)
%{_bindir}/upgrade.sh
