import formatter, htmllib
from formatter import AbstractFormatter
from htmllib import HTMLParser

class writer(formatter.AbstractWriter):
	def __init__(self):
		formatter.AbstractWriter.__init__(self)

	def send_literal_data(self,data):
		print "<<LITERAL>>", data
		self.send_flowing_data(data)

	def send_line_break(self):
		print "<<LB>>"
		self.send_paragraph(1)

	def send_flowing_data(self, data):
		print  "<<FLOW>>", data

	def send_paragraph(self, blankline):
		print "<<PARA>>"

class Parser(htmllib.HTMLParser):
	def __init__(self, writer, *args):
		htmllib.HTMLParser.__init__(self, *args)
		self.writer = writer

	def feedme(self, html):
		self.html = html
		self.feed(html)

#	def handle_starttag(self, tag, method, attrs):
#		method(attrs)
#		print "<<* handle starttag *>>", tag, method, attrs
#		pass

#	def handle_endtag(self, tag,method):
#		method()
#		print "<<* handle endtag *>>", tag, method
#		pass

	def parse_starttag(self, i):
		index = htmllib.HTMLParser.parse_starttag(self,i) 
		self.writer.index =index
		print "<<parsing starttag>>", self.html[i:i+3], " - ", self.html[index: index+3]
		return index
	
	def parse_endtag(self, i):
		self.writer.index = i
		index =  htmllib.HTMLParser.parse_endtag(self,i)
		print "<<parsing endtag>>", self.html[i:i+3], ' - ', self.html[index:index+3]
		return index

	def start_p(self, attrs):
		self.get_starttag_text(attrs)
		print "<<p>>"

	def start_script(self, attrs):
		print "<<script>>"

	def start_div(self, attrs):
		print "<<div>>"

	def start_head(self, attrs):
		print "<<head>>"

	def get_starttag_text(self,data):
		print "<<starttag>>", data
	
	def handle_data(self,data):
		print "<<arbit data>>",data

	def start_img(self, attrs):
		print "<<img>>"

	def end_p(self):
		print "<<end p>>"

	def end_script(self):
		print "<<end script>>"

	def end_img(self):
		print "<<end img>>"

	def end_head(self):
		print "<<end head>>"

	def end_div(self):
		print "<<end div>>"

	def end_head(self):
		print "<<end head>>"

	def start_cite(self, attrs):
		print "<<cite>>", attrs

	def end_cite(self):
		print "<<end_cite>>"

	def start_span(self, attrs):
		print "<<span>>", attrs

	def end_span(self):
		print "<<end span>>"

def  extract(html):
	mywriter = writer()
	formatter = AbstractFormatter(mywriter)
	parser = Parser(mywriter, formatter)
	parser.feedme(html)
	parser.close()

str = '''<head>
<div class="cnn_strylceclbtn"><img src="http://i.cdn.turner.com/cnn/.e/img/3.0/mosaic/bttn_close.gif" alt="" border="0" height="23" width="58"/></div>
<script>
	<p>This is an \n experiment. &lt; is less than. You better be kidding.<br>kill me</p>
</script>
</head>'''


str ='''
<a name="em11"></a>
<div class="cnn_strylftcntnt cnn_strylftcexpbx" id="expand116">
<div class="cnn_strylceclbtn"><img src="http://i.cdn.turner.com/cnn/.e/img/3.0/mosaic/bttn_close.gif" alt="" border="0" height="23" width="58"/></div>
<img src="http://i2.cdn.turner.com/cnn/dam/assets/140731074452-newday-intv-cuomo-jeremy-writebol-son-of-american-battling-ebola-00003118-story-body.jpg" alt="" border="0" class="box-image" height="120" width="214"/><cite class="expCaption"><span>Could Ebola make its way to the U.S.? </span></cite>
</div>
<p class="cnn_storypgraphtxt cnn_storypgraph6">The plane, also equipped with a unit meant to isolate the patient, was able to take only one patient at a time. Organizers expect the plane will now pick up Writebol in Liberia, and bring her to Georgia early next week, said Todd Shearer, spokesman for Christian charity Samaritan's Purse, with which both Americans were affiliated.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph7">Brantly's wife, parents and sister cried when they saw him on CNN, walking from the ambulance into the hospital, a family representative said on condition of anonymity. His wife, Amber, later said she was relieved that her husband was back in the United States.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph8">"I spoke with him, and he is glad to be back in the U.S.," she said in statement sent to CNN. "I am thankful to God for his safe transport and for giving him the strength to walk into the hospital."</p>
<p class="cnn_storypgraphtxt cnn_storypgraph9">Brantly's family was expected to be allowed to see him through a glass wall at Emory later Saturday, the source said.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph10">Brantly, of Texas, and Writebol, of North Carolina, became sick while caring for Ebola patients in Liberia, one of three West African nations hit by an outbreak that health officials believe has sickened more than 1,300 people and killed more than 700 this year.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph11"><strong>Treatment in isolation</strong></p>
<p class="cnn_storypgraphtxt cnn_storypgraph12">This will be the first human Ebola test for a U.S. medical facility. But both Brantly and Writebol will be treated at an isolated unit where precautions have been in place to keep such deadly diseases from spreading, unit supervisor Dr. Bruce Ribner said.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph13">Everything that comes in and out of the unit will be controlled, Ribner told reporters Thursday, and it will have windows and an intercom for staff to interact with patients without being in the room.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph14">Ebola is not airborne or waterborne, and spreads through contact with organs and bodily fluids such as blood, saliva, urine and other secretions of infected people.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph15">There is no FDA-approved treatment for Ebola, and Emory will use what Ribner calls "supportive care." That means carefully tracking a patient's symptoms, vital signs and organ function and taking measures, such as blood transfusions and dialysis, to keep him or her as stable as possible.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph16">"We just have to keep the patient alive long enough in order for the body to control this infection," Ribner said.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph17">Writebol was given an experimental serum this week, Samaritan's Purse said, though its purpose and effects, if any, weren't immediately publicized.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph18">The Ebola virus causes viral hemorrhagic fever, which refers to a group of viruses that affect multiple organ systems in the body and are often accompanied by bleeding.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph19">Early symptoms include sudden onset of fever, weakness, muscle pain, headaches and a sore throat, but progress to vomiting, diarrhea, impaired kidney and liver function and sometimes internal and external bleeding.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph20">Bruce Johnson, president of SIM USA, a Christian mission organization with which Writebol also is linked, said Saturday that both Brantly and Writebol were seriously ill but stable.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph21">"My last report (on Brantly) was yesterday. ... He was ambulatory, being able to talk, converse, and get up. So that was encouraging," Johnson said Saturday morning.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph22">On Writebol, Johnson said: "She's responsive, and we're encouraged at how she's doing."</p>
<p class="cnn_storypgraphtxt cnn_storypgraph23">Emory's isolation unit was created with the Centers for Disease Control and Prevention, based down the road. It aims to optimize care for those with highly infectious diseases and is one of four U.S. institutions capable of providing such treatment.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph24">The <a href='http://www.who.int/csr/don/2014_07_31_ebola/en/' target='_blank'>World Health Organization reports</a> that the outbreak in Liberia, Sierra Leone and Guinea is believed to have infected 1,323 people and killed more than 729 this year, as of July 27.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph25"><strong>'Compassionate' Brantly had focus in mission fields</strong></p>
<p class="cnn_storypgraphtxt cnn_storypgraph26">Brantly, a man with ties to Indiana and Texas, went to Liberia with his wife and two children last year to serve a two-year fellowship with Samaritan's Purse.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph27">Brantly was there initially to practice general medicine, but he focused on Ebola when the outbreak began, charity spokeswoman Melissa Strickland said.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph28">He attended high school in Indianapolis before graduating from <a href='http://blogs.acu.edu/acutoday/2014/07/31/brantlys-follow-heart-faith-in-missions-field/' target='_blank'>Abilene Christian University</a> in 2003 and <a href='http://inscope.iu.edu/headlines/2014-07-30-headline-brantley-statement-inscope.shtml' target='_blank'>Indiana University's medical school in 2009.</a></p>
<p class="cnn_storypgraphtxt cnn_storypgraph29">While at Abilene Christian, he spent a summer interning overseas with an ACU program focused on vocational missions experiences, ACU's online alumni magazine reported.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph30">"Everyone here who has been connected with Kent knows him to be someone who is very compassionate, considerate and always upbeat in all he does," the program's director, Dr. Gary Green, told the magazine. ".. Kent's the kind of guy who would weigh benefits versus risk, then try to take himself out of the equation so that he would be thinking, 'What do I bring to the table? Is the risk worth taking because I can benefit so many people?' "</p>
<p class="cnn_storypgraphtxt cnn_storypgraph31">Before heading to Liberia, Brantly did his residency at John Peter Smith Hospital in Fort Worth.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph32">"We're kind of proud that there was a hero out there trying to do his best to make life better for other folks under the circumstances," a physician who knows him, Dr. Paul Pepe of Dallas' UT Southwestern Medical Center, <a href='http://www.wfaa.com/news/health/Ebola-doctors-message-Pray-along-with-me-268952711.html' target='_blank'>told CNN affiliate WFAA </a>this week.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph33">Though Brantly's wife and children had been in Liberia with him, they were in the United States when he became ill, and they are not symptomatic themselves, the CDC has said.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph34"><strong>Fear, conspiracy theories </strong></p>
<p class="cnn_storypgraphtxt cnn_storypgraph35">As officials worked to bring Brantly and Writebol home, the idea of intentionally bringing Ebola into the United States has rattled many nerves.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph36">"The road to hell was paved with good intentions," wrote one person, using the hashtag #EbolaOutbreak. "What do we say to our kids When they get sick&amp; die?"</p>
<p class="cnn_storypgraphtxt cnn_storypgraph37">On the website of conspiracy talker Alex Jones, who has long purported the CDC could unleash a pandemic and the government would react by instituting authoritarian rule, the news was a feast of fodder.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph38">"Feds would exercise draconian emergency powers if Ebola hits U.S.," a headline read on infowars.com.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph39">Ribner repeatedly downplayed the risk for anyone who will be in contact with Brantly or Writebol.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph40">"We have two individuals who are critically ill, and we feel that we owe them the right to receive the best medical care," Ribner said.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph41"><strong>The fight against Ebola</strong></p>
<p class="cnn_storypgraphtxt cnn_storypgraph42">All concerns about the United States pale in comparison to the harsh reality in the hardest-hit areas.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph43">Even in the best-case scenario, it could take three to six months to stem the epidemic in West Africa, said Dr. Thomas Frieden, director of the CDC.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph44">There's no vaccine, though one is in the works.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph45">There's no standardized treatment for the disease, either; the most common approach is to support organ functions and keep up bodily fluids such as blood and water long enough for the body to fight off the infection.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph46">The National Institutes of Health plans to begin testing an experimental Ebola vaccine in people as early as September. Tests on primates have been successful.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph47">So far, the outbreak is confined to West Africa. Although infections are dropping in Guinea, they are on the rise in Liberia and Sierra Leone.</p>
<p class="cnn_storypgraphtxt cnn_storypgraph48">In the 1990s, an Ebola strain tied to monkeys -- Ebola-Reston -- was found in the United States, but no humans got sick from it, according to <a href='http://www.cdc.gov/ncidod/dvrd/spb/outbreaks/qaEbolaRestonPhilippines.htm' target='_blank'>the CDC</a>.</p>
<script type="text/javascript">if(typeof CNN.expElements==='object'){CNN.expElements.init();}</script>
<p class="cnn_strycbftrtxt">CNN's Greg Botelho<strong>, </strong>John Branch, Danielle Dellorto, Barbara Starr, MaryLynn Ryan and Ben Brumfield contributed to this report.</p>
'''