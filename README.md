# SECCON Beginners CTF 2026 - Quick Writeup

These are my quick notes for the challenges I solved during the event.  
The writeups are intentionally short and focus on the key idea and solver used to get each flag.

Note: I used AI assistance to organize notes, review solver scripts, and polish explanations. The challenge analysis and final solves were based on my own hands-on work during the CTF.

## baby-rev / reversing

### KeyIdea
The source code included an encrypted xorFlag[] and an xorKey.
The flag could be recovered by XORing each byte of xorFlag[] with the key.

### Solver
flag = bytes([b ^ key for b in enc])
print(flag.decode(errors="replace"))

### Flag
ctf4b{l00k_m0m_n0_h4nds_just_x0r!}


## 1st-Memory-Errand / reversing

### Key Idea
The program message implies that the flag is stored somewhere in memory.

Mom: Go fetch the flag from memory! </br>
You: OK! Heading out... </br>
You: I'm at the memory store now. Looking around... </br>
Mom: Did you find it? Type what you got: 

### Solver
I used gdb and set a breakpoint at strcmp@plt.
By checking the arguments passed to strcmp, I was able to find the flag in memory.

### Flag
ctf4b{My_fir5t_3rr4nd_w45_4_5ucc355!}


## Reversing-2050 / reversing 

### Key Idea
This challenge is written in Q#. I found the `xored` in the source code, and decoded the cipher using the key.

### Solver
flag = bytes([c ^ key[i % len(key)] for i, c in enumerate(cipher)])
print(flag)

### Flag
ctf4b{Hello_Quantum_World!!!}


## old-virus / reversing

### Key Idea
I inspected the file and found suspicious strings embedded in the program.

- “THISISNOTAESKEY!ImashyKey!Dontlookme!!!” </br>
- AES_KEY</br>
- RC4_KEY

### Solver
OldVirus_recover.py

### Flag
ctf4b{Y2K_n05t419ic_viru5_6ut_G2G}


## twins / crypto

### Key Idea
The challenge message said that two RSA keys were generated.
I checked the source code and found that n1 and n2 shared a prime factor.

### Solver
p = gcd(n1, n2) </br>
q1 = n1 // p </br>
phi1 = (p - 1) * (q1 - 1) </br>
d1 = inverse(e1, phi1)</br>

m = pow(c1, d1, n1) </br>
print(long_to_bytes(m))

### Flag
ctf4b{tw1n_pr1m35_4r3_n0t_1nd3p3nd3nt}


## InvertedRSA /crypto
### Key Idea
Some RSA parameters were given as negative numbers.
Since negative numbers are not prime numbers, I needed to handle the signs correctly before solving it as an RSA challenge.

### Solver
twins_solve.py

### Flag
ctf4b{of_cours3_n3g4tiv3_numb3rs_4r3_not_prim3_numb3rs}


## viewer / misc
### Key Idea
This challenge was an online file viewer system.
When I entered flag, the request was blocked.

In the source code, I found that the filename was normalized with NFKC.

normalized = unicodedata.normalize("NFKC", filename)

This meant that Unicode characters could be converted into normal ASCII characters after the check.

### Solver
I entered the filename using full-width characters.
ｆｌａｇ．ｔｘｔ

### Flag
ctf4b{un1C0dE_N0rMal12a710n_15_7r1CKy}


## login / pwnable

### Key Idea
The service accepted a username as input.
In the source code, I found that the username buffer was only 0x10 bytes.

`char username[0x10];

By sending 17 bytes as the username, switched to interactive mode, and read the flag with `cat flag.txt`

### Solver
I sent 17 bytes and connected to interactive mode, and `cat flag.txt`

### Flag
ctf4b{l0g1n_r00t_us4r!}


## defeat_monster / pwnable
### Key Idea
This challenge was online game to defeat a boss using monster. After inspecting the source code, I found that the bug was a Use-After-Free.

### Solver
I used the following flow:
1  capture monster
3  release monster
4  check boss
5  battle
By releasing the monster and then using it again, I could trigger the UAF and defeat the boss.

### Flag
ctf4b{d3fe4t_b0ss_by_U4F!!}


## rop4b / pwnable
### Key Idea
The challenge message gave a clear hint:

"Call read_file(\"/flag.txt\") using ROP!"

So I built a ROP chain to call read_file("/flag.txt").

### Solver
rop4b_exploit.py

### Flag
 ctf4b{3Xp10it_ROP!}


## Homework / misc

### Key Idea
This challenge provided a PDF file.
When I checked the file with strings, I found FLAG.txtPK, which suggested that a ZIP file was embedded at the end of the PDF.

### Solver
I extracted/unzipped the embedded ZIP file and read flag.txt.

### Flag
ctf4b{Im_914d_y0u_f0und_thi5_f149}


## filter / reversing
### Key Idea
This challenge provided a `.sh` code that only printed “Nothing to do.”
I found two EOF markers in the script. After checking the hidden part, I found that it attached a BPF filter to the lo interface.
### Solver
I used three terminals in Kali Linux VM and sent / received the data through the local interface.
### Flag
ctf4b{ebpf_m4g1c_kn0ck}


## scoreboard / pwnable

### Key Idea
This challenge accepts three input in a row: rank, score and feedback.
The key bug was an arbitrary 8-byte write using a negative index in scores[index].
By using scores[negative_index], I could overwrite a GOT entry and redirect the function call.

### Solver
score_exploit.py

### Flag
ctf4b{c4n4Ry_g0T_0v3rwr1t3!!}
