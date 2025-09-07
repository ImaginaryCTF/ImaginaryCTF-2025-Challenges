enc=input()
ans=""
a="abcdefghijklmnopqrstuvwxyz"
n="0123456789"
s="!@#$%^&*()_+{}[]|"
for i in range(len(enc)):
    if enc[i] in a:
        ind = a.index(enc[i])
        ind-=i
        ind%=len(a)
        ans+=a[ind]
    if enc[i] in n:
        ind =n.index(enc[i])
        ind-=i*2
        ind%=len(n)
        ans+=n[ind]
    if enc[i] in s:
        ind = s.index(enc[i])
        ind-=i*i
        ind%=len(s)
        ans+=s[ind]
print(ans)
