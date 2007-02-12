#
# Conditional build:
%bcond_without	nvidia_settings	# build the main package
%bcond_without	libXNVCtrl	# build libXNVCtrl for http://websvn.kde.org/trunk/kdenonbeta/nvidia/
#
%define		_buildid	20061219
%define		_rel	2
Summary:	Tool for configuring the NVIDIA driver
Summary(pl.UTF-8):   Narzędzie do konfigurowania sterownika NVIDIA
Name:		nvidia-settings
Version:	1.0
Release:	0.%{_buildid}.%{_rel}
License:	GPL
Group:		X11
Source0:	ftp://download.nvidia.com/XFree86/nvidia-settings/%{name}-%{version}.tar.gz
# Source0-md5:	414a838f01093ceb0ae8535c35e21eac
Patch0:		libXNVCtrl-shared.patch
Patch1:		%{name}-xlibs.patch
URL:		ftp://download.nvidia.com/XFree86/nvidia-settings/
BuildRequires:	XFree86-devel
%if %{with nvidia_settings}
BuildRequires:	gtk+2-devel
BuildRequires:	m4
BuildRequires:	pkgconfig
%endif
Requires:	libXNVCtrl = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The `nvidia-settings` utility is a tool for configuring the NVIDIA
Linux graphics driver. It operates by communicating with the NVIDIA X
driver, querying and updating state as appropriate. This communication
is done with the NV-CONTROL X extension.

Values such as brightness and gamma, XVideo attributes, temperature,
and OpenGL settings can be queried and configured via nvidia-settings.

When nvidia-settings starts, it reads the current settings from its
configuration file and sends those settings to the X server. Then, it
displays a graphical user interface (GUI) interface for configuring
the current settings. When nvidia-settings exits, it queries the
current settings from the X server and saves them to the configuration
file.

%description -l pl.UTF-8
Narzędzie nvidia-settings służy do konfiguracji sterownika do kart
graficznych firmy NVIDIA. Działa komunikując się ze sterownikiem X
NVIDIA, sprawdzając i uaktualniając stan w razie potrzeby. Komunikacja
odbywa się poprzez rozszerzenie X NV-CONTROL.

Za pomocą nvidia-settings można odczytywać i zmieniać wartości takie
jak jasność i korekcja gamma, atrybuty XVideo, temperatura barw i
ustawienia OpenGL.

Przy uruchamianiu nvidia-settings odczytuje bieżące ustawienia z pliku
konfiguracyjnego i wysyła te ustawienia do serwera X. Następnie
wyświetla graficzny interfejs użytkownika (GUI) do konfiguracji
ustawień. Przy wyłączniu nvidia-settings odczytuje bieżące ustawienia
z serwera X i zapisuje je do pliku konfiguracyjnego.

%package -n libXNVCtrl
Summary:	libXNVCtrl library
Summary(pl.UTF-8):   Biblioteka libXNVCtrl
Group:		Libraries

%description -n libXNVCtrl
Library for accessing NV-CONTROL extension in NVIDIA's latest drivers.

%description -n libXNVCtrl -l pl.UTF-8
Biblioteka do obsługi rozszerzenia NV-CONTROL z najnowszych
sterowników NVIDIA.

%package -n libXNVCtrl-devel
Summary:	libXNVCtrl development headers
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki libXNVCtrl
Group:		Development/Libraries
Requires:	XFree86-devel
Requires:	libXNVCtrl = %{version}-%{release}

%description -n libXNVCtrl-devel
Development headers for libXNVCtrl.

%description -n libXNVCtrl-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libXNVCtrl.

%package -n libXNVCtrl-static
Summary:	libXNVCtrl static library
Summary(pl.UTF-8):   Biblioteka statyczna libXNVCtrl
Group:		Development/Libraries
Requires:	libXNVCtrl-devel = %{version}-%{release}

%description -n libXNVCtrl-static
Static library for libXNVCtrl.

%description -n libXNVCtrl-static -l pl.UTF-8
Biblioteka statyczna libXNVCtrl.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%if %{with libXNVCtrl}
cd src/libXNVCtrl
xmkmf
%{__make} clean
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"
cd ../..
%endif

%if %{with nvidia_settings}
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with nvidia_settings}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install nvidia-settings $RPM_BUILD_ROOT%{_bindir}
install doc/nvidia-settings.1 $RPM_BUILD_ROOT%{_mandir}/man1/nvidia-settings.1
%endif

%if %{with libXNVCtrl}
install -d $RPM_BUILD_ROOT%{_examplesdir}/libXNVCtrl-%{version}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/libXNVCtrl-%{version}
%{__make} install \
	-C src/libXNVCtrl \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libXNVCtrl -p /sbin/ldconfig
%postun	-n libXNVCtrl -p /sbin/ldconfig

%if %{with nvidia_settings}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/*
%endif

%if %{with libXNVCtrl}
%files -n libXNVCtrl
%defattr(644,root,root,755)
%attr(755,root,root) /usr/X11R6/%{_lib}/libXNVCtrl.so.*.*.*

%files -n libXNVCtrl-devel
%defattr(644,root,root,755)
%doc doc/{FRAMELOCK,NV-CONTROL-API}.txt
/usr/X11R6/include/X11/extensions/NVCtrl.h
/usr/X11R6/include/X11/extensions/NVCtrlLib.h
/usr/X11R6/%{_lib}/libXNVCtrl.so
%{_examplesdir}/libXNVCtrl-%{version}

%files -n libXNVCtrl-static
%defattr(644,root,root,755)
/usr/X11R6/%{_lib}/libXNVCtrl.a
%endif
