Name: perl-XML-TreePP
Version: 0.43
Release: 2%{?dist}
Summary: Pure Perl implementation for parsing/writing XML documents
Group: Development/Libraries
License: GPL+ or Artistic
URL: http://search.cpan.org/dist/XML-TreePP
Source0: http://search.cpan.org/CPAN/authors/id/K/KA/KAWASAKI/XML-TreePP-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
BuildRequires: perl(ExtUtils::MakeMaker), perl(Test::More)
BuildRequires: perl(IO::Socket)
# Extra build requirements for tests (with $MORE_TESTS)
#BuildRequires: perl(HTTP::Lite)
#BuildRequires: perl(LWP::UserAgent::WithCache)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Pure Perl implementation for parsing/writing XML documents

%prep
%setup -q -n XML-TreePP-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT

chmod a-x Changes
chmod a-x $RPM_BUILD_ROOT/%{perl_vendorlib}/XML/TreePP.pm

%check
make %{?_smp_mflags} test || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README Changes
%dir %{perl_vendorlib}/XML/
%{perl_vendorlib}/XML/TreePP.pm
%{_mandir}/man3/XML::TreePP.3*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Marianne Lombard <marianne@tuxette.fr> - 0.43-1
- New version 

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-15
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.39-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.39-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.39-6
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.39-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Jun 27 2010 Jeroen van Meeuwen <jeroen.van.meeuwen@ergo-project.org> - 0.39-3
- Fix Source0 URL (#607878)
- Add extra build requirements for tests
- Fix executable permissions on some files (#607878)

* Sat Jun 19 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.39-1
- First package
