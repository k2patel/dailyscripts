%define _httpd_apxs /usr/bin/apxs
%define httpd httpd

Summary:	mod_auth_urs for Apache
Name:		mod_jk
Version:	1.2.41
Release:	1%{?dist}
License:	Apache
Group:		Development/Java
URL:		http://tomcat.apache.org/
Source0:	http://www.apache.org/dist/tomcat/tomcat-connectors/jk/tomcat-connectors-1.2.41-src.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	%{httpd}-devel
Requires:	%{httpd}
Obsoletes:      mod_jk < %{epoch}:%{version}-%{release}
Provides:       mod_jk = %{epoch}:%{version}-%{release}
Obsoletes:      tomcat-mod < %{epoch}:%{version}-%{release}


%description
mod_jk allows Apache to serve as a front-end for Tomcat, GlassFish or any other
AJP1.3-enabled application server, with optional load-balancing.

%prep
%setup -q -n tomcat-connectors-%{version}-src
(cd native && %{__libtoolize} --copy --force)


%build
cd native
%configure \
  --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --target=x86_64-redhat-linux-gnu \
  --with-apxs=%{_httpd_apxs}
make
cd ..

%install
rm -rf %{buildroot}
 
mkdir -p %{buildroot}/%{httpd}/modules
mkdir -p %{buildroot}/%{httpd}/conf/
mkdir -p %{buildroot}/%{httpd}/conf.d/

%{__install} -D -m 755 native/apache-2.0/mod_jk.so %{buildroot}/%{_sysconfdir}/%{httpd}/modules/mod_jk.so
%{__install} -D -m 644 conf/workers.properties -D %{buildroot}/%{_sysconfdir}/%{httpd}/conf/workers.properties
%{__install} -D -m 644 conf/httpd-jk.conf -D %{buildroot}/%{_sysconfdir}/%{httpd}/conf.d/10_mod_jk.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc LICENSE NOTICE conf/workers.properties
%doc native/BUILDING.txt native/README.txt native/STATUS.txt native/TODO.txt
%config(noreplace) /%{_sysconfdir}/%{httpd}/conf.d/10_mod_jk.conf
%config(noreplace) /%{_sysconfdir}/%{httpd}/conf/workers.properties
/%{_sysconfdir}/%{httpd}/modules/mod_jk.so

%post
echo "Please see /etc/httpd/conf.d/10_mod_jk.conf for configuration option"

%preun
apxs -e -A -n jk_module $(apxs -q LIBEXECDIR)/mod_jk.so

%changelog
* Fri Dec 04 2015 Ketan Patel <patelkr@ornl.gov> - 1.1
- Please see detail list of changelog at https://tomcat.apache.org/connectors-doc/miscellaneous/changelog.html

