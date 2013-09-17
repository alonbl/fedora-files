#
# otopi -- plugable installer
# Copyright (C) 2012-2013 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

Summary:	oVirt Task Oriented Pluggable Installer/Implementation (%{name})
Name:		otopi
Version:	1.1.1
Release:	1
License:	LGPLv2+
URL:		http://www.ovirt.org
Source:		http://resources.ovirt.org/releases/3.3/src/%{name}-%{version}.tar.gz
Group:		Development/Libraries

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Requires:	python
BuildRequires:	gettext
BuildRequires:	python2-devel
BuildRequires:	java-devel

BuildRequires:	apache-commons-logging
BuildRequires:	junit
BuildRequires:	maven-compiler-plugin
BuildRequires:	maven-enforcer-plugin
BuildRequires:	maven-install-plugin
BuildRequires:	maven-jar-plugin
BuildRequires:	maven-javadoc-plugin
BuildRequires:	maven-source-plugin
BuildRequires:	maven-surefire-provider-junit4
BuildRequires:	maven-local

%description
Standalone plugin based installation framework to be used to setup
system components. The plugin nature provides simplicity to
add new installation functionality without the complexity of the state
and transaction management.

%package java
Summary:	%{name} java support
Requires:	%{name} = %{version}-%{release}
Requires:	java
Requires:	apache-commons-logging
Requires:	jpackage-utils

%description java
java libraries.

%package javadoc
Summary:	Javadocs for %{name}
Group:		Documentation

%description javadoc
This package contains the API documentation for %{name}.

%package devtools
Summary:	%{name} development tools
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-devel < 1.1.1-1
Provides:	%{name}-devel = %{version}-%{release}
%description devtools
Development tools for %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
%configure \
	--docdir="%{_docdir}/%{name}-%{version}" \
	--disable-python-syntax-check \
	--enable-java-sdk \
	--disable-java-sdk-compile \
	--with-local-version="%{name}-%{version}-%{release}" \
	%{?conf}
make %{?_smp_mflags}

cd src/java
%mvn_build
cd ../..

%install
rm -rf "%{buildroot}"
make %{?_smp_mflags} install DESTDIR="%{buildroot}"

cd src/java
%mvn_install
cd ../..

install -d -m 755 "%{buildroot}%{_sysconfdir}/%{name}.conf.d"

%files
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/plugins
%dir %{_sysconfdir}/%{name}.conf.d
%doc AUTHORS
%doc COPYING
%doc README
%doc README.API
%doc README.dialog
%doc README.environment
%{_datadir}/%{name}/plugins/%{name}/
%{_sbindir}/%{name}
%{python_sitelib}/%{name}/

%files java -f src/java/.mfiles
%dir %{_javadir}/%{name}

%files javadoc -f src/java/.mfiles-javadoc

%files devtools
%{_datadir}/%{name}/%{name}-bundle
%{python_sitelib}/%{name}/codegen/

%changelog
* Tue Sep 17 2013 Alon Bar-LEv <alonbl@redhat.com> - 1.1.1-1
- rename devel->devtools
- own %{_javadir}/%{name}

* Mon Aug 26 2013 Alon Bar-Lev <alonbl@redhat.com> - 1.1.0-1
- Release.

* Thu Feb 14 2013 Alon Bar-Lev <alonbl@redhat.com> - 1.0.0-1
- Release.

* Sat Oct 13 2012 Alon Bar-Lev <alonbl@redhat.com> - 1.0.0-0.1_beta
- Initial add.
