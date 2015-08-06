%{?scl:%scl_package freeside}
%{!?scl:%global pkg_name %{name}}

%{!?version:%define version 4.0}
%{!?rt_version:%define rt_version XXXX}
%{!?release:%define release XXXX}

Summary: Freeside ISP Billing System
Name: %{?scl_prefix}freeside
Version: %{version}
Release: %{release}
License: AGPLv3
Group: Applications/Internet
URL: http://www.sisd.com/freeside/
Vendor: Freeside
Source: http://www.sisd.com/freeside/%{pkg_name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-root

# Patch0:		rt-%{rt_version}-config.diff
# Patch1:		rt-%{rt_version}-shebang.diff
# Patch2:		rt-%{rt_version}-Makefile.diff
# Patch3:		rt-%{rt_version}-test-dependencies.diff

BuildArch: noarch

Requires: %{?scl_prefix}%{pkg_name}-frontend
Requires: %{?scl_prefix}%{pkg_name}-backend

Requires: %{?scl_prefix}perl-Email-Sender
Requires: %{?scl_prefix}perl-Email-Sender-Transport-SMTP-TLS
Requires: %{?scl_prefix}perl-Log-Dispatch
Requires: %{?scl_prefix}perl(Apache::AuthCookie)

%if "%{_vendor}" != "suse"
Requires: tetex-latex
Requires: ghostscript
%else
Requires: te_latex
Requires: ghostscript-library
%endif

%{?_with_hylafax:Requires: %{?scl_prefix}perl-Fax-Hylafax-Client}

%{?scl:Requires: %{scl}-runtime}
BuildRequires: %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires: perl(ExtUtils::MakeMaker)

BuildRequires: %{?scl_prefix}perl(MemcacheDBI)
BuildRequires: %{?scl_prefix}perl(Apache::DBI)
BuildRequires: %{?scl_prefix}perl(Apache::Session)
BuildRequires: %{?scl_prefix}perl(Cache::Simple::TimedExpiry)
BuildRequires: %{?scl_prefix}perl(Class::Accessor)
BuildRequires: %{?scl_prefix}perl(Class::ReturnValue)
BuildRequires: %{?scl_prefix}perl(Convert::Color)
BuildRequires: %{?scl_prefix}perl(CSS::Squish)
BuildRequires: %{?scl_prefix}perl(Data::ICal)
BuildRequires: %{?scl_prefix}perl(DateTime::Locale)
BuildRequires: %{?scl_prefix}perl(DateTime)
BuildRequires: %{?scl_prefix}perl(DBD::Pg)
BuildRequires: %{?scl_prefix}perl(DBIx::SearchBuilder)
BuildRequires: %{?scl_prefix}perl(Devel::GlobalDestruction)
BuildRequires: %{?scl_prefix}perl(Devel::StackTrace)
BuildRequires: %{?scl_prefix}perl(Email::Address)
BuildRequires: %{?scl_prefix}perl(File::ShareDir)
BuildRequires: %{?scl_prefix}perl(HTML::FormatText)
BuildRequires: %{?scl_prefix}perl(HTML::Mason)
BuildRequires: %{?scl_prefix}perl(HTML::Quoted)
BuildRequires: %{?scl_prefix}perl(HTML::RewriteAttributes)
BuildRequires: %{?scl_prefix}perl(HTML::Scrubber)
BuildRequires: %{?scl_prefix}perl(HTML::TreeBuilder)
BuildRequires: %{?scl_prefix}perl(HTTP::Request::Common)
BuildRequires: %{?scl_prefix}perl(IPC::Run3)
BuildRequires: %{?scl_prefix}perl(JSON)
BuildRequires: %{?scl_prefix}perl(List::MoreUtils)
BuildRequires: %{?scl_prefix}perl(Locale::Maketext::Fuzzy)
BuildRequires: %{?scl_prefix}perl(Locale::Maketext::Lexicon)
BuildRequires: %{?scl_prefix}perl(Log::Dispatch)
BuildRequires: %{?scl_prefix}perl(LWP)
BuildRequires: %{?scl_prefix}perl(LWP::UserAgent)
BuildRequires: %{?scl_prefix}perl(Mail::Mailer)
BuildRequires: %{?scl_prefix}perl(MIME::Entity)
BuildRequires: %{?scl_prefix}perl(MIME::Types)
BuildRequires: %{?scl_prefix}perl(Module::Versions::Report)
BuildRequires: %{?scl_prefix}perl(Net::CIDR)
BuildRequires: %{?scl_prefix}perl(Regexp::Common)
BuildRequires: %{?scl_prefix}perl(Regexp::Common::net::CIDR)
BuildRequires: %{?scl_prefix}perl(Regexp::IPv6)
BuildRequires: %{?scl_prefix}perl(Term::ReadKey)
BuildRequires: %{?scl_prefix}perl(Text::Password::Pronounceable)
BuildRequires: %{?scl_prefix}perl(Text::Quoted)
BuildRequires: %{?scl_prefix}perl(Text::Template)
BuildRequires: %{?scl_prefix}perl(Text::WikiFormat)
BuildRequires: %{?scl_prefix}perl(Text::Wrapper)
BuildRequires: %{?scl_prefix}perl(Time::ParseDate)
BuildRequires: %{?scl_prefix}perl(Tree::Simple)
BuildRequires: %{?scl_prefix}perl(UNIVERSAL::require)
BuildRequires: %{?scl_prefix}perl(URI)
BuildRequires: %{?scl_prefix}perl(XML::RSS)
BuildRequires: %{?scl_prefix}perl(PerlIO::eol)
BuildRequires: %{?scl_prefix}perl(GnuPG::Interface)
Requires: %{?scl_prefix}perl(MemcacheDBI)

%define obsoletes_ver   4.0git_bh_dev
Obsoletes: %{?scl_prefix}%{pkg_name} <= %{obsoletes_ver}-%{release}



%if "%{_vendor}" != "suse"
%define apache_conffile		/etc/httpd/conf/httpd.conf
%define	apache_confdir		/etc/httpd/conf.d
%define	apache_version		2
%define freeside_document_root	/var/www/freeside
%define freeside_selfservice_document_root	/var/www/freeside-selfservice
%else
%define apache_conffile		/etc/apache2/uid.conf
%define	apache_confdir		/etc/apache2/conf.d
%define	apache_version		2
%define freeside_document_root	/srv/www/freeside
%define freeside_selfservice_document_root	/srv/www/freeside-selfservice
%endif
# Can change this back to /var/cache/subsys/freeside when cache relocation is fixed and released
%define freeside_cache		/etc/freeside
%define freeside_conf		/etc/freeside
%define freeside_export		/etc/freeside
%define freeside_lock		/var/lock/freeside
%define freeside_log		/var/log/freeside
%define freeside_socket		/etc/freeside
%define	rt_enabled		0
%define	fs_queued_user		fs_queue
%define	fs_api_user		    fs_api
%define	fs_selfservice_user	fs_selfservice
%define	fs_cron_user		fs_daily
%define	db_types		Pg mysql

%define texmflocal	/usr/share/texmf

%define _rpmlibdir	/usr/lib/rpm/
%define	rpmfiles	rpm

%description
Freeside is a flexible ISP billing system

%package mason
Summary: HTML::Mason interface for %{pkg_name}
Group: Applications/Internet
Prefix: %{freeside_document_root}
%if "%{_vendor}" != "suse"
Requires: mod_ssl
%endif
Requires: %{?scl_prefix}perl-Apache-DBI
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Obsoletes: %{?scl_prefix}%{pkg_name}-frontend <= %{obsoletes_ver}-%{release}
Provides: %{?scl_prefix}%{pkg_name}-frontend = %{version}-%{release}
BuildArch: noarch

%description mason
This package includes the HTML::Mason web interface for %{pkg_name}.
You should install only one %{pkg_name} web interface.

%package postgresql
Summary: PostgreSQL backend for %{pkg_name}
Group: Applications/Internet
Requires: %{?scl_prefix}perl-DBI
Requires: %{?scl_prefix}perl-DBD-Pg >= 1.32
Requires: %{?scl_prefix}%{pkg_name} = %{version}
Conflicts: %{?scl_prefix}%{pkg_name}-mysql
Obsoletes: %{?scl_prefix}%{pkg_name}-backend <= %{obsoletes_ver}
Provides: %{?scl_prefix}%{pkg_name}-backend = %{version}

%description postgresql
This package includes the PostgreSQL database backend for %{pkg_name}.
You should install only one %{pkg_name} database backend.
Please note that this RPM does not create the database or database user; it only installs the required drivers.

%package mysql
Summary: MySQL database backend for %{pkg_name}
Group: Applications/Internet
Requires: %{?scl_prefix}perl-DBI
Requires: %{?scl_prefix}perl-DBD-MySQL
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Conflicts: %{?scl_prefix}%{pkg_name}-postgresql
Obsoletes: %{?scl_prefix}%{pkg_name}-backend <= %{obsoletes_ver}-%{release}
Provides: %{?scl_prefix}%{pkg_name}-backend = %{version}-%{release}

%description mysql
This package includes the MySQL database backend for %{pkg_name}.
You should install only one %{pkg_name} database backend.
Please note that this RPM does not create the database or database user; it only installs the required drivers.

%package selfservice
Summary: Self-service interface for %{pkg_name}
Group: Applications/Internet
Obsoletes: %{?scl_prefix}%{pkg_name}-selfservice <= %{obsoletes_ver}-%{release}
Requires: %{?scl_prefix}%{pkg_name}-selfservice-cgi

%description selfservice
This package installs the Perl modules and CGI scripts for the self-service interface for %{pkg_name}.
For security reasons, it is set to conflict with %{pkg_name} as you should not install the billing system and self-service interface on the same computer.

%package selfservice-core
Summary: Core Perl libraries for the self-service interface for %{pkg_name}
Group: Applications/Internet
Obsoletes: %{?scl_prefix}%{pkg_name}-selfservice-core <= %{obsoletes_ver}-%{release}

%description selfservice-core
This package installs the Perl modules and client daemon for the self-service interface for %{pkg_name}.  It does not install the CGI interface and can be used with a different front-end.
For security reasons, it is set to conflict with %{pkg_name} as you should not install the billing system and self-service interface on the same computer.

%package selfservice-cgi
Summary: CGI scripts for the self-service interface for %{pkg_name}
Group: Applications/Internet
Requires: %{?scl_prefix}%{pkg_name}-selfservice-core
Obsoletes: %{?scl_prefix}%{pkg_name}-selfservice-cgi <= %{obsoletes_ver}-%{release}
Prefix: %{freeside_selfservice_document_root}

%description selfservice-cgi
This package installs the CGI scripts for the self-service interface for %{pkg_name}.  The scripts use some core libraries packaged in a separate RPM.
For security reasons, it is set to conflict with %{pkg_name} as you should not install the billing system and self-service interface on the same computer.

%package selfservice-php
Summary: Sample PHP files for the self-service interface for %{pkg_name}
Group: Applications/Internet
Obsoletes: %{?scl_prefix}%{pkg_name}-selfservice-php <= %{obsoletes_ver}-%{release}
Prefix: %{freeside_selfservice_document_root}

%description selfservice-php
This package installs the sample PHP scripts for the self-service interface for %{pkg_name}.
For security reasons, it is set to conflict with %{pkg_name} as you should not install the billing system and self-service interface on the same computer.

### %package rt4
### # rpm fails to add these
### Provides: %{?scl_prefix}perl(RT::Shredder::Exceptions)
### Provides: %{?scl_prefix}perl(RT::Shredder::Record)
### Provides: %{?scl_prefix}perl(RT::Shredder::Transaction)
### Provides: %{?scl_prefix}perl(RT::Tickets_SQL)
### 
### %description
### RT is an enterprise-grade ticketing system which enables a group of people
### to intelligently and efficiently manage tasks, issues, and requests submitted
### by a community of users.
### 
### %package rt4-mailgate
### Summary: rt4's mailgate utility
### Group:   Applications/Internet
### # rpm doesn't catch these:
### Requires:	%{?scl_prefix}perl(Pod::Usage)
### Requires:	%{?scl_prefix}perl(HTML::TreeBuilder)
### Requires:	%{?scl_prefix}perl(HTML::FormatText)
### %description rt-mailgate
### %{summary}
### 
### %package rt4-tests
### Summary:	Test suite for package rt4
### Group:		Development/Debug
### Requires:	%{name} = %{version}-%{release}
### Requires(postun): %{__rm}
### Requires:	/usr/bin/prove
### Requires:	%{?scl_prefix}perl(RT::Test)
### # rpm doesn't catch these:
### Requires:	%{?scl_prefix}perl(DBD::SQLite)
### Requires:	%{?scl_prefix}perl(GnuPG::Interface)
### Requires:	%{?scl_prefix}perl(PerlIO::eol)
### Requires:	%{?scl_prefix}perl(Plack::Handler::Apache2)
### # Bug: The testsuite unconditionally depends upon perl(GraphViz)
### Requires:	%{?scl_prefix}perl(GraphViz)
### 
### %description rt4-tests
### %{summary}
### 
### %postun rt4-tests
### if [ $1 -eq 0 ]; then
###   %{__rm} -rf %{perl_testdir}/%{name}
### fi
### 
### %package -n %{?scl_prefix}perl-RT-Test
### Summary: rt4's test utility module
### Group:   Applications/Internet
### Requires:	rt4 = %{version}-%{release}
### Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
### 
### %description -n %{?scl_prefix}perl-RT-Test
### %{summary}
### 

%prep
%setup -n %{pkg_name}-%{version} -q
%{__rm} -f bin/pod2x # Only useful to Ivan Kohler now
perl -pi -e 's|/usr/local/bin|%{_bindir}|g' FS/Makefile.PL
# RPM handles changing file ownership, so Makefile shouldn't
perl -pi -e 's/\s+-o\s+(freeside|root)(\s+-g\s+\$\{\w+\})?\s+/ /g' Makefile
perl -ni -e 'print if !/\s+chown\s+/;' Makefile

# Fix-ups for self-service.  Should merge this into Makefile
perl -pi -e 's|/usr/local/sbin|%{_sbindir}|g' FS/bin/freeside-selfservice-server
perl -pi -e 's|/usr/local/bin|%{_bindir}|g' fs_selfservice/FS-SelfService/Makefile.PL
perl -pi -e 's|/usr/local/sbin|%{_sbindir}|g' fs_selfservice/FS-SelfService/Makefile.PL
perl -pi -e 's|/usr/local/freeside|%{freeside_socket}|g' fs_selfservice/FS-SelfService/*.pm
perl -pi -e 's|socket\s*=\s*"/usr/local/freeside|socket = "%{freeside_socket}|g' fs_selfservice/FS-SelfService/freeside-selfservice-*
perl -pi -e 's|log_file\s*=\s*"/usr/local/freeside|log_file = "%{freeside_log}|g' fs_selfservice/FS-SelfService/freeside-selfservice-*
perl -pi -e 's|lock_file\s*=\s*"/usr/local/freeside|lock_file = "%{freeside_lock}|g' fs_selfservice/FS-SelfService/freeside-selfservice-*
# Comment out lines that use DBIx::DBSchema::ColGroup* modules
sed -i '/DBIx::DBSchema::ColGroup/ s/^/# /' bin/fix-sequences

# Get rid of the RT Apache conf file
rm htetc/freeside-rt.conf

# Fix-ups for SuSE
%if "%{_vendor}" == "suse"
perl -pi -e 's|htpasswd|/usr/sbin/htpasswd2|g if /system/;' FS/FS/access_user.pm
perl -pi -e 'print "Order deny,allow\nAllow from all\n" if /<Files/i;' htetc/freeside*.conf
%endif

# Override find-requires/find-provides to supplement Perl requires for HTML::Mason file handler.pl
%if 0%{?scl:1}
cat << \EOF > %{pkg_name}-req
#!/bin/sh
tee %{_tmppath}/filelist | %{_rpmlibdir}/rpmdeps --requires | grep -v -E 'perl\(the\)$' \
| grep -v -E 'perl\((lib|strict|vars|RT)\)$' \
| grep -v -E 'perl\(RT::' \
| grep -v -E 'perl\(FS::' \
| grep -v -E 'perl\(Term::Query' \
| grep -v -E 'perl\(config' \
| grep -v -E 'perl\(Debug' \
| grep -v -E 'perl\(API::Client' \
| grep -v -E 'perl\(AuthService' \
| sed -r 's/(^|\s)perl\(/\1perl516-perl\(/g' \
| sort -u | tee /tmp/rpmdeps.txt
grep handler.pl %{_tmppath}/filelist | xargs scl enable perl516 "%{__perl} -T %{_rpmlibdir}/perldeps.pl --requires" \
| grep -v -E 'perl\((lib|strict|vars|RT)\)$' \
| grep -v -E 'perl\(RT::' \
| grep -v -E 'perl\(Term::Query' \
| grep -v -E 'perl\(config' \
| grep -v -E 'perl\(Debug' \
| grep -v -E 'perl\(API::Client' \
| grep -v -E 'perl\(AuthService' \
| grep -v -E '^Requires:' \
| sed -r 's/(^|\s)perl\(/\1perl516-perl\(/g' \
| sort -u | tee /tmp/grepper.txt
EOF
%else 
cat << \EOF > %{pkg_name}-req
#!/bin/sh
tee %{_tmppath}/filelist | %{_rpmlibdir}/rpmdeps --requires | grep -v -E 'perl\(the\)$' \
| grep -v -E 'perl\((lib|strict|vars|RT)\)$' \
| grep -v -E 'perl\(RT::' \
| grep -v -E 'perl\(FS::' \
| grep -v -E 'perl\(Term::Query' \
| sort -u | tee /tmp/rpmdeps.txt
grep handler.pl %{_tmppath}/filelist | xargs %{__perl} -T %{_rpmlibdir}/perldeps.pl --requires \
| grep -v -E 'perl\((lib|strict|vars|RT)\)$' \
| grep -v -E 'perl\(RT::' \
| grep -v -E 'perl\(Term::Query' \
| sort -u | tee /tmp/grepper.txt
EOF
%endif

# Change she-bang line 
for FILE in `grep -rl '#!/usr/bin/perl' .`  
do
        sed -i '1 s&#!/usr/bin/perl.*&#!/usr/bin/env perl&' "$FILE"
done

%if 0%{?scl:1}
# Fix PATH in init script
perl -pi -e 's|/usr/local/bin|%{_bindir}|g' init.d/freeside-init
# Fix invocations in init script
sed -i 's/^  *\(freeside.*\)$/\tscl enable perl516 "\1"/g' init.d/freeside-init
sed -i 's/^  *\(\${SERVICE} \$QUEUED_USER.*\)$/\tscl enable perl516 "\1"/g' \
init.d/freeside-queued.init \
init.d/freeside-xmlrpcd.init \
init.d/freeside-torrus-srvderive.init \
init.d/freeside-sqlradius-radacctd.init \
init.d/freeside-prepaidd.init  \
init.d/freeside-cdrrewrited.init \
init.d/freeside-cdrrated.init \
init.d/freeside-cdrd.init
sed -i 's/^  *\(\${SERVICE} \$QUEUED_USER.*\)$/\tscl enable perl516 "\1"/g' init.d/freeside-prepaidd.init
sed -i 's/^  *\(\${SERVICE} collector.*\)$/\tscl enable perl516 "\1"/g' init.d/freeside-torrus.init
%endif

%define __find_provides %{_rpmlibdir}/rpmdeps --provides
%define __find_requires %{_builddir}/%{pkg_name}-%{version}/%{pkg_name}-req
%{__chmod} +x %{__find_requires}
%define _use_internal_dependency_generator 0

%build

# False laziness...
# The htmlman target now makes wiki documentation.  Let's pretend we made it.
touch htmlman
%{__make} alldocs

#perl -pi -e 's|%%%%%%VERSION%%%%%%|%{version}|g' FS/bin/*
cd FS
if [ "%{_vendor}" = "suse" ]; then
	CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL
else
	CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=$RPM_BUILD_ROOT%{_prefix} SITELIBEXP=$RPM_BUILD_ROOT%{perl_sitelib} SITEARCHEXP=$RPM_BUILD_ROOT%{perl_sitearch} INSTALLSCRIPT=$RPM_BUILD_ROOT%{_bindir}
fi
%{__make} OPTIMIZE="$RPM_OPT_FLAGS"
cd ..
    %{__make} perl-modules RT_ENABLED=%{rt_enabled} FREESIDE_CACHE=%{freeside_cache} FREESIDE_CONF=%{freeside_conf} FREESIDE_EXPORT=%{freeside_export} FREESIDE_LOCK=%{freeside_lock} FREESIDE_LOG=%{freeside_log} FREESIDE_DOCUMENT_ROOT=%{freeside_document_root}
    touch perl-modules

    pushd fs_selfservice/FS-SelfService
    if [ "%{_vendor}" = "suse" ]; then
        CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL
    else
        CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=$RPM_BUILD_ROOT%{_prefix} SITELIBEXP=$RPM_BUILD_ROOT%{perl_sitelib} SITEARCHEXP=$RPM_BUILD_ROOT%{perl_sitearch} INSTALLSCRIPT=$RPM_BUILD_ROOT%{_sbindir} DESTDIR=$RPM_BUILD_ROOT%{_prefix} INSTALLSITEBIN=/sbin INSTALLSITESCRIPT=/sbin

fi
# %{__make} OPTIMIZE="$RPM_OPT_FLAGS"
%{?scl:scl enable %{scl} "}
%{__make}
%{?scl:"}
popd

%if "%{rt_enabled}" == "1"
# %patch0 -p1
# %patch1 -p1
# %patch2 -p1
# %patch3 -p1
# %{__make} configure-rt RT_DOMAIN=RT_DOMAIN.NAME
%endif

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_document_root}

touch install-perl-modules perl-modules
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_cache}
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_conf}
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_export}
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_lock}
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_log}
for DBTYPE in %{db_types}; do
	%{__mkdir_p} $RPM_BUILD_ROOT/tmp
	[ -d $RPM_BUILD_ROOT%{freeside_conf}/default_conf ] && %{__rm} -rf $RPM_BUILD_ROOT%{freeside_conf}/default_conf
	%{__make} create-config DB_TYPE=$DBTYPE DATASOURCE=DBI:$DBTYPE:dbname=%{pkg_name} RT_ENABLED=%{rt_enabled} FREESIDE_CACHE=$RPM_BUILD_ROOT%{freeside_cache} FREESIDE_CONF=$RPM_BUILD_ROOT/tmp FREESIDE_EXPORT=$RPM_BUILD_ROOT%{freeside_export} FREESIDE_LOCK=$RPM_BUILD_ROOT%{freeside_lock} FREESIDE_LOG=$RPM_BUILD_ROOT%{freeside_log} DIST_CONF=$RPM_BUILD_ROOT%{freeside_conf}/default_conf
	%{__mv} $RPM_BUILD_ROOT/tmp/secrets $RPM_BUILD_ROOT%{freeside_conf}
	%{__rm} -rf $RPM_BUILD_ROOT/tmp
done
%{__rm} install-perl-modules perl-modules $RPM_BUILD_ROOT%{freeside_conf}/default_conf/ticket_system

touch docs
%{__perl} -pi -e "s|%%%%%%FREESIDE_DOCUMENT_ROOT%%%%%%|%{freeside_document_root}|g" htetc/handler.pl
%{__make} install-docs RT_ENABLED=%{rt_enabled} PREFIX=$RPM_BUILD_ROOT%{_prefix} TEMPLATE=mason FREESIDE_DOCUMENT_ROOT=$RPM_BUILD_ROOT%{freeside_document_root} MASON_HANDLER=$RPM_BUILD_ROOT%{freeside_conf}/handler.pl MASONDATA=$RPM_BUILD_ROOT%{freeside_cache}/masondata FREESIDE_EXPORT=$RPM_BUILD_ROOT%{freeside_export} FREESIDE_CONF=$RPM_BUILD_ROOT%{freeside_conf}
%{__perl} -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{freeside_conf}/handler.pl
%{__rm} docs

# Install the init scripts
%if 0%{?scl:1}
    %{__mkdir_p} $RPM_BUILD_ROOT%{_root_initddir}
    %{__make} install-init INSTALLGROUP=root INIT_FILE_PREPAIDD=$RPM_BUILD_ROOT%{_root_initddir}/freeside-prepaidd INIT_FILE_QUEUED=$RPM_BUILD_ROOT%{_root_initddir}/freeside-queued INIT_FILE_XMLRPCD=$RPM_BUILD_ROOT%{_root_initddir}/freeside-xmlrpcd INIT_FILE_CDRREWRITED=$RPM_BUILD_ROOT%{_root_initddir}/freeside-cdrrewrited INIT_FILE_CDRD=$RPM_BUILD_ROOT%{_root_initddir}/freeside-cdrd INIT_FILE_CDRRATED=$RPM_BUILD_ROOT%{_root_initddir}/freeside-cdrrated INIT_FILE_TORRUS_SRVDERIVE=$RPM_BUILD_ROOT%{_root_initddir}/freeside-torrus-srvderive INIT_FILE_SQLRADIUS_RADACCTD=$RPM_BUILD_ROOT%{_root_initddir}/freeside-sqlradius-radacctd INIT_FILE_TORRUS=$RPM_BUILD_ROOT%{_root_initddir}/freeside-torrus INIT_FILE_SELFSERVICE_SERVER=$RPM_BUILD_ROOT%{_root_initddir}/freeside-selfservice-server INIT_FILE_SELFSERVICE_XMLRPCD=$RPM_BUILD_ROOT%{_root_initddir}/freeside-selfservice-xmlrpcd INIT_FILE=$RPM_BUILD_ROOT%{_root_initddir}/%{pkg_name} QUEUED_USER=%{fs_queued_user} API_USER=%{fs_api_user} SELFSERVICE_USER=%{fs_selfservice_user} SELFSERVICE_MACHINES= INIT_INSTALL= INIT_INSTALL_QUEUED= INIT_INSTALL_PREPAIDD= INIT_INSTALL_XMLRPCD= INIT_INSTALL_CDRREWRITED= INIT_INSTALL_CDRD= INIT_INSTALL_CDRRATED= INIT_INSTALL_TORRUS_SRVDERIVE= INIT_INSTALL_TORRUS= INIT_INSTALL_SQLRADIUS_RADACCTD= INIT_INSTALL_SELFSERVICE_SERVER= INIT_INSTALL_SELFSERVICE_XMLRPCD=
    %{__perl} -pi -e "\
        s|/etc/default|/etc/sysconfig|g;\
        " $RPM_BUILD_ROOT%{_root_initddir}/%{pkg_name} \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-queued \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-xmlrpcd \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-cdrrewrited \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-cdrd \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-prepaidd \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-torrus-srvderive \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-sqlradius-radacctd \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-torrus \
        $RPM_BUILD_ROOT%{_root_initddir}/freeside-selfservice-xmlrpcd 
%else 
    %{__mkdir_p} $RPM_BUILD_ROOT%{_initddir}
    %{__make} install-init INSTALLGROUP=root INIT_FILE_QUEUED=$RPM_BUILD_ROOT%{_initddir}/freeside-queued INIT_FILE_PREPAIDD=$RPM_BUILD_ROOT%{_initddir}/freeside-prepaidd INIT_FILE_XMLRPCD=$RPM_BUILD_ROOT%{_initddir}/freeside-xmlrpcd INIT_FILE_CDRREWRITED=$RPM_BUILD_ROOT%{_initddir}/freeside-cdrrewrited INIT_FILE_CDRD=$RPM_BUILD_ROOT%{_initddir}/freeside-cdrd INIT_FILE_CDRRATED=$RPM_BUILD_ROOT%{_initddir}/freeside-cdrrated INIT_FILE_TORRUS_SRVDERIVE=$RPM_BUILD_ROOT%{_initddir}/freeside-torrus-srvderive INIT_FILE_SQLRADIUS_RADACCTD=$RPM_BUILD_ROOT%{_initddir}/freeside-sqlradius-radacctd INIT_FILE_TORRUS=$RPM_BUILD_ROOT%{_initddir}/freeside-torrus INIT_FILE_SELFSERVICE_XMLRPCD=$RPM_BUILD_ROOT%{_initddir}/freeside-selfservice-xmlrpcd INIT_FILE=$RPM_BUILD_ROOT%{_initddir}/%{pkg_name} QUEUED_USER=%{fs_queued_user} API_USER=%{fs_api_user} SELFSERVICE_USER=%{fs_selfservice_user} SELFSERVICE_MACHINES= INIT_INSTALL= INIT_INSTALL_QUEUED= INIT_INSTALL_PREPAIDD= INIT_INSTALL_XMLRPCD=INIT_INSTALL_CDRREWRITED= INIT_INSTALL_CDRD= INIT_INSTALL_CDRRATED= INIT_INSTALL_TORRUS_SRVDERIVE= INIT_INSTALL_TORRUS= INIT_INSTALL_SQLRADIUS_RADACCTD= INIT_INSTALL_SELFSERICE_XMLRPCD=
 
    %{__perl} -pi -e "\
        s|/etc/default|/etc/sysconfig|g;\
        " $RPM_BUILD_ROOT%{_initddir}/%{pkg_name} \
        $RPM_BUILD_ROOT%{_initddir}/freeside-queued \
        $RPM_BUILD_ROOT%{_initddir}/freeside-xmlrpcd \
        $RPM_BUILD_ROOT%{_initddir}/freeside-cdrrewrited \
        $RPM_BUILD_ROOT%{_initddir}/freeside-cdrd \
        $RPM_BUILD_ROOT%{_initddir}/freeside-prepaidd \
        $RPM_BUILD_ROOT%{_initddir}/freeside-torrus-srvderive \
        $RPM_BUILD_ROOT%{_initddir}/freeside-sqlradius-radacctd \
        $RPM_BUILD_ROOT%{_initddir}/freeside-torrus \
        $RPM_BUILD_ROOT%{_initddir}/freeside-selfservice-xmlrpcd
%endif

# Install the HTTPD configuration snippet for HTML::Mason
%{__mkdir_p} $RPM_BUILD_ROOT%{apache_confdir}
%{__make} install-apache FREESIDE_DOCUMENT_ROOT=%{freeside_document_root} RT_ENABLED=%{rt_enabled} APACHE_CONF=$RPM_BUILD_ROOT%{apache_confdir} APACHE_VERSION=%{apache_version} FREESIDE_CONF=%{freeside_conf} MASON_HANDLER=%{freeside_conf}/handler.pl
%{__perl} -pi -e 'print "Alias /%{pkg_name} %{freeside_document_root}\n\n" if /^<Directory/;' $RPM_BUILD_ROOT%{apache_confdir}/freeside-*.conf
%{__perl} -pi -e 'print "SSLRequireSSL\n" if /^AuthName/i;' $RPM_BUILD_ROOT%{apache_confdir}/freeside-*.conf

# Make lists of the database-specific configuration files
for DBTYPE in %{db_types}; do
	echo "%%attr(600,freeside,freeside) %%config(noreplace) %{freeside_conf}/secrets" > %{pkg_name}-%{version}-%{release}-$DBTYPE-filelist
	for DIR in `echo -e "%{freeside_conf}\n%{freeside_cache}\n%{freeside_export}\n" | sort | uniq`; do
		find $RPM_BUILD_ROOT$DIR -type f -print | \
			grep ":$DBTYPE:" | \
			sed "s@^$RPM_BUILD_ROOT@%%attr(640,freeside,freeside) %%config(noreplace) @g" >> %{pkg_name}-%{version}-%{release}-$DBTYPE-filelist
		find $RPM_BUILD_ROOT$DIR -type d -print | \
			grep ":$DBTYPE:" | \
			sed "s@^$RPM_BUILD_ROOT@%%attr(711,freeside,freeside) %%dir @g" >> %{pkg_name}-%{version}-%{release}-$DBTYPE-filelist
	done
	if [ "$(cat %{pkg_name}-%{version}-%{release}-$DBTYPE-filelist)X" = "X" ] ; then
		echo "ERROR: EMPTY FILE LIST"
		exit 1
	fi
done

# Make a list of the Mason files before adding self-service, etc.
echo "%attr(-,freeside,freeside) %{freeside_conf}/handler.pl" > %{pkg_name}-%{version}-%{release}-mason-filelist
find $RPM_BUILD_ROOT%{freeside_document_root} -type f -print | \
	sed "s@^$RPM_BUILD_ROOT@@g" >> %{pkg_name}-%{version}-%{release}-mason-filelist
if [ "$(cat %{pkg_name}-%{version}-%{release}-mason-filelist)X" = "X" ] ; then
	echo "ERROR: EMPTY FILE LIST"
	exit 1
fi

# Install all the miscellaneous binaries into /usr/share or similar
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}-%{version}/bin
%{__install} bin/* $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}-%{version}/bin

%if 0%{?scl:1}
    %{__mkdir_p} $RPM_BUILD_ROOT%{_root_sysconfdir}/sysconfig
    %{__install} %{rpmfiles}/freeside.sysconfig $RPM_BUILD_ROOT%{_root_sysconfdir}/sysconfig/%{pkg_name}
%else
    %{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
    %{__install} %{rpmfiles}/freeside.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{pkg_name}
%endif

%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_selfservice_document_root}
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/cgi
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/cgi/images
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/cgi/misc
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/php
%{__mkdir_p} $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/templates
%{__install} fs_selfservice/FS-SelfService/cgi/{*.cgi,*.html,*.gif} $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/cgi
%{__install} fs_selfservice/FS-SelfService/cgi/images/* $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/cgi/images
%{__install} fs_selfservice/FS-SelfService/cgi/misc/* $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/cgi/misc
%{__install} fs_selfservice/php/* $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/php
%{__install} fs_selfservice/FS-SelfService/*.template $RPM_BUILD_ROOT%{freeside_selfservice_document_root}/templates

# Install the main billing server Perl files
cd FS
eval `perl '-V:installarchlib'`

%{__mkdir_p} $RPM_BUILD_ROOT$installarchlib
%{?scl:scl enable %{scl} "}
%makeinstall PREFIX=$RPM_BUILD_ROOT%{_prefix}
%{?scl:"}
%{__rm} -f `find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist`

%if 0%{?scl:1}
    [ -x %{_rpmlibdir}/brp-compress ] && RPM_BUILD_ROOT=$RPM_BUILD_ROOT%{_scl_root} %{_rpmlibdir}/brp-compress
%else 
    [ -x %{_rpmlibdir}/brp-compress ] && %{_rpmlibdir}/brp-compress
%endif

find $RPM_BUILD_ROOT%{_prefix} -type f -print | \
	grep -v '/etc/freeside/conf' | \
	grep -v '/etc/freeside/secrets' | \
	sed "s@^$RPM_BUILD_ROOT@@g" > %{pkg_name}-%{version}-%{release}-filelist
if [ "$(cat %{pkg_name}-%{version}-%{release}-filelist)X" = "X" ] ; then
	echo "ERROR: EMPTY FILE LIST"
	exit 1
fi
cd ..

# Install the self-service interface Perl files
cd fs_selfservice/FS-SelfService
%{__mkdir_p} $RPM_BUILD_ROOT%{_prefix}/local/bin
%makeinstall
%{__rm} -f `find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist`

%if 0%{?scl:1}
    [ -x %{_rpmlibdir}/brp-compress ] && RPM_BUILD_ROOT=$RPM_BUILD_ROOT%{scl_root} %{_rpmlibdir}/brp-compress
%else
    [ -x %{_rpmlibdir}/brp-compress ] && %{_rpmlibdir}/brp-compress
%endif

find $RPM_BUILD_ROOT%{_prefix} -type f -print | \
	grep -v '/etc/freeside/conf' | \
	grep -v '/etc/freeside/secrets' | \
	sed "s@^$RPM_BUILD_ROOT@@g" > %{pkg_name}-%{version}-%{release}-temp-filelist
cat ../../FS/%{pkg_name}-%{version}-%{release}-filelist %{pkg_name}-%{version}-%{release}-temp-filelist | sort | uniq -u > %{pkg_name}-%{version}-%{release}-selfservice-core-filelist
if [ "$(cat %{pkg_name}-%{version}-%{release}-selfservice-core-filelist)X" = "X" ] ; then
	echo "ERROR: EMPTY FILE LIST"
	exit 1
fi
cd ../..

# Install the Apache configuration file for self-service
%{__install} %{rpmfiles}/freeside-selfservice.conf $RPM_BUILD_ROOT%{apache_confdir}/%{pkg_name}-selfservice.conf
%{__perl} -pi -e "s|%%%%%%FREESIDE_SELFSERVICE_DOCUMENT_ROOT%%%%%%|%{freeside_selfservice_document_root}|g" $RPM_BUILD_ROOT%{apache_confdir}/%{pkg_name}-selfservice.conf

# This is part of Makefile's install-texmf.  The rest is in triggers.  These files are not in the filelist
# %{__install} -D etc/fslongtable.sty $RPM_BUILD_ROOT%{texmflocal}/tex/generic/fslongtable.sty

%if "%{rt_enabled}" == "1"
%{?scl:scl enable %{scl} "}
# %{__make} install-rt PERL=%{__perl}
%{?scl:"}
%endif

%pre
if ! %{__id} freeside &>/dev/null; then
%if "%{_vendor}" == "suse"
	/usr/sbin/groupadd freeside
%endif
	/usr/sbin/useradd -m freeside
fi

%pre mason
if ! %{__id} freeside &>/dev/null; then
%if "%{_vendor}" == "suse"
	/usr/sbin/groupadd freeside
%endif
	/usr/sbin/useradd -m freeside
fi

%pre postgresql
if ! %{__id} freeside &>/dev/null; then
%if "%{_vendor}" == "suse"
	/usr/sbin/groupadd freeside
%endif
	/usr/sbin/useradd -m freeside
fi

%pre mysql
if ! %{__id} freeside &>/dev/null; then
%if "%{_vendor}" == "suse"
	/usr/sbin/groupadd freeside
%endif
	/usr/sbin/useradd -m freeside
fi

%pre selfservice-cgi
if ! %{__id} freeside &>/dev/null; then
%if "%{_vendor}" == "suse"
	/usr/sbin/groupadd freeside
%endif
	/usr/sbin/useradd -m freeside
fi

%post
if [ -x /sbin/chkconfig ]; then
	/sbin/chkconfig --add freeside
fi
#if [ $1 -eq 2 -a -x /usr/bin/freeside-upgrade ]; then
#	/usr/bin/freeside-upgrade
#fi

%post postgresql
if [ -f %{freeside_conf}/secrets ]; then
	perl -p -i.fsbackup -e 's/^DBI:.*?:/DBI:Pg:/' %{freeside_conf}/secrets
fi

%post mysql
if [ -f %{freeside_conf}/secrets ]; then
	perl -p -i.fsbackup -e 's/^DBI:.*?:/DBI:mysql:/' %{freeside_conf}/secrets
fi

%post mason
# Make local httpd run with User/Group = freeside
if [ -f %{apache_conffile} ]; then
%if "%{_vendor}" != "suse"
	perl -p -i.fsbackup -e 's/^(User|Group) .*/$1 freeside/' %{apache_conffile}
%else
	perl -p -i.fsbackup -e 's/^(User) .*/$1 freeside/' %{apache_conffile}
%endif
fi
# Fix up environment so pslatex will run
%if "%{_vendor}" == "suse"
if ! %{__grep} TEXINPUTS /etc/profile.local >/dev/null; then
	echo "unset TEXINPUTS" >>/etc/profile.local
fi
if ! %{__grep} TEXINPUTS /etc/init.d/apache2 >/dev/null; then
	perl -p -i.fsbackup -e 'print "unset TEXINPUTS\n\n" if /^httpd_conf\s*=\s*/;' /etc/init.d/apache2
fi
%endif

%triggerin -- tetex 
#texhash `kpsewhich -expand-var \$TEXMFLOCAL`
texhash %{texmflocal}

%clean
%{__rm} -rf %{buildroot}

%files -f FS/%{pkg_name}-%{version}-%{release}-filelist
%if "%{rt_enabled}" == "1"
# %{apache_confdir}/freeside-rt.conf
%endif
%if 0%{?scl:1}
    %attr(0711,root,root) %{_root_initddir}/%{pkg_name}
    %attr(0711,root,root) %{_root_initddir}/freeside-queued
    %attr(0711,root,root) %{_root_initddir}/freeside-prepaidd
    %attr(0711,root,root) %{_root_initddir}/freeside-xmlrpcd
    %attr(0711,root,root) %{_root_initddir}/freeside-cdrrewrited
    %attr(0711,root,root) %{_root_initddir}/freeside-cdrd
    %attr(0711,root,root) %{_root_initddir}/freeside-cdrrated
    # %attr(0711,root,root) %{_root_initddir}/freeside-torrus-srvderive
    # %attr(0711,root,root) %{_root_initddir}/freeside-torrus
    %attr(0711,root,root) %{_root_initddir}/freeside-sqlradius-radacctd
    %attr(0711,root,root) %{_root_initddir}/freeside-selfservice-xmlrpcd
    %attr(0711,root,root) %{_root_initddir}/freeside-selfservice-server
    %attr(0644,root,root) %config(noreplace) %{_root_sysconfdir}/sysconfig/%{pkg_name}
%else
    %attr(0711,root,root) %{_initddir}/%{pkg_name}
    %attr(0711,root,root) %{_initddir}/freeside-queued
    %attr(0711,root,root) %{_initddir}/freeside-prepaidd
    %attr(0711,root,root) %{_initddir}/freeside-xmlrpcd
    %attr(0711,root,root) %{_initddir}/freeside-cdrrewrited
    %attr(0711,root,root) %{_initddir}/freeside-cdrd
    %attr(0711,root,root) %{_initddir}/freeside-cdrrated
    # %attr(0711,root,root) %{_initddir}/freeside-torrus-srvderive
    # %attr(0711,root,root) %{_initddir}/freeside-torrus
    %attr(0711,root,root) %{_initddir}/freeside-sqlradius-radacctd
    %attr(0711,root,root) %{_initddir}/freeside-selfservice-xmlrpcd
    %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{pkg_name}
    %attr(0600,freeside,freeside) %config(noreplace) %{_sysconfdir}/sysconfig/%{pkg_name}/secrets
%endif
%defattr(-,freeside,freeside,-)
# %doc README INSTALL CREDITS AGPL
%doc README CREDITS AGPL
%attr(-,freeside,freeside) %dir %{freeside_conf}
%attr(-,freeside,freeside) %dir %{freeside_lock}
%attr(-,freeside,freeside) %dir %{freeside_log}
%attr(0711,freeside,freeside) %config(noreplace) %{freeside_conf}/default_conf
%attr(0644,freeside,freeside) %config(noreplace) %{freeside_conf}/default_conf/*
# %attr(444,root,root) %{texmflocal}/tex/generic/fslongtable.sty
# %{freeside_conf}/htpasswd.logout

%files mason -f %{pkg_name}-%{version}-%{release}-mason-filelist
%defattr(-, freeside, freeside, 0755)
%attr(-,freeside,freeside) %{freeside_cache}/masondata
%attr(0644,root,root) %config(noreplace) %{apache_confdir}/%{pkg_name}-base%{apache_version}.conf

%files postgresql -f %{pkg_name}-%{version}-%{release}-Pg-filelist

%files mysql -f %{pkg_name}-%{version}-%{release}-mysql-filelist

%files selfservice
%defattr(-, freeside, freeside, 0644)
%attr(0644,root,root) %config(noreplace) %{apache_confdir}/%{pkg_name}-selfservice.conf

%files selfservice-core -f fs_selfservice/FS-SelfService/%{pkg_name}-%{version}-%{release}-selfservice-core-filelist
%defattr(-, freeside, freeside, 0644)
%attr(-,freeside,freeside) %dir %{freeside_socket}
%attr(-,freeside,freeside) %dir %{freeside_lock}
%attr(-,freeside,freeside) %dir %{freeside_log}

%files selfservice-cgi
%defattr(-, freeside, freeside, 0644)
%attr(0711,freeside,freeside) %{freeside_selfservice_document_root}/cgi
%attr(0644,freeside,freeside) %{freeside_selfservice_document_root}/templates

%files selfservice-php
%defattr(-, freeside, freeside, 0644)
%attr(0755,freeside,freeside) %{freeside_selfservice_document_root}/php

%changelog
* Tue May 26 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-60
- New build of Freeside RPM (-60) (doran@bluehost.com)

* Tue Apr 14 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-59
- New build, includes SCT-1211, SCT-1800, and others (doran@bluehost.com)

* Fri Mar 20 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-58
- New build (-58) (doran@bluehost.com)

* Thu Mar 19 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-57
- New build (-57) (doran@bluehost.com)

* Thu Mar 19 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-56
- New build (-56) (doran@bluehost.com)

* Wed Mar 18 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-55
- New build (-55) (doran@bluehost.com)

* Thu Feb 12 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-54
- New build (-54) (doran@bluehost.com)

* Fri Jan 23 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-53
- New build (-53) (doran@bluehost.com)

* Thu Jan 22 2015 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-52
- New build (-52) (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-51
- Added init.d/freeside-selfservice-service to %%files. New build (51)
  (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-50
- New build (50) (doran@bluehost.com)
- Commented torrus packages from files (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com>
- Commented torrus packages from files (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-49
- Stupid space after a backslash. New build (49) (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-48
- Added INIT_INSTALL_SELFSERVICE_SERVER make override. New build (48)
  (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-47
- Added missing INIT_FILE_SELFSERVICE_SERVER make override. New build
  (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-46
- New build (46) (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-45
- New build (45) (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-44
- New build (44) (doran@bluehost.com)

* Mon Dec 08 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-43
- New build (43) (doran@bluehost.com)

* Mon Sep 29 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-42
- Fixed a lovely sed line (doran@bluehost.com)

* Mon Sep 29 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-41
- Added freeside-queued to the %%files section (doran@bluehost.com)

* Mon Sep 29 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-40
- Added INIT_INSTALL_QUEUED= to spec file to disable the normal chkconfig call
  (doran@bluehost.com)

* Mon Sep 29 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-39
- Fixed the init-install paths for sane RPM build (doran@bluehost.com)

* Mon Sep 29 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-38
- New build (38) (doran@bluehost.com)

* Wed Sep 24 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-37
- New build (37) (doran@bluehost.com)

* Wed Sep 24 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-36
- New build! (doran@bluehost.com)

* Fri Sep 19 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-35
- Fine-tuned Requires (doran@bluehost.com)

* Fri Sep 19 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-34
- new package built with tito

* Fri Sep 19 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-33
- Added version dependencies (doran@bluehost.com)

* Wed Sep 10 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-32
- New build (32) (fozz@iodynamics.com)

* Thu Aug 14 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-31
- New build (31) - includes merge with freeside_github/master
  (fozz@iodynamics.com)

* Thu Aug 14 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-30
- New build (30) (fozz@iodynamics.com)

* Wed Aug 13 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-29
- New build (29) (fozz@iodynamics.com)

* Wed Aug 13 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-28
- New build (28) (fozz@iodynamics.com)

* Mon Aug 11 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-27
- New build (27) (fozz@iodynamics.com)

* Tue Aug 05 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-26
- New build (26) with super minor bug fix (fozz@iodynamics.com)

* Mon Aug 04 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-25
- Fixed bug in FS::Record. New build -25. (fozz@iodynamics.com)

* Mon Aug 04 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-24
- New build (Includes Project40178) of Freeside (-24) (fozz@iodynamics.com)

* Fri Jul 18 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-23
- New build of freeside: -23 (fozz@iodynamics.com)

* Thu Jul 17 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-22
- New build: -22 (fozz@iodynamics.com)

* Thu Jul 17 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-21
- New build: -21 (fozz@iodynamics.com)

* Mon Jul 07 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-20
- Added noreplace config to secrets file TWeaked PATH in freeside-init
  (fozz@iodynamics.com)

* Tue Jul 01 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-19
- New build: -19 (fozz@iodynamics.com)

* Tue Jun 10 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-18
- New spec file for -18 (fozz@iodynamics.com)
- New build -18 (fozz@iodynamics.com)

* Tue Jun 10 2014 Doran Barton <fozz@iodynamics.com>
- New build -18 (fozz@iodynamics.com)

* Mon Jun 09 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-17
- New build: -17     - Uses MemcacheDBI     - Better error handling for DB
  errors     - Config::General secrets format (fozz@iodynamics.com)

* Wed Apr 23 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-16
- Changed Release to 16. Woops. (fozz@iodynamics.com)
- Turned rt_enabled off (fozz@iodynamics.com)
- Merge branch 'master' of ssh://git.bluehost.com/gitroot/ul-perl-scl
  (fozz@iodynamics.com)
- Automatic commit of package [freeside] minor release [4.0git_bh_dev-15].
  (doran@bluehost.com)

* Wed Apr 23 2014 Doran Barton <fozz@iodynamics.com>
- Turned rt_enabled off (fozz@iodynamics.com)
- Merge branch 'master' of ssh://git.bluehost.com/gitroot/ul-perl-scl
  (fozz@iodynamics.com)
- Automatic commit of package [freeside] minor release [4.0git_bh_dev-15].
  (doran@bluehost.com)

* Wed Apr 23 2014 Doran Barton <fozz@iodynamics.com>
- Turned rt_enabled off (fozz@iodynamics.com)
- Merge branch 'master' of ssh://git.bluehost.com/gitroot/ul-perl-scl
  (fozz@iodynamics.com)
- Automatic commit of package [freeside] minor release [4.0git_bh_dev-15].
  (doran@bluehost.com)

* Wed Apr 23 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-15
- Turned rt_enabled off (fozz@iodynamics.com)
* Tue Mar 18 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-15
- Migrated some (overdue) code from perl514 to perl516 (fozz@iodynamics.com)

* Tue Mar 11 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-14
- Removed dependency on AuthSystem and DBIx::DBSchema::ColGroup*
  (fozz@iodynamics.com)
- Merge branch 'master' of ssh://git.bluehost.com/gitroot/ul-perl-scl
  (doran@bluehost.com)
- New source tarball (fozz@iodynamics.com)

* Mon Mar 10 2014 Doran Barton <doran@bluehost.com> 4.0git_bh_dev-13
- Updated release (doran@bluehost.com)

* Mon Mar 10 2014 Unknown name
- 

* Thu Feb 27 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-12
- Bumping release to 12 (fozz@iodynamics.com)
- Rebuilt tarball with correct paths (fozz@iodynamics.com)

* Thu Feb 27 2014 Doran Barton <fozz@iodynamics.com>
- Rebuilt tarball with correct paths (fozz@iodynamics.com)

* Thu Feb 27 2014 Doran Barton <fozz@iodynamics.com>
- Rebuilt tarball with correct paths (fozz@iodynamics.com)

* Thu Feb 27 2014 Doran Barton <fozz@iodynamics.com>
- Rebuilt tarball with correct paths (fozz@iodynamics.com)

* Wed Feb 26 2014 Doran Barton <fozz@iodynamics.com> 4.0git_bh_dev-11
- new package built with tito

* Mon Apr 22 2013 Doran Barton <doran@bluehost.com> - 1.9-9
- Updated for Freeside 3.0 

* Thu Jun 11 2009 Richard Siddall <richard.siddall@elirion.net> - 1.9-8
- Since configuration is now kept in the RDBMS, don't install a configuration folder

* Mon Dec 22 2008 Richard Siddall <richard.siddall@elirion.net> - 1.9-5
- Modifications to make self-service work if you really insist on installing it on the same machine as Freeside

* Tue Dec 9 2008 Richard Siddall <richard.siddall@elirion.net> - 1.9-4
- Cleaning up after rpmlint

* Tue Aug 26 2008 Richard Siddall <richard.siddall@elirion.net> - 1.9-3
- More revisions for self-service interface

* Sat Aug 23 2008 Richard Siddall <richard.siddall@elirion.net> - 1.7.3-2
- Revisions for self-service interface
- RT support is still missing

* Sun Jul 8 2007 Richard Siddall <richard.siddall@elirion.net> - 1.7.3
- Updated for upcoming Freeside 1.7.3
- RT support is still missing

* Fri Jun 29 2007 Richard Siddall <richard.siddall@elirion.net> - 1.7.2
- Updated for Freeside 1.7.2
- Removed support for Apache::ASP

* Wed Oct 12 2005 Richard Siddall <richard.siddall@elirion.net> - 1.5.7
- Added self-service package

* Sun Feb 06 2005 Richard Siddall <richard.siddall@elirion.net> - 1.5.0pre6-1
- Initial package
