%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           python-setuptools
Version:        0.6a10
Release:        1%{?dist}
Summary:        Download, build, install, upgrade, and uninstall Python packages

Group:          Development/Languages
License:        PSFL/ZPL
URL:            http://peak.telecommunity.com/DevCenter/setuptools
Source0:        http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-abi = %{pyver}

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

%prep
%setup -q -n setuptools-%{version}
sed -i '1s@#!python@#!/usr/bin/python@' easy_install.py

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --single-version-externally-managed
find $RPM_BUILD_ROOT%{python_sitelib} -name \*.py -exec grep -q '^#!' {} \; -print | while read file ; do sed -i '1d' $file ; done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc api_tests.txt EasyInstall.txt pkg_resources.txt setuptools.txt
%{_bindir}/*
%{python_sitelib}/*

%changelog
* Wed Feb 15 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.6a10-1
- Upstream update

* Mon Jan 16 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.6a9-1
- Upstream update

* Sat Dec 24 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.6a8-1
- Initial RPM release
