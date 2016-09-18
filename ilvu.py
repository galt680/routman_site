
from flask import render_template





def love():
	love_sayings = [
	"I love that you can accept criticism and are working on all those things to be a better person and to make me happy.",
	"I love looking into your eyes! They are amazing! I can't describe how happy it makes me to gaze into them.",
	"I love the way you make me feel loved and wanted.",
	"I love that you are so smart and capable.",
	"I love your smile. When you smile at me it makes my heart flutter and my mind melt.",
	"I love when you blush I can't even describe what that does to me.",
	"I love that you make me want to be a better person.",
	"I love that you are adventurous, and want to explore the world with me",
	"I love the way we argue, I never feel like it's out of control and we resolve it quickly.",
	"I love that you feel you can be honest with me.",
	"I love when you open up to me.",
	"I love when you trust me."
	"I love how you much fun I have hanging out with you.",
	"I love how you want to make a difference and help people with your work.",
	"I love how you consider my feelings and opinions.",
	#"I love how you make the world seem brighter when I'm with you.",
	#"I love the way you laugh",
	#"I love that you get along with my family.",

	]
	return render_template("ilvu.html", love_sayings = love_sayings)
	"""
	I love you more than anything and last week you listed some of the things
	you like about me but I'm gonna take a risk and name some of the things
	I that bother me
	There are 5 things that bother me about you;
	1)you sometimes bulldoze me;
	2)you call me sruli;
	3)you have that weird thing with meat and animals;
	4)your grammar needs work;
	5)you sometimes are still uncomfortable around me .
	These are all the things I dislike. All of them.
	Yet I can't even begin to count the ways I love you; so I won't even try now.
	Instead everyday I'll try and put another way I love you.
	My love for you is infinite and growing everyday.


	"""

