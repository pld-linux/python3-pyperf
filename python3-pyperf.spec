#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"

Summary:	Python module to run and analyze benchmarks
Summary(pl.UTF-8):	Moduł Pythona do uruchamiania i analizy testów wydajności
Name:		python3-pyperf
Version:	2.0.0
Release:	4
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyperf/
Source0:	https://files.pythonhosted.org/packages/source/p/pyperf/pyperf-%{version}.tar.gz
# Source0-md5:	7f62d3f6fc5475138791d3d883fdf4cd
URL:		https://pypi.org/project/pyperf/
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
BuildRequires:	python3-psutil
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.4
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
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m nose pyperf/tests
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pyperf/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.rst
%attr(755,root,root) %{_bindir}/pyperf
%{py3_sitescriptdir}/pyperf
%{py3_sitescriptdir}/pyperf-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_images,_static,*.html,*.js}
%endif
