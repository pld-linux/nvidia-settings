#
# Conditional build:
%bcond_with	nvidia_settings	# build the main package
%bcond_without	libXNVCtrl	# build libXNVCtrl for http://websvn.kde.org/trunk/kdenonbeta/nvidia/
#
Summary:	Tool for configuring the NVIDIA driver
Name:		nvidia-settings
Version:	1.0
Release:	0.3
License:	GPL
Group:		X11
Source0:	ftp://download.nvidia.com/XFree86/nvidia-settings/%{name}-%{version}.tar.gz
# Source0-md5:	e6025e7fe05162c4608333702895f97c
Patch0:		libXNVCtrl-shared.patch
Patch1:		%{name}-xlibs.patch
URL:		ftp://download.nvidia.com/XFree86/nvidia-settings/
%if %{with nvidia_settings}
#BuildRequires:	XFree86-devel
#BuildRequires:	XFree86-libs
#BuildRequires:	fontconfig
#BuildRequires:	freetype2
#BuildRequires:	glib2-devel
#BuildRequires:	libatk-devel
#BuildRequires:	libgtk+2-devel
#BuildRequires:	libpango-devel
#BuildRequires:	pkgconfig
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

%description -l pl
Narzêdzie nvidia-settings s³u¿y do konfiguracji sterownika do kart
graficznych firmy NVIDIA. Dzia³a komunikuj±c siê ze sterownikiem X
NVIDIA, sprawdzaj±c i uaktualniaj±c stan w razie potrzeby. Komunikacja
odbywa siê poprzez rozszerzenie X NV-CONTROL.

Za pomoc± nvidia-settings mo¿na odczytywaæ i zmieniaæ warto¶ci takie
jak jasno¶æ i korekcja gamma, atrybuty XVideo, temperatura barw i
ustawienia OpenGL.

Przy uruchamianiu nvidia-settings odczytuje bie¿±ce ustawienia z pliku
konfiguracyjnego i wysy³a te ustawienia do serwera X. Nastêpnie
wy¶wietla graficzny interfejs u¿ytkownika (GUI) do konfiguracji
ustawieñ. Przy wy³±czniu nvidia-settings odczytuje bie¿±ce ustawienia
z serwera X i zapisuje je do pliku konfiguracyjnego.

%package -n libXNVCtrl
Summary:	libXNVCtrl library
Summary(pl):	Biblioteka libXNVCtrl
Group:		Libraries

%description -n libXNVCtrl
Library for accessing NV-CONTROL extension in NVIDIA's latest drivers.

%description -n libXNVCtrl -l pl
Biblioteka do obs³ugi rozszerzenia NV-CONTROL z najnowszych
sterowników NVIDIA.

%package -n libXNVCtrl-devel
Summary:	libXNVCtrl development headers
Summary(pl):	Pliki nag³ówkowe biblioteki libXNVCtrl
Group:		Development/Libraries
Requires:	libXNVCtrl = %{version}-%{release}
Requires:	XFree86-devel

%description -n libXNVCtrl-devel
Development headers for libXNVCtrl.

%description -n libXNVCtrl-devel -l pl
Pliki nag³ówkowe biblioteki libXNVCtrl.

%package -n libXNVCtrl-static
Summary:	libXNVCtrl static library
Summary(pl):	Biblioteka statyczna libXNVCtrl
Group:		Developmment/Libraries
Requires:	libXNVCtrl-devel = %{version}-%{release}

%description -n libXNVCtrl-static
Static library for libXNVCtrl.

%description -n libXNVCtrl-static -l pl
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
%{__make}
cd ../..
%endif

%if %{with nvidia_settings}
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with nvidia_settings}
install -d $RPM_BUILD_ROOT%{_bindir}
install nvidia-settings $RPM_BUILD_ROOT%{_bindir}
%endif

%if %{with libXNVCtrl}
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
%doc doc/*.txt samples
%attr(755,root,root) %{_bindir}/%{name}
%endif

%if %{with libXNVCtrl}
%files -n libXNVCtrl
%defattr(644,root,root,755)
%attr(755,root,root) /usr/X11R6/%{_lib}/libXNVCtrl.so.*.*.*

%files -n libXNVCtrl-devel
%defattr(644,root,root,755)
/usr/X11R6/include/X11/extensions/NVCtrl.h
/usr/X11R6/include/X11/extensions/NVCtrlLib.h
/usr/X11R6/%{_lib}/libXNVCtrl.so

%files -n libXNVCtrl-static
%defattr(644,root,root,755)
/usr/X11R6/%{_lib}/libXNVCtrl.a
%endif
