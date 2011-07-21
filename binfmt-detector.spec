Summary:	Microsoft PE executable type detector
Summary(pl.UTF-8):	Detector typu plików wykonywalnych PE Microsoftu
Name:		binfmt-detector
Version:	0.2
Release:	4
License:	GPL
Group:		Base
Source0:	http://team.pld-linux.org/~wolf/%{name}.tar.gz
# Source0-md5:	d6e9d6d8888b58c97eb65875853fd778
Source1:	%{name}.init
Source2:	binfmt-detector.upstart
Patch0:		spelling.patch
Patch1:		libdir.patch
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Conflicts:	wine < 1:0.9.12-2
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
%patch0 -p1
%patch1 -p1

%build
%{__cc} %{rpmldflags} %{rpmcflags} binfmt-detector-cli.c -o binfmt-detector

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},/etc/{rc.d/init.d,init}}

install -p binfmt-detector $RPM_BUILD_ROOT%{_libdir}
install -p binfmt-detector.sh $RPM_BUILD_ROOT%{_bindir}/binfmt-detector
sed -i -e 's,/usr/lib,%{_libdir},' $RPM_BUILD_ROOT%{_bindir}/binfmt-detector
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/binfmt-detector
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/init/%{name}.conf

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
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(754,root,root) /etc/init/%{name}.conf
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}
