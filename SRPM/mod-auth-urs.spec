Summary: mod_auth_urs for Apache
Name: mod-auth-urs
Version: 1.2.1
Release: 2
License: Apache
Group: System Environment/Daemons
URL: https://git.earthdata.nasa.gov/scm/aam/apache-urs-authentication-module.git
Source0: %{name}-%{version}.tar.gz
Source1: URS_db
Source2: mod_auth_urs.conf
Source3: mod_auth_web_dav.conf
Source4: URS_Wevdav_example.conf
Source5: URS_Wevdav_SSL_example.conf
Source6: content.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: httpd-devel python-flask-wtf python-flask sqlite-devel openssl-devel
Requires: httpd python-flask-wtf python-flask sqlite openssl apr-util-sqlite mod_wsgi mod_ssl

%description
An Apache HTTPD module that provides URS authentication services.
It now support WevDAV.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -m0755 -d $RPM_BUILD_ROOT$(apxs -q LIBEXECDIR)
make DESTDIR=$RPM_BUILD_ROOT install
install -m0644 -D %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.d/mod_auth_urs.conf
install -m0644 -D %{SOURCE3} $RPM_BUILD_ROOT/etc/httpd/conf.d/mod_auth_web_dav.conf
install -m0644 -D %{SOURCE4} $RPM_BUILD_ROOT/etc/httpd/conf.d/URS_Wevdav_example.conf
install -m0644 -D %{SOURCE5} $RPM_BUILD_ROOT/etc/httpd/conf.d/URS_Wevdav_SSL_example.conf
mkdir -p $RPM_BUILD_ROOT/usr/local/share/urs_dav_content
tar -xvf %{SOURCE6} -C $RPM_BUILD_ROOT/usr/local/share/urs_dav_content --strip-components=1
mkdir -p $RPM_BUILD_ROOT/tmp/session
cp %{SOURCE1} $RPM_BUILD_ROOT/tmp/session/db
mkdir -p $RPM_BUILD_ROOT/var/tmp/urs/session

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/mod_auth_urs.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_auth_urs.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_auth_web_dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/URS_Wevdav_example.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/URS_Wevdav_SSL_example.conf
%dir /usr/local/share/urs_dav_content
/usr/local/share/urs_dav_content/*
%dir /tmp/session/
/tmp/session/*
%dir /var/tmp/urs/session/

%post
echo "Please see /etc/httpd/conf.d/mod_auth_urs.conf for configuration option"
echo "Required files for webpages are located in '/usr/local/share/urs_dav_content'"
echo "You require to copy most of the files to your Website directory" 

%preun
apxs -e -A -n auth_urs_module $(apxs -q LIBEXECDIR)/mod_auth_urs.so


%changelog
* Thu Feb 02 2017 Ketan Patel <patelkr@ornl.gov> - 1.2.1-2
- Added missing content to /usr/local/share folder so it can be copied.
- updated echo to provide those information.
* Wed Feb 01 2017 Ketan Patel <patelkr@ornl.gov> - 1.2.1
- Added support for the webdav
* Fri Dec 04 2015 Ketan Patel <patelkr@ornl.gov> - 1.1
- Please see detail list of changelog at https://git.earthdata.nasa.gov/projects/AAM/repos/apache-urs-authentication-module/commits
