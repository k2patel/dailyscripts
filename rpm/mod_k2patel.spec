Summary: mod_k2patel for Apache
Name: mod-auth-urs
Version: 1.1
Release: 1
License: Apache
Group: System Environment/Daemons
URL: http://<some URL>
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: httpd-devel
Requires: httpd httpd-devel

%description
An Apache HTTPD module that provides authentication services.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -m0755 -d $RPM_BUILD_ROOT$(apxs -q LIBEXECDIR)
make DESTDIR=$RPM_BUILD_ROOT install
install -m0644 -D mod_k2patel.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/mod_k2patel.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/mod_k2patel.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_k2patel.conf

%post
/usr/sbin/apxs -e -A -n rpaf $(apxs -q LIBEXECDIR)/mod_k2patel.so

%preun
/usr/sbin/apxs -e -A -n rpaf $(apxs -q LIBEXECDIR)/mod_k2patel.so


%changelog
* Fri Dec 04 2015 Ketan Patel <k2patel@gmail.com> - 1.1
- Please see detail list of changelog at https://<some_url>
