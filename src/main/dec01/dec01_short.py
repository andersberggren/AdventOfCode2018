d=[int(x)for x in open("i").read().split()]
print(sum(d))
c=0
p=set([c])
while True:
	c+=d[(len(p)-1)%len(d)]
	if c in p:
		print(c)
		break
	p.add(c)
