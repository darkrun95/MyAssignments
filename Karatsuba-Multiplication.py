"""
Author : Arun Pottekat
Domain : Algorithms
Problem : Karatsuba Multiplication
"""

def karatsuba(a_dash, b_dash):
	# Base Case
	if len(a_dash) == 1:
		return str(int(a_dash)*int(b_dash))
	else:
		w, x = a_dash[:(len(a_dash)//2)], a_dash[(len(a_dash)//2):]
		y, z = b_dash[:(len(b_dash)//2)], b_dash[(len(b_dash)//2):]

		if w == "":
			w = "0"
		if x == "":
			x = "0"
		if y == "":
			y = "0"
		if z == "":
			z = "0"

		wy = karatsuba(w, y) 
		xz = karatsuba(x, z)
		print(w,x,y,z)
		wxyz = karatsuba(str(int(w)+int(x)), str(int(y)+int(z)))
		wzxy = str(int(wxyz) - int(wy) - int(xz)) + ("0"*(len(a_dash)//2))
		wy = wy + ("0"*len(a_dash))
		result = str(int(wy) + int(xz) + int(wzxy))

		return result

str_x = input()
str_y = input()
x, y = int(str_x), int(str_y)

a, b = str_x[:(len(str_x)//2)], str_x[(len(str_x)//2):]
c, d = str_y[:(len(str_y)//2)], str_y[(len(str_y)//2):]

if a == "":
	a = "0"
if b == "":
	b = "0"
if c == "":
	c = "0"
if d == "":
	d = "0"

ac = karatsuba(a, c) 
bd = karatsuba(b, d)
abcd = karatsuba(str(int(a)+int(b)), str(int(c)+int(d)))

adbc = str(int(abcd) - int(ac) - int(bd)) + ("0"*(len(str_x)//2))
ac = ac + ("0"*len(str_x))
result = str(int(ac) + int(bd) + int(adbc))

print(result)