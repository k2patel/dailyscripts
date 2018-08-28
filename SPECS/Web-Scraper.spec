# Supported rpmbuild options:
#
# --with live-test/--without live-test
#   include/exclude LIVE_TEST testsuite
#   Default: --without (Requires networking, doesn't work in mock)
%bcond_with     live_test

Name:           perl-Web-Scraper
Version:        0.38
Release:        3%{?dist}
Summary:        Web Scraping Toolkit using HTML and CSS Selectors or XPath expressions
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Web-Scraper/
Source0:        http://www.cpan.org/authors/id/M/MI/MIYAGAWA/Web-Scraper-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl(base)
BuildRequires:  perl(Module::Build::Tiny) >= 0.039
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::Selector::XPath) >= 0.03
BuildRequires:  perl(HTML::Tagset)
BuildRequires:  perl(HTML::TreeBuilder) >= 3.23
BuildRequires:  perl(HTML::TreeBuilder::XPath) >= 0.08
# BuildRequires:  perl(HTML::TreeBuilder::LibXML) >= 0.13
BuildRequires:  perl(List::Util)
BuildRequires:  perl(LWP) >= 5.827
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Base)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(UNIVERSAL::require)
BuildRequires:  perl(URI)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XML::XPathEngine) >= 0.08
BuildRequires:  perl(YAML)
BuildRequires:  perl(strict)

# Required by the testsuite
BuildRequires:  /bin/ps

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# rpm's deptracker misses these:
Requires:  perl(LWP::UserAgent)

%{?perl_default_filter}

%description
Web::Scraper is a web scraper toolkit, inspired by Ruby's equivalent
Scrapi. It provides a DSL-ish interface for traversing HTML documents and
returning a neatly arranged Perl data structure.

%prep
%setup -q -n Web-Scraper-%{version}

# Package does not depend on ExtUtils::MakeMaker
sed -i '/ExtUtils::MakeMaker/d' META.*

%build
%{__perl} Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=$RPM_BUILD_ROOT --create_packlist=0

# Web-Scraper >= 0.38 misses to install bin/scaper
# Install it manually
install -m 755 -d ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 bin/scraper ${RPM_BUILD_ROOT}%{_bindir}

find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
LEAK_TEST=1 %{?with_live_test:LIVE_TEST=1} ./Build test

%files
%doc Changes README
%{_bindir}/scraper
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-2
- Perl 5.22 rebuild

* Thu Oct 23 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.38-1
- Upstream update.
- Fix bogus %%changelog entry.
- Reflect upstream having changed to Build.PL.
- Work-around to upstream having missed to install bin/scrapper.

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.37-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.37-1
- Upstream update.

* Tue Aug 07 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.36-2
- R: perl(LWP::UserAgent).
- Make live tests working (Add Web-Scraper-0.36-testsuite-hacks.patch).
- BR: /bin/ps.

* Tue Jul 10 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.36-1.20120710.0
- Merge in Xavier's spec.

* Sat Jan 21 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.36-1.20120121.0
- More deps.
- Add %%{?perl_default_filter}.

* Mon Dec 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.36-1
- Upstream update.
- Add --with/without live-test (disabled by default).

* Wed Mar 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.34-1
- Upstream update.
- Spec cleanup.

* Tue Dec 21 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.32-1
- Initial Fedora package.
