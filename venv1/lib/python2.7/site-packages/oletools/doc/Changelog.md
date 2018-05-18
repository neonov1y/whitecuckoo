Python-oletools Changelog
=========================

- **2017-06-29 v0.51**: 
    - added the [oletools cheatsheet](https://github.com/decalage2/oletools/blob/master/cheatsheet/oletools_cheatsheet.pdf)
    - improved [rtfobj](https://github.com/decalage2/oletools/wiki/rtfobj) to handle malformed RTF files, detect vulnerability CVE-2017-0199
    - olevba: improved deobfuscation and Mac files support
    - [mraptor](https://github.com/decalage2/oletools/wiki/mraptor): added more ActiveX macro triggers
    - added [DocVarDump.vba](https://github.com/decalage2/oletools/blob/master/oletools/DocVarDump.vba) to dump document variables using Word
    - olemap: can now detect and extract [extra data at end of file](http://decalage.info/en/ole_extradata), improved display
    - oledir, olemeta, oletimes: added support for zip files and wildcards
    - many [bugfixes](https://github.com/decalage2/oletools/milestone/3?closed=1) in all the tools
    - improved Python 2+3 support
    
- 2016-11-01 v0.50: all oletools now support python 2 and 3.
    - olevba: several bugfixes and improvements.
    - mraptor: improved detection, added mraptor_milter for Sendmail/Postfix integration.
    - rtfobj: brand new RTF parser, obfuscation-aware, improved display, detect
    executable files in OLE Package objects.
    - setup: now creates handy command-line scripts to run oletools from any directory.
- 2016-06-10 v0.47: [olevba](https://github.com/decalage2/oletools/wiki/olevba) added PPT97 macros support,
improved handling of malformed/incomplete documents, improved error handling and JSON output,
now returns an exit code based on analysis results, new --relaxed option.
[rtfobj](https://github.com/decalage2/oletools/wiki/rtfobj): improved parsing to handle obfuscated RTF documents,
added -d option to set output dir. Moved repository and documentation to GitHub.
- 2016-04-19 v0.46: [olevba](https://github.com/decalage2/oletools/wiki/olevba)
does not deobfuscate VBA expressions by default (much faster), new option --deobf
to enable it. Fixed color display bug on Windows for several tools.
- 2016-04-12 v0.45: improved [rtfobj](https://github.com/decalage2/oletools/wiki/rtfobj)
to handle several [anti-analysis tricks](http://www.decalage.info/rtf_tricks),
improved [olevba](https://github.com/decalage2/oletools/wiki/olevba)
to export results in JSON format.
- 2016-03-11 v0.44: improved [olevba](https://github.com/decalage2/oletools/wiki/olevba)
to extract and analyse strings from VBA Forms.
- 2016-03-04 v0.43: added new tool [MacroRaptor](https://github.com/decalage2/oletools/wiki/mraptor) (mraptor)
to detect malicious macros, bugfix and slight improvements in [olevba](https://github.com/decalage2/oletools/wiki/olevba).
- 2016-02-07 v0.42: added two new tools oledir and olemap, better handling of malformed
files and several bugfixes in [olevba](https://github.com/decalage2/oletools/wiki/olevba),
improved display for [olemeta](https://github.com/decalage2/oletools/wiki/olemeta).
- 2015-09-22 v0.41: added new --reveal option to [olevba](https://github.com/decalage2/oletools/wiki/olevba),
to show the macro code with VBA strings deobfuscated.
- 2015-09-17 v0.40: Improved macro deobfuscation in [olevba](https://github.com/decalage2/oletools/wiki/olevba),
to decode Hex and Base64 within VBA expressions. Display printable deobfuscated strings by
default. Improved the VBA_Parser API. Improved performance.
Fixed [issue #23](https://github.com/decalage2/oletools/issues/23) with sys.stderr.
- 2015-06-19 v0.12: [olevba](https://github.com/decalage2/oletools/wiki/olevba) can now deobfuscate VBA
expressions with any combination of Chr, Asc, Val, StrReverse, Environ, +, &, using a VBA parser built with
[pyparsing](http://pyparsing.wikispaces.com). New options to display only the analysis results or only the macros source code.
The analysis is now done on all the VBA modules at once.
- 2015-05-29 v0.11: Improved parsing of MHTML and ActiveMime/MSO files in
[olevba](https://github.com/decalage2/oletools/wiki/olevba), added several suspicious keywords to VBA scanner
(thanks to @ozhermit and Davy Douhine for the suggestions)
- 2015-05-06 v0.10: [olevba](https://github.com/decalage2/oletools/wiki/olevba) now supports Word MHTML files
with macros, aka "Single File Web Page" (.mht) - see [issue #10](https://github.com/decalage2/oletools/issues/10) for more info
- 2015-03-23 v0.09: [olevba](https://github.com/decalage2/oletools/wiki/olevba) now supports Word 2003 XML files,
added anti-sandboxing/VM detection
- 2015-02-08 v0.08: [olevba](https://github.com/decalage2/oletools/wiki/olevba) can now decode strings
obfuscated with Hex/StrReverse/Base64/Dridex and extract IOCs. Added new triage mode, support for non-western
codepages with olefile 0.42, improved API and display, several bugfixes.
- 2015-01-05 v0.07: improved [olevba](https://github.com/decalage2/oletools/wiki/olevba) to detect suspicious
keywords and IOCs in VBA macros, can now scan several files and open password-protected zip archives, added a Python API,
upgraded OleFileIO_PL to olefile v0.41
- 2014-08-28 v0.06: added [olevba](https://github.com/decalage2/oletools/wiki/olevba), a new tool to extract VBA Macro
source code from MS Office documents (97-2003 and 2007+). Improved [documentation](https://github.com/decalage2/oletools/wiki)
- 2013-07-24 v0.05: added new tools [olemeta](https://github.com/decalage2/oletools/wiki/olemeta) and
[oletimes](https://github.com/decalage2/oletools/wiki/oletimes)
- 2013-04-18 v0.04: fixed bug in rtfobj, added documentation for [rtfobj](https://github.com/decalage2/oletools/wiki/rtfobj)
- 2012-11-09 v0.03: Improved [pyxswf](https://github.com/decalage2/oletools/wiki/pyxswf) to extract Flash objects from RTF
- 2012-10-29 v0.02: Added [oleid](https://github.com/decalage2/oletools/wiki/oleid)
- 2012-10-09 v0.01: Initial version of [olebrowse](https://github.com/decalage2/oletools/wiki/olebrowse) and pyxswf

See also the changelog in each source file for more details.
