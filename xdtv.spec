%define	name	xdtv
%define Name	XdTV
%define	version	2.4.0
%define release 3
%define summary TV application with plugin capabilities

%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

# build with -with optimization
%define build_optimization 0
%{?_with_optimization: %{expand: %%define build_optimization 1}}

# build with -with alsa
%define build_alsa 1
%{?_with_alsa: %{expand: %%define build_alsa 1}}

%if %mdkversion >= 200700 
%define app_defaults_dir %{_datadir}/X11/app-defaults
%else
%define app_defaults_dir %{_sysconfdir}/X11/app-defaults
%endif

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Summary:	%{summary}
URL:		http://xawdecode.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Group:		Video
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  libjpeg-devel
BuildRequires:  libxpm-devel
BuildRequires:  libneXtaw-devel
BuildRequires:	liblirc-devel
BuildRequires:	libxosd-devel
BuildRequires:	libzvbi-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libtheora-devel
BuildRequires:	libpng-devel
BuildRequires:	desktop-file-utils
# for DVB support
BuildRequires:	SDL-devel curl-devel
%if %mdkversion > 200600
BuildRequires:	bdftopcf
BuildRequires:	xset
BuildRequires:	libxv-devel
BuildRequires:	libxxf86dga-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:	libxext-devel
BuildRequires:	libxinerama-devel
%else
BuildRequires:	XFree86-devel 
BuildRequires:	XFree86
%endif
%if %build_plf
BuildRequires:	xvid-devel	
BuildRequires:	lame
BuildRequires:	liblame-devel
BuildRequires:	x264-devel
BuildRequires:	libfaac-devel
%endif
%if %build_alsa
BuildRequires:  libalsa-devel
BuildRequires:  alsa-utils
Requires:	alsa-utils
%endif
Requires:	tv-fonts
Provides:	xawdecode
Obsoletes:	xawdecode
		
%description
XdTV is a software to watch, record & stream TV.
It interacts with AleVT (Teletext) and Nxtvepg (NextView) & supports
the bttv, bktr & dvb APIs. It contains some deinterlacing filters &
record video files with various containers (AVI, MPEG, OGG, etc.) &
many codecs: FFMpeg >=0.4.6, XviD 0.9 & 1.x, DivX 4 & 5,
Ogg Vorbis + Theora >=1.0a5.
It has some plugin capabilities.

%if %build_plf
This package is in PLF as some of its dependencies are covered by patents.
%endif


%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Provides:	xawdecode-devel
Obsoletes:	xawdecode-devel

%description devel
This package contains the development files needed to compile
and link programs which use %{name}.

%prep
%setup -q

%build
%configure \
	--enable-xosd \
	--disable-makefonts \
	--with-appdefaultsdir=%{app_defaults_dir} \
%if !%build_optimization
	--disable-cpu-detection \
%endif
%if !%build_alsa
	--disable-alsa \
%endif
%if !%build_plf
	--disable-lame \
	--disable-faac \
	--disable-x264 \
	--disable-xvid
%endif

%make

%install
rm -fr %{buildroot}
%makeinstall_std

# clean-up
rm -f %{buildroot}%{_datadir}/%{name}/icons/*.png

# icons
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png
# menu entry
install -d -m 755 %{buildroot}%{_menudir}
cat >%{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
	command="%{_bindir}/%{name}" \
	needs="X11" \
	icon="%{name}.png" \
	section="Multimedia/Video" \
	title="%{Name}" \
	longtitle="%{summary}" \
	xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="TV" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir %{buildroot}%{_datadir}/applications gentoo/%{name}.desktop

%clean
rm -fr %{buildroot}

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog FAQfr-xdtv README.* NEWS TODO
%doc lircrc.* lisez-moi xdtvrc.sample
%{app_defaults_dir}/%{Name}
%config(noreplace) %{_sysconfdir}/%{name}/xdtv_wizard-en*.conf
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files devel
%defattr(-,root,root)
%doc COPYING README.*
%{_includedir}/*


