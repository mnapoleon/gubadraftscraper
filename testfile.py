import re, requests, bs4, slackclient, time, configparser

testHtml ="""
<html>
<head>
<title>Test</title>
</head>
<table>
<tr>
<td>121</td>
<td>Marauders</td>
<td align='right'>SP <a href='#'>Eugene Pagonis</a></td>
</tr>
<tr>
<th width=25 style='border-top:1px solid #818586;'>#</th>
<th style='width:180px;border-top:1px solid #818586;'>Round 5</th>
<th style='border-top:1px solid #818586;'>&nbsp;</th>
</tr>
<tr>
<td>138</td>
<td>Tiburones(from Prospectors)</td>
<td align='right'>Pick due by Thursday at 10:59 am</td>
</tr>
<table>
</html>
"""

testHtml1 ="""
<html>
<head>
<title>Test</title>
</head>
<table>
<tr>
<td>137</td>
<td>Shamrocks(from Sounds)</td>
<td align='right'>SP <a href='#' onclick="document.getElementById('playerId').value=31643;playerDetails(['detailsType', 'links', 'playerId'], [showPlayerDetail])">Arthur Price</a></td>
</tr>
<tr>
<td>138</td>
<td>Tiburones(from Prospectors)</td>
<td align='right'>Pick due by Thursday at 10:59 am</td>
</tr>
<table>
</html>
"""

from bs4 import BeautifulSoup
res = requests.get('http://www.thefibb.net/cgi-bin/ootpou.pl?page=draftPicks')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

pickDueParent = soup.find('td', string=re.compile("Pick due")).parent

print(pickDueParent)
prev_sib = None
if type(pickDueParent) is bs4.element.NavigableString:
    # means first pick in next round
    print("is Navi")
    prev_sib = pickDueParent.previous_sibling.previous_sibling.previous_sibling
else:
    prev_sib = pickDueParent.previous_sibling.previous_sibling

print("***")
print (prev_sib)
print("***")
