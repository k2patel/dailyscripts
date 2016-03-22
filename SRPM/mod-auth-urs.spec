Summary: mod_auth_urs for Apache
Name: mod-auth-urs
Version: 1.1
Release: 1
License: Apache
Group: System Environment/Daemons
URL: https://git.earthdata.nasa.gov/scm/aam/apache-urs-authentication-module.git
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: httpd-devel
Requires: httpd httpd-devel

%description
An Apache HTTPD module that provides URS authentication services.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -m0755 -d $RPM_BUILD_ROOT$(apxs -q LIBEXECDIR)
make DESTDIR=$RPM_BUILD_ROOT install
install -m0644 -D mod_auth_urs.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/mod_auth_urs.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/mod_auth_urs.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_auth_urs.conf

%post
echo "Please see /etc/httpd/conf.d/mod_auth_urs.conf for configuration option"

%preun
apxs -e -A -n auth_urs_module $(apxs -q LIBEXECDIR)/mod_auth_urs.so

%changelog
* Fri Dec 04 2015 Ketan Patel <k2patel@live.com> - 1.1
- Please see detail list of changelog at https://git.earthdata.nasa.gov/projects/AAM/repos/apache-urs-authentication-module/commits
