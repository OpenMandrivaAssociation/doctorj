%define gcj_support 1
%bcond_with tests

Name:		doctorj
Version:	5.1.2
Release:	9
Epoch:		0
Summary:	Compares javadoc comments against code
License:	LGPL
Group:		Development/Java
URL:		http://www.incava.org/projects/java/doctorj/index.html
Source0:	http://superb-east.dl.sourceforge.net/sourceforge/doctorj/doctorj-%{version}.tar.gz
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch: 	noarch
BuildRequires:	java-devel
%endif
BuildRequires:	ant
%if %with tests
BuildRequires:	ant-junit
%endif
BuildRequires:	java-rpmbuild
BuildRequires:  xmlto

%description
Beyond the level of what Javadoc does, DoctorJ compares
documentation against code. Among what it detects:

    * misspelled words
    * parameter and exception names:
          o missing
          o misordered
          o misspelled
    * Javadoc tags:
          o invalid
          o misordered
          o missing expected arguments
          o invalid arguments
          o missing descriptions
    * undocumented classes, methods, fields, parameters

%package        javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
export CLASSPATH=
export OPT_JAR_LIST=
%ant dist
%ant doc

%if %with tests
%check
export CLASSPATH=
export OPT_JAR_LIST="%{__cat} %{_sysconfdir}/ant.d/junit"
%ant tests
%endif

%install
%ant -Ddestdir=%{buildroot} install

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a doc/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%attr(0755,root,root) %{_bindir}/%{name}
# XXX: This should probably go in %%{_javadir}.
%{_datadir}/%{name}/doctorj.jar
%{_datadir}/%{name}/words.*
%{_mandir}/man1/%{name}.1*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0:5.1.2-8mdv2011.0
+ Revision: 617869
- the mass rebuild of 2010.0 packages

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 0:5.1.2-7mdv2010.0
+ Revision: 428320
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0:5.1.2-6mdv2009.0
+ Revision: 244448
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:5.1.2-4mdv2008.1
+ Revision: 136373
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:5.1.2-3mdv2008.0
+ Revision: 87320
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Aug 28 2007 David Walluck <walluck@mandriva.org> 0:5.1.2-2mdv2008.0
+ Revision: 72559
- BuildRequires: xmlto
- rebuild
- Import doctorj



* Wed Aug 23 2006 David Walluck <walluck@mandriva.org> 0:5.1.2-1mdv2007.0
- 5.1.2

* Mon Jun 05 2006 David Walluck <walluck@mandriva.org> 0:5.0.0-3mdv2007.0
- rebuild for libgcj.so.7
- conditionalize gcj support
- better summary and description

* Wed Nov 02 2005 David Walluck <walluck@mandriva.org> 0:5.0.0-2mdk
- BuildRequires: java-devel
- build gcj database on %%post and %%postun

* Tue Oct 25 2005 David Walluck <walluck@mandriva.org> 0:5.0.0-1mdk
- release
