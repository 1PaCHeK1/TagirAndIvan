import re

with open('text.txt') as f:
	result = re.findall(r"""<td>([a-zA-Z .]+) ([a-zA-Z]+)</td>
	<td>(0\d{2}-\d{3}-\d{4})</td>
	<td>([a-zA-Z0-9.-_]+@[a-zA-Z]+[.a-zA-Z]+)</td>
	<td>([\w#;., -]+)</td>
	<td>([a-zA-Z]{3} \d+, \d{4})</td>
	""", f.read())

[ print(i) for i in result]

# (0[1-9]-\d{2}-\d{2}|1[0-2]-\d{2}-\d{2})