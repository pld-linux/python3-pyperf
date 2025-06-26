#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Python module to run and analyze benchmarks
Summary(pl.UTF-8):	Moduł Pythona do uruchamiania i analizy testów wydajności
Name:		python3-pyperf
Version:	2.9.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyperf/
Source0:	https://files.pythonhosted.org/packages/source/p/pyperf/pyperf-%{version}.tar.gz
# Source0-md5:	b5eaba731ba712c6e63f5ecc6a711ba6
URL:		https://pypi.org/project/pyperf/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:61
%if %{with tests}
BuildRequires:	python3-psutil >= 5.9.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python pyperf module is a toolkit to write, run and analyze
benchmarks.

%description -l pl.UTF-8
Moduł Pythona pyperf to zestaw narzędzi do tworzenia, uruchamiania i
analizy testów wydajności (benchmarków).

%package apidocs
Summary:	API documentation for Python pyperf module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pyperf
Group:		Documentation

%description apidocs
API documentation for Python pyperf module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pyperf.

%prep
%setup -q -n pyperf-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m unittest discover -s pyperf/tests
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pyperf/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.rst
%attr(755,root,root) %{_bindir}/pyperf
%{py3_sitescriptdir}/pyperf
%{py3_sitescriptdir}/pyperf-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_images,_static,*.html,*.js}
%endif
