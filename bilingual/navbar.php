

<ul>
	<li><a href = "?lang=english">English</a></li>
	<li><a href = "?lang=chinese">中文</a></li>
<ul>

<!--
在上面的语言切换按钮中，我们通过点击按钮实现语言切换，比如点击英文后，就会给当前页面的网址传去一个参数，告知将其切换成英文。此时，如果点击进入到另一个页面，比如从index.php进入到about.php页面，一旦点击”关于，页面就会跳转至"about.php"，此时URL参数确实，再次回到原始状态。

所以关键点在于我们要给按钮链接一个

-->

<ul>
	<li><a href = "index.php"><?php echo $lang["home"];?></a></li>
	<li><a href = "about.php"><?php echo $lang["about"];?></a></li>
<ul>