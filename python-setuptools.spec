%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-setuptools
Version:        0.6c1
Release:        1%{?dist}
Summary:        Download, build, install, upgrade, and uninstall Python packages

Group:          Development/Languages
License:        PSFL/ZPL
URL:            http://peak.telecommunity.com/DevCenter/setuptools
Source0:        http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}.zip
Source1:		psfl.txt
Source2:		zpl.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.


%prep
%setup -q -n setuptools-%{version}
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build \
	--root $RPM_BUILD_ROOT \
	--single-version-externally-managed
cp -a %{SOURCE1} %{SOURCE2} .
find $RPM_BUILD_ROOT%{python_sitelib} -name '*.exe' | xargs rm -f


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc *.txt
%{_bindir}/*
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/setuptools
%dir %{python_sitelib}/setuptools/command
%dir %{python_sitelib}/setuptools/tests
%{python_sitelib}/*.py
%{python_sitelib}/*/*.py
%{python_sitelib}/*/*/*.py
%{python_sitelib}/*.pyc
%{python_sitelib}/*/*.pyc
%{python_sitelib}/*/*/*.pyc
%ghost %{python_sitelib}/*.pyo
%ghost %{python_sitelib}/*/*.pyo
%ghost %{python_sitelib}/*/*/*.pyo


%changelog
* Sat Jul 22 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c1-1
- Version 0.6c1

* Wed Jun 28 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6b3-1
- Taking over from Ignacio
- Version 0.6b3
- Ghost .pyo files in sitelib
- Add license files
- Remove manual python-abi, since we're building FC4 and up
- Kill .exe files

* Wed Feb 15 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.6a10-1
- Upstream update

* Mon Jan 16 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.6a9-1
- Upstream update

* Sat Dec 24 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.6a8-1
- Initial RPM release
