%define	module	dimp
%define	name	horde-%{module}
%define version 1.1.3
%define release %mkrel 3

%define _requires_exceptions pear(Horde.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde Dynamic Internet Messaging Program
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Requires(post):	rpm-helper
Requires:	horde >= 3.0
BuildArch:	noarch

%description
IMP is a project to create a version of IMP utilizing AJAX-like technologies to
allow a more dynamic user experience (thus DIMP... Dynamic IMP).

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Require all denied
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// DIMP Horde configuration file
//
 
$this->applications['dimp'] = array(
    'fileroot' => $this->applications['horde']['fileroot'] . '/dimp',
    'webroot' => $this->applications['horde']['webroot'] . '/dimp',
    'name' => _("Dynamic Mail"),
    'status' => 'notoolbar',
    'target' => '_parent',
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR js %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi

%files
%defattr(-,root,root)
%doc README COPYING docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}



%changelog
* Mon Aug 02 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.1.3-3mdv2011.0
+ Revision: 564908
- Increased release for rebuild

* Mon Nov 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.3-2mdv2010.1
+ Revision: 472086
- restrict default access permissions to localhost only, as per new policy

* Wed Sep 16 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.3-1mdv2010.0
+ Revision: 443650
- new version
- new files setup

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 1.1-3mdv2010.0
+ Revision: 437880
- rebuild

* Wed Nov 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1-2mdv2009.1
+ Revision: 304680
- fix automatic dependencies

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1-1mdv2009.1
+ Revision: 295326
- import horde-dimp


* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1-1mdv2009.1
- first mdv release
