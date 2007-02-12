Summary:	Microsoft PE executable type detector
Summary(pl.UTF-8):	Detector typu plików wykonywalnych PE Microsoftu
Name:		binfmt-detector
Version:	0.1
Release:	3
License:	GPL
Group:		Base
Source0:	http://team.pld-linux.org/~wolf/%{name}.tar.gz
# Source0-md5:	11623bddbeb536e88c47c8a1aedc9189
Source1:	%{name}.init
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Conflicts:	wine <= 1:0.9.12-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This utility determines the Microsoft PE executable file's type
(Native, .NET CLR) and runs it using the appropriate runtime (Wine,
Mono).

It is inteded to be used in a Linux binfmt configuration, since binfmt
itself is incapable of reliably distinguishing between various PE file
types (since they have no different "magic string") and runtimes
refuse to run files which they don't support (CLR runtimes refuse to
run Native images and vice versa).

%description -l pl.UTF-8
To narzędzie określa typ pliku wykonywalnego PE Microsoftu (natywny,
.NET CLR) i uruchamia odpowiednie środowisko wykonawcze (Wine, Mono).

Jest używane w połączeniu z linuksowym binfmt, ponieważ samo binfmt
nie jest w stanie odróżnić różnych typów plików PE (nie zawierają one
różnych "magicznych ciągów"), a środowiska uruchomieniowe nie
pozwalają uruchomić nieobsługiwanych przez siebie plików (CLR nie
uruchamia natywnych obrazów i vice versa).

%prep
%setup -q -n %{name}

%build
%{__cc} %{rpmcflags} binfmt-detector-cli.c -o binfmt-detector-cli

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/rc.d/init.d}

install binfmt-detector-cli $RPM_BUILD_ROOT%{_bindir}
install binfmt-detector.sh $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/binfmt-detector

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add binfmt-detector
%service binfmt-detector restart

%preun
if [ "$1" = "0" ]; then
	%service binfmt-detector stop
	/sbin/chkconfig --del binfmt-detector
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/binfmt-detector
