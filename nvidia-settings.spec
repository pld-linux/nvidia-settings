#
# Conditional build:
%bcond_without	nvidia_settings	# build the main package
%bcond_without	utils	# build utils from samples dir
%bcond_without	libXNVCtrl	# build libXNVCtrl for http://websvn.kde.org/trunk/kdenonbeta/nvidia/

Summary:	Tool for configuring the NVIDIA driver
Summary(pl.UTF-8):	Narzędzie do konfigurowania sterownika NVIDIA
Name:		nvidia-settings
Version:	295.40
Release:	1
License:	GPL
Group:		X11
Source0:	ftp://download.nvidia.com/XFree86/nvidia-settings/%{name}-%{version}.tar.bz2
# Source0-md5:	e9fd5dcb7f69c12334d199a783544d42
Source1:	%{name}.desktop
Source2:	%{name}.png
URL:		ftp://download.nvidia.com/XFree86/nvidia-settings/
BuildRequires:	OpenGL-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
%if %{with nvidia_settings}
BuildRequires:	gtk+2-devel
BuildRequires:	m4
BuildRequires:	pkgconfig
%endif
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

%package -n libXNVCtrl-devel
Summary:	libXNVCtrl development headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libXNVCtrl
Group:		Development/Libraries
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXxf86vm-devel
Obsoletes:	libXNVCtrl-static

%description -n libXNVCtrl-devel
Library for accessing NV-CONTROL extension in NVIDIA's latest drivers.

%description -n libXNVCtrl-devel -l pl.UTF-8
Biblioteka do obsługi rozszerzenia NV-CONTROL z najnowszych
sterowników NVIDIA.

%prep
%setup -q

%{__rm} src/libXNVCtrl/libXNVCtrl.a

%build
%if %{with libXNVCtrl}
%{__make} -C src/libXNVCtrl \
	NV_VERBOSE=1 \
	CC="%{__cc}" \
	X_CFLAGS="%{rpmcppflags} %{rpmcflags} -fPIC"
%endif

%if %{with utils}
%{__make} -C samples \
	NV_VERBOSE=1 \
	CC="%{__cc}" \
	OUTPUTDIR=$(pwd)/_out/utils \
	X_CFLAGS="%{rpmcppflags} %{rpmcflags} -fPIC"
%endif

%if %{with nvidia_settings}
%{__make} \
	NV_VERBOSE=1 \
	STRIP_CMD=: \
	CC="%{__cc}" \
	X_CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	X_LDFLAGS="%{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with nvidia_settings}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_desktopdir},%{_pixmapsdir}}
%{__make} install \
	INSTALL="install -p" \
	prefix=$RPM_BUILD_ROOT%{_prefix}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
%endif

%if %{with libXNVCtrl}
install -d $RPM_BUILD_ROOT%{_examplesdir}/libXNVCtrl-%{version} \
	$RPM_BUILD_ROOT{%{_libdir},%{_includedir}/NVCtrl}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/libXNVCtrl-%{version}
cp -p src/libXNVCtrl/NVCtrl.h $RPM_BUILD_ROOT%{_includedir}/NVCtrl
cp -p src/libXNVCtrl/NVCtrlLib.h $RPM_BUILD_ROOT%{_includedir}/NVCtrl
cp -p src/libXNVCtrl/libXNVCtrl.a $RPM_BUILD_ROOT%{_libdir}
%endif

%if %{with utils}
install -d $RPM_BUILD_ROOT%{_bindir}
for prog in _out/utils/nv-control-*; do
	case "$prog" in
	*.*)
		continue
		;;
	esac
	install -p $prog $RPM_BUILD_ROOT%{_bindir}
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with nvidia_settings}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nvidia-settings
%{_mandir}/man1/nvidia-settings.1*
%{_desktopdir}/nvidia-settings.desktop
%{_pixmapsdir}/nvidia-settings.png
%endif

%if %{with utils}
%attr(755,root,root) %{_bindir}/nv-control-3dvisionpro
%attr(755,root,root) %{_bindir}/nv-control-dpy
%attr(755,root,root) %{_bindir}/nv-control-dvc
%attr(755,root,root) %{_bindir}/nv-control-events
%attr(755,root,root) %{_bindir}/nv-control-framelock
%attr(755,root,root) %{_bindir}/nv-control-gvi
%attr(755,root,root) %{_bindir}/nv-control-info
%attr(755,root,root) %{_bindir}/nv-control-targets
%endif

%if %{with libXNVCtrl}
%files -n libXNVCtrl-devel
%defattr(644,root,root,755)
%doc doc/{FRAMELOCK,NV-CONTROL-API}.txt
%dir %{_includedir}/NVCtrl
%{_includedir}/NVCtrl/NVCtrl.h
%{_includedir}/NVCtrl/NVCtrlLib.h
%{_libdir}/libXNVCtrl.a
%{_examplesdir}/libXNVCtrl-%{version}
%endif
