Name: perl-XML-FeedPP
Version: 0.43
Release: 1%{?dist}
Summary: Parse/write/merge/edit RSS/RDF/Atom syndication feeds
Group: Development/Libraries
License: GPL+ or Artistic
URL: http://search.cpan.org/dist/XML-FeedPP
Source0: http://www.cpan.org/modules/by-module/XML/XML-FeedPP-%{version}.tar.gz

BuildArch: noarch
BuildRequires: coreutils
BuildRequires: findutils
BuildRequires: make
BuildRequires: perl
BuildRequires: perl(Carp)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Encode)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(strict)
BuildRequires: perl(Test::More)
BuildRequires: perl(Time::Local)
BuildRequires: perl(vars)
BuildRequires: perl(XML::TreePP)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Parse/write/merge/edit RSS/RDF/Atom syndication feeds

%prep
%setup -q -n XML-FeedPP-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT

%check
make %{?_smp_mflags} test || :

%files
%doc README Changes
%dir %{perl_vendorlib}/XML/
%{perl_vendorlib}/XML/FeedPP.pm
%{_mandir}/man3/XML::FeedPP.3*

%changelog
* Thu Aug 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-1
- 0.43 bump
- Updated dependencies and spec

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-15
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.41-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.41-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.41-6
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.41-5
- Perl mass rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.41-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.41-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Jun 19 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.41-1
- First package
