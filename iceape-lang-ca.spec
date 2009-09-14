%define	_lang	ca
%define	_reg	AD
%define _lare	%{_lang}-%{_reg}
Summary:	Catalan resources for Iceape
Summary(ca.UTF-8):	Recursos catalans per a Iceape
Summary(es.UTF-8):	Recursos catalanes para Iceape
Summary(pl.UTF-8):	Katalońskie pliki językowe dla Iceape
Name:		iceape-lang-%{_lang}
Version:	1.1.15
Release:	3
License:	GPL
Group:		I18n
Source0:	http://releases.mozilla.org/pub/mozilla.org/seamonkey/releases/%{version}/contrib-localized/seamonkey-%{version}.%{_lare}.langpack.xpi
# Source0-md5:	46e6d08cafe2e852fe0d8f77444fd848
Source1:	http://www.mozilla-enigmail.org/download/release/0.96/enigmail-%{_lare}-0.96.xpi
# Source1-md5:	b2305f139f1f2c816acbd38c5d3eff7f
Source2:	gen-installed-chrome.sh
URL:		http://www.seamonkey-project.org/
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zip
Requires(post,postun):	iceape >= %{version}
Requires(post,postun):	textutils
Requires:	iceape >= %{version}
Obsoletes:	mozilla-lang-ca
Obsoletes:	seamonkey-lang-ca
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_chromedir	%{_datadir}/iceape/chrome

%description
Catalan resources for Iceape.

%description -l ca.UTF-8
Recursos catalans per a Iceape.

%description -l es.UTF-8
Recursos catalanes para Iceape.

%description -l pl.UTF-8
Katalońskie pliki językowe dla Iceape.

%prep
%setup -qc
%{__unzip} -o -qq %{SOURCE1}
install %{SOURCE2} .
./gen-installed-chrome.sh locale \
	chrome/{%{_reg},%{_lare},%{_lang}-unix,enigmail-%{_lare}}.jar \
		> lang-%{_lang}-installed-chrome.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chromedir}

install chrome/{%{_reg},%{_lare},%{_lang}-unix,enigmail-%{_lare}}.jar \
	$RPM_BUILD_ROOT%{_chromedir}
install lang-%{_lang}-installed-chrome.txt $RPM_BUILD_ROOT%{_chromedir}
cp -r searchplugins defaults $RPM_BUILD_ROOT%{_datadir}/iceape

# rebrand locale for iceape
cd $RPM_BUILD_ROOT%{_chromedir}
unzip %{_lare}.jar locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm
sed -i -e 's/SeaMonkey/Iceape/g;' locale/%{_lare}/branding/brand.dtd \
	locale/%{_lare}/branding/brand.properties locale/%{_lare}/communicator/search/default.htm
zip -0 %{_lare}.jar locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm
rm -f locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/iceape-chrome+xpcom-generate

%postun
%{_sbindir}/iceape-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%{_chromedir}/%{_reg}.jar
%{_chromedir}/%{_lare}.jar
%{_chromedir}/%{_lang}-unix.jar
%{_chromedir}/enigmail-%{_lare}.jar
%{_chromedir}/lang-%{_lang}-installed-chrome.txt
%{_datadir}/iceape/searchplugins/*
%{_datadir}/iceape/defaults/profile/%{_reg}
