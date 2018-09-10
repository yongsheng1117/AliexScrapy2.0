# -*- coding: utf-8 -*-
__author__='wys'

from lxml import etree


ul = '''<ul id="zg_browseRoot">
<li class="zg_browseUp"> ‹

     <a href="https://www.amazon.co.uk/Best-Sellers-Welcome/zgbs">Any Department</a>
</li>
<ul>
<li>
<span class="zg_selected"> Sports &amp; Outdoors</span>
</li>
<ul>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-American-Football/zgbs/sports/671783011">American Football</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Archery/zgbs/sports/324259011">Archery</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Badminton/zgbs/sports/324054011">Badminton</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Ballet-Dancing/zgbs/sports/671792011">Ballet &amp; Dancing</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Baseball/zgbs/sports/324109011">Baseball</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Basketball/zgbs/sports/324105011">Basketball</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Billiard-Snooker-Pool/zgbs/sports/324253011">Billiard, Snooker &amp; Pool</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Bowling/zgbs/sports/671619011">Bowling</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Boxing/zgbs/sports/324248011">Boxing</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Camping-Hiking/zgbs/sports/319545011">Camping, Hiking &amp; Mountaineering</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Cricket/zgbs/sports/324071011">Cricket</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Bikes-Cycling-Equipment/zgbs/sports/324144011">Cycling</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Darts-Accessories/zgbs/sports/324249011">Darts</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Equestrian/zgbs/sports/324128011">Equestrian</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Fishing/zgbs/sports/324129011">Fishing</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Fitness/zgbs/sports/319535011">Fitness</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Football/zgbs/sports/324078011">Football</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Winter/zgbs/sports/3076655031">Winter Sports</a></li>
<li><a href="https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-Wrestling/zgbs/sports/671791011">Wrestling</a></li>
</ul>
</ul></ul>'''

html = etree.HTML(ul)
print(html)
result = etree.tostring(html)
print(result.decode("utf-8"))
cate_current = html.xpath('//ul/li/span/text()')
print(cate_current)

