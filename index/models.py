from django.db import models
import re

# Create your models here.
class link(models.Model):
	hash = models.CharField(max_length=1000, primary_key=True)
	url = models.CharField(max_length=2000)

def convert62(n):
	ret = ""
	table = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
	while 1:
		ret += table[n%62]
		n = int(n/62)
		if(n == 0):
			break
	return ret


def unconvert62(str):
	ret = 0
	i = len(str) - 1
	table = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
	while 1:
		ret += table.index(str[i])
		i -= 1
		if(i < 0):
			break
		else:
			ret = ret*62
	return ret

def addLink(url):
	# URL Test
	capture = re.compile('(http|https):\/\/([\w-]+(\.[\w-]+)+[\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?')
	header = capture.search(url)
	if(not header):
		return False

	# Increment the last Hash
	all = link.objects.all()
	existance = link.objects.filter(url=url)
	if(existance):
		return existance[0].hash
	if(len(all) == 0):
		hash = 'A'
	else:
		hash = convert62(unconvert62(all[len(all)-1].hash) + 1)

	# Save the new link
	l = link(hash, url)
	l.save()
	return hash

def getTag(url):
	tag = re.compile('.+?/\?(.+?)$')
	res = tag.search(url)
	if(res):
		return res.group(1)
	return False

def getLink(tag):
	res = link.objects.filter(hash=tag)
	if(res):
		return res[0].url
	else:
		return False