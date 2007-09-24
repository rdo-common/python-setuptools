%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-setuptools
Version:        0.6c7
Release:        2%{?dist}
Summary:        Download, build, install, upgrade, and uninstall Python packages

Group:          Applications/System
License:        Python or ZPLv2.0
URL:            http://peak.telecommunity.com/DevCenter/setuptools
Source0:        http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz
Source1:        psfl.txt
Source2:        zpl.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%package devel
Summary:        Download, install, upgrade, and uninstall Python packages
Group:          Development/Languages
Requires:       python-devel
Requires:       %{name} = %{version}-%{release}

%description devel
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package contains the components necessary to build and install software
requiring setuptools.


%prep
%setup -q -n setuptools-%{version}
chmod -x *.txt
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%check
# We expect one failure with the current setup
%{__python} setup.py test || :


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build \
    --root $RPM_BUILD_ROOT \
    --single-version-externally-managed

rm -rf $RPM_BUILD_ROOT%{python_sitelib}/setuptools/tests

install -p -m 0644 %{SOURCE1} %{SOURCE2} .
find $RPM_BUILD_ROOT%{python_sitelib} -name '*.exe' | xargs rm -f
find $RPM_BUILD_ROOT%{python_sitelib} -name '*.txt' | xargs chmod -x
chmod +x $RPM_BUILD_ROOT%{python_sitelib}/setuptools/command/easy_install.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc psfl.txt zpl.txt pkg_resources.txt setuptools.txt
%{python_sitelib}/*
%exclude %{python_sitelib}/easy_install*

%files devel
%defattr(-,root,root,-)
%doc psfl.txt zpl.txt EasyInstall.txt README.txt api_tests.txt
%{python_sitelib}/easy_install*
%{_bindir}/*


%changelog
* Mon Sep 24 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c7-2
- Move pretty much everything back into runtime in order to avoid more
  brokenness than we're trying to address with these fixes.

* Fri Sep 14 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c7-1
- Upstream 0.6c7
- Move some things from devel into runtime, in order to not break other
  projects.

* Sat Aug 18 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c6-2
- Make license tag conform to the new Licensing Guidelines
- Move everything except pkg_resources.py into a separate -devel package
  so we avoid bundling python-devel when it's not required (#251645)
- Do not package tests

* Sun Jun 10 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c6-1
- Upstream 0.6c6
- Require python-devel (#240707)

* Sun Jan 28 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c5-1
- Upstream 0.6c5 (known bugs, but the promised 0.6c6 is taking too long)

* Tue Dec 05 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c3-1
- Upstream 0.6c3 (#218540, thanks to Michel Alexandre Salim for the patch)

* Tue Sep 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c2-1
- Upstream 0.6c2
- Ghostbusting

* Mon Jul 31 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c1-2
- Set perms on license files (#200768)

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
