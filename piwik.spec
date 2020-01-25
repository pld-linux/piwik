%define		php_min_version 5.1.3
Summary:	Open source web analytics
Name:		piwik
Version:	1.6
Release:	0.1
License:	GPL v3 and other OSS licenses
Group:		Applications/WWW
Source0:	http://piwik.org/latest.zip
# Source0-md5:	04c5dc7f595adce4d68be9f94bbb140c
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://www.piwik.org
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-pdo-mysql
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	php-gd
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# bad depsolver
%define		_noautopear	pear
# exclude optional php dependencies
%define		_noautophp	php-curl
# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
Piwik is a downloadable, open source (GPL licensed) real time web
analytics software program. It provides you with detailed reports on
your website visitors: the search engines and keywords they used, the
language they speak, your popular pages... and so much more.

Piwik aims to be an open source alternative to Google Analytics, and
is already used on more than 200,000 websites.

%prep
%setup -qc

# relocate for simplier install and doc section
mv %{name}/{config,misc} .
mv %{name}/{LEGALNOTICE,README} .

# common license
rm misc/gpl-3.0.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a %{name}/* $RPM_BUILD_ROOT%{_appdir}

cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LEGALNOTICE README misc
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
