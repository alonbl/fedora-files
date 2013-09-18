#
# ovirt-host-deploy -- ovirt host deployer
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

%global		ovirt_host_deploy_root %{_datadir}/%{name}/interface-3

Summary:	oVirt host deploy tool
Name:		ovirt-host-deploy
Version:	1.1.1
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://www.ovirt.org
Source:		http://resources.ovirt.org/releases/stable/3.3/%{name}-%{version}.tar.gz
Group:		Applications/System

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Requires:	python
Requires:	otopi
BuildRequires:	gettext
BuildRequires:	otopi-devel
BuildRequires:	python2-devel
BuildRequires:	java-devel

BuildRequires:	maven-compiler-plugin
BuildRequires:	maven-enforcer-plugin
BuildRequires:	maven-install-plugin
BuildRequires:	maven-jar-plugin
BuildRequires:	maven-javadoc-plugin
BuildRequires:	maven-source-plugin
BuildRequires:	maven-local

%description
Host deployment tool for oVirt project.

%package java
Summary:	%{name} java support
Requires:	%{name} = %{version}-%{release}
Requires:	java

Requires:	otopi-java
%description java
java libraries.

%package javadoc
Summary:	Javadocs for %{name}
Group:		Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
%configure \
	--docdir="%{_docdir}/%{name}-%{version}" \
	--disable-python-syntax-check \
	--enable-java-sdk \
	--with-local-version="%{name}-%{version}-%{release}" \
	--disable-java-sdk-compile \
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
%dir %{ovirt_host_deploy_root}
%dir %{ovirt_host_deploy_root}/pythonlib
%doc AUTHORS
%doc COPYING
%doc README
%doc README.environment
%{_datadir}/%{name}/plugins/%{name}/
%{_datadir}/otopi/plugins/%{name}
%{_sbindir}/%{name}
%{ovirt_host_deploy_root}/.bundled
%{ovirt_host_deploy_root}/otopi
%{ovirt_host_deploy_root}/otopi-plugins
%{ovirt_host_deploy_root}/ovirt-host-deploy
%{ovirt_host_deploy_root}/pythonlib/otopi
%{ovirt_host_deploy_root}/pythonlib/ovirt_host_deploy
%{ovirt_host_deploy_root}/setup
%{python_sitelib}/ovirt_host_deploy/

%files java -f src/java/.mfiles
%dir %{_javadir}/%{name}

%files javadoc -f src/java/.mfiles-javadoc

%changelog
* Wed Sep 18 2013 Alon Bar-Lev <alonbl@redhat.com> - 1.1.1-1
- Release.

* Mon Aug 26 2013 Alon Bar-Lev <alonbl@redhat.com> - 1.1.0-1
- Release.

* Thu Feb 14 2013 Alon Bar-Lev <alonbl@redhat.com> - 1.0.0-1
- Release.

* Sat Oct 13 2012 Alon Bar-Lev <alonbl@redhat.com> - 1.0.0-0.1_beta
- Initial add.
