%bcond_without mp3rtp

Summary: A free MP3 codec
Name: lame
Version: 3.99.3
Release: 23%{?dist}
License: LGPLv2+
Group: Applications/Multimedia
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
URL: http://lame.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-root
#BuildRequires: autoconf, automake, libtool
#BuildRequires: gcc-c++
BuildRequires: ncurses-devel, libsndfile-devel, gtk+-devel >= 1.2.0
%ifarch %{ix86} x86_64
BuildRequires: nasm
%endif
Requires: ncurses >= 5.0
Provides: lame-libs = %{version}-%{release}
Provides: mp3encoder = %{version}-%{release}
Obsoletes: lame-libs < %{version}-%{release}, mp3encoder < %{version}-%{release}

%lib_package mp3lame 0
%lib_dependencies

%description
LAME is an educational tool to be used for learning about MP3 encoding.
The goal of the LAME project is to use the open source model to improve
the psycho acoustics, noise shaping and speed of MP3. Another goal of
the LAME project is to use these improvements for the basis of a patent
free audio compression codec for the GNU project.

%prep
%setup -q
sed -i -e '/define sp/s/+/ + /g' libmp3lame/i386/nasm.h
%{_bindir}/iconv -f iso8859-1 -t utf-8 ChangeLog -o ChangeLog.txt
touch -r ChangeLog ChangeLog.txt
mv ChangeLog.txt ChangeLog

%build
#autoreconf
%configure \
  --disable-dependency-tracking \
  --disable-static \
%ifarch %{ix86} x86_64
  --enable-nasm \
%endif
  --enable-decoder \
  --enable-decode-layer1 \
  --enable-mp3x \
  %{?with_mp3rtp:--enable-mp3rtp} \
  --enable-brhist

# Disable RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%check
make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Some apps still expect to find <lame.h>
ln -sf lame/lame.h %{buildroot}%{_includedir}/lame.h

rm -rf %{buildroot}%{_datadir}/doc/%{name}
cat > develfiles.list << EOF
%defattr(-,root,root,-)
%doc API HACKING STYLEGUIDE
EOF

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root,-)
%doc ChangeLog COPYING LICENSE README TODO USAGE
%doc doc/html/*.html
#doc doc/html/*.css
%{_bindir}/lame
%{_bindir}/mp3x
%if %{with mp3rtp}
%{_bindir}/mp3rtp
%endif
%{_mandir}/man1/lame.1*

%changelog
* Sun Nov 27 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.99.3-23
- Update to 3.99.3.

* Mon Nov  1 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.98.4-22
- Fix build for nasm >= 2.09.x.

* Sun Apr  4 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.98.4-21
- Update to 3.98.4.

* Fri Nov 14 2008 Paulo Roma <roma@lcg.ufrj.br> - 3.98.2-19
- Providing lame-libs because of rpmfusion.
- Only including the relevant files in doc.

* Tue Sep 23 2008 Paulo Roma <roma@lcg.ufrj.br> - 3.98.2-18
- Fixed mp3rtp.
- Using %%check.

* Fri Jul 18 2008 Paulo Roma <roma@lcg.ufrj.br> - 3.98-17
- Removed patch0 (libm).
- Using %%bcond_with mp3rtp (the build fails with it).
- Using nasm for x86_64.
- Disabled rpath.
- Changed license.
- Converted ChangeLog to utf8.

* Thu Jul 17 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.98-16
- Update to 3.98.

* Wed Dec 27 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.97-15
- fix unresolved symbols from libm (Rex Dieter).

* Sun Oct 15 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.97-14
- Update to 3.97.

* Fri Oct  1 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.96.1.

* Tue Apr 13 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.96.

* Wed Jan 14 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.95.1.

* Mon Nov 17 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.94alpha cvs build.

* Thu Oct  9 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.94alpha cvs build.
- Many small fixes.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.
- Exclude .la file.

* Mon Jan 13 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.93.1.
- Removed Epoch: tag, upgrade by hand! :-/

* Sat Oct  5 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fix unpackaged doc problem.

* Fri Sep 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 8.0.
- Simplified deps as it now builds VBR code fine with default nasm and gcc 3.2.

* Tue Jul 16 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fix to the lamecc stuff.

* Wed Jul 10 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Changes to now support ppc with no ugly workarounds.

* Thu May  2 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Wed Apr 24 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.92.

* Mon Apr  8 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Added a symlink from lame.h to lame/lame.h to fix some include file
  detection for most recent programs that use lame.

* Wed Jan  2 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.91.
- Simplified the compilation optimizations after heavy home-made tests.
- Now build only i386 version but optimized for i686. Don't worry i686
  owners, you loose only 1% in speed but gain about 45% compared to if
  you had no optimizations at all!

* Mon Dec 24 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.90.1.
- Enabled the GTK+ frame analyzer.
- Spec file cleanup (CVS, man page, bindir are now fixed).

* Fri Nov 16 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt with mpg123 decoding support.

* Tue Oct 23 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fixed the %%pre and %%post that should have been %%post and %%postun, silly me!
- Removed -malign-double (it's evil, Yosi told me and I tested, brrr ;-)).
- Now build with gcc3, VBR encoding gets a hell of a boost, impressive!
  I recommend you now use "lame --r3mix", it's the best.
- Tried to re-enable vorbis, but it's a no-go.

* Thu Jul 26 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Build with kgcc to have VBR working.

* Wed Jul 25 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.89beta : Must be built with a non-patched version of nasm
  to work!

* Mon May  7 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat 7.1.
- Disabled the vorbis support since it fails to build with it.
- Added a big optimisation section, thanks to Yosi Markovich
  <senna@camelot.com> for this and other pointers.

* Sun Feb 11 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Split the package, there is now a -devel

* Thu Oct 26 2000 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release for RedHat 7.0 from scratch

