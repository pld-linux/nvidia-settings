#
# Conditional build:
%bcond_without	gtk3		# GTK+ 3.x GUI library for nvidia-settings
%bcond_without	nvidia_settings	# build the main package
%bcond_without	utils		# build utils from samples dir
%bcond_without	libXNVCtrl	# build libXNVCtrl for external packages

Summary:	Tool for configuring the NVIDIA driver
Summary(pl.UTF-8):	Narzędzie do konfigurowania sterownika NVIDIA
Name:		nvidia-settings
# keep the version in sync with xorg-driver-video-nvidia.spec
Version:	384.59
Release:	1
License:	GPL v2 (with MIT parts)
Group:		X11/Applications
Source0:	https://download.nvidia.com/XFree86/nvidia-settings/%{name}-%{version}.tar.bz2
# Source0-md5:	18a45291de0c93aae27c70eee40a5665
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	%{name}-autostart.desktop
URL:		ftp://download.nvidia.com/XFree86/nvidia-settings/
BuildRequires:	OpenGL-devel
BuildRequires:	libvdpau-devel >= 1.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
%if %{with nvidia_settings}
BuildRequires:	gtk+2-devel >= 2.0
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	jansson-devel >= 2.2
BuildRequires:	m4
BuildRequires:	pkgconfig
%endif
Requires:	%{name}-guilib = %{version}-%{release}
Requires:	libvdpau >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# requires symbols from main binary
%define		skip_post_check_so	libnvidia-gtk[23].so.*

%description
The nvidia-settings utility is a tool for configuring the NVIDIA Linux
graphics driver. It operates by communicating with the NVIDIA X
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

%package gtk2
Summary:	GTK+ 2.x GUI library for nvidia-settings
Summary(pl.UTF-8):	Biblioteka interfejsu graficznego GTK+ 2.x dla nvidia-settings
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-guilib = %{version}-%{release}

%description gtk2
GTK+ 2.x GUI library for nvidia-settings.

%description gtk2 -l pl.UTF-8
Biblioteka interfejsu graficznego GTK+ 2.x dla nvidia-settings.

%package gtk3
Summary:	GTK+ 3.x GUI library for nvidia-settings
Summary(pl.UTF-8):	Biblioteka interfejsu graficznego GTK+ 3.x dla nvidia-settings
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-guilib = %{version}-%{release}

%description gtk3
GTK+ 3.x GUI library for nvidia-settings.

%description gtk3 -l pl.UTF-8
Biblioteka interfejsu graficznego GTK+ 3.x dla nvidia-settings.

%package -n libXNVCtrl-devel
Summary:	libXNVCtrl development files
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libXNVCtrl
License:	MIT
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

%build
%if %{with libXNVCtrl}
%{__make} -C src/libXNVCtrl \
	NV_VERBOSE=1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -fPIC"
%endif

%if %{with utils}
%{__make} -C samples \
	NV_VERBOSE=1 \
	CC="%{__cc}" \
	OUTPUTDIR=$(pwd)/_out/utils \
	X_CFLAGS="%{rpmcppflags} %{rpmcflags} -fPIC"
%endif

%if %{with nvidia_settings}
%{__make} -C src \
	%{!?with_gtk3:BUILD_GTK3LIB=} \
	NV_USE_BUNDLED_LIBJANSSON=0 \
	NV_VERBOSE=1 \
	STRIP_CMD=: \
	CC="%{__cc}" \
	X_CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	X_LDFLAGS="%{rpmldflags}"

%{__make} -C doc \
	NV_VERBOSE=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with nvidia_settings}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_desktopdir},%{_pixmapsdir},/etc/xdg/autostart}
%{__make} install \
	NV_USE_BUNDLED_LIBJANSSON=0 \
	NV_VERBOSE=1 \
	INSTALL="install -p" \
	LIBDIR="$RPM_BUILD_ROOT%{_libdir}" \
	PREFIX=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/xdg/autostart/%{name}.desktop

# let RPM autogenerate deps
chmod 755 $RPM_BUILD_ROOT%{_libdir}/lib*.so*
%endif

%if %{with libXNVCtrl}
install -d $RPM_BUILD_ROOT%{_examplesdir}/libXNVCtrl-%{version} \
	$RPM_BUILD_ROOT{%{_libdir},%{_includedir}/NVCtrl}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/libXNVCtrl-%{version}
cp -p src/libXNVCtrl/nv_control.h $RPM_BUILD_ROOT%{_includedir}/NVCtrl
cp -p src/libXNVCtrl/NVCtrl.h $RPM_BUILD_ROOT%{_includedir}/NVCtrl
cp -p src/libXNVCtrl/NVCtrlLib.h $RPM_BUILD_ROOT%{_includedir}/NVCtrl
cp -p src/libXNVCtrl/libXNVCtrl.a $RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_pkgconfigdir}/libXNVCtrl.pc
prefix=%{_prefix}
libdir=%{_libdir}
includedir=${prefix}/include/NVCtrl

Name: libXNVCtrl
Description: Library for accessing NV-CONTROL extension in NVIDIA's latest drivers.
Version: %{version}
Libs: -L${libdir} -lXNVCtrl
Cflags: -I${includedir}
EOF
#'
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

%post	gtk2 -p /sbin/ldconfig
%postun	gtk2 -p /sbin/ldconfig

%post	gtk3 -p /sbin/ldconfig
%postun	gtk3 -p /sbin/ldconfig

%if %{with nvidia_settings}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nvidia-settings
%if %{with utils}
%attr(755,root,root) %{_bindir}/nv-control-3dvisionpro
%attr(755,root,root) %{_bindir}/nv-control-dpy
%attr(755,root,root) %{_bindir}/nv-control-dvc
%attr(755,root,root) %{_bindir}/nv-control-events
%attr(755,root,root) %{_bindir}/nv-control-framelock
%attr(755,root,root) %{_bindir}/nv-control-gvi
%attr(755,root,root) %{_bindir}/nv-control-info
%attr(755,root,root) %{_bindir}/nv-control-targets
%attr(755,root,root) %{_bindir}/nv-control-warpblend
%endif
%{_mandir}/man1/nvidia-settings.1*
%{_desktopdir}/nvidia-settings.desktop
%{_pixmapsdir}/nvidia-settings.png
/etc/xdg/autostart/%{name}.desktop

%files gtk2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvidia-gtk2.so.%{version}

%if %{with gtk3}
%files gtk3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvidia-gtk3.so.%{version}
%endif
%endif

%if %{with libXNVCtrl}
%files -n libXNVCtrl-devel
%defattr(644,root,root,755)
%doc doc/{FRAMELOCK,NV-CONTROL-API}.txt
%{_libdir}/libXNVCtrl.a
%{_includedir}/NVCtrl
%{_pkgconfigdir}/libXNVCtrl.pc
%{_examplesdir}/libXNVCtrl-%{version}
%endif
