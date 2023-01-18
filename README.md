# Dell-ACL-Generator
This program creates a Dell ACL based off of a file with variables and a file with a template. It then outputs it to a file.

## Syntax
There are 3 arguments, in this order:
1. Variable input file location
2. Template input file location
3. Output file location

## Variable File Syntax
```
Define Variable1
  Value1
  Value2
Define Variable2
  Value1
  Value2
```
Example:
```
Define BGP_FROM
  host 255.255.254
  host 255.255.255
Define BGP_TO
  host 254.254.254
  host 254.254.255
```

## Template File Syntax
```
Line before variable {Variable} Line after variable
```
It can also do two variables in one line, in which case it outputs all possible combinations of those variables in that line.
```
Line before variable {Variable1} {Variable2} Line after variable
```

Example:
```
permit tcp {BGP_FROM} eq 179 {BGP_TO}
```
This will output, if used with the above example, the following lines:
```
permit tcp host 255.255.254 eq 179 host 254.254.254
permit tcp host 255.255.254 eq 179 host 254.254.255
permit tcp host 255.255.255 eq 179 host 254.254.254
permit tcp host 255.255.255 eq 179 host 254.254.255
```
