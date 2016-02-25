# banker.ai
The startup world is not for the faint of heart. Behind every success story lies a dozen failures, and the odds can still turn for even the most robust startup. Countless resources have been poured into aiding would-be founders - websites like CrunchBase or AngelList, new podcasts like StartUp, not to mention countless how-to guides and videos.

<span style="font-weight: 400;">All well and good, but what remains largely unaddressed is the question of funding. The general process is known - line up your investors, hone your pitch, and be prepared for rejection. But that first crucial step: how do you find would-be investors? There are resources available, but it often still feels like a stab in the dark. Perhaps we can do better.</span>

# **M3 - Investor / Startup Matching**

<span style="font-weight: 400;">This is M3 - a tool meant to aid in exactly this process. What does it do?</span>

**We create text-based "fingerprints" of your startup, run that against our database of venture capital firms, and return your best bets for funding.** <span style="font-weight: 400;">These are firms that have funded startups like yours in the past, and will fund similar ones in the future. In short - we're a shortcut for finding the right venture capital firm. How exactly this fingerprint is generated and used will be discussed in more detail below.</span>

On the technical side, here's what you're looking at:

*   <span style="font-weight: 400;">Python-based app, Flask framework</span>
*   <span style="font-weight: 400;">Designed with heavily tweaked Bootstrap templates</span>
    *   <span style="font-weight: 400;">(So we definitely had to get deep into the HTML/CSS/Javascript!)</span>
*   <span style="font-weight: 400;">MySQL back-end on Google Cloud Services</span>
*   <span style="font-weight: 400;">Site hosted on an Amazon EC2 server</span>
*   <span style="font-weight: 400;">5000+ websites scraped with Scrapy</span>
*   <span style="font-weight: 400;">Asynchronous Scrapy jobs running through Celery</span>

<span style="font-weight: 400;">Lots of infrastructure. This was a challenging app for us to get up and running in just under two weeks - at times we were much closer to being full-stack engineers rather than data scientists!</span>

Let's take a second to talk algorithms, though - what are we actually using to pair startups with VCs?

# **Semantic Fingerprinting**

###### _<span style="font-weight: 400;">Note: this section is primarily theoretical background - if you’re just interested in our project, skip to the next section.</span>_

<span style="font-weight: 400;">An aside: Shakespeare scholars often discuss issues of authorship and authenticity in Shakespeare's oeuvre. Example: the scene involving the Greek goddess Hecate in MacBeth is often attributed to fellow English playwright Thomas Middleton. There are historical arguments to be made, about its role as song and dance interlude, but there are also stylistic and syntactic arguments. It just doesn't read quite like the rest of Shakespeare.</span>

<span style="font-weight: 400;">If you'll permit a slight stretch, these scholars are doing what we're doing. Semantic fingerprinting is a technique that maps bodies of text into comparable, analyzable "fingerprints" - a fingerprint being simply a large, sparse vector, otherwise known as a Sparsely Distributed Representation (SDR). Once you have an SDR for two bodies of text, whether they be Shakespeare or company descriptions, comparisons become simultaneously insightful and simple.</span>

<span style="font-weight: 400;">The underlying theory of the semantic fingerprinting technique used here comes courtesy of Cortical.io, an AI company led by researcher and author Jeff Hawkins. Cortical.io is seeking to create a new kind of artificial intelligence by taking cues from the most powerful intelligence engine we know of - namely, the human brain. In brief, Hawkins and researchers at Cortical.io believe that the human neocortex (the largest and most evolutionarily-recent area of the brain) is underpinned by one universal learning algorithm. The stands in opposition to a more compartmentalized understanding of intelligence in the brain (this area corresponds to language, here music, here math), but modern research supports the idea. A 2009 article from Scientific American discusses technology allowing</span> [<span style="font-weight: 400;">a blind man to see with his tongue</span>](http://www.scientificamerican.com/article/device-lets-blind-see-with-tongues/) <span style="font-weight: 400;">- a strong example of the brain’s ability to adapt by employing a common learning algorithm across all senses and experiences.</span>

<span style="font-weight: 400;">A full explanation of Hawkin’s theory is beyond the scope of this blog post - interested readers are enthusiastically directed towards his excellent 2004 book</span> [<span style="font-weight: 400;">On Intelligence</span>](http://www.amazon.com/On-Intelligence-Jeff-Hawkins/dp/0805078533)<span style="font-weight: 400;">, which has remained relevant despite a full decade of progress in AI. Two shorter but more complex reads are available on the</span> [<span style="font-weight: 400;">statistical properties of Sparse Distributed Representations</span>](http://arxiv.org/pdf/1503.07469.pdf) <span style="font-weight: 400;">and a white paper on</span> [<span style="font-weight: 400;">Semantic Folding Theory</span>](http://www.cortical.io/static/downloads/semantic-folding-theory-white-paper.pdf)<span style="font-weight: 400;">.</span>

We can outline the basic pieces fairly quickly, however:

1.  <span style="font-weight: 400;">Define your source corpus / dictionary - a random sampling of Wikipedia articles would serve as a General English dictionary, whereas an assortment of medical papers would be a General Medical dictionary.</span>
2.  <span style="font-weight: 400;">Create an appropriate base vector representation out of your source corpus. This involves generic tokenization, lemmatization, and importance weighting of your texts, followed by an unsupervised algorithm for the extraction of keywords and phrases. These keywords are weighted and linked to one another (think</span> [<span style="font-weight: 400;">PageRank</span>](https://en.wikipedia.org/wiki/PageRank)<span style="font-weight: 400;">), and then used in the construction of a 128 x 128 grid, where each pixel represents a “context”. One context could roughly be “things involved with opera” - expected keywords then might be “opera, concert hall, singing, classical, costumes”, etc. Semantically similar contexts are placed near each other on the grid.</span>
3.  <span style="font-weight: 400;">An input corpus is entered for vectorization. Similar keyword extraction takes place, and those keywords / contexts are mapped to the original 128 x 128 grid, where an ON-bit represents a recognized context in your input corpus.</span>

<span style="font-weight: 400;">As outlined in the mathematical properties paper above, two vectorized corpora are related to each other in a simple way. The core of it is overlapping bits - take the union of two SDRs, and the more bits they share, the more closely related they are. It’s not quite so simple, of course - some common distance metrics employed are:</span>

1.  [<span style="font-weight: 400;">Euclidean Distance</span>](https://en.wikipedia.org/wiki/Euclidean_distance)
2.  [<span style="font-weight: 400;">Cosine Similarity</span>](https://en.wikipedia.org/wiki/Cosine_similarity)
3.  [<span style="font-weight: 400;">Hamming Distance</span>](https://en.wikipedia.org/wiki/Hamming_distance)
4.  [<span style="font-weight: 400;">Jaccard Index</span>](https://en.wikipedia.org/wiki/Jaccard_index)

Last but certainly not least - how are we generating these fingerprints of a given input text? That's where Cortical.io's API comes in. Play around with this [fingerprinting demo here](http://www.cortical.io/keyword-extraction.html) - cortical.io provides API keys upon request, and the API provides everything you need to begin fingerprinting and comparing. The default base corpus is a generic English language corpus - this was the corpus used for all fingerprinting in our project.

# **Stage 1: Adventures in Scraping**

So our procedure is now clear: gather text data on startups and venture capital firm, generate fingerprints using cortical.io's API, and given a startup, select the best match. This best match is the venture capital firm whose text indicates the closest semantic similarity to the text of your own product - the a priori assumption here being that a venture capital firm who describes themselves similarly to your startup (OR: a venture capital firm whose portfolio includes similar startups to yours) is a venture capital firm that is more likely to fund your startup.

This procedure was broken into several stages:

1.  Scrape websites for data; clean and analyze data
2.  Produce front-end for querying data

Stage 1 - how do we get this data? We scrape. Lots and lots and lot of websites. 5000+ websites, to be more specific. We do this with lots of infrastructure, and a powerful enough scraper / crawler to take care of most of the dirty work. Simultaneously, we begin to analyze the text that comes in. Jumping straight into it, our workflow for stage 1:

[![Screen Shot 2015-12-12 at 3.20.23 PM](http://2igww43ul7xe3nor5h2ah1yq.wpengine.netdna-cdn.com/wp-content/uploads/2015/12/Screen-Shot-2015-12-12-at-3.20.23-PM-1024x625.png)](http://2igww43ul7xe3nor5h2ah1yq.wpengine.netdna-cdn.com/wp-content/uploads/2015/12/Screen-Shot-2015-12-12-at-3.20.23-PM.png)

Without lingering too long, the gist is: Scrapy goes out and scrapes lots of pages on lots of websites. We used Goose for text extraction as well as some generic XPath / CSS selector manipulations. A few cleaning functions were defined, and pages were consolidated into one body of text per website. A Scrapy pipeline was built to dump into a MySQL database, hosted on Google Cloud Services.

Meanwhile, as text was being dumped, a simultaneous process was running to analyze the extracted text per site. We used a few different APIs for analyzing - cortical.io primarily, but also TextBlob and OpenCalais, just so we could play a bit.

This scraping/analyzing cycle went on for several days. We launched 10+ spiders simultaneously on an AWS instance, all scraping and dumping different websites. We ran these processes in the background, handled connectivity issues, checked for bad data, and so on. It was a lot of spinning cogs, but it came together, and we had our data set.

What sorts of issues did we have? How good was our data? Can we do better? Here are some issues / thoughts we had while in stage 1.

*   Goose for text extraction - how robust?
*   Min / Max page scraping depth - 2, 3, 4 pages deep? How much is enough?
*   ASCII vs UTF-8 - how to handle? How is a website encoded? The MySQL database? Python data types like unicode vs str?
*   Python relative paths - how best to navigate a project?
*   Boilerplate text - how much of the scraped text has real meaning? How much of it is generic legal / VC text?

This last bullet is worth lingering on. Not all text on a website is meaningful - in fact, most of it probably isn't. What we're actually interested in how a VC / startup describes itself, its projects, its mission. So how do we get there? Well, one way could be with an algorithm called tf-idf (text-frequency inverse-document frequency), which allows you to properly weight the importance of word based on a ratio of its frequency in one document vs a set of documents. You could also do TextRank, an algorithm based on PageRank that uses a graph approach to discover important words and phrases, unsupervised. Or perhaps we generate a fingerprint using cortical.io of just boilerplate finance / legal, and subtract out that fingerprint from our VCs and startups.

All of these are worth pondering and investigating, and so will be in future iterations of M3\. They're especially worthwhile, because right now, the keywords for some websites are nothing more than "legal, agreement, finance, disclosure" and so on. Not particularly meaningful. Stay tuned!

# Stage 2: Adventures in Flask

Now we need our queryable front-end. For this, we chose Flask, a fairly light-weight Python framework meant for full-stack development. Flask provides interactivity between Python and the web dev side using a language called Jinja, so the challenge was established. Figure out Flask, figure out Jinja, figure out enough web dev to get by, and put it all together in a speedy front-end.

For the visual component, we used [Bootstrap](http://getbootstrap.com/) - specifically, the simple but elegant Cover template, freely available. Bootstrap comes with a little setup required, especially when working with Flask. There are a handful of default components, including the Bootstrap minimum CSS / Javascript files, plus a few other things here and there. Mostly though, Bootstrap was delightful. The entire power of the internet is at your fingertips, with a little elbow grease.

Flask and Jinja was another story. Flask is compact compared to Django, but a full-stack framework is complex regardless. Many [tutorials](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) were read, many long hours debugging silly web dev problems, and so on. A few main points:

*   Originally, distance metrics were calculated via API calls to cortical.io - mainly Cosine and Euclidean to start. This was slowing down our app tremendously, so we reverse-engineered the algorithms used for these metrics (NOT just plain Euclidean distance - tell me how you calculate that distance for vectors of unequal length?) and now run them locally. Much faster.
*   Streaming images are a bit tricky and involve two routings instead of one for a page.
*   Our site scrapes an input website using Scrapy in stand-alone mode - unfortunately Scrapy has to run in its own thread, and so enter Celery. Celery is an asynchronous job module, allowing functions to be run asynchronously in a queue with a simple decorator attached to the module. A Celery instance does need to be initialized, however, along with a "broker", which is simply a back-end Celery interacts with while running jobs. We used Redis as our broker.
*   MySQL is a nightmare. Flask has its own MySQL connector module (two, actually), and it's terribly unwieldy. We also are guilty of abusing proper database usage with this product - SQL queries are sprinkled throughout the code, instead of being called as Stored Procedures. The database calls are properly parameterized to protect from SQL injection, but the attempt we made to move to Stored Procedures was an exercise in frustration (if you're curious - one cursor per proc call, then you gotta dump the cursor). We're also guilty of re-initializing too many connections and cursors. Main point - next time, a different back-end. Also, our data isn't huge, but it's getting there, and so MySQL will be out-scaled pretty soon.
*   A lot of work was done in the AWS environment - simple shell scripts, resource monitoring, logging, the works. To kick off the app, we needed a Redis server instance, a Celery worker, and the Flask app itself (which needed connectivity to the MySQL DB).
*   There's a lot of mess in the code. We're working on it.

To be honest, there's simply too much code to go into here. You're welcome to explore the code on GitHub - we're continually making efforts to increase commentary, modularization, etc. The total code output is well over 1000 lines of Python, and that doesn't begin to touch the HTML, CSS, and Javascript that was customized for the app.

How it works in the end is simple - enter your website OR a text description of your product, and we'll find the top 3 best matches based on a variety of metrics and return them to you That's it. We'll be working on a brief video tour of our product in the near future.

<div id="attachment_8571" style="width: 539px" class="wp-caption aligncenter">[![M3 Results.](http://2igww43ul7xe3nor5h2ah1yq.wpengine.netdna-cdn.com/wp-content/uploads/2015/12/Screen-Shot-2015-12-12-at-5.52.30-PM-1024x704.png)](http://2igww43ul7xe3nor5h2ah1yq.wpengine.netdna-cdn.com/wp-content/uploads/2015/12/Screen-Shot-2015-12-12-at-5.52.30-PM.png)

M3 Results.

</div>

# So what?

Does it work? Yes (mostly). The algorithm works very well, and the data is all there. We're working on getting better representative texts as discussed above - subtract out boilerplate, scrape supplementary sites, and so on. One success story is the company kaplancleantech.com - enter in that site, and your best bets for VC funding all come from VCs with a history of clean tech entrepreneurship.

<div id="attachment_8570" style="width: 578px" class="wp-caption aligncenter">[![Example M3 results, with keywords](http://2igww43ul7xe3nor5h2ah1yq.wpengine.netdna-cdn.com/wp-content/uploads/2015/12/Screen-Shot-2015-12-12-at-5.50.40-PM-1024x660.png)](http://2igww43ul7xe3nor5h2ah1yq.wpengine.netdna-cdn.com/wp-content/uploads/2015/12/Screen-Shot-2015-12-12-at-5.50.40-PM.png)

Example M3 results for kaplancleantech.com, with keywords

</div>

This technology is incredibly powerful if used well. We've used it, but we too have a lot of work to do before the algorithm is truly robust. But once it is, this matching algorithm could be used in any industry, on any two bodies of text, for any time there are buyers and sellers. Site content creation, medical community, fiction - the sky's the limit.

This project was an exercise is putting together a very complex workflow from scratch - we started with nothing more than an API and an idea, and now we have Python, Flask, Bootstrap, Scrapy, MySQL, and more all woven together into a presentable product. There is certainly much more work to be done, but we're just getting started.
![Startups](http://assets.amuniversal.com/1457335027e60133fee0005056a9545d)

@aviyashchin
